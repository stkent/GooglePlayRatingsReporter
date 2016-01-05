from __future__ import division
import json
import requests
from bs4 import BeautifulSoup
import diskops
import hipchat

global latest_saved_version, latest_saved_ratings, latest_saved_average


def _post_message_if_version_updated():
    if new_version != latest_saved_version:
        hipchat.post_message_for_new_app_version(ROOM_NAME, PROJECT_NAME, new_version)


def _post_messages_if_ratings_changed():
    rating_count_changes = [new_ratings[j] - latest_saved_ratings[j] for j in range(5)]

    for k in range(5):
        rating_count_change = rating_count_changes[k]

        if rating_count_change != 0:
            stars = 5 - k

            if rating_count_change < 0:
                hipchat.post_message_for_rating_lost(
                    PROJECT_NAME,
                    ROOM_NAME,
                    stars,
                    abs(rating_count_change),
                    stars < latest_saved_average
                )
            else:
                hipchat.post_message_for_rating_gained(
                    PROJECT_NAME,
                    ROOM_NAME,
                    stars,
                    abs(rating_count_change),
                    stars > latest_saved_average
                )


def _try_loading_config_from_disk():
    try:
        c = json.load(open("configuration.json", "r"))
    except (IOError, ValueError):
        c = {}
    return c


if __name__ == "__main__":
    config = _try_loading_config_from_disk()

    project_names = config.keys()

    for PROJECT_NAME in project_names:
        # load per-project configuration
        project_config = config[PROJECT_NAME]
        ROOM_NAME = project_config.get("room_name")
        SCRAPE_URL = project_config.get("scrape_url")

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
            # TODO: compare X.X.X version numbers more intelligently
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

        # print latest_saved_version
        # print latest_saved_ratings
        # print latest_saved_average

        _post_message_if_version_updated()
        _post_messages_if_ratings_changed()

        # save updated app data
        diskops.write_data_to_file(PROJECT_NAME, latest_saved_data, new_version, new_ratings)
