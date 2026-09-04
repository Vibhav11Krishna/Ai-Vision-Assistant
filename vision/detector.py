from ultralytics import YOLO


class ObjectDetector:

    def __init__(self):
        # YOLO11 nano model
        # Ultralytics automatically downloads it
        # the first time the application runs.
        self.model = YOLO("yolo11n.pt")

    def detect(self, frame, confidence=0.45):

        results = self.model(
            frame,
            conf=confidence,
            verbose=False
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                class_id = int(box.cls[0])
                conf = float(box.conf[0])

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0].tolist()
                )

                object_name = self.model.names[class_id]

                detections.append({
                    "name": object_name,
                    "confidence": conf,
                    "box": (x1, y1, x2, y2)
                })

        return detections