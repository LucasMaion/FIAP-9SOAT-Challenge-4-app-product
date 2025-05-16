from typing import Optional
from src.core.domain.base.entity import Entity, PartialEntity


class MeioDePagamentoEntity(Entity):
    name: str
    sys_name: str
    description: str
    is_active: bool
    internal_comm_method_name: Optional[str] = None
    internal_comm_delay: Optional[int] = None


class PartialMeioDePagamentoEntity(PartialEntity, MeioDePagamentoEntity):
    name: Optional[str] = None
    sys_name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
