from typing import List, Optional
import uuid
from datetime import datetime
# from kubernetes import client, config  # To be used later

from app.schemas.k8s import K8sDeployment, K8sDeploymentCreate, K8sDeploymentUpdate

class K8sService:
    def __init__(self):
        # Placeholder for K8s deployments storage
        self._deployments = {}

    def create_deployment(self, deployment_in: K8sDeploymentCreate) -> K8sDeployment:
        deployment_id = str(uuid.uuid4())
        deployment = K8sDeployment(
            id=deployment_id,
            status="Running",
            creation_timestamp=datetime.now().isoformat(),
            **deployment_in.model_dump()
        )
        self._deployments[deployment_id] = deployment
        return deployment

    def get_deployment(self, deployment_id: str) -> Optional[K8sDeployment]:
        return self._deployments.get(deployment_id)

    def list_deployments(self) -> List[K8sDeployment]:
        return list(self._deployments.values())

    def update_deployment(self, deployment_id: str, deployment_in: K8sDeploymentUpdate) -> Optional[K8sDeployment]:
        if deployment_id not in self._deployments:
            return None
        
        deployment = self._deployments[deployment_id]
        update_data = deployment_in.model_dump(exclude_unset=True)
        
        updated_deployment = deployment.model_copy(update=update_data)
        self._deployments[deployment_id] = updated_deployment
        return updated_deployment

    def delete_deployment(self, deployment_id: str) -> bool:
        if deployment_id in self._deployments:
            del self._deployments[deployment_id]
            return True
        return False

k8s_service = K8sService()
