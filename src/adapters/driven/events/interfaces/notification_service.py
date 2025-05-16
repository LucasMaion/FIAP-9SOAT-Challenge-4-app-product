from abc import abstractmethod
from src.adapters.driven.events.model.notification import Notification


class NotificationService:

    @abstractmethod
    def send_notification(self, notification: Notification) -> None:
        raise NotImplementedError
