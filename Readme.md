# Cotabest-API

Api do teste da Cotabest.
para as especificações do que a api pode fazer ver o arquivo [test.md](./test.md) que consta todos os itens necessarios para completar o test

a modelagem do banco de dados pode ser vista no arquivo [models.png](./database/models.png)

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

## ⚙️ Executando os testes e a aplicação

<br>

para rodar os testes unitários utilizamos código:
```
pytest
```


Com o virtualenv ativado podemos rodar a api em localhost, fazemos uso do seguinte comando:

```
uvicorn main:app --reload
```

em seguida vamos até http://127.0.0.1:8000/docs para temos uma vizualização de cada Rota da API.




docker inspect cotabest  | grep "IPAddress"
docker inspect mycontainer  | grep "IPAddress"

https://fastapi.tiangolo.com/deployment/docker/
https://stackoverflow.com/questions/17157721/how-to-get-a-docker-containers-ip-address-from-the-host