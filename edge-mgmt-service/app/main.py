import sys
import logging
from app.services.edge_manager import edge_manager
from app.core.config import settings

logging.basicConfig(level=logging.INFO)

def run_demo():
    print(f"--- Medical AI Edge Management Demo ---")
    print(f"Target Host: {settings.EDGE_HOST}")
    print(f"Target VM: {settings.VM_NAME}\n")

    try:
        # 1. Check GPU Status
        print("[Step 1] Checking GPU status on remote host...")
        gpu_status = edge_manager.check_gpu_status()
        print(f"GPU Status: {gpu_status['status']}")
        if gpu_status['status'] == 'active':
            print(f"  - Name: {gpu_status['gpu_name']}")
            print(f"  - Driver: {gpu_status['driver_version']}")

        # 2. Check VM Status
        print("\n[Step 2] Checking VM status...")
        status = edge_manager.get_vm_status(settings.VM_NAME)
        print(f"VM '{settings.VM_NAME}' is currently: {status}")

        # 3. Demonstrate Start/Stop (Logic only, won't execute without real SSH)
        # Note: In a real scenario, you'd call edge_manager.start_vm(settings.VM_NAME)
        print("\n[Note] Functions edge_manager.start_vm() and edge_manager.stop_vm() are ready for use.")

    except Exception as e:
        print(f"\nDEMO FAILED: {e}")
        print("Ensure SSH key is configured and host is reachable.")

if __name__ == "__main__":
    run_demo()
