from pydantic import BaseModel


class CreatePaymentSchema(BaseModel):
    pedido_id: int
    payment_method_id: int
    webhook_url: str
