from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.schemas.vm import VM, VMCreate, VMUpdate
from app.services.vm_service import vm_service

router = APIRouter()

@router.get("/", response_model=List[VM])
def read_vms(
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Retrieve VMs.
    """
    return vm_service.list_vms()[skip : skip + limit]

@router.post("/", response_model=VM, status_code=status.HTTP_201_CREATED)
def create_vm(
    *,
    vm_in: VMCreate,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Create new VM.
    """
    return vm_service.create_vm(vm_in)

@router.get("/{vm_id}", response_model=VM)
def read_vm(
    vm_id: str,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Get VM by ID.
    """
    vm = vm_service.get_vm(vm_id)
    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")
    return vm

@router.put("/{vm_id}", response_model=VM)
def update_vm(
    *,
    vm_id: str,
    vm_in: VMUpdate,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Update a VM.
    """
    vm = vm_service.update_vm(vm_id, vm_in)
    if not vm:
        raise HTTPException(status_code=404, detail="VM not found")
    return vm

@router.delete("/{vm_id}", response_model=Any)
def delete_vm(
    *,
    vm_id: str,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Delete a VM.
    """
    if not vm_service.delete_vm(vm_id):
        raise HTTPException(status_code=404, detail="VM not found")
    return {"status": "success"}
