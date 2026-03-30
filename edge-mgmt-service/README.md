# Edge Management Service

The **Edge Management Service** is a Python-based utility designed to orchestrate remote hardware nodes (Edge Nodes) located at hospitals or clinics. It provides secure SSH-based management for virtual machines and hardware health monitoring.

## 🌟 Key Features

-   **Secure SSH Orchestration**: Uses `paramiko` with robust context management for safe remote command execution.
-   **KVM/QEMU VM Management**: Built-in functions to `start`, `stop`, and check the `status` of virtual machines using `virsh`.
-   **Hardware Health Monitoring**: Programmatically parses `nvidia-smi` to verify NVIDIA driver and CUDA activity on the host.
-   **Automated Remote Commands**: Easily extensible for other remote maintenance tasks.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   SSH access to the target remote Ubuntu server.
-   `virsh` and `libvirt` installed on the remote host (for VM management).
-   `nvidia-smi` installed on the remote host (for GPU monitoring).

### Installation

1.  Navigate to the `edge-mgmt-service` directory:
    ```bash
    cd edge-mgmt-service
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # macOS/Linux
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Edit the `.env` file to match your edge node's details:

```ini
EDGE_HOST="192.168.1.50"
EDGE_USER="ubuntu"
EDGE_KEY_PATH="~/.ssh/id_rsa"
VM_NAME="medical-inference-vm"
```

---

## 🛠️ Usage

### Running the Management Demo

To test the connection and status logic (requires a valid SSH key and reachable host):

```bash
python -m app.main
```

### Programmatic Example

```python
from app.services.edge_manager import edge_manager

# Check if GPU is ready
gpu_info = edge_manager.check_gpu_status()
print(f"GPU Status: {gpu_info['status']}")

# Manage a VM
edge_manager.start_vm("medical-inference-vm")
status = edge_manager.get_vm_status("medical-inference-vm")
print(f"VM Status: {status}")
```

---

## 📁 Project Structure

```text
edge-mgmt-service/
├── app/
│   ├── core/           # Configuration management
│   ├── services/       # Core management logic (edge_manager.py)
│   └── main.py         # Management demo script
├── requirements.txt
└── .env
```
