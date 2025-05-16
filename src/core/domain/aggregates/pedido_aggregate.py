from typing import List, Optional

from src.core.domain.base.aggregate import AggregateRoot
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity


class PedidoAggregate(AggregateRoot):
    purchase: CompraEntity
    payments: Optional[List[PagamentoEntity]] = None
