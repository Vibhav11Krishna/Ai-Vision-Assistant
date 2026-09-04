def create_response(detection):

    name = detection["name"]

    position = detection["position"]

    distance = detection["distance"]

    # Unknown distance

    if distance is None:

        if position == "front":

            return f"{name} in front of you."

        return f"{name} on your {position}."

    # Convert distance into natural language

    if distance < 0.5:

        distance_text = "very close to you"

    elif distance < 1:

        distance_text = "less than one meter away"

    else:

        distance_text = f"{distance} meters away"

    # Front

    if position == "front":

        return (
            f"{name} in front of you, "
            f"{distance_text}."
        )

    # Left / right

    return (
        f"{name} on your {position}, "
        f"{distance_text}."
    )