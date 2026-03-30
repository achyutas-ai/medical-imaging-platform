from fastapi import APIRouter, HTTPException
from app.services.gateway import gateway

router = APIRouter()

@router.get("/dashboard")
async def get_dashboard():
    """
    Returns a unified view of all platform services.
    """
    return await gateway.get_unified_dashboard()

@router.post("/workflows/{workflow_name}")
async def trigger_workflow(workflow_name: str, payload: dict):
    """
    Triggers a cross-module coordinated workflow.
    """
    result = await gateway.trigger_coordinated_workflow(workflow_name, payload)
    if result.get("status") == "error":
        raise HTTPException(status_code=404, detail=result.get("message"))
    return result
