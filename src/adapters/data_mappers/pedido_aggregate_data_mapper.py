from typing import List, Optional
from src.adapters.data_mappers.compra_data_mapper import CompraEntityDataMapper
from src.adapters.data_mappers.pagamento_data_mapper import PagamentoEntityDataMapper
from src.adapters.driven.infra.models.payments import Payment
from src.adapters.driven.infra.models.purchases import Purchase
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate


class PedidoAggregateDataMapper:
    @classmethod
    def from_db_to_domain(
        cls, purchase: Purchase, payments: Optional[List[Payment]] = None
    ):
        return PedidoAggregate(
            purchase=CompraEntityDataMapper.from_db_to_domain(purchase),
            payments=(
                [
                    PagamentoEntityDataMapper.from_db_to_domain(payment)
                    for payment in payments
                ]
                if payments
                else []
            ),
        )
