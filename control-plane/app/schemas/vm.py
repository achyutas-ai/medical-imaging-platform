from typing import Optional
from pydantic import BaseModel

class VMBase(BaseModel):
    name: str
    image: str
    flavor: str
    ssh_key_name: Optional[str] = None

class VMCreate(VMBase):
    pass

class VMUpdate(BaseModel):
    flavor: Optional[str] = None
    status: Optional[str] = None

class VM(VMBase):
    id: str
    status: str
    ip_address: Optional[str] = None

    class Config:
        from_attributes = True
