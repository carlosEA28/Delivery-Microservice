from pydantic import BaseModel


class DeliveryCreate(BaseModel):
    pedido_id: int
    cliente: str
    cep: str
    peso_kg: float
    chovendo: bool = False
