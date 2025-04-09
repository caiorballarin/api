from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from router import item
from router import site

#Instanciando o fastapi
app = FastAPI()

#Montando os arquivos estáticos do projeto
app.mount("/static", StaticFiles(directory="static"), name="static")

#Incluindo a rota, defiindo como prefixo para os endpoints como /api
app.include_router(item.router, tags=["Item"])

app.include_router(site.router, tags=["Site"])
