from fastapi import APIRouter, HTTPException
from model import Item

router = APIRouter()

db = []

@router.get("/items/{item_id}")
def busca_item(item_id: int):
    item_verif = next((i for i in db if i.id == item_id), None)
    if not item_verif:
        raise HTTPException(status_code=422, detail="Item inválido")
    return item_verif

@router.post("/item/")
def cria_item(item: Item):
    item_verif = any(j for j in db if j.id == item.id)
    if item_verif is True:
        raise HTTPException(status_code=422, detail="Item já existe")
    db.append(item)
    return {"mensagem":"Item criado com sucesso!", "Item": item}

@router.put("/item/{item_id}")
def atualiza_item(item: Item, item_id: int):
    item_verif = next((k for k in db if k.id == item_id), None)
    if not item_verif:
        raise HTTPException(status_code=422, detail="Item não encontrado")
    for campo, valor in item.dict().items():
        setattr(item_verif, campo, valor)
    return {"mensagem": "item atualizado com sucesso!", "Item": item_verif}

@router.delete("/item/{item_id}")
def deleta_item(item_id: int):
    item_verif = next((l for l in db if l.id == item_id), None)
    if item_verif is None:
        raise HTTPException(status_code=422, detail="Item inválido")
    db.remove(item_verif)
    return {"mensagem": "Item removido com sucesso!"}
    