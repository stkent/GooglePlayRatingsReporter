from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from requests import post
from tokens import HIPCHAT_TOKEN, SLACK_TOKEN


class MessageType(Enum):
    Good = 1
    Bad = -1


class BaseMessagingService(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def post_message(self, room_name, base_message, message_type=None):
        pass


class HipChat(BaseMessagingService):
    BASE_URL = "https://api.hipchat.com/v1/rooms/message"

    def post_message(self, room_name, base_message, message_type=None):
        message_emoji_string = self._get_message_emoji_string(message_type)
        full_message = base_message + message_emoji_string

        message_color = HipChat._get_message_color(message_type)

        HipChat._post_message(room_name, full_message, message_color)

    @staticmethod
    def _get_message_emoji_string(message_type):
        return {
            MessageType.Good: " (success)",
            MessageType.Bad: " (sadpanda)"
        }[message_type]

    @staticmethod
    def _get_message_color(message_type):
        return {
            MessageType.Good: "green",
            MessageType.Bad: "red"
        }[message_type]

    @staticmethod
    def _post_message(room_name, full_message, message_color):
        url_parameters = {
            "auth_token": HIPCHAT_TOKEN,
            "room_id": room_name,
            "from": "Google Play",
            "message_format": "text"
        }

        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {"message": full_message}

        if message_color:
            payload["color"] = message_color

        post(HipChat.BASE_URL, headers=headers, params=url_parameters, data=payload)


class Slack(BaseMessagingService):
    BASE_URL = "https://slack.com/api/chat.postMessage"

    def post_message(self, room_name, base_message, message_type=None):
        message_emoji_string = self._get_message_emoji_string(message_type)
        full_message = base_message + message_emoji_string

        Slack._post_message(room_name, full_message)

    @staticmethod
    def _get_message_emoji_string(message_type):
        return {
            MessageType.Good: " :yey:",
            MessageType.Bad: " :sadpanda:"
        }[message_type]

    @staticmethod
    def _post_message(room_name, full_message):
        prefixed_room_name = "#" + room_name

        url_parameters = {
            "token": SLACK_TOKEN,
            "channel": prefixed_room_name,
            "username": "Google Play",
            "text": full_message
        }

        post(Slack.BASE_URL, params=url_parameters)
