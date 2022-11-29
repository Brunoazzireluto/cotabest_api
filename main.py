from fastapi import FastAPI
from routes import items, cart
from database.db import engine
from database import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="model FastAPI",)

app.include_router(items.router)
app.include_router(cart.router)