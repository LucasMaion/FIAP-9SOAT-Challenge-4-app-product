from abc import ABC, abstractmethod
from typing import Any, List, Optional

from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.base.repository import Repository
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class ProdutoRepository(Repository, ABC):

    @abstractmethod
    def create(self, produto: PartialProdutoEntity) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def update(self, produto: ProdutoEntity) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def delete(self, produto_id: int) -> None:
        raise NotImplementedError()

    @abstractmethod
    def get_by_product_id(self, produto_id: int) -> ProdutoAggregate:
        raise NotImplementedError()

    @abstractmethod
    def find(self, query_options: ProdutoFindOptions) -> List[ProdutoAggregate]:
        raise NotImplementedError()

    @abstractmethod
    def set_selected_product_and_components(
        self,
        produto_id: int,
        purchase_id: int,
        component_ids: Optional[List[int]] = None,
    ) -> ProdutoAggregate:
        raise NotImplementedError()
