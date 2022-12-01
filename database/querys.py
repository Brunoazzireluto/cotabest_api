import random
import string
from fastapi import responses
from sqlalchemy.orm import Session
from . import models, schemas

# Querys para os items

def create_items(db: Session):
    '''
    Função que adiciona os dados de teste no banco de dados
    '''
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
    '''
    Função que retorna um item com base no id dele
    '''
    return db.query(models.Item).filter(models.Item.id == id).first()

def get_items(db: Session):
    '''
    Função que retorna todos os items no banco de dados
    '''
    return db.query(models.Item).all()

def consult_item(db: Session, name: str):
    '''
    Função que consulta o banco de dados dos produtos com base em um nome
    '''
    return db.query(models.Item).filter(models.Item.name.contains(name)).all()

#query para o Carrinho

def create_cart(db:Session, buyer: int):
    '''
    Função que cria um carrinho
    '''
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase  # Pegando uma lista de caracteres
    id = ''.join(random.choice(random_str) for i in range(35))
    db_cart = models.Cart(id=id, buyer=buyer)
    db.add(db_cart)
    db.commit()
    db.refresh(db_cart)
    return db_cart.id

def get_cart(db: Session, id: str):
    '''
    Função que Busca um carrinho com base no ID dele
    '''
    return db.query(models.Cart).filter(models.Cart.id == id).first() 

def add_item_cart(db:Session, id_item: int, id_cart: str, quantity:int):
    '''
    Função que verifica se a quantidade do item bate com a quantidade minima e com o estoque.
    '''
    cart = get_cart(db=db, id=id_cart)
    item = get_item(db=db, id=id_item)
    price = item.price * item.amount_per_package
    cart_item = models.CartItem(id_cart=id_cart, id_item=item.id, quantity=quantity, amount=(price*quantity))
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    cart.total_price = cart.total_price + cart_item.amount
    db.commit()
    return cart_item

def verify_quantity(db:Session, id_item: int, quantity:int, id_cart: str):
    '''
    Função que verifica se a quantidade do item bate com a quantidade minima e com o estoque.
    '''
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

def cart(db:Session,  id_cart: str):
    '''
    Função que faz a query pelo banco de dados e retorna os dados do carrinho formatados.
    '''
    cart_db = db.query(models.Cart).filter(models.Cart.id == id_cart).first()
    cart = []
    cart_items = []
    if cart_db:
        for items in cart_db.items:
            item = get_item(db=db, id=items.id_item)
            value = schemas.CartItem(id=items.id,id_item=items.id_item, name=item.name, quantity=items.quantity, amount=items.amount)
            cart_items.append(value)
        cart.append({'total_price':cart_db.total_price, 'items': cart_items})
        return cart
    else:
         return responses.JSONResponse( {"Message": "Carrinho Vazio"}, status_code=200)

def edit_quantity(db:Session, quantity:int, id:int):
    '''
    Função que Edita A quantidade de um item do carrinho e faz a Verificação das quantidades do produto
    '''
    item_cart = db.query(models.CartItem).filter(models.CartItem.id == id).first()
    item = get_item(db=db, id=item_cart.id_item)
    cart = get_cart(db=db, id=item_cart.id_cart)
    if item:
        if quantity < item.minimun:
            return responses.JSONResponse(
                {"Message": "Quantidade do item '{}' não pode ser menor que {}".format(item.name, item.minimun)}, status_code=403)
        elif item.max_availability < quantity:
            return responses.JSONResponse(
                {"Message": "Quantidade do item '{}' não pode ser Maior que {}".format(item.name, item.max_availability)}, status_code=403)
        else:
            cart.total_price = cart.total_price - item_cart.amount
            db.commit()
            price = item.price * item.amount_per_package
            item_cart.quantity = quantity
            item_cart.amount = price*quantity
            db.commit()
            db.refresh(item_cart)
            cart.total_price = cart.total_price + item_cart.amount
            db.commit()
            return responses.JSONResponse({"Message": "Quantidade alterada"})
    else:
        return responses.JSONResponse( {"Message": "Item  Não existe no Banco de dados"}, status_code=404)

def remove_item(db:Session, id:int):
    '''
    Função que remove um item do carrinho
    '''
    item_cart = db.query(models.CartItem).filter(models.CartItem.id == id).first()
    db.delete(item_cart)
    db.commit()
    return responses.JSONResponse({"Message": "Item Removido"})

#Querys dos pedidos

def close_order (db:Session, id_cart: str):
    """
    Função que copia os dados do banco de dados 'cart' e 'cartItem' para o banco de dados 'Order' e 'OrderItem' e 
    logo em seguida deleta os dados do carrinho deixando ele vazio
    """
    random_str = string.ascii_letters + string.digits + string.ascii_uppercase  # Pegando uma lista de caracteres
    first = ''.join(random.choice(random_str) for i in range(5))
    second = ''.join(random.choice(random_str) for i in range(6))
    cart = db.query(models.Cart).filter(models.Cart.id == id_cart).first()
    order = models.Order(id= first+'-'+second, buyer=cart.buyer, total_price=cart.total_price)
    db.add(order)
    db.commit()
    db.refresh(order)
    for item in cart.items:
        order_item = models.OrderItem(id_order=order.id, id_item=item.id_item, quantity=item.quantity, amount=item.amount )
        db.add(order_item)
        db.commit()
        db.delete(item)
        db.commit()
    db.delete(cart)
    db.commit()
    order_return = []
    order_item_return = []
    for items in order.items:
       item_db = get_item(db=db, id=items.id_item)
       item = schemas.OrderItem(id=items.id_item, name=item_db.name, quantity=items.quantity, amount=items.amount)
       order_item_return.append(item)
    order_return.append({'id': order.id, 'total_price': order.total_price, 'items': order_item_return})
    return order_return
	