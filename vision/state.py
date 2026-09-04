import threading


class VisionState:

    def __init__(self):
        self.lock = threading.Lock()

        self.message = "Looking for objects..."

        self.detections = []

        self.version = 0

    def update(self, message, detections):

        with self.lock:

            self.message = message

            self.detections = detections

            self.version += 1

    def get(self):

        with self.lock:

            return (
                self.message,
                list(self.detections),
                self.version
            )


# One state object for this Python process
vision_state = VisionState()