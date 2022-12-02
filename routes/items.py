from fastapi import APIRouter, HTTPException, Depends, responses
from sqlalchemy.orm import Session
from database import schemas, querys
from dependencies import get_db


router = APIRouter(
    prefix="/itens",
    tags=["Itens"]
)


@router.get("/", status_code=200,  response_model=list[schemas.Item], description="Rota que trás como retorno todos os produtos \
     cadastrados no banco de dados")
def get_items(db: Session = Depends(get_db)):
    items = querys.get_items(db=db)
    return items

@router.get('/buscar/{name}', status_code=200, response_model=list[schemas.Item], description="Rota para fazer a consulta de um produto \
     pelo nome")
def consult_items(name: str, db: Session = Depends(get_db)):
    items = querys.consult_item(db=db, name=name)
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="Items Não encontrados")
    return items
