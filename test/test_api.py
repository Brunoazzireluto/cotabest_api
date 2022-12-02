from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db import Base
from database import querys
from main import app, get_db, config



SQLALCHEMY_DATABASE_URL = "sqlite:///./cotabest-test.db"


engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@app.on_event('startup')
async def Populate_db():
    if not querys.get_item(db=TestingSessionLocal(), id=1):
        querys.create_items(db=TestingSessionLocal())
    else:
        pass

id = querys.create_cart(TestingSessionLocal(), 1)


def test_get_items():
    with TestClient(app) as client:
        response = client.get('itens/')
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 8
        
def test_search_item():
    with TestClient(app) as client:
        response = client.get(
            '/itens/buscar/cachorro'
        )
        assert response.status_code == 200, response.text
        data = response.json()
        assert data[0]['name'] == 'Ração para cachorro'
        assert data[0]['minimun'] == 10

def test_create_cart():
    with TestClient(app) as client:
        response = client.post('/carrinho/carrinho/1/')     
        assert response.status_code == 200, response.text
        data = response.json()
        assert len(data) == 35

def test_adding_item_cart_minimun():
    with TestClient(app) as client:
        
        response = client.post(f'/carrinho/adicionar/{id}?id_item=6&quantity=20')    
        assert response.status_code == 403, response.text
        data = response.json()
        assert data['Message'] == "Quantidade do item 'Arroz agulha' não pode ser menor que 40"

def test_adding_item_cart_max_availability():
    with TestClient(app) as client:
        response = client.post(f'/carrinho/adicionar/{id}?id_item=6&quantity=350')    
        assert response.status_code == 403, response.text
        data = response.json()
        assert data['Message'] == "Quantidade do item 'Arroz agulha' não pode ser Maior que 300"
    
def test_adding_item_cart_normal():
    with TestClient(app) as client:
        response = client.post(f'/carrinho/adicionar/{id}?id_item=6&quantity=100')    
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['Message'] == "Item Adicionando ao carrinho"
        
        response = client.get(f'/carrinho/{id}')
        assert response.status_code == 200, response.text
        data = response.json()
        assert  data[0]['total_price'] == 4000 



def test_editing_item_cart():
    with TestClient(app) as client:        
        response = client.get(f'/carrinho/{id}')
        assert response.status_code == 200, response.text
        data = response.json()
        id_item = data[0]['items'][0]['id']

        response_edit_wrong = client.put(f'/carrinho/editar-item/{id_item}?quantity=20')
        assert response_edit_wrong.status_code == 403, response.text
        data_edit_wrong = response_edit_wrong.json()
        assert data_edit_wrong['Message'] == "Quantidade do item 'Arroz agulha' não pode ser menor que 40"

        response_edit = client.put(f'/carrinho/editar-item/{id_item}?quantity=55')
        assert response_edit.status_code == 200, response.text
        data_edit = response_edit.json()
        assert data_edit['Message'] == "Quantidade alterada"

        response = client.get(f'/carrinho/{id}')
        assert response.status_code == 200, response.text
        data = response.json()
        assert  data[0]['total_price'] == 2200 


def test_remove_item_cart():
    with TestClient(app) as client:        
        response = client.get(f'/carrinho/{id}')
        assert response.status_code == 200, response.text
        data = response.json()
        id_item = data[0]['items'][0]['id']

        response_delete = client.delete(f'/carrinho/remover/{id_item}')
        assert response_delete.status_code == 200, response.text
        data_edit = response_delete.json()
        assert data_edit['Message'] == "Item Removido"

        response = client.get(f'/carrinho/{id}')
        assert response.status_code == 200, response.text
        data = response.json()
        assert  data[0]['total_price'] == 0 

def test_create_order():
    with TestClient(app) as client:
        response = client.post(f'/carrinho/adicionar/{id}?id_item=6&quantity=100')    
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['Message'] == "Item Adicionando ao carrinho"

        response = client.post(f'/carrinho/adicionar/{id}?id_item=6&quantity=100')    
        assert response.status_code == 200, response.text
        data = response.json()
        assert data['Message'] == "Item Adicionando ao carrinho"

        response = client.post(f'/pedido/fechar_pedido/{id}')    
        assert response.status_code == 200, response.text
        data = response.json()
        assert data[0]['total_price'] == 8000 
        assert data[0]['items'][0]['quantity'] == 100
        assert data[0]['items'][0]['amount'] == 4000
        assert data[0]['items'][0]['name'] == 'Arroz agulha'


def test_xfinal_delete():
    with TestClient(app) as client:
        querys.delete_test_data(db=TestingSessionLocal())

    