# K8s AI Orchestrator

The **K8s AI Orchestrator** is a Python-based service designed to programmatically manage AI inference workloads on a Kubernetes cluster. It is specifically optimized for medical imaging tasks that require NVIDIA GPU acceleration and access to large DICOM datasets.

## 🌟 Key Features

-   **NVIDIA GPU Support**: Automatically configures resource limits (`nvidia.com/gpu`) for inference containers.
-   **DICOM Data Integration**: Seamlessly mounts Persistent Volume Claims (PVCs) for medical imaging data access.
-   **Automated Jobs**: Uses Kubernetes `BatchV1Api` to deploy and track inference tasks.
-   **Log Streaming**: Programmatically retrieves and streams pod logs for debugging and monitoring.
-   **Environment Agnostic**: Supports both in-cluster (production) and local `kube-config` (development) authentication.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   Access to a Kubernetes cluster (e.g., Minikube, GKE, EKS)
-   `kubectl` configured locally (for development)

### Installation

1.  Navigate to the `orchestrator` directory:
    ```bash
    cd orchestrator
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

Edit the `.env` file to match your cluster environment:

```ini
K8S_NAMESPACE="default"
DICOM_PVC_NAME="dicom-pvc"
DICOM_MOUNT_PATH="/mnt/dicom"
```

---

## 🛠️ Usage

### Programmatic Usage

```python
from app.services.k8s_orchestrator import orchestrator

# Deploy a job
job = orchestrator.deploy_inference_job(
    image_name="your-ai-image:latest",
    gpu_count=1
)
print(f"Job Triggered: {job['job_name']}")

# Fetch logs (after pod starts)
logs = orchestrator.get_pod_logs(job['job_name'])
print(logs)
```

### Running the Demo

To test the orchestrator logic (ensure your `kube-config` is active):

```bash
python -m app.main
```

---

## 📁 Project Structure

```text
orchestrator/
├── app/
│   ├── core/           # Configuration management
│   ├── services/       # K8s client logic (k8s_orchestrator.py)
│   └── main.py         # CLI Demo script
├── .env                # Environment-specific settings
├── .gitignore          # Git exclusion rules
└── requirements.txt    # Python dependencies
```
