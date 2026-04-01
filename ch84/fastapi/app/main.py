from fastapi import FastAPI,Request,Form
from contextlib import asynccontextmanager
from app.db.config import create_table,SessionDep
from app.product.model import ProductCreate,ProductOut
from app.product.service import *
from fastapi.responses import HTMLResponse,RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def  lifespan(app:FastAPI):
    create_table()
    yield
app=FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
        "http://localhost:5173",],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]

)
app.mount("/css",StaticFiles(directory="app/static"),name="css")
template=Jinja2Templates(directory="app/templates")
@app.get("/",response_class=HTMLResponse)
async def home(request:Request):
    return template.TemplateResponse(request,"index.html")
@app.get("/form",response_class=HTMLResponse)
async def load_form(request:Request):
    return template.TemplateResponse(request,"product_form.html")
@app.get("/product", response_class=HTMLResponse)
async def product_list(request: Request, session: SessionDep):
    products = await get_all_product(session)
    
    # Corrected TemplateResponse signature
    return template.TemplateResponse(
        request=request, 
        name="product_list.html", 
        context={"products": products}
    )
@app.post("/create", response_class=HTMLResponse)
async def product_create(request: Request, session: SessionDep,title:str=Form(...),description:str=Form(...)):
    product_data=ProductCreate(title=title,description=description)
    await create_product(session,product_data)
    products = await get_all_product(session)
    
    # Corrected TemplateResponse signature
    return template.TemplateResponse(
        request=request, 
        name="product_list.html", 
        context={"products": products}
    )
@app.get("/products", response_model=list[ProductOut])
async def get_products(session: SessionDep):
    return await get_all_product(session)
@app.post("/products", response_model=ProductOut)
async def add_product(
    product: ProductCreate,
    session: SessionDep
):
    return await create_product(session, product)