from fastapi import APIRouter, HTTPException, Depends, responses
from sqlalchemy.orm import Session
from database import schemas, querys
from dependencies import get_db


router = APIRouter(
    prefix="/Items",
    tags=["Items"]
)


@router.post("/criar_items")
def create_item( db: Session = Depends(get_db)):
    querys.create_item(db=db) 
    return responses.JSONResponse({"Message": "Items Criados com Sucesso"})


@router.get("/item/{id}", response_model=schemas.Item)
def get_item(id: int, db: Session = Depends(get_db)):
    db_item = querys.get_item(db=db, id=id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get("/Items", status_code=200,  response_model=list[schemas.Item])
def get_items(db: Session = Depends(get_db)):
    items = querys.get_items(db=db)
    return items

@router.get('/buscar/{name}', status_code=200, response_model=list[schemas.Item])
def consult_items(name: str, db: Session = Depends(get_db)):
    items = querys.consult_item(db=db, name=name)
    if len(items) == 0:
        raise HTTPException(status_code=404, detail="Items Não encontrados")
    return items
