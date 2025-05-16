import threading
from time import sleep
from loguru import logger
from src.adapters.driven.events.interfaces.notification_service import (
    NotificationService,
)
from src.adapters.driven.events.model.notification import Notification
from src.adapters.driver.events import internal_events


class InternalNotifierService(NotificationService):

    def __init__(self, method_name: str, notification_delay: int = 5):
        self.notification_delay = notification_delay
        self.method_name = method_name

    def send_notification(self, notification: Notification) -> None:
        thread = threading.Thread(
            target=self._send_notification,
            daemon=True,
            kwargs={"notification": notification},
        )
        thread.start()

    def _send_notification(self, notification: Notification) -> None:
        logger.info(f"Sending notification {notification}")
        class_name, method_name = self.method_name.rsplit(".", 1)
        cls = getattr(internal_events, class_name)(notification)
        method = getattr(cls, method_name, None)
        sleep(self.notification_delay)
        logger.info("Processing notification")
        method(notification)
        logger.success("Notification processed")
