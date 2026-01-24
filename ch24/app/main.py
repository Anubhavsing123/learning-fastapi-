from fastapi import FastAPI,HTTPException
app=FastAPI()
items={
    "apple":"REd light color",
    "grapes":"green  in color"
}
#httpexception
# @app.get('/{id}')
# async def main(id:str):
#     if id not in items:
#         raise HTTPException(status_code=404,detail="id not found")
#     return items[id]
# #add custom header
@app.get('/{id}')
async def main(id:str):
    if id not in items:
        raise HTTPException(status_code=404,detail="id not found",
                            headers={"x-error-type":"missing item"})
    return items[id]

