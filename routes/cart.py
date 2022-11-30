from fastapi import APIRouter, HTTPException, Depends, responses
from sqlalchemy.orm import Session
from database import schemas, querys
from dependencies import get_db


router = APIRouter(
    prefix="/Carrinho",
    tags=["Carrinho"]
)

@router.post("/carrinho/{buyer}")
def create_cart(buyer:int,  db: Session = Depends(get_db)):
    return querys.create_cart(db=db, buyer=buyer)
     
@router.post('/adicionar/{cart}')
def add_item_cart(id_item:int, id_cart:str, quantity: int ,db: Session = Depends(get_db) ):
    return querys.verify_quantity(db=db, id_item=id_item, quantity=quantity, id_cart=id_cart)

@router.get('/{id_cart}',)
def get_cart(id_cart:str, db: Session = Depends(get_db)):
    return querys.cart(db=db, id_cart=id_cart, cart_item=schemas.CartItem  )

@router.put('/editar-item/{id_item}')
def edit_item(id_item:int, id_cart:str, db: Session = Depends(get_db)):
    pass
