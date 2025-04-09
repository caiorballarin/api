from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

#Configurando os templates
templates = Jinja2Templates(directory="template")

#Colocando umas informações teste
figuras = [
   {
        "id": 1,
        "name": "Servidor 1",
        "description": "A perfect circle with equal radius in all directions.",
    },
    {
        "id": 2,
        "name": "Servidor 2",
        "description": "A four-sided polygon with equal sides and right angles.",
    },
    {
        "id": 3,
        "name": "Servidor 3",
        "description": "A three-sided polygon with three angles.",
    },
    {
        "id": 4,
        "name": "Servidor 4",
        "description": "A six-sided polygon with six angles.",
    },
    {
        "id": 5,
        "name": "Servidor 5",
        "description": "A quadrilateral with all sides equal in length.",
    },
    {
        "id": 6,
        "name": "Servidor 6",
        "description": "A five-sided polygon with five angles.",
    }
]

#Usando o Request para converter a resposta de saida para html puro usando o response_class
@router.get("/", response_class=HTMLResponse)
async def exibir_interface(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "figuras": figuras})

@router.get("/figuras", response_class=HTMLResponse)
async def lista_figuras(request: Request):
    return templates.TemplateResponse("item_list.html", {"request": request, "figuras": figuras})

@router.get("/figura/{item_id}", response_class=HTMLResponse)
async def detalhe_figura(request: Request, item_id: int):
    fig_verif = next((f for f in figuras if f["id"] == item_id), None)
    if fig_verif is None:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("item_detail.html", {"request": request, "figura": fig_verif})