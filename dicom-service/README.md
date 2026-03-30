# DICOM Processing Service

The **DICOM Processing Service** is a specialized pipeline for handling medical imaging data and orchestrating AI inference. It provides a bridge between raw DICOM storage and modern machine learning frameworks.

## 🌟 Key Features

-   **Metadata Extraction**: Uses `pydicom` to parse Patient ID, Study Date, and other critical DICOM headers.
-   **Image Normalization**: Employs **OpenCV** to convert and normalize 16-bit DICOM pixel data into 8-bit, AI-ready NumPy arrays.
-   **AI Inference Engine**: Integrates **PyTorch** for model execution (currently includes a `MockModel` for demonstration).
-   **Structured Reporting (SR)**: Automatically exports AI findings into a JSON-formatted DICOM Structured Report.

---

## 🚀 Getting Started

### Prerequisites

-   Python 3.9+
-   Sample DICOM files (`.dcm`)

### Installation

1.  Navigate to the `dicom-service` directory:
    ```bash
    cd dicom-service
    ```

2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate  # Windows
    # source venv/bin/activate # macOS/Linux
    ```

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

Edit the `.env` file to customize processing parameters:

```ini
DEFAULT_IMAGE_SIZE=512
MODEL_PATH="app/models/mock_model.pt"
OUTPUT_DIR="output/sr"
```

---

## 🛠️ Usage

### Running the Processing Pipeline

To process a DICOM file and run a mock inference:

```bash
python -m app.main <path_to_your_dicom_file>
```

### Programmatic Example

```python
from app.services.dicom_processor import dicom_processor
from app.services.inference_engine import inference_engine

# Step 1: Process Image
metadata = dicom_processor.read_metadata("path/to/image.dcm")
image = dicom_processor.normalize_pixel_data("path/to/image.dcm")

# Step 2: Run Inference
results = inference_engine.perform_inference(image)

# Step 3: Export Report
sr_path = inference_engine.export_structured_report(metadata, results)
print(f"Report saved at: {sr_path}")
```

---

## 📁 Project Structure

```text
dicom-service/
├── app/
│   ├── core/           # Configuration management
│   ├── services/       # Core logic (dicom_processor.py, inference_engine.py)
│   └── main.py         # Pipeline entry point
├── output/             # Generated Structured Reports (SR)
├── requirements.txt
└── .env
```
