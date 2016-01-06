from __future__ import division
import json
import requests
from bs4 import BeautifulSoup
import diskops
from msg_services import MessageType
from msg_services import HipChat, Slack
import msg_providers

global latest_saved_version, latest_saved_ratings, latest_saved_average


def _post_message_if_version_updated(msg_service, room_name):
    if new_version != latest_saved_version:
        msg_service.post_message(
            room_name=room_name,
            base_message=PROJECT_NAME + " app v" + new_version + " released!",
            message_type=MessageType.Good)


def _post_messages_if_ratings_changed(msg_service, room_name):
    rating_count_changes = [new_ratings[j] - latest_saved_ratings[j] for j in range(5)]

    for k in range(5):
        rating_count_change = rating_count_changes[k]

        if rating_count_change != 0:
            stars = 5 - k

            if rating_count_change < 0:
                base_message = msg_providers.get_message_for_rating_lost(PROJECT_NAME, stars, abs(rating_count_change))

                msg_service.post_message(
                    room_name=room_name,
                    base_message=base_message,
                    message_type=MessageType.Good if stars < latest_saved_average else MessageType.Bad)
            else:
                base_message = msg_providers.get_message_for_rating_gained(PROJECT_NAME, stars, rating_count_change)

                msg_service.post_message(
                    room_name=room_name,
                    base_message=base_message,
                    message_type=MessageType.Good if stars >= latest_saved_average else MessageType.Bad)


def _try_loading_config_from_disk():
    try:
        c = json.load(open("configuration.json", "r"))
    except (IOError, ValueError):
        c = {}
    return c


if __name__ == "__main__":
    config = _try_loading_config_from_disk()

    # TODO: refactor/relocate these checks
    if not isinstance(config, dict):
        raise LookupError("Configuration file is malformed.")

    if "services" not in config:
        raise LookupError("Configuration file is malformed.")

    if "apps" not in config:
        raise LookupError("Configuration file is malformed.")

    enabled_service_names = config["services"]

    service_lookup_dict = {
        "hipchat": HipChat(),
        "slack": Slack()
    }

    for app in config["apps"]:
        # load per-project configuration
        PROJECT_NAME = app["name"]
        SCRAPE_URL = app["scrape_url"]
        CHANNELS = app["channels"]

        # get updated app data from the play store:
        r = requests.get(SCRAPE_URL)

        # extract rating counts and app version number:
        soup = BeautifulSoup(r.text)
        new_version = soup.find("div", {"itemprop": "softwareVersion"}).next.strip()
        new_ratings = [int(rating.string.replace(",", "")) for rating in soup.find_all("span", "bar-number")]

        # load stored app data
        latest_saved_data = diskops.read_data_from_file(PROJECT_NAME)

        # extract saved data for comparisons
        try:
            latest_saved_version = max(latest_saved_data.keys())
            latest_saved_version_data = latest_saved_data[latest_saved_version]
            latest_saved_date = max(latest_saved_version_data.keys())
            latest_saved_ratings = latest_saved_version_data[latest_saved_date]

            num_ratings = sum(latest_saved_ratings)
            latest_saved_average = sum([(5 - i) * latest_saved_ratings[i] for i in range(5)]) / num_ratings
        except (ValueError, KeyError):
            latest_saved_version = ""
            latest_saved_ratings = [0 for x in range(5)]
            latest_saved_average = 3

        for service_name in CHANNELS:
            if service_name in enabled_service_names and service_name in service_lookup_dict:
                service = service_lookup_dict[service_name]
                channel = CHANNELS[service_name]

                _post_message_if_version_updated(service, channel)
                _post_messages_if_ratings_changed(service, channel)

        # save updated app data
        diskops.write_data_to_file(PROJECT_NAME, latest_saved_data, new_version, new_ratings)
