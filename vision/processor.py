import av
import cv2

from streamlit_webrtc import VideoProcessorBase

from vision.detector import ObjectDetector
from vision.position import get_position
from vision.distance import estimate_distance
from vision.state import vision_state
from assistant.response import create_response


class VisionProcessor(VideoProcessorBase):

    def __init__(self):

        self.detector = ObjectDetector()

        self.confidence = 0.45

    def recv(self, frame):

        image = frame.to_ndarray(
            format="bgr24"
        )

        height, width = image.shape[:2]

        # -----------------------------
        # YOLO DETECTION
        # -----------------------------

        detections = self.detector.detect(
            image,
            self.confidence
        )

        processed = []

        # -----------------------------
        # PROCESS OBJECTS
        # -----------------------------

        for detection in detections:

            name = detection["name"]

            confidence = detection["confidence"]

            x1, y1, x2, y2 = detection["box"]

            pixel_width = max(
                1,
                x2 - x1
            )

            center_x = (
                x1 + x2
            ) / 2

            # Position

            position = get_position(
                center_x,
                width
            )

            # Distance

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

            # -----------------------------
            # DRAW BOX
            # -----------------------------

            cv2.rectangle(

                image,

                (x1, y1),

                (x2, y2),

                (0, 255, 0),

                2
            )

            # -----------------------------
            # LABEL
            # -----------------------------

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
                    max(y1 - 10, 25)
                ),

                cv2.FONT_HERSHEY_SIMPLEX,

                0.55,

                (0, 255, 0),

                2
            )

        # -----------------------------
        # CREATE MESSAGE
        # -----------------------------

        if processed:

            best = max(

                processed,

                key=lambda x:
                x["confidence"]
            )

            message = create_response(
                best
            )

        else:

            message = (
                "I don't see any objects."
            )

        # -----------------------------
        # UPDATE SHARED STATE
        # -----------------------------

        vision_state.update(

            message,

            processed
        )

        # -----------------------------
        # SHOW MESSAGE ON VIDEO
        # -----------------------------

        cv2.rectangle(

            image,

            (0, 0),

            (width, 60),

            (0, 0, 0),

            -1
        )

        cv2.putText(

            image,

            message,

            (15, 38),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.65,

            (255, 255, 255),

            2
        )

        return av.VideoFrame.from_ndarray(

            image,

            format="bgr24"
        )