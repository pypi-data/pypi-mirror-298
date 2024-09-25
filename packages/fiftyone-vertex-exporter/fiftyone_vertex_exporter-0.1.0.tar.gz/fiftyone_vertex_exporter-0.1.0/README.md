# Fiftyone Vertex AI exporter

This package provides exporter for fiftyone compatible with format used by Vertex AI.
Currently it only supports detections, and does not move the actual images to gcs bucket.

## Usage
```python
dataset = foz.load_zoo_dataset(
    "coco-2017", split="test", label_types=["detections"]
)

exporter = VertexAiLabeledImageDatasetExporterGCS(
    "export",
    gcs_bucket="gs://bucket/test",
)

dataset.export(dataset_exporter=exporter)
```
