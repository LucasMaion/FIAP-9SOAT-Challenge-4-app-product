from peewee import FloatField, ForeignKeyField, IntegerField

from src.adapters.driven.infra.models.base_model import BaseModel
from src.adapters.driven.infra.models.currencies import Currency
from src.adapters.driven.infra.models.payment_methods import PaymentMethod
from src.adapters.driven.infra.models.purchases import Purchase


class Payment(BaseModel):
    payment_method = ForeignKeyField(PaymentMethod, backref="payments")
    currency = ForeignKeyField(Currency, backref="payments")
    value = FloatField()
    status = IntegerField()
    purchase = ForeignKeyField(Purchase, backref="payments", null=True, unique=True)
