from src.adapters.driven.payment_providers.model.payment_metadata_entity import (
    PaymentMetadataEntity,
)


# Deve manipular a tabela SQL de metadados de pagamentos - esses metadados não são relevantes para o business domain
class PaymentMetadataOrmService:
    def get(self, payment_id: str) -> PaymentMetadataEntity:
        pass

    def create(self, payment_id: str, metadata: PaymentMetadataEntity) -> None:
        pass

    def delete(self, payment_id: str) -> None:
        pass

    def update(self, payment_id: str, metadata: PaymentMetadataEntity) -> None:
        pass
