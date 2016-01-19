import json
import itertools
import redis
import os
from datetime import datetime

class DataSaver(object):
    """docstring for DataSaver"""
    def __init__(self):
        super(DataSaver, self).__init__()
        self.r = redis.StrictRedis()


    def read_data_from_file(self, project_name):
        try:
            project_file = open(self._get_project_file_name(project_name), "r")
            print project_file
            return json.load(project_file)
        except IOError:
            project_json_string = self.r.get(project_name)
            print project_json_string
            return json.loads(project_json_string)
        except ValueError:
            return {}


    def write_data_to_file(self, project_name, latest_saved_data, new_version, new_ratings):
        # load saved data for the current app version
        version_rating_history = self._get_rating_history_for_version(latest_saved_data, new_version)

        # get date string in format YYYY-MM-DD
        current_utc_date = "".join(itertools.takewhile(lambda x: x != " ", str(datetime.utcnow())))

        # add/overwrite version ratings for the current date
        version_rating_history[current_utc_date] = new_ratings

        # overwrite version data with updated dictionary
        latest_saved_data[new_version] = version_rating_history

        # save updated data to disk
        json_data = json.dumps(latest_saved_data)
        self.r.set(project_name, json_data)
        try:
            os.remove(self._get_project_file_name(project_name))
        except OSError:
            pass


    def _get_rating_history_for_version(self, saved_data, new_app_version):
        for version_number in saved_data:
            if version_number == new_app_version:
                return saved_data[new_app_version]

        return {}


    def _get_project_file_name(self, project_name):
        return project_name.replace(" ", "_").replace(",", "") + "_app_data.txt"
