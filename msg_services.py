from abc import ABCMeta
from abc import abstractmethod
from requests import post
from tokens import HIPCHAT_TOKEN
import msg_providers


class BaseMessagingService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def post_message_for_rating_lost(self, project_name, room_name, star_rating, num_lost, increased_average):
        pass

    @abstractmethod
    def post_message_for_rating_gained(self, project_name, room_name, star_rating, num_lost, increased_average):
        pass

    @abstractmethod
    def post_message_for_new_app_version(self, project_name, room_name, new_app_version):
        pass


class HipChat(BaseMessagingService):
    BASE_URL = "https://api.hipchat.com/v1/rooms/message"

    def post_message_for_rating_lost(self, project_name, room_name, star_rating, num_lost, increased_average):
        message_emoji = HipChat._get_emoji_for_rating_change(increased_average)
        self._post_message(
                room_name,
                msg_providers.get_message_for_rating_lost(project_name, star_rating, num_lost) + message_emoji,
                HipChat._get_color_for_rating_change(increased_average)
        )

    def post_message_for_rating_gained(self, project_name, room_name, star_rating, num_lost, increased_average):
        message_emoji = HipChat._get_emoji_for_rating_change(increased_average)
        self._post_message(
                room_name,
                msg_providers.get_message_for_rating_gained(project_name, star_rating, num_lost) + message_emoji,
                HipChat._get_color_for_rating_change(increased_average)
        )

    def post_message_for_new_app_version(self, project_name, room_name, new_app_version):
        HipChat._post_message(
                room_name,
                project_name + " app v" + new_app_version + " released!" + " (yey)",
                "green"
        )

    @staticmethod
    def _post_message(room_name, message_text, message_color):
        hipchat_url = HipChat.BASE_URL \
                      + "?auth_token=" + HIPCHAT_TOKEN \
                      + "&room_id=" + room_name \
                      + "&from=Google+Play" \
                      + "&message_format=text"

        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {"message": message_text, "color": message_color}
        post(hipchat_url, data=payload, headers=headers)

    @staticmethod
    def _get_color_for_rating_change(increased_average):
        return "green" if increased_average else "red"

    @staticmethod
    def _get_emoji_for_rating_change(increased_average):
        return " (success)" if increased_average else " (sadpanda)"
