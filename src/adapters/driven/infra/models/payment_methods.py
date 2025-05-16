from peewee import CharField, BooleanField

from src.adapters.driven.infra.models.base_model import BaseModel


class PaymentMethod(BaseModel):
    class Meta:
        db_table = "payment_method"

    name = CharField()
    sys_name = CharField()
    internal_comm_method_name = CharField(null=True)
    internal_comm_delay = CharField(null=True)
    description = CharField(null=True)
    is_active = BooleanField(default=True)
