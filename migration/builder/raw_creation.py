from src.adapters.driven.infra import db
from src.adapters.driven.infra.models.categories import Category
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.product_components import ProductComponent
from src.adapters.driven.infra.models.products import Product
from src.adapters.driven.infra.models.purchase_selected_products import (
    PurchaseSelectedProducts,
)
from src.adapters.driven.infra.models.select_product import SelectedProduct

from src.adapters.driven.infra.models.select_product_components import (
    SelectedProductComponent,
)


def create_tables():
    db.create_tables(
        [
            Category,
            Currency,
            ProductComponent,
            Product,
            PurchaseSelectedProducts,
            SelectedProductComponent,
            SelectedProduct,
        ],
        safe=True,
    )
