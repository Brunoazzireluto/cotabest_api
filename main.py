from fastapi import FastAPI, Depends
from routes import items, cart, order
from database.db import engine, SessionLocal
from database import models, querys
from sqlalchemy.orm import Session
from dependencies import get_db
from starlette.config import Config

config = Config(".env")

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cotabest API", description="Uma api montada para o teste da Cotabest")

app.include_router(items.router)
app.include_router(cart.router)
app.include_router(order.router)

@app.on_event('startup')
async def Populate_db():
    if not querys.get_item(db=SessionLocal(), id=1):
        querys.create_items(db=SessionLocal())
    else:
        pass