import os
import sys
import numpy as np
from app.services.dicom_processor import dicom_processor
from app.services.inference_engine import InferenceEngine

def run_pipeline(dicom_file_path: str):
    print(f"--- Medical AI DICOM Pipeline Demo ---")
    
    if not os.path.exists(dicom_file_path):
        print(f"ERROR: File not found - {dicom_file_path}")
        print("Please provide a valid path to a DICOM file.")
        return

    # 1. Read Metadata
    print("\n[Step 1] Extraction metadata...")
    metadata = dicom_processor.read_metadata(dicom_file_path)
    print(f"Patient ID: {metadata['PatientID']}")
    print(f"Study Date: {metadata['StudyDate']}")

    # 2. Normalize Pixel Data
    print("\n[Step 2] Normalizing pixel data...")
    processed_image = dicom_processor.normalize_pixel_data(dicom_file_path)
    print(f"Processed image shape: {processed_image.shape}")

    # 3. Perform Inference
    print("\n[Step 3] Running AI inference...")
    engine = InferenceEngine()
    results = engine.perform_inference(processed_image)
    print(f"Inference complete. Overall confidence: {results['overall_confidence']:.4f}")

    # 4. Export Structured Report
    print("\n[Step 4] Exporting Structured Report...")
    sr_path = engine.export_structured_report(metadata, results)
    print(f"Structured Report exported to: {sr_path}")

if __name__ == "__main__":
    # If no file provided, print usage
    if len(sys.argv) < 2:
        print("Usage: python -m app.main <path_to_dicom_file>")
    else:
        run_pipeline(sys.argv[1])
