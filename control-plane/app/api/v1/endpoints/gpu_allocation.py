from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status

from app.core.deps import get_current_user
from app.schemas.gpu import GPUAllocation, GPUAllocationCreate, GPUAllocationUpdate
from app.services.gpu_service import gpu_service

router = APIRouter()

@router.get("/", response_model=List[GPUAllocation])
def read_allocations(
    skip: int = 0,
    limit: int = 100,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Retrieve GPU allocations.
    """
    return gpu_service.list_allocations()[skip : skip + limit]

@router.post("/", response_model=GPUAllocation, status_code=status.HTTP_201_CREATED)
def create_allocation(
    *,
    allocation_in: GPUAllocationCreate,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Create new GPU allocation.
    """
    return gpu_service.create_allocation(allocation_in)

@router.get("/{allocation_id}", response_model=GPUAllocation)
def read_allocation(
    allocation_id: str,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Get GPU allocation by ID.
    """
    allocation = gpu_service.get_allocation(allocation_id)
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return allocation

@router.put("/{allocation_id}", response_model=GPUAllocation)
def update_allocation(
    *,
    allocation_id: str,
    allocation_in: GPUAllocationUpdate,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Update a GPU allocation.
    """
    allocation = gpu_service.update_allocation(allocation_id, allocation_in)
    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return allocation

@router.delete("/{allocation_id}", response_model=Any)
def delete_allocation(
    *,
    allocation_id: str,
    current_user: str = Depends(get_current_user),
) -> Any:
    """
    Delete a GPU allocation.
    """
    if not gpu_service.delete_allocation(allocation_id):
        raise HTTPException(status_code=404, detail="Allocation not found")
    return {"status": "success"}
