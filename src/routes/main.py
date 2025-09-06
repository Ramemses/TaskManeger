from fastapi import APIRouter
from fastapi.responses import HTMLResponse



router = APIRouter(tags=['main'], prefix='/api')

@router.get('/')
def root():
    response = HTMLResponse("<h2>Hello world!</h2>")
    return response

