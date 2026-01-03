#curd opeartion in fastapi

from fastapi import FastAPI
app=FastAPI()
products_db = [
    {"id": 1, "name": "Laptop", "price": 999.99, "description": "High performance", "category": "Electronics"},
    {"id": 2, "name": "Smartphone", "price": 499.99, "description": "Latest model", "category": "Electronics"},
    {"id": 3, "name": "Coffee Maker", "price": 49.99, "category": "Appliances"},
]
#get product
#read all the product
@app.get('/product')
async def gat_all_product():
    return products_db
#read the product by id
@app.get('/product/{id}')
async def get_product_id(id:int):
    for product in products_db:
        if product['id'] == id:
            return product
    return {}
#post the new data
@app.post('/products')
async def created_at(new_product:dict):

    products_db.append(new_product)
    return products_db
#put 
#update data (full)
@app.put('/product/{prodcut_id}')
async def  put(product_id:int,new_product:dict):
    for idx,pro in enumerate(products_db):
        if pro['id']== product_id:
            products_db[idx]=new_product
            return {"status":"new_productupadeted","product_id":product_id,"new_product":pro}
#pacth
#update data (paritally)
@app.patch('/product_id/{prodcut_id}')
async def patch(product_id:int,new_product:dict):
    for pro in products_db:
        if pro["id"]==product_id:
            pro.update(new_product)
            return {"status":"updated","product_id":product_id,"new_product":pro}
#delete 
#remove the data
@app.delete('/product/{prodcut_id}')
async def  delete(product_id:int):
    for idx,pro in enumerate(products_db):
        if pro['id']== product_id:
            products_db.pop(idx)
            return {"status":"delted","product_id":product_id,"new_product":pro}



            


