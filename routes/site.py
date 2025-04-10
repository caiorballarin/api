from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from influxdb_client import QueryApi
from db_conect import query_api
import urllib.parse
import os

router = APIRouter()

#Configurando os templates
templates = Jinja2Templates(directory="template")

INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
INFLUX_ORG = os.getenv("INFLUX_ORG")

#Usando o Request para converter a resposta de saida para html puro usando o response_class
@router.get("/", response_class=HTMLResponse)
async def exibir_interface(request: Request):
    flux_query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -30d)
      |> filter(fn: (r) => r._measurement == "Leitura")
      |> group(columns: ["cidade"])
      |> count()
      |> keep(columns: ["cidade"])
    '''

    result = query_api.query(flux_query, org=INFLUX_ORG)
    cidades = list({record.values.get("cidade") for table in result for record in table.records})

    figuras = []
     
    for idx, cidade in enumerate(cidades, start=1):
        figuras.append({
            "id": idx,
            "name": cidade,
            "name_encoded": urllib.parse.quote(str(cidade), safe=''),
            "description": f"Dashboard de sensores da cidade {cidade}."
        })

    return templates.TemplateResponse("index.html", {
        "request": request, 
        "figuras": figuras})
