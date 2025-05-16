import json
from fastapi import APIRouter, HTTPException
from loguru import logger
from peewee import DoesNotExist
from src.adapters.driven.events.factory.notification_factory import NotificationFactory
from src.adapters.driven.events.model.notification import Notification
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
from src.adapters.driver.API.schemas.create_payment_schema import CreatePaymentSchema
from src.adapters.driver.API.schemas.web_hook_example_schema import WebHookExampleSchema
from src.core.application.services.pagamento_service import PagamentoService
from src.core.domain.aggregates.pagamento_aggregate import PagamentoAggregate
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.helpers.services.in_memory_cache import InMemoryCacheService

router = APIRouter(
    prefix="/example/webhook",
    tags=["exemplos"],
)


@router.post("/")
async def initiate_payment(event: WebHookExampleSchema) -> None:
    try:
        logger.info("Received webhook event")
        logger.info(event)
        body = json.loads(event.message)
        logger.success("extracted body")
        logger.success(body)

    except (ValueError, AttributeError) as e:
        logger.exception(e)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.exception(e)
        raise HTTPException(status_code=500, detail=str(e))
