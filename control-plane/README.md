# Medical AI Control Plane

The **Medical AI Control Plane** is a centralized orchestration layer built with FastAPI. It provides a robust API for managing Virtual Machines (VMs), Kubernetes clusters, and GPU resource allocations, specifically tailored for medical AI workloads.

## 🏗️ Architecture

The project follows **Clean Architecture** principles, ensuring a clear separation of concerns:

-   **API Layer (`app/api`)**: Handles HTTP requests, routing, and response formatting.
-   **Service Layer (`app/services`)**: Contains the business logic and orchestrations. Currently implemented as placeholders designed to integrate with:
    -   **Paramiko**: For SSH-based VM management.
    -   **Kubernetes Python Client**: For cluster orchestration.
-   **Schema Layer (`app/schemas`)**: Defines data models and performs strict validation using **Pydantic**.
-   **Core Layer (`app/core`)**: Manages global configuration, JWT-based security, and dependency injection.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+ 
-   `virtualenv` or `venv`

### Installation

1.  **Clone the project** and navigate to the `control-plane` directory:
    ```bash
    cd control-plane
    ```

2.  **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    # Windows:
    .\venv\Scripts\activate
    # macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    Edit the `.env` file in the root directory to set your `SECRET_KEY` and other configurations.

### Running the Server

Start the development server with auto-reload:

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

---

## 🔐 Authentication

The API uses **JWT (JSON Web Token)** for authentication.

-   **Login Endpoint**: `POST /api/v1/auth/login`
-   **Placeholder Credentials**:
    -   **Username**: `admin`
    -   **Password**: `admin123`

To access protected endpoints, include the token in the `Authorization` header:
`Authorization: Bearer <your_access_token>`

---

## 🛠️ API Endpoints

| Category | Endpoint | Description |
| :--- | :--- | :--- |
| **Auth** | `/api/v1/auth/login` | Obtain a JWT access token. |
| **VMs** | `/api/v1/vm-management/` | List, create, and manage virtual machines. |
| **K8s** | `/api/v1/k8s-deployment/` | Orchestrate Kubernetes deployments. |
| **GPU** | `/api/v1/gpu-allocation/` | Allocate and track GPU resources. |

**Interactive Documentation**: Visit `http://127.0.0.1:8000/docs` for the full Swagger UI.

---

## ⚙️ Service Layer Integration

The services in `app/services/` are currently implementation placeholders. To integrate with real infrastructure:

1.  **VM Management**: Update `vm_service.py` with `Paramiko` logic to run commands via SSH.
2.  **Kubernetes**: Configure the `kubernetes-python` client in `k8s_service.py` to talk to your cluster API.
3.  **GPU Allocation**: Implement resource tracking logic in `gpu_service.py`.

---

## 💻 Tech Stack

-   **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
-   **Validation**: [Pydantic v2](https://docs.pydantic.dev/)
-   **Auth**: [python-jose](https://python-jose.readthedocs.io/), [passlib](https://passlib.readthedocs.io/)
-   **Web Server**: [Uvicorn](https://www.uvicorn.org/)
