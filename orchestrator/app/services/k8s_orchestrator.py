import logging
import time
from typing import Dict, Any, Optional

from kubernetes import client, config
from kubernetes.client.rest import ApiException
from kubernetes.config import ConfigException

from app.core.config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class K8sOrchestrator:
    def __init__(self):
        self._batch_api = None
        self._core_api = None
        self._initialized = False

    def _initialize_client(self):
        """Initializes K8s client with fallback logic."""
        if self._initialized:
            return
        
        try:
            # Try to load in-cluster config first (if running inside K8s)
            config.load_incluster_config()
            logger.info("Loaded in-cluster Kubernetes configuration.")
        except ConfigException:
            try:
                # Fallback to local kubeconfig
                config.load_kube_config()
                logger.info("Loaded local kube-config.")
            except ConfigException as e:
                logger.error(f"Failed to load Kubernetes configuration: {e}")
                raise ConfigException("Could not connect to Kubernetes cluster.") from e
        
        self._batch_api = client.BatchV1Api()
        self._core_api = client.CoreV1Api()
        self._initialized = True

    def deploy_inference_job(self, image_name: str, gpu_count: int, job_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Deploys a Kubernetes Job for AI inference with GPU resources.
        """
        self._initialize_client()
        
        if not job_name:
            job_name = f"inference-job-{int(time.time())}"

        # 1. Container Spec with GPU Limits
        container = client.V1Container(
            name="inference-container",
            image=image_name,
            resources=client.V1ResourceRequirements(
                limits={"nvidia.com/gpu": str(gpu_count)}
            ),
            volume_mounts=[
                client.V1VolumeMount(
                    name="dicom-storage",
                    mount_path=settings.DICOM_MOUNT_PATH
                )
            ]
        )

        # 2. Pod Spec with Volumes
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"app": "inference-job", "job-name": job_name}),
            spec=client.V1PodSpec(
                restart_policy="Never",
                containers=[container],
                volumes=[
                    client.V1Volume(
                        name="dicom-storage",
                        persistent_volume_claim=client.V1PersistentVolumeClaimVolumeSource(
                            claim_name=settings.DICOM_PVC_NAME
                        )
                    )
                ]
            )
        )

        # 3. Job Spec
        job_spec = client.V1JobSpec(
            template=template,
            backoff_limit=2,
            ttl_seconds_after_finished=3600
        )

        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(name=job_name),
            spec=job_spec
        )

        try:
            logger.info(f"Creating job: {job_name} in namespace: {settings.K8S_NAMESPACE}")
            api_response = self._batch_api.create_namespaced_job(
                namespace=settings.K8S_NAMESPACE,
                body=job
            )
            
            # Wait a few seconds for the pod to be created before attempting to get logs
            # In a real-world scenario, you might want to watch the job status
            
            return {
                "job_name": job_name,
                "status": api_response.status.to_dict() if api_response.status else "Created",
                "message": "Job successfully triggered."
            }

        except ApiException as e:
            logger.error(f"ApiException when calling BatchV1Api: {e}")
            raise

    def get_pod_logs(self, job_name: str) -> str:
        """
        Retrieves logs from the first pod associated with the given job name.
        """
        self._initialize_client()
        
        try:
            # Find the pod associated with the job
            label_selector = f"job-name={job_name}"
            pods = self._core_api.list_namespaced_pod(
                namespace=settings.K8S_NAMESPACE,
                label_selector=label_selector
            )

            if not pods.items:
                return f"No pods found for job: {job_name}"

            pod_name = pods.items[0].metadata.name
            logger.info(f"Retrieving logs for pod: {pod_name}")
            
            return self._core_api.read_namespaced_pod_log(
                name=pod_name,
                namespace=settings.K8S_NAMESPACE
            )

        except ApiException as e:
            logger.error(f"ApiException when retrieving logs: {e}")
            return f"Error retrieving logs: {e}"

orchestrator = K8sOrchestrator()
