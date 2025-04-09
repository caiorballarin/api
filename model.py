from pydantic import BaseModel

class Item(BaseModel):
    id: int
    nome: str
    valor: float
    detalhe: str