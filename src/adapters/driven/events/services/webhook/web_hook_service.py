import json
import requests
from src.adapters.driven.events.interfaces.notification_service import (
    NotificationService,
)
from src.adapters.driven.events.model.notification import Notification


class WebHookService(NotificationService):
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url

    def send_notification(self, notification: Notification) -> None:
        requests.post(self.webhook_url, json=json.loads(notification.model_dump_json()))
