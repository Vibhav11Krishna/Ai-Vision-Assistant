def get_position(center_x, frame_width):

    left_boundary = frame_width * 0.35
    right_boundary = frame_width * 0.65

    if center_x < left_boundary:
        return "left"

    elif center_x > right_boundary:
        return "right"

    else:
        return "front"