from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.v1.endpoints import auth, vm_management, k8s_deployment, gpu_allocation

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(vm_management.router, prefix="/vm-management", tags=["vm-management"])
api_router.include_router(k8s_deployment.router, prefix="/k8s-deployment", tags=["k8s-deployment"])
api_router.include_router(gpu_allocation.router, prefix="/gpu-allocation", tags=["gpu-allocation"])
