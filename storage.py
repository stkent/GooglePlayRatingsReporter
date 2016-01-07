import json
import itertools
from datetime import datetime


def read_data_from_file(project_name):
    try:
        return json.load(open(_get_project_file_name(project_name), "r"))
    except IOError:
        return {}


def write_data_to_file(project_name, latest_saved_data, new_version, new_ratings):
    # load saved data for the current app version
    version_rating_history = _get_rating_history_for_version(latest_saved_data, new_version)

    # get date string in format YYYY-MM-DD
    current_utc_date = "".join(itertools.takewhile(lambda x: x != " ", str(datetime.utcnow())))

    # add/overwrite version ratings for the current date
    version_rating_history[current_utc_date] = new_ratings

    # overwrite version data with updated dictionary
    latest_saved_data[new_version] = version_rating_history

    # save updated data to disk
    json.dump(latest_saved_data, open(_get_project_file_name(project_name), "w"))


def _get_rating_history_for_version(saved_data, new_app_version):
    for version_number in saved_data:
        if version_number == new_app_version:
            return saved_data[new_app_version]

    return {}


def _get_project_file_name(project_name):
    return project_name.replace(" ", "_").replace(",", "") + "_app_data.txt"
