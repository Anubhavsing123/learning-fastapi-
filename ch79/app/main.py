from fastapi import FastAPI,Request,Form
from contextlib import asynccontextmanager
from app.db.config import create_table,SessionDep
from app.product.model import ProductCreate,ProductOut
from app.product.service import *
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

@asynccontextmanager
async def  lifespan(app:FastAPI):
    create_table()
    yield
app=FastAPI(lifespan=lifespan)
app.mount("/css",StaticFiles(directory="app/static"),name="css")
template=Jinja2Templates(directory="app/templates")
@app.get("/",response_class=HTMLResponse)
async def get_temp(request:Request,session:SessionDep):
    prod= await get_all_product(session)
    return template.TemplateResponse(
    request=request,
    name="template.html",
    context={"products": prod}
)
@app.post("/create",response_class=HTMLResponse)
async def post_temp(request:Request,session:SessionDep,title:str=Form(...),description:str=Form(...)):
    prod= ProductCreate(title=title, description=description)
    await create_product(session,prod)
    return RedirectResponse("/",status_code=302)

# @app.post("/create_product",response_model=ProductOut)
# async def post_product(sess:SessionDep,new_product:ProductCreate):
#     prod= await create_product(sess,new_product)
#     return prod
# @app.get("/get_product",response_model=list[ProductOut])
# async def get_product(sess:SessionDep):
#     prod= await get_all_product(sess)
#     return prod
# @app.get("/get_id_product",response_model=ProductOut)
# async def get_product_by_id(sess:SessionDep,new_id:int):
#     pro= await get_product_id(sess,new_id)
#     return pro
# @app.delete("/delete_product")
# async def delete(sess:SessionDep,new_id:int):
#     prod= await delete_product(sess,new_id)
#     return {}
