# Approximate real-world object widths in meters

OBJECT_WIDTHS = {

    "person": 0.45,

    "bicycle": 0.60,

    "car": 1.80,

    "motorcycle": 0.80,

    "bus": 2.50,

    "truck": 2.50,

    "chair": 0.50,

    "couch": 1.80,

    "bed": 1.60,

    "dining table": 1.20,

    "tv": 1.00,

    "laptop": 0.35,

    "cell phone": 0.07,

    "bottle": 0.07,

    "dog": 0.40,

    "cat": 0.25
}


# Approximate camera focal length.
# This will later be replaced with
# camera calibration / depth estimation.

FOCAL_LENGTH = 700


def estimate_distance(object_name, pixel_width):

    if object_name not in OBJECT_WIDTHS:
        return None

    if pixel_width <= 0:
        return None

    real_width = OBJECT_WIDTHS[object_name]

    distance = (
        real_width
        * FOCAL_LENGTH
        / pixel_width
    )

    return round(distance, 2)