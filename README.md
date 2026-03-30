# 🏥 Medical AI Imaging Platform

> **An end-to-end, high-performance orchestration ecosystem for medical imaging AI.**

Welcome to the **Medical AI Imaging Platform**, a distributed micro-services architecture designed to handle medical imaging workloads (DICOM) across hybrid cloud and edge environments. This platform integrates secure data ingestion, AI-optimized orchestration, and automated infrastructure management into a unified product.

---

## 🏗️ Platform Architecture

The platform is composed of **six specialized services**, each handling a critical phase of the medical AI lifecycle:

| Service | Primary Role | Tech Stack |
| :--- | :--- | :--- |
| **[Control Plane](file:///d:/codespace/medical-imaging-platform/control-plane)** | Central API Gateway & Resource Orchestration. | FastAPI, Pydantic, JWT |
| **[Connect Service](file:///d:/codespace/medical-imaging-platform/connect-service)** | Secure data ingestion and system-wide connectivity. | Python, AsyncIO |
| **[DICOM Processor](file:///d:/codespace/medical-imaging-platform/dicom-service)** | Image normalization and Structured Reporting (SR). | PyDICOM, OpenCV, PyTorch |
| **[Edge Management](file:///d:/codespace/medical-imaging-platform/edge-mgmt-service)** | Remote node management and VM/GPU monitoring. | Paramiko, libvirt, virsh |
| **[K8s Orchestrator](file:///d:/codespace/medical-imaging-platform/orchestrator)** | Scalable AI inference lifecycle on Kubernetes clusters. | K8s API, NVIDIA GPU Support |
| **[Infra Automation](file:///d:/codespace/medical-imaging-platform/infra-mgmt)** | CI/CD pipelines and custom ISO builder for edge nodes. | Docker, GitLab CI, Bash |

---

## 🚀 Product Guide: From Imaging to Insights

### 1. Unified Control
Access the **Control Plane** (default: `http://localhost:8000/docs`) to manage your hybrid infrastructure. From here, you can allocate GPU resources, spin up edge VMs, and monitor system health.

### 2. DICOM Pipeline Execution
Upload your `.dcm` files through the **Connect Service**. The **DICOM Processor** automatically:
- Extracts patient metadata.
- Normalizes 16-bit imaging data for AI readiness.
- Runs high-confidence inference models.
- Generates a **DICOM Structured Report (SR)** JSON.

### 3. Edge-Scale Inference
When running at scale, the **K8s AI Orchestrator** triggers containers with direct NVIDIA GPU access, ensuring low-latency processing even for the most demanding radiology studies.

### 4. Continuous Deployment
The **Infra Management** service ensures that your AI models and system patches are deployed seamlessly to clinics via automated ISO updates and secure CI/CD pipelines.

---

## 🛠️ Unified Quick Start

To "up" the entire development environment, follow these steps:

### Prerequisites
- Python 3.9+
- Docker (optional, for infra-mgmt)
- Access to a Kubernetes cluster (requested by `orchestrator`)

### Launch All Services
```bash
# 1. Run the Control Plane (Central API)
cd control-plane && uvicorn app.main:app --reload

# 2. Start the Connect Service
cd connect-service && python -m app.main

# 3. Launch Edge Monitoring
cd edge-mgmt-service && python -m app.main

# 4. Initialize K8s Orchestrator
cd orchestrator && python -m app.main

# 5. Process Sample DICOM (Requires sample.dcm)
cd dicom-service && python -m app.main <path_to_dicom>
```

---

## 🔐 Security & Compliance
- **Authentication**: JWT-based security at the Control Plane level.
- **Audit**: Every inference job and infrastructure change is logged for medical compliance.
- **Isolation**: Remote commands are executed over secure SSH tunnels managed by the Edge service.

---

## 📁 Repository Structure
```text
medical-imaging-platform/
├── control-plane/       # Central Management API (Active)
├── connect-service/     # Communication Middleman (Active)
├── dicom-service/       # Image Processing Engine (Ready)
├── edge-mgmt-service/   # Remote Hardware Ops (Active)
├── orchestrator/        # Kubernetes AI Workloads (Active)
├── infra-mgmt/          # CI/CD & Docker Orchestration
└── requirements.txt     # Global dependencies
```

*Built with ❤️ for High-Reliability Healthcare AI.*
