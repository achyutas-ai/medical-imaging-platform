import httpx
import logging
import asyncio
from typing import Dict, Any, List
from app.core.config import settings

logger = logging.getLogger(__name__)

class ServiceGateway:
    def __init__(self):
        self.services = {
            "control_plane": settings.CONTROL_PLANE_URL,
            "orchestrator": settings.ORCHESTRATOR_URL,
            "dicom_service": settings.DICOM_SERVICE_URL,
            "edge_mgmt": settings.EDGE_MGMT_URL,
        }

    async def get_service_health(self, service_name: str, url: str) -> Dict[str, Any]:
        """
        Pings a service to check its health.
        """
        async with httpx.AsyncClient(timeout=2.0) as client:
            try:
                # Most services should have a /docs or a specific health endpoint
                # For this demo, we'll try to hit a basic path
                response = await client.get(f"{url}/docs")
                if response.status_code == 200:
                    return {"name": service_name, "status": "online", "url": url}
                return {"name": service_name, "status": "degraded", "url": url}
            except Exception as e:
                return {"name": service_name, "status": "offline", "url": url, "error": str(e)}

    async def get_unified_dashboard(self) -> Dict[str, Any]:
        """
        Aggregates health and status from all internal services.
        """
        tasks = [self.get_service_health(name, url) for name, url in self.services.items()]
        results = await asyncio.gather(*tasks)
        
        return {
            "platform_status": "operational" if all(r["status"] == "online" for r in results) else "issues_detected",
            "services": results
        }

    async def trigger_coordinated_workflow(self, workflow_name: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Orchestrates a multi-service workflow.
        Example: Process DICOM -> Create K8s Job.
        """
        logger.info(f"Triggering coordinated workflow: {workflow_name}")
        
        # This is a placeholder for actual coordination logic
        if workflow_name == "dicom_to_inference":
            # 1. Call DICOM service to process
            # 2. Call Orchestrator to deploy job
            return {"status": "workflow_started", "steps": ["dicom_processing", "k8s_job_deployment"]}
            
        return {"status": "error", "message": f"Workflow {workflow_name} not found"}

gateway = ServiceGateway()
