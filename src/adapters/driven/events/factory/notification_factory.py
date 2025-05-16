from src.adapters.driven.events.services.internal.internal_notifier_service import (
    InternalNotifierService,
)
from src.adapters.driven.events.services.webhook.web_hook_service import WebHookService


class NotificationFactory:
    @classmethod
    def create_web_hook_service(cls, webhook_url) -> WebHookService:
        return WebHookService(webhook_url)

    @classmethod
    def create_internal_event_service(
        cls, method_name: str, notification_delay: int
    ) -> InternalNotifierService:
        return InternalNotifierService(method_name, notification_delay)
