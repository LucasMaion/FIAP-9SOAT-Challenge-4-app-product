from src.adapters.driven.infra.models.payment_metadata import PaymentMetadata
from src.adapters.driven.payment_providers.model.payment_metadata_entity import (
    PaymentMetadataEntity,
)


class PaymentMetadataDataMapper:
    @classmethod
    def from_db_to_domain(cls, payment: PaymentMetadata):
        raise NotImplementedError()

    @classmethod
    def from_domain_to_db(cls, payment: PaymentMetadataEntity):
        raise NotImplementedError()
