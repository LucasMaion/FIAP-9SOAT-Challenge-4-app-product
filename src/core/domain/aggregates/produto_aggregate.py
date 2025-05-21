from typing import List, Optional

from pydantic import Field
from src.core.domain.base.aggregate import AggregateRoot
from src.core.domain.entities.produto_entity import ProdutoEntity


class ProdutoAggregate(AggregateRoot):
    product: ProdutoEntity
    orders: Optional[List[int]] = None
