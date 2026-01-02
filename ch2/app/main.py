#predfine value in fatspai done by using enum
from fastapi import FastAPI
from enum import Enum
app=FastAPI()
##predfined values using enum
class ProductCategory(str,Enum):
    book="book"
    clothing="clothing"




@app.get('/{caterogy}')
async def main(caterogy:ProductCategory):
    return {"respone":"hello","caterogy":caterogy}
@app.get("/producut/{category}")
async def main2(category:ProductCategory):
    if category== ProductCategory.book:
        return {"category":category,"msg":"Books are aswome!"}
    elif category==ProductCategory.clothing.value:
        return {"category":category,"msg":"caterogy  are aswome!"}
    else:
        return {"category":category,"msg":"Unknow category!"}
