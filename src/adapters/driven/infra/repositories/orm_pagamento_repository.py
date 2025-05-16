from src.adapters.data_mappers.pagamento_aggregate_data_mapper import (
    PagamentoAggregateDataMapper,
)
from src.adapters.data_mappers.pagamento_data_mapper import PagamentoEntityDataMapper
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.repositories.orm_repository import OrmRepository
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.compra_entity import PartialCompraEntity
from src.core.domain.entities.pagamento_entity import PartialPagamentoEntity
from src.core.domain.repositories.pagamento_repository import PagamentoRepository


class OrmPagamentoRepository(OrmRepository, PagamentoRepository):
    def create(
        self, payment: PartialPagamentoEntity, purchase: PartialCompraEntity
    ) -> PedidoAggregate:
        db_item = PagamentoEntityDataMapper.from_domain_to_db(payment, purchase)
        payment: Payment = Payment.create(**db_item)
        payment.save()
        return PagamentoAggregateDataMapper.from_db_to_domain(payment)

    def get(self, payment_id: int) -> PedidoAggregate:
        payment = Payment.get_by_id(payment_id)
        return PagamentoAggregateDataMapper.from_db_to_domain(payment)

    def update(
        self, payment: PartialPagamentoEntity, purchase: PartialCompraEntity
    ) -> PedidoAggregate:
        db_item = PagamentoEntityDataMapper.from_domain_to_db(payment, purchase)
        update_query: Payment = Payment.update(**db_item).where(
            Payment.id == db_item["id"]
        )
        update_query.execute()
        payment = Payment.get_by_id(db_item["id"])
        return PagamentoAggregateDataMapper.from_db_to_domain(payment)
