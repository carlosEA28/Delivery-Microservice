from fastapi import FastAPI
from sqlmodel import Session, SQLModel, create_engine

from app.config import Settings
from app.dto import DeliveryCreate
from app.message import publish_delivery_event
from app.models import Delivery

engine = create_engine(Settings.DATABASE_URL, echo=True)

app = FastAPI()


@app.on_event("startup")
async def startup():
    SQLModel.metadata.create_all(engine)


@app.post("/delivery")
async def create_delivery(delivery: DeliveryCreate):
    transporte = "moto" if delivery.peso_kg <= 10.0 else "carro"
    alertas = None

    if delivery.chovendo and transporte == "moto":
        alertas = "Cuidado, clima chuvoso podendo ter atraso"

    delivery_now = Delivery(
        pedido_id=delivery.pedido_id,
        peso_kg=delivery.peso_kg,
        transporte=transporte,
        alerta=alertas,
        client=delivery.cliente,
        cep=delivery.cep,
    )

    with Session(engine) as session:
        session.add(delivery_now)
        session.commit()
        session.refresh(delivery_now)

    await publish_delivery_event(delivery_now.model_dump())
    return delivery_now
