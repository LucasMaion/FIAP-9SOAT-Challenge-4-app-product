from peewee import ForeignKeyField, CharField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.payments import Payment


class PaymentMetadata(BaseModel):
    class Meta:
        db_table = "payment_metadata"

    provider_transaction_id = CharField()
    payment = ForeignKeyField(Payment, backref="metadata", null=True, unique=True)
