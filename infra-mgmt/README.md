# Infrastructure Management Service

The **Infrastructure Management Service** handles the CI/CD pipelines, containerization, and automated edge node deployment updates for the Medical AI platform.

## 🏗️ Components

### 1. GitLab CI/CD Pipeline
The root-level `.gitlab-ci.yml` orchestrates:
-   **Automated Testing**: Runs unit tests for the `control-plane` FastAPI backend.
-   **Docker Build**: Builds production-ready images for the `dicom-service`.
-   **Manual Deployment**: A safety-gated `deploy-to-edge` stage for critical updates.

### 2. Docker Orchestration
-   **Dockerfile.dicom**: A optimized, multi-stage Docker build for the DICOM processing service, pre-configured with OpenCV and PyTorch dependencies.

### 3. ISO Builder Automation
-   **`update_iso_builder.sh`**: A utility script used by the CI/CD pipeline to inject the latest AI model weights into a custom ISO image for edge node provisioning.

---

## 🚀 Usage

### Running Locally
To test the Docker build for the DICOM service:
```bash
docker build -f infra-mgmt/Dockerfile.dicom -t dicom-service:local .
```

### Triggering ISO Update
To manually simulate an ISO update:
```bash
bash infra-mgmt/scripts/update_iso_builder.sh --weights-version v2.1.0
```

---

## 📁 Project Structure
```text
infra-mgmt/
├── scripts/
│   └── update_iso_builder.sh   # ISO automation
├── Dockerfile.dicom           # Optimized DICOM build
└── README.md                  # Infrastructure manual
```
