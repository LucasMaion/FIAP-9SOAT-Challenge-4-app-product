from abc import ABC, abstractmethod

from src.core.domain.entities.compra_entity import CompraEntity
from src.core.domain.entities.pagamento_entity import PagamentoEntity


# deve expandir para conter métodos para processar a finalização do pagamento
# deve ser capaz de armazenar metadados no DB e atualiza-los, sem repassar para o serviço de domínio
class PaymentProvider(ABC):
    @abstractmethod
    def initiate_payment(self, compra: CompraEntity) -> PagamentoEntity:
        raise NotImplementedError()

    @abstractmethod
    def cancel_payment(self, payment: PagamentoEntity) -> PagamentoEntity:
        raise NotImplementedError()

    @abstractmethod
    def finalize_payment(self, payment: PagamentoEntity) -> PagamentoEntity:
        raise NotImplementedError()
