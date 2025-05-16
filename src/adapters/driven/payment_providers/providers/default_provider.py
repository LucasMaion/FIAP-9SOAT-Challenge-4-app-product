from src.adapters.driven.payment_providers.interfaces.payment_provider import (
    PaymentProvider,
)
from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity


class DefaultPaymentProvider(PaymentProvider):

    def initiate_payment(self, compra: CompraEntity) -> PagamentoEntity:
        return True

    def cancel_payment(self, payment: PagamentoEntity) -> PagamentoEntity:
        return True

    def finalize_payment(self, payment: PagamentoEntity) -> PagamentoEntity:
        return True
