import requests

from src.py.deployment.utils.config import PUSHCUT_TOKEN, PUSHCUT_USER

URL = "https://api.pushover.net/1/messages.json"


class Pushcut:
    def send_notification(
        self, title: str, message: str, priority: int = 0, sound: str = "pushover"
    ) -> None:
        body = {
            "token": PUSHCUT_TOKEN,
            "user": PUSHCUT_USER,
            "title": title,
            "message": message,
            "priority": priority,
            "sound": sound,
        }
        requests.post(URL, data=body)
