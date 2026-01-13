from fastapi import FastAPI, Cookie, Body
from typing import Annotated
from pydantic import BaseModel, Field

app = FastAPI()
# cookie with pydantic model

# class ProductCookie(BaseModel):
#     session_id: str
#     pref_cat: str | None = None
#     tracking_id: str | None = None

# @app.get("/product")
# async def get_item(cookie: Annotated[ProductCookie, Cookie()]):

#     response = {
#         "session_id": cookie.session_id
#     }

#     if cookie.pref_cat:
#         response["pref_cat_msg"] = f"Recommended for {cookie.pref_cat} products"
#     else:
#         response["default_msg"] = f"Default id {cookie.session_id}"

#     if cookie.tracking_id:
#         response["tracking_msg"] = cookie.tracking_id


#     return response
"""C:\>curl -H "Cookie:session_id=abc123; extra_data=mydata;pref_cat=Electronic ; tracking_id=xyz124" http://127.0.0.1:8000/product
{"session_id":"abc123","pref_cat_msg":"Recommended for Electronic products","tracking_msg":"xyz124"}"""
# forrbidden extra cookie
# class ProductCookie(BaseModel):
#     model_config={"extra":"forbid"}
#     session_id: str
#     pref_cat: str | None = None
#     tracking_id: str | None = None

# @app.get("/product")
# async def get_item(cookie: Annotated[ProductCookie, Cookie()]):

#     response = {
#         "session_id": cookie.session_id
#     }

#     if cookie.pref_cat:
#         response["pref_cat_msg"] = f"Recommended for {cookie.pref_cat} products"
#     else:
#         response["default_msg"] = f"Default id {cookie.session_id}"

#     if cookie.tracking_id:
#         response["tracking_msg"] = cookie.tracking_id


#     return response
# combine with body parameter
class ProductCookie(BaseModel):
    model_config = {"extra": "forbid"}
    session_id: str = Field(title="SESSION_ID", description="User session identifier")
    pref_cat: str | None = Field(
        default=None, title="perfed catgory ", description="user's preferd catgeory"
    )


class PriceFilterBody(BaseModel):
    min_price: float = Field(
        ge=0, title="Mininum price", description="Minimum price of the catergory"
    )
    max_price: float | None = Field(
        default=None, title="Maxmimu price ", description="Describe the maximum price"
    )


@app.post("/product")
async def get_item(
    cookie: Annotated[ProductCookie, Cookie()],
    price_filter: Annotated[PriceFilterBody, Body(embed=True)],
):

    response = {"session_id": cookie.session_id}

    if cookie.pref_cat:
        response["pref_cat_msg"] = cookie.pref_cat
        response["price_range"] = {
            "min": price_filter.min_price,
            "max": price_filter.max_price,
        }
        response["msg"] = (
            f"recdom . sesion id {cookie.session_id} price rage from {price_filter.min_price}to {price_filter.max_price}"
        )

    return response
