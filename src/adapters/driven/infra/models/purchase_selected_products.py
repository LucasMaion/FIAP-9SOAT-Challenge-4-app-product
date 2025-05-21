from peewee import ForeignKeyField, IntegerField, FloatField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.select_product import SelectedProduct


class PurchaseSelectedProducts(BaseModel):
    class Meta:
        db_table = "purchase_selected_product"

    product = ForeignKeyField(SelectedProduct, backref="purchases")
    purchase_id = IntegerField()
