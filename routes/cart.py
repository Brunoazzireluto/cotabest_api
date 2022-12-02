from fastapi import APIRouter, HTTPException, Depends, responses
from sqlalchemy.orm import Session
from database import schemas, querys
from dependencies import get_db


router = APIRouter(
    prefix="/carrinho",
    tags=["Carrinho"]
)

@router.post("/carrinho/{buyer}", description="Rota que cria um carrinho e retorna um ID desse carrinho")
def create_cart(buyer:int,  db: Session = Depends(get_db)):
    return querys.create_cart(db=db, buyer=buyer)
     
@router.post('/adicionar/{id_cart}', description="Rota para adicionar produtos no carrinho, o ID do carrinho é necessario neste cenário")
def add_item_cart(id_item:int, id_cart:str, quantity: int ,db: Session = Depends(get_db) ):
    return querys.verify_quantity(db=db, id_item=id_item, quantity=quantity, id_cart=id_cart)

@router.get('/{id_cart}', description="Rota que retorna o carrinho com o valor total e todos os produtos dentro dele.")
def get_cart(id_cart:str, db: Session = Depends(get_db)):
    return querys.cart(db=db, id_cart=id_cart )

@router.put('/editar-item/{id}', description="Rota para editar a quantidade de um item do carrinho com base no id daquele item")
def edit_item(id:int, quantity: int, db: Session = Depends(get_db)):
    return querys.edit_quantity(db=db, id=id, quantity=quantity)

@router.delete('/remover/{id}', description="Rota para remover um item do carrinho")
def remove_item(id:int, db: Session = Depends(get_db)):
    return querys.remove_item(db=db, id=id)