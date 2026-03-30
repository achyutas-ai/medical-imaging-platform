import sys
from app.services.k8s_orchestrator import orchestrator
from kubernetes.config import ConfigException

def main():
    print("--- Medical AI K8s Orchestrator Demo ---")
    
    image = "nvcr.io/nvidia/tensorflow:23.01-tf2-py3"
    gpu_count = 1
    
    try:
        print(f"Triggering inference job with image: {image} and GPU count: {gpu_count}...")
        result = orchestrator.deploy_inference_job(image, gpu_count)
        print(f"Job triggered: {result['job_name']}")
        print(f"Status: {result['status']}")
        
        # Note: In a real-world scenario, you would wait for the job to complete
        # before fetching logs.
        print("\nNote: Pod log retrieval is available via 'orchestrator.get_pod_logs(job_name)'")
        
    except ConfigException as e:
        print(f"FAILED: Connection error - {e}")
    except Exception as e:
        print(f"FAILED: Unexpected error - {e}")

if __name__ == "__main__":
    main()
