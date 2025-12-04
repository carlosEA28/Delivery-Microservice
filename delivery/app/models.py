from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel


class Status(str, Enum):
    AGUARDANDO = "AGUARDANDO RETIRADA"
    PROCESSANDO = "PROCESSANDO"
    ENTREGUE = "ENTREGUE"


class Delivery(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int
    client: str
    cep: str
    peso_kg: float
    transporte: str
    status: Status = Status.AGUARDANDO
    alerta: Optional[str] = None
