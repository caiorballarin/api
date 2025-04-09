from fastapi import APIRouter
from influxdb_client import Point
from db_conect import write_api, query_api
import os

router = APIRouter()
INFLUX_BUCKET = os.getenv("INFLUX_BUCKET")

#Criando as operações
@router.post("/sensor")
def enviar_dados(cidade: str, temperatura: float, umidade: float):
    ponto = (
        Point("Leitura")
        .tag("cidade", cidade)
        .field("temperatura", temperatura)
        .field("umidade", umidade)
    )
    write_api.write(bucket=INFLUX_BUCKET, record=ponto)
    return {"mensagem": "Dado salvo com sucesso!"}

@router.get("/sensor")
def consultar_dados():
    if not INFLUX_BUCKET:
        return {"mensagem": "BUCKET não definido"}
    
    query = f'''from(bucket: "{INFLUX_BUCKET}")
        |> range(start: -1h)
        |> filter(fn: (r) => r._measurement == "Leitura")
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