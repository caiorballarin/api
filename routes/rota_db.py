from fastapi import APIRouter, Request
from influxdb_client import Point
from datetime import datetime, timedelta
from fastapi.templating import Jinja2Templates
from db_conect import write_api, query_api, client
import os

router = APIRouter()
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")
INFLUX_ORG = os.getenv("INFLUX_ORG")

templates = Jinja2Templates(directory="template")

#Criando as operações
@router.post("/sensor")
def enviar_dados(cidade: str, temperatura: float, umidade: float):
    ponto = (
        Point("Leitura")
        .tag("cidade", cidade)
        .field("temperatura", temperatura)
        .field("umidade", umidade)
    )
    write_api.write(bucket=INFLUX_BUCKET, org=INFLUX_ORG, record=ponto)
    return {"mensagem": "Dado salvo com sucesso!"}

@router.get("/sensor")
def consultar_dados():
    if not INFLUX_BUCKET:
        return {"mensagem": "BUCKET não definido"}
    
    query = f'''from(bucket: "{INFLUX_BUCKET}")
        |> range(start: -3h)
        |> filter(fn: (r) => r._measurement == "Leitura")
        |> keep(columns: ["_time", "_field", "_value", "cidade"])
        '''
    
    result = []
    tables = query_api.query(query)
    for tables in tables:
        for record in tables.records:
            result.append({
                "tempo": record.get_time(),
                "cidade": record.values.get("cidade"),
                "campo": record.get_field(),
                "valor": record.get_value()
            })
    return result

@router.get("/cidades-validas")
def listar_cidades_validas():
    flux_query = f'''
    from(bucket: "{INFLUX_BUCKET}")
      |> range(start: -24h)
      |> filter(fn: (r) => r._measurement == "Leitura")
      |> group(columns: ["cidade"])
      |> count()
      |> keep(columns: ["cidade"])
    '''
    result = query_api.query(flux_query, org=INFLUX_ORG)
    cidades = list({record.values.get("cidade") for table in result for record in table.records})
    return cidades

@router.get("/dashboard/{cidade}")
def dashboard(request: Request, cidade: str):
    dash_query = f'''
    from(bucket= "{INFLUX_BUCKET}")
        |> range(start: -30d)
        |> filter( (r) => r._measurement == "Leitura" and r["cidade"] == "{cidade}")
    '''
    result = query_api.query(dash_query, org=INFLUX_ORG)

    dados = []
    for table in table:
        for record in table.records:
            dados.append({
                "tempo": record.get_time(),
                "campo": record.get_field(),
                "valor": record.get_value()
            })
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "cidade": cidade,
        "dados": dados
    })

@router.delete("/sensor")
def deleta_dados(cidade: str):
    delete_api = client.delete_api()

    stop = datetime.utcnow()
    start = stop - timedelta(days=1) # Ultimas 24 Horasr
    
    predicate = f'_measurement="Leitura" AND cidade="{cidade}"'

    delete_api.delete(
        start = start,
        stop = stop,
        predicate = predicate,
        bucket = INFLUX_BUCKET, 
        org = INFLUX_ORG
        )

    return{"mensagem": f"Dados da cidade '{cidade}' deletados com sucesso!"}