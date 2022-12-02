# Cotabest-API

Api do teste da Cotabest.
para as especificações do que a api pode fazer ver o arquivo [test.md](./test.md) que consta todos os itens necessarios para completar o test

a modelagem do banco de dados pode ser vista no arquivo [models.png](./database/models.png)

---
<br>

### 🛠️ Ferramentas utilizadas no projeto

<br>

<div style="display: inline_block">

<img align="center" style="margin: 3px" alt="Python" src="https://img.shields.io/badge/-python-%233776AB?style=for-the-badge&logo=python&logoColor=white" />
<img align="center" style="margin: 3px"  alt="FastAPI" src="https://img.shields.io/badge/-fastapi-%23009688?style=for-the-badge&logo=fastapi&logoColor=white" />
<img align="center" style="margin: 3px"  alt="Sqlite" src="https://img.shields.io/badge/-sqlite-%23003B57?style=for-the-badge&logo=sqlite&logoColor=white" />
<img align="center" style="margin: 3px"  alt="Docker" src="https://img.shields.io/badge/-docker-%232496ED?style=for-the-badge&logo=docker&logoColor=white" />

</div>

<Br>

---


<br>

### 📋 Pré-requisitos

<br>

Para conseguir implementar este software são necessarios os seguintes itens:

```
Python 3.10 ou superior
Pip 22.2 ou superior
virtualenv 20.16.5 ou superior
```
---

<br>

### 🔧 Instalação

<br>

Para fazer a instalação do requirements é necessario primeiramente criar um ambiente virtual para podermos utilizar a API.

**Linux**
instalação do virtualenv:
```
sudo apt-get install python3-venv
```
criando o ambiente virtual:
```
python3 -m venv nome_do_ambiente
```
para ativar o ambiente virtual :
```
source nome_do_ambiente/bin/activate
```
Com o ambiente devidamente ativado instalamos os requerimentos com o seguinte código:
```
pip3 install -r requirements.txt
```
após a instalação dos frameworks 

---

<br>

## ⚙️ Executando os testes e rodando aplicação em localhost

<br>

com o virtualenv ativado podemos rodar os testes unitários utilizamos código:
```
pytest
```


e para rodar a api em localhost, fazemos uso do seguinte comando:

```
uvicorn main:app --reload
```

em seguida vamos até http://127.0.0.1:8000/docs para temos uma vizualização de cada Rota da API.

---
<br>
 
## 🐋 Executando os testes e rodando a aplição em um Contêiner Docker

<br>

Para Criar a imagem do Contêiner com base no dockerfile utilizamos o comando:
```
sudo docker build -t cotabestapi .
```

após o download(se necessário) da imagem do Python 3.10 utilizamos o código:
```
sudo docker run -d --name cotabestapi -p 80:80 cotabestapi
```

Para rodar os testes usamos o comando:
```
sudo docker exec cotabestapi pytest
```

para acessarmos a primeiro pegamos o Ip do Contêiner:
```
sudo docker inspect cotabestapi  | grep "IPAddress" 
```

e por fim acessamos no navegador
```
ip.ip.ip.ip/docs
```
---
<br>

## 🌐 Rotas da API

<br>

```
get -> /itens/ 
```
Retorna a Lista de Itens cadastradas no banco de dados

---
```
get -> /itens/buscar/{name}
```
Retorna uma lista de itens com base no nome pesquisado

---
```
post -> /carrinho/carrinho/{buyer}
```
Cria um novo carrinho e retorna a string desse carrinho.  `buyer` -> id do usuario que está fazendo a compra

---
```
post -> /carrinho/adicionar/{id_cart}?id_item={id_item}&quantity={quantity}
```
Adiciona ao carrinho um produto com base no id do item e da quantidade passada, caso a quantidade seja menor que o mínimo do produto ou ultrapasse o máximo em estoque a rota retorna um erro contendo a mensagem de aviso.

---
```
get -> /carrinho/{id_cart}
```
Busca os dados do carrinho mostrando o valor total e os itens adicionados.

---
```
put -> /carrinho/editar-item/{id}?quantity={quantity}
```
Edita a quantidade de itens em um carrinho com a mesma validação que existe na rota de adição, 
o id neste caso seria o do item que está na tabela `cart_item`

---
```
delete -> /carrinho/remover/{id}
```
Remove o item do carrinho, o id neste caso seria o do item que está na tabela `cart_item`

---
```
post -> /pedido/fechar_pedido/{id_cart}
```
Cria um pedido, salva ele no banco de dados e limpa o carrinho anterior.

---

<br>
<br>
<br>
<br>


Feito por [Bruno Alves](https://github.com/Brunoazzireluto)