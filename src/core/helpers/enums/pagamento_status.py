from enum import Enum


class PagamentoStatus(Enum):
    PENDENTE = 1
    PAGO = 2
    PROCESSANDO = 3
    CANCELADO = 4
