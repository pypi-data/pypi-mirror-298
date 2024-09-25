import os

import fiftyone as fo
import fiftyone.utils.data as foud
import fiftyone.zoo as foz
import jsonlines


class VertexAiLabeledImageDatasetExporterGCS(foud.LabeledImageDatasetExporter):
    def __init__(self, export_dir=None, **kwargs):
        super().__init__(export_dir)
        self.labels_path = None
        self.labels: list[tuple[fo.Detections, str]] | None = None
        self.gcs_bucket = kwargs.get("gcs_bucket")

    @property
    def requires_image_metadata(self):
        return True

    @property
    def label_cls(self):
        return fo.Detections

    def setup(self):
        assert self.export_dir is not None

        self.labels_path = os.path.join(self.export_dir, "labels.jsonl")
        self.labels = []

    def export_sample(self, image_or_path: str, label: fo.Detections, metadata=None):
        assert self.labels is not None
        print(image_or_path)

        self.labels.append((label, image_or_path))

    def close(self, *args):
        assert self.labels_path is not None
        assert self.labels is not None
        assert self.gcs_bucket is not None

        basedir = os.path.dirname(self.labels_path)
        if basedir is not None and not os.path.isdir(basedir):
            os.makedirs(basedir)

        final_labels = []

        for detections, path in self.labels:
            bounding_box_annotations = []
            filename = os.path.basename(path)
            gcs_path = f"{self.gcs_bucket}/{filename}"
            if detections is not None:
                for detection in list(detections.detections):
                    x_min, y_min, width, height = detection.bounding_box
                    label = detection.label
                    x_max = x_min + width
                    y_max = y_min + height

                    bounding_box_annotations.append(
                        {
                            "displayName": label,
                            "xMin": x_min,
                            "yMin": y_min,
                            "xMax": min(1.0, x_max),
                            "yMax": min(1.0, y_max),
                        }
                    )
            final_labels.append(
                {
                    "imageGcsUri": gcs_path,
                    "boundingBoxAnnotations": bounding_box_annotations,
                }
            )

        with jsonlines.open(self.labels_path, mode="w") as writer:
            writer.write_all(final_labels)
