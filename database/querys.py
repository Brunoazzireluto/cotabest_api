import random
import string
from fastapi import responses
from sqlalchemy.orm import Session
from . import models, schemas

# Querys para os items

def create_item(db: Session,):
    items = [
	{
		"id": 1,
		"name": "Ração para cachorro",
		"price": 50.00,
		"minimun": 10,
		"amount-per-package": 2,
		"max-availability": 50000
	},
	{
		"id": 2,
		"name": "Ração para coelho",
		"price": 30.00,
		"minimun": 2,
		"amount-per-package": 2,
		"max-availability": 70000
	},
	{
		"id": 3,
		"name": "Refrigerante",
		"price": 1.00,
		"minimun": 120,
		"amount-per-package": 12,
		"max-availability": 150000
	},
	{
		"id": 4,
		"name": "Feijão preto",
		"price": 4.00,
		"minimun": 24,
		"amount-per-package": 12,
		"max-availability": 12000
	},
	{
		"id": 5,
		"name": "Feijão carioca",
		"price": 6.00,
		"minimun": 24,
		"amount-per-package": 12,
		"max-availability": 12000
	},
	{
		"id": 6,
		"name": "Arroz agulha",
		"price": 4.00,
		"minimun": 40,
		"amount-per-package": 10,
		"max-availability": 300
	},
	{
		"id": 7,
		"name": "Ração para gato",
		"price": 50.00,
		"minimun": 40,
		"amount-per-package": 7,
		"max-availability": 50000
	},
	{
		"id": 8,
		"name": "Pão de forma",
		"price": 4.50,
		"minimun": 200,
		"amount-per-package": 20,
		"max-availability": 400000
	}
	
]
    for item in items:
        db_item = models.Item(
            id=item['id'], 
        name=item['name'], 
        price=item['price'], 
        minimun=item['minimun'], 
        amount_per_package=item['amount-per-package'],
        max_availability=item['max-availability']
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
    return items

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
    if item:
        if quantity < item.minimun:
            return responses.JSONResponse(
                {"Message": "Quantidade do item '{}' não pode ser menor que {}".format(item.name, item.minimun)}, status_code=403)
        elif item.max_availability < quantity:
            return responses.JSONResponse(
                {"Message": "Quantidade do item '{}' não pode ser Maior que {}".format(item.name, item.max_availability)}, status_code=403)
        else:
            add_item_cart(db=db, id_item=id_item, id_cart=id_cart, quantity=quantity)
            return responses.JSONResponse({"Message": "Item Adicionando ao carrinho"})
    else:
        return responses.JSONResponse( {"Message": "Item  Não existe no Banco de dados"}, status_code=404)

def cart(db:Session,  id_cart: str, cart_item: schemas.CartItem):
    cart = db.query(models.CartItem).filter(models.CartItem.id_cart == id_cart).all()
    items = schemas.CartItem(**cart_item.dict(), cart)
    print(items)
    return cart

