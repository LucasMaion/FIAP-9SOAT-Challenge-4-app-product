from enum import Enum


class CompraStatus(Enum):
    CRIANDO = 1
    PAGO = 2
    CANCELADO = 3
    CONCLUINDO = 4
    CONCLUIDO = 5
    EM_PREPARO = 6
    PRONTO_PARA_ENTREGA = 7
    ENTREGUE = 8
    FINALIZADO = 9
