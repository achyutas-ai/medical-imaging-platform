from typing import List, Optional
import uuid

from app.schemas.gpu import GPUAllocation, GPUAllocationCreate, GPUAllocationUpdate

class GPUService:
    def __init__(self):
        # Placeholder for GPU allocations storage
        self._allocations = {}

    def create_allocation(self, allocation_in: GPUAllocationCreate) -> GPUAllocation:
        allocation_id = str(uuid.uuid4())
        allocation = GPUAllocation(
            id=allocation_id,
            status="allocated",
            **allocation_in.model_dump()
        )
        self._allocations[allocation_id] = allocation
        return allocation

    def get_allocation(self, allocation_id: str) -> Optional[GPUAllocation]:
        return self._allocations.get(allocation_id)

    def list_allocations(self) -> List[GPUAllocation]:
        return list(self._allocations.values())

    def update_allocation(self, allocation_id: str, allocation_in: GPUAllocationUpdate) -> Optional[GPUAllocation]:
        if allocation_id not in self._allocations:
            return None
        
        allocation = self._allocations[allocation_id]
        update_data = allocation_in.model_dump(exclude_unset=True)
        
        updated_allocation = allocation.model_copy(update=update_data)
        self._allocations[allocation_id] = updated_allocation
        return updated_allocation

    def delete_allocation(self, allocation_id: str) -> bool:
        if allocation_id in self._allocations:
            del self._allocations[allocation_id]
            return True
        return False

gpu_service = GPUService()
