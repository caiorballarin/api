#Fazendo a conexao com o influxdb
import os #Importando o modulo do sistema
from dotenv import load_dotenv #Importantdo a biblioteca do python que vai vai ser o load do txt .env que defini as variaveis de ambiente como variaveis de ambiente do sistema.
from influxdb_client import InfluxDBClient

# Força o caminho absoluto até o .env
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path=dotenv_path) #Instanciando essa funcao para usar o arquivo .env

#Definindo as variaveis com base no que tem salvo no arquivo .env
INFLUX_URL = os.getenv("INFLUX_URL")
INFLUX_TOKEN = os.getenv("INFLUX_TOKEN")
INFLUX_ORG = os.getenv("INFLUX_ORG")

#instanciando um parametro de rota
client = InfluxDBClient(   
    url = INFLUX_URL,
    token = INFLUX_TOKEN,
    org = INFLUX_ORG
)

write_api = client.write_api()
query_api = client.query_api()
