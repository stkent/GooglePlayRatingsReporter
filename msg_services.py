from abc import ABCMeta
from abc import abstractmethod
from enum import Enum
from requests import post
from tokens import HIPCHAT_TOKEN


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
        hipchat_url = HipChat.BASE_URL \
                      + "?auth_token=" + HIPCHAT_TOKEN \
                      + "&room_id=" + room_name \
                      + "&from=Google+Play" \
                      + "&message_format=text"

        headers = {"content-type": "application/x-www-form-urlencoded"}
        payload = {"message": full_message}

        if message_color:
            payload["color"] = message_color

        post(hipchat_url, data=payload, headers=headers)
