from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.schemas.k8s import K8sDeployment, K8sDeploymentCreate, K8sDeploymentUpdate
from app.services.k8s_service import k8s_service

router = APIRouter()

@router.get("/", response_model=List[K8sDeployment])
def read_deployments(
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Retrieve Kubernetes deployments.
    """
    return k8s_service.list_deployments()[skip : skip + limit]

@router.post("/", response_model=K8sDeployment, status_code=status.HTTP_201_CREATED)
def create_deployment(
    *,
    deployment_in: K8sDeploymentCreate,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Create new Kubernetes deployment.
    """
    return k8s_service.create_deployment(deployment_in)

@router.get("/{deployment_id}", response_model=K8sDeployment)
def read_deployment(
    deployment_id: str,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Get K8s deployment by ID.
    """
    deployment = k8s_service.get_deployment(deployment_id)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment

@router.put("/{deployment_id}", response_model=K8sDeployment)
def update_deployment(
    *,
    deployment_id: str,
    deployment_in: K8sDeploymentUpdate,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Update a K8s deployment.
    """
    deployment = k8s_service.update_deployment(deployment_id, deployment_in)
    if not deployment:
        raise HTTPException(status_code=404, detail="Deployment not found")
    return deployment

@router.delete("/{deployment_id}", response_model=Any)
def delete_deployment(
    *,
    deployment_id: str,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Delete a K8s deployment.
    """
    if not k8s_service.delete_deployment(deployment_id):
        raise HTTPException(status_code=404, detail="Deployment not found")
    return {"status": "success"}
