from fastapi import APIRouter, HTTPException, Depends, responses
from sqlalchemy.orm import Session
from database import schemas, querys
from dependencies import get_db


router = APIRouter(
    prefix="/Pedido",
    tags=["pedidos"]
)

@router.post('/fechar_pedido/{id_cart}', description="Rota para Fechar o pedido \
    Passamos o ID do carrinho para ele fazer a operação dentro do banco de dados",)
def close_order(id_cart: str ,db: Session = Depends(get_db)):
    return querys.close_order(db=db, id_cart=id_cart)