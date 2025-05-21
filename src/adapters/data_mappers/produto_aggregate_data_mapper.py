from typing import List, Optional
from src.adapters.data_mappers.produto_entity_data_mapper import ProdutoEntityDataMapper
from src.adapters.driven.infra.models.products import Product
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.helpers.enums.compra_status import CompraStatus


class ProdutoAggregateDataMapper:
    @classmethod
    def from_db_to_domain(cls, produto: Product):
        purchases = []
        for selected_product in produto.selected_product:
            purchases.extend(
                [purchase.purchase_id for purchase in selected_product.purchases]
            )
        return ProdutoAggregate(
            orders=list(set(purchases)),
            product=ProdutoEntityDataMapper.from_db_to_domain(produto),
        )
