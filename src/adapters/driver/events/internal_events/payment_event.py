import json
from loguru import logger
from src.adapters.driven.events.model.notification import Notification
from src.adapters.driven.events.services.webhook.web_hook_service import WebHookService
from src.adapters.driven.infra.ports.orm_meio_de_pagamento_query import (
    OrmMeioDePagamentoQuery,
)
from src.adapters.driven.infra.ports.orm_pedido_query import OrmPedidoQuery
from src.adapters.driven.infra.repositories.orm_pagamento_repository import (
    OrmPagamentoRepository,
)
from src.adapters.driven.infra.repositories.orm_pedido_repository import (
    OrmPedidoRepository,
)
from src.adapters.driven.payment_providers.functions.get_payment_provider_from_sys_name import (
    get_payment_provider_from_sys_name,
)
from src.adapters.driven.payment_providers.providers.default_provider import (
    DefaultPaymentProvider,
)
from src.core.application.services.pagamento_service import PagamentoService
from src.core.helpers.services.in_memory_cache import InMemoryCacheService
from src.adapters.driver.events.interface.event import Event


class PaymentEvent(Event):
    def __init__(self, notification: Notification):
        super().__init__(notification)
        notification_body = json.loads(notification.message)

        self.pagamento_service = PagamentoService(
            OrmPagamentoRepository(),
            OrmPedidoRepository(InMemoryCacheService()),
            OrmPedidoQuery(),
            OrmMeioDePagamentoQuery(),
            DefaultPaymentProvider(),
            [],
        )
        payment = self.pagamento_service.get_payment(notification_body["payment_id"])
        web_hook_service = (
            WebHookService(payment.payment.webhook_url)
            if payment.payment.webhook_url
            else None
        )
        correct_payment_provider = get_payment_provider_from_sys_name(
            payment.payment.payment_method.sys_name
        )
        self.pagamento_service.payment_provider = correct_payment_provider()
        if web_hook_service:
            self.pagamento_service.notification_services.append(web_hook_service)

    def internal_finalize_payment(self, notification: Notification) -> bool:
        logger.info("Finalizando pagamento...")
        body = json.loads(notification.message)
        if not body.get("payment_id"):
            raise ValueError(
                "ID do pagamento não encontrado no corpo da mensagem, impossível continuar."
            )

        current_payment = self.pagamento_service.get_payment(body["payment_id"])
        logger.info("Finalizando pagamento: {}", current_payment.payment.id)
        self.pagamento_service.finalize_purchase_payment(current_payment.payment.id)
        logger.success("Pagamento finalizado com sucesso.")
        return True
