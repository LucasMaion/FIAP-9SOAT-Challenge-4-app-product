from datetime import datetime
from typing import List, Optional
from src.adapters.data_mappers.produto_entity_data_mapper import ProdutoEntityDataMapper
from src.adapters.data_mappers.produto_aggregate_data_mapper import (
    ProdutoAggregateDataMapper,
)
from src.adapters.driven.infra.models.product_components import ProductComponent
from src.adapters.driven.infra.models.products import Product
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.select_product import SelectedProduct
from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)
from src.adapters.driven.infra.ports.orm_produto_query import OrmProductQuery
from src.adapters.driven.infra.repositories.orm_repository import OrmRepository
from src.core.domain.aggregates.produto_aggregate import ProdutoAggregate
from src.core.domain.entities.produto_entity import PartialProdutoEntity, ProdutoEntity
from src.core.domain.repositories.produto_repository import ProdutoRepository
from src.core.helpers.options.produto_find_options import ProdutoFindOptions


class OrmProdutoRepository(OrmRepository, ProdutoRepository):

    def create(self, produto: PartialProdutoEntity) -> ProdutoAggregate:
        db_item = ProdutoEntityDataMapper.from_domain_to_db(produto)
        product: Product = Product.create(**db_item)
        product.save()
        return ProdutoAggregateDataMapper.from_db_to_domain(product)

    def update(self, produto: ProdutoEntity) -> ProdutoAggregate:
        db_item = ProdutoEntityDataMapper.from_domain_to_db(produto)
        new_component = db_item.pop("components", [])

        update_query: Product = Product.update(**db_item).where(
            Product.id == db_item["id"]
        )
        update_query.execute()

        ProductComponent.delete().where(
            ProductComponent.product == produto.id
        ).execute()

        for component in new_component or []:
            ProductComponent.create(
                product=component["product"], component=component["component"]
            )
        return ProdutoAggregateDataMapper.from_db_to_domain(
            Product.get(Product.id == db_item["id"])
        )

    def delete(self, produto_id: int):
        update_query: Product = Product.update(deleted_at=datetime.now()).where(
            Product.id == produto_id
        )
        update_query.execute()

    def get_by_product_id(self, produto_id: int) -> ProdutoAggregate:
        return OrmProductQuery().get(produto_id)

    def find(self, query_options: ProdutoFindOptions) -> list[ProdutoAggregate]:
        return OrmProductQuery().find(query_options)

    def set_selected_product_and_components(
        self,
        produto_id: int,
        purchase_id: int,
        component_ids: Optional[List[int]] = None,
    ) -> ProdutoAggregate:
        selected_product = SelectedProduct.create(product=produto_id)
        selected_product.save()

        purchase_selected_product = PurchaseSelectedProducts.create(
            purchase=purchase_id,
            product=selected_product,
        )
        purchase_selected_product.save()

        for component_id in component_ids or []:
            selected_product_component = SelectedProductComponent.create(
                selected_product=selected_product,
                product_component={"id": component_id},
            )
            selected_product_component.save()

        return ProdutoAggregateDataMapper.from_db_to_domain(
            Product.get(Product.id == produto_id)
        )
