import random
import string
from fastapi import responses
from sqlalchemy.orm import Session
from . import models, schemas

# Querys para os items

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, id: int):
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_items(db: Session):
    return db.query(models.Item).all()

def consult_item(db: Session, name: str):
    return db.query(models.Item).filter(models.Item.name.contains(name)).all()

def create_cart(db:Session, buyer: int):
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase  # Pegando uma lista de caracteres
    id = ''.join(random.choice(random_str) for i in range(35))
    db_cart = models.Cart(id=id, buyer=buyer)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart.id

#query para o Carrinho

def get_cart(db: Session, id: str):
    return db.query(models.Cart).filter(models.Cart.id == id).first() 

def add_item_cart(db:Session, id_item: int, id_cart: str, quantity:int):
    cart = get_cart(db=db, id=id_cart)
    item = get_item(db=db, id=id_item)
    cart_item = models.CartItem(id_cart=id_cart, id_item=item.id, quantity=quantity, amount=(item.price*quantity))
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    return cart_item

def verify_quantity(db:Session, id_item: int, quantity:int, id_cart: str):
    item = get_item(db=db, id=id_item)
    if quantity < item.minimun:
        return responses.JSONResponse(
            {"Message": "Quantidade do item '{}' não pode ser menor que {}".format(item.name, item.minimun)})
    elif item.max_availability < quantity:
        return responses.JSONResponse(
            {"Message": "Quantidade do item '{}' não pode ser Maior que {}".format(item.name, item.max_availability)})
    else:
        add_item_cart(db=db, id_item=id_item, id_cart=id_cart, quantity=quantity)
        return responses.JSONResponse({"Message": "Item Adicionando ao carrinho"})