def get_message_for_rating_lost(project_name, star_rating, num_lost):
    message_suffix = _get_message_suffix(num_lost)
    message_text = project_name + " app lost " + str(num_lost) + " existing " + str(star_rating) + message_suffix

    return message_text


def get_message_for_rating_gained(project_name, star_rating, num_gained):
    message_suffix = _get_message_suffix(num_gained)
    message_text = project_name + " app received " + str(num_gained) + " new " + str(star_rating) + message_suffix

    return message_text


def _get_message_suffix(num_lost):
    return " star reviews." if num_lost > 1 else " star review."
