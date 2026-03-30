import pydicom
import cv2
import numpy as np
from typing import Dict, Any, Tuple
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

class DICOMProcessor:
    @staticmethod
    def read_metadata(file_path: str) -> Dict[str, Any]:
        """
        Reads essential metadata from a DICOM file.
        """
        try:
            ds = pydicom.dcmread(file_path)
            metadata = {
                "PatientID": getattr(ds, "PatientID", "Anonymous"),
                "PatientName": str(getattr(ds, "PatientName", "Unknown")),
                "StudyDate": getattr(ds, "StudyDate", "19000101"),
                "Modality": getattr(ds, "Modality", "OT"),
                "Manufacturer": getattr(ds, "Manufacturer", "Generic"),
                "InstanceNumber": getattr(ds, "InstanceNumber", 0),
            }
            return metadata
        except Exception as e:
            logger.error(f"Error reading DICOM metadata: {e}")
            raise

    @staticmethod
    def normalize_pixel_data(file_path: str, target_size: Tuple[int, int] = None) -> np.ndarray:
        """
        Converts DICOM pixel data into a normalized NumPy array.
        """
        try:
            ds = pydicom.dcmread(file_path)
            pixel_array = ds.pixel_array.astype(float)

            # Rescale to 0-255
            rescaled = (np.maximum(pixel_array, 0) / pixel_array.max()) * 255.0
            uint8_image = np.uint8(rescaled)

            # Resize using OpenCV
            if not target_size:
                target_size = (settings.DEFAULT_IMAGE_SIZE, settings.DEFAULT_IMAGE_SIZE)
            
            resized = cv2.resize(uint8_image, target_size, interpolation=cv2.INTER_AREA)

            # Normalize to 0-1 for AI inference
            normalized = resized.astype(np.float32) / 255.0
            
            # Add channel dimension if necessary (e.g. for CNNs)
            if len(normalized.shape) == 2:
                normalized = np.expand_dims(normalized, axis=0)

            return normalized
        except Exception as e:
            logger.error(f"Error normalizing DICOM pixel data: {e}")
            raise

dicom_processor = DICOMProcessor()
