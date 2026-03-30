from typing import Optional, Dict
from pydantic import BaseModel

class K8sDeploymentBase(BaseModel):
    name: str
    namespace: str = "default"
    image: str
    replicas: int = 1
    labels: Optional[Dict[str, str]] = None

class K8sDeploymentCreate(K8sDeploymentBase):
    pass

class K8sDeploymentUpdate(BaseModel):
    replicas: Optional[int] = None
    image: Optional[str] = None

class K8sDeployment(K8sDeploymentBase):
    id: str
    status: str
    creation_timestamp: str

    class Config:
        from_attributes = True
