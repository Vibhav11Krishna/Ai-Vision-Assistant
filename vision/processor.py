import av
import cv2

from streamlit_webrtc import VideoProcessorBase

from vision.detector import ObjectDetector
from vision.position import get_position
from vision.distance import estimate_distance
from assistant.response import create_response


class VisionProcessor(VideoProcessorBase):

    def __init__(self):

        self.detector = ObjectDetector()

        self.confidence = 0.45

        self.current_message = "Looking..."

        self.detections = []

    def recv(self, frame):

        # Convert WebRTC frame to OpenCV image

        image = frame.to_ndarray(
            format="bgr24"
        )

        height, width = image.shape[:2]

        # YOLO detection

        detections = self.detector.detect(
            image,
            self.confidence
        )

        processed = []

        # Process every detected object

        for detection in detections:

            name = detection["name"]

            confidence = detection["confidence"]

            x1, y1, x2, y2 = detection["box"]

            # Object width in pixels

            pixel_width = max(
                1,
                x2 - x1
            )

            # Object center

            center_x = (
                x1 + x2
            ) / 2

            # Left / right / front

            position = get_position(
                center_x,
                width
            )

            # Approximate distance

            distance = estimate_distance(
                name,
                pixel_width
            )

            object_data = {

                "name": name,

                "confidence": confidence,

                "position": position,

                "distance": distance,

                "box": (
                    x1,
                    y1,
                    x2,
                    y2
                )
            }

            processed.append(
                object_data
            )

            # Draw bounding box

            cv2.rectangle(
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            # Label

            if distance is not None:

                label = (
                    f"{name} "
                    f"{confidence:.0%} "
                    f"| {position} "
                    f"| {distance}m"
                )

            else:

                label = (
                    f"{name} "
                    f"{confidence:.0%} "
                    f"| {position}"
                )

            cv2.putText(
                image,
                label,
                (
                    x1,
                    max(y1 - 10, 20)
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.55,
                (0, 255, 0),
                2
            )

        # Save processed detections

        self.detections = processed

        # Generate assistant message

        if processed:

            # Highest confidence detection

            best = max(
                processed,
                key=lambda x: x["confidence"]
            )

            self.current_message = create_response(
                best
            )

        else:

            self.current_message = (
                "I don't see any objects."
            )

        # Return processed frame

        return av.VideoFrame.from_ndarray(
            image,
            format="bgr24"
        )