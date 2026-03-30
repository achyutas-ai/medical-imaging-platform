# Connect Service (API Gateway)

The **Connect Service** is the central entry point and API Gateway for the Medical AI Platform. It orchestrates communication between all backend modules and provides a unified, aggregated interface for frontend applications.

## 🌟 Key Features

-   **Service Aggregation**: Provides a single endpoint (`/api/v1/dashboard/dashboard`) that reports the health and connectivity status of all internal modules.
-   **Unified Frontend Interface**: Handles CORS, common authentication, and routing for easy frontend integration.
-   **Workflow Orchestration**: Simplifies complex multi-service tasks into single API calls (e.g., triggering a DICOM-to-Inference workflow).
-   **Internal Service Discovery**: Manages internal networking between the Control Plane, Orchestrator, DICOM Service, and Edge Management.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   All other platform services (Control Plane, etc.) should be running for full functionality.

### Installation

1.  Navigate to the `connect-service` directory:
    ```bash
    cd connect-service
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Edit the `.env` file to point to the correct internal service URLs:

```ini
CONTROL_PLANE_URL="http://localhost:8000"
ORCHESTRATOR_URL="http://localhost:8001"
DICOM_SERVICE_URL="http://localhost:8002"
EDGE_MGMT_URL="http://localhost:8003"
```

---

## 🛠️ Usage

### Starting the Gateway

```bash
python -m app.main
```
The gateway will start on **port 8888** by default.

### Accessing the Dashboard

Visit `http://localhost:8888/api/v1/dashboard/dashboard` to see the current status of all platform components.

### Interactive Docs

Explore the aggregated API surface at: `http://localhost:8888/docs`

---

## 📁 Project Structure

```text
connect-service/
├── app/
│   ├── api/            # Gateway endpoints (dashboard, workflows)
│   ├── core/           # Gateway configuration
│   ├── services/       # Service orchestration (gateway.py)
│   └── main.py         # Entry point
├── requirements.txt
└── .env
```
