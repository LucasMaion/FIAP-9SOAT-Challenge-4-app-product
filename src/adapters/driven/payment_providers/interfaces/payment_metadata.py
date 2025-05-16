from abc import ABC, abstractmethod

from src.adapters.driven.payment_providers.model.payment_metadata_entity import (
    PaymentMetadataEntity,
)


class PaymentMetadata(ABC):
    @abstractmethod
    def get(self, payment_id: str) -> PaymentMetadataEntity:
        pass

    @abstractmethod
    def create(self, payment_id: str, metadata: PaymentMetadataEntity) -> None:
        pass

    @abstractmethod
    def delete(self, payment_id: str) -> None:
        pass

    @abstractmethod
    def update(self, payment_id: str, metadata: PaymentMetadataEntity) -> None:
        pass
