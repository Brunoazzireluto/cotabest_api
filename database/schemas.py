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

class Cart(CartBase):
    items: list[Item] = []

    class Config:
        orm_mode = True

class CartItem(BaseModel):
    id: int
    id_cart: str
    id_item: int
    quantity: int
    amount: float