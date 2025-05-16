from abc import ABC

from src.adapters.driven.events.model.notification import Notification


class Event(ABC):
    def __init__(self, notification: Notification):
        self.notification = notification
