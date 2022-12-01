from pydantic import BaseModel, validator

#Schema para chamar os Items
class ItemBase(BaseModel):
    name: str
    price:  float 
    minimun: int
    amount_per_package: int
    max_availability: int

    
class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True
        

#Schema para chamar os modelos do carrinho
   
class CartBase(BaseModel):
    id: str
    buyer: int

class CartCreate(CartBase):
    pass


class CartItem(BaseModel):
    id:int
    id_item:int
    name: str
    quantity: int
    amount: float


#Schemas para o modelo de pedidos
class OrderItem(BaseModel):
    id:int
    name: str
    quantity: int
    amount: float

class Order(BaseModel):
    id: str
    total_price: float
    items: list[OrderItem] = []
