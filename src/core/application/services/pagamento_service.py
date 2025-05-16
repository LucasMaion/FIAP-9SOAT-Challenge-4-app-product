import json
from typing import List
from src.adapters.driven.events.model.notification import Notification
from src.core.application.interfaces.pagamento import IPagamentoService
from src.core.domain.aggregates.pagamento_aggregate import PagamentoAggregate
from src.core.domain.aggregates.pedido_aggregate import PedidoAggregate
from src.core.domain.entities.meio_de_pagamento_entity import MeioDePagamentoEntity
from src.core.domain.entities.pagamento_entity import PartialPagamentoEntity
from src.core.helpers.enums.compra_status import CompraStatus
from src.core.helpers.enums.pagamento_status import PagamentoStatus


class PagamentoService(IPagamentoService):
    def initiate_purchase_payment(
        self, pedido_id: int, payment_method_id: int, webhook_url: str
    ) -> PagamentoAggregate:
        notification_title = "Inicialização de Pagamento"
        notification_message = {"payment_id": None, "message": ""}
        payment: PagamentoAggregate = None
        try:
            pedido = self.purchase_query.get(pedido_id)
            if not pedido:
                raise ValueError("Pedido não encontrado.")
            if pedido.payments:
                raise ValueError("Pedido já foi pago.")
            if pedido.purchase.total.value <= 0:
                raise ValueError("Valor do pedido não pode ser zero ou negativo")
            if pedido.purchase.status != CompraStatus.CRIANDO:
                raise ValueError("Pedido inválido para pagamento.")
            payment_method = self.meio_de_pagamento_query.get(payment_method_id)
            if not payment_method:
                raise ValueError("Meio de pagamento não encontrado.")
            if payment_method.is_active is False:
                raise ValueError("Meio de pagamento inativo.")
            if self.payment_provider.initiate_payment(pedido.purchase):
                payment_entity = PartialPagamentoEntity(
                    payment_method=payment_method,
                    status=PagamentoStatus.PROCESSANDO,
                    payment_value=pedido.purchase.total,
                    webhook_url=webhook_url,
                )
                payment: PagamentoAggregate = self.payment_repository.create(
                    payment_entity, pedido.purchase
                )
                pedido.purchase.status = CompraStatus.CONCLUINDO
                payment.purchase = self.pedido_repository.update(pedido.purchase)
                notification_message["message"] = f"Pagamento iniciado com sucesso."
                notification_message["payment_id"] = payment.payment.id
                return payment
            raise ValueError("Falha ao processar pagamento pelo provedor.")

        except ValueError as e:
            notification_message["message"] = f"Erro ao finalizar pagamento: {str(e)}"
            raise e
        except Exception as e:
            notification_message["message"] = f"Erro inesperado ao finalizar pagamento"
            raise e
        finally:
            self._notify_payment_status(
                payment, notification_message, notification_title
            )

    def cancel_purchase_payment(self, payment_id: int) -> PedidoAggregate:
        notification_title = "Cancelamento de Pagamento"
        notification_message = {"payment_id": payment_id, "message": ""}
        payment = self.payment_repository.get(payment_id)
        try:
            if not payment:
                raise ValueError("Pagamento não encontrado.")

            if payment.payment.status == PagamentoStatus.PAGO:
                raise ValueError("Pagamento já concluído.")

            if payment.payment.status not in (
                PagamentoStatus.PROCESSANDO,
                PagamentoStatus.PENDENTE,
            ):
                raise ValueError("Pagamento não está ativo.")

            if not payment.purchase:
                raise ValueError("Nenhum pedido associado ao pagamento encontrado.")

            if self.payment_provider.cancel_payment(payment.payment):
                payment.payment.status = PagamentoStatus.CANCELADO
                payment.payment = self.payment_repository.update(
                    payment.payment, payment.purchase
                )
                payment.purchase.status = CompraStatus.CRIANDO
                payment.purchase = self.pedido_repository.update(payment.purchase)
            else:
                raise ValueError("Falha ao cancelar pagamento.")
            notification_message["message"] = f"Pagamento cancelado com sucesso."
            return payment
        except ValueError as e:
            notification_message["message"] = f"Erro ao finalizar pagamento: {str(e)}"
            raise e
        except Exception as e:
            notification_message["message"] = f"Erro inesperado ao finalizar pagamento"
            raise e
        finally:
            self._notify_payment_status(
                payment, notification_message, notification_title
            )

    def finalize_purchase_payment(self, payment_id: int) -> PagamentoAggregate:
        notification_title = "Finalização de Pagamento"
        notification_message = {"payment_id": payment_id, "message": ""}
        payment: PagamentoAggregate = None
        try:
            payment = self.payment_repository.get(payment_id)
            if not payment:
                raise ValueError("Pagamento não encontrado.")

            if payment.payment.status == PagamentoStatus.PAGO:
                raise ValueError("Pagamento já concluído.")

            if payment.payment.status not in (
                PagamentoStatus.PROCESSANDO,
                PagamentoStatus.PENDENTE,
            ):
                raise ValueError("Pagamento não está ativo.")

            if not payment.purchase:
                raise ValueError("Nenhum pedido associado ao pagamento encontrado.")

            if self.payment_provider.finalize_payment(payment.payment):
                payment.payment.status = PagamentoStatus.PAGO
                payment.payment = self.payment_repository.update(
                    payment.payment, payment.purchase
                )
                payment.purchase.status = CompraStatus.CONCLUIDO
                payment.purchase = self.pedido_repository.update(payment.purchase)
            else:
                raise ValueError("Falha ao finalizar o pagamento.")
            notification_message["message"] = f"Pagamento finalizado com sucesso."
            return payment

        except ValueError as e:
            notification_message["message"] = f"Erro ao finalizar pagamento: {str(e)}"
            raise e
        except Exception as e:
            notification_message["message"] = f"Erro inesperado ao finalizar pagamento."
            raise e
        finally:
            self._notify_payment_status(
                payment, notification_message, notification_title
            )

    def list_payment_methods(self) -> List[MeioDePagamentoEntity]:
        return self.meio_de_pagamento_query.get_all()

    def get_payment_method(
        self, payment_method_id: int
    ) -> MeioDePagamentoEntity | None:
        return self.meio_de_pagamento_query.get(payment_method_id)

    def get_payment(self, payment_id: int) -> PagamentoAggregate | None:
        return self.payment_repository.get(payment_id)

    def _notify_payment_status(
        self, payment: PagamentoAggregate, message: str | dict, title: str
    ):
        for notification_service in self.notification_services:
            notification = Notification(
                title=title,
                message=json.dumps(message) if isinstance(message, dict) else message,
                user_id=(
                    payment.purchase.client.id
                    if hasattr(payment, "purchase")
                    and hasattr(payment.purchase, "client")
                    else None
                ),
            )
            notification_service.send_notification(notification)
