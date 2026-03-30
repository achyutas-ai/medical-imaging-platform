from typing import Optional
from pydantic import BaseModel

class GPUAllocationBase(BaseModel):
    vm_id: str
    gpu_type: str
    count: int = 1

class GPUAllocationCreate(GPUAllocationBase):
    pass

class GPUAllocationUpdate(BaseModel):
    count: Optional[int] = None

class GPUAllocation(GPUAllocationBase):
    id: str
    status: str

    class Config:
        from_attributes = True
