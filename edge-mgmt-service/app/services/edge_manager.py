import paramiko
import logging
import os
from typing import Tuple, Optional
from contextlib import contextmanager

from app.core.config import settings

logger = logging.getLogger(__name__)

class EdgeManager:
    def __init__(self, host: str, user: str, key_path: str):
        self.host = host
        self.user = user
        self.key_path = os.path.expanduser(key_path)

    @contextmanager
    def ssh_connection(self):
        """
        Context manager for handling SSH connections safely.
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            logger.info(f"Connecting to {self.user}@{self.host}...")
            client.connect(
                hostname=self.host,
                username=self.user,
                key_filename=self.key_path,
                timeout=10
            )
            yield client
        except Exception as e:
            logger.error(f"SSH Connection failed: {e}")
            raise
        finally:
            client.close()
            logger.info("SSH Connection closed.")

    def execute_command(self, command: str) -> Tuple[int, str, str]:
        """
        Executes a command on the remote host and returns (exit_code, stdout, stderr).
        """
        with self.ssh_connection() as client:
            stdin, stdout, stderr = client.exec_command(command)
            exit_status = stdout.channel.recv_exit_status()
            return exit_status, stdout.read().decode().strip(), stderr.read().decode().strip()

    def start_vm(self, vm_name: str) -> bool:
        """
        Starts a specific QEMU/KVM VM using virsh.
        """
        logger.info(f"Starting VM: {vm_name}")
        exit_code, out, err = self.execute_command(f"sudo virsh start {vm_name}")
        if exit_code == 0:
            return True
        logger.error(f"Failed to start VM: {err}")
        return False

    def stop_vm(self, vm_name: str) -> bool:
        """
        Stops a specific QEMU/KVM VM using virsh.
        """
        logger.info(f"Stopping VM: {vm_name}")
        exit_code, out, err = self.execute_command(f"sudo virsh shutdown {vm_name}")
        if exit_code == 0:
            return True
        logger.error(f"Failed to stop VM: {err}")
        return False

    def get_vm_status(self, vm_name: str) -> str:
        """
        Checks the status of a specific QEMU/KVM VM.
        """
        exit_code, out, err = self.execute_command(f"sudo virsh domstate {vm_name}")
        if exit_code == 0:
            return out
        return f"Error: {err}"

    def check_gpu_status(self) -> dict:
        """
        Checks if NVIDIA drivers and CUDA are active by parsing nvidia-smi.
        """
        exit_code, out, err = self.execute_command("nvidia-smi --query-gpu=name,driver_version,memory.total --format=csv,noheader")
        
        if exit_code != 0:
            return {"status": "inactive", "error": err}
        
        gpu_info = out.split(", ")
        return {
            "status": "active",
            "gpu_name": gpu_info[0] if len(gpu_info) > 0 else "Unknown",
            "driver_version": gpu_info[1] if len(gpu_info) > 1 else "Unknown",
            "memory_total": gpu_info[2] if len(gpu_info) > 2 else "Unknown"
        }

edge_manager = EdgeManager(
    host=settings.EDGE_HOST,
    user=settings.EDGE_USER,
    key_path=settings.EDGE_KEY_PATH
)
