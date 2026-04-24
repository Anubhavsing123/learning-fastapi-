import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.product.service import *
from app.product.schema import ProductBase,ProductUpdate
from app.product.model import Product
from fastapi import HTTPException
# Service tests (Hybrid unit/Integration Test)
# these tests indiviual  service function from app/product/service.py
# they are unit  tests in that they foucs on specifics funtions,
#but  integrations test
#because  they use a real sqlite database via AsyncSession

@pytest.mark.asyncio
async def test_create_product(setup_data,test_session:AsyncSession):
    """
    Hybrid unit/Integration test for the create_service function.
        - create a product with title"Test Product" using  the test
        session.
        - verifies the product is created with correct title and a non null id.
        -use real database ,testing function logic and database interaction.

      """
    product_data = ProductBase(
    title="Test Product",
    price=100.0,
    stock=10
   )
    product=await create_product(test_session,product_data)
    assert product.title=="Test Product"
    assert product.id is not None
@pytest.mark.asyncio
async def test_get_all_product(setup_data,test_session:AsyncSession):
     product_data = ProductBase(
        title="Test Product",
        price=100.0,
        stock=10
       )
     await create_product(test_session,product_data)
     product= await get_all_products(test_session)
     assert len(product)==1
     assert product[0].title=="Test Product"
@pytest.mark.asyncio
async def test_get_product(setup_data,test_session:AsyncSession):
      product_data = ProductBase(
             title="Test Product",
             price=100.0,
             stock=10
            )
      product=await create_product(test_session,product_data)
      fetch_product=await get_product(product.id,test_session)
      assert fetch_product.title=="Test Product"
      assert fetch_product.id==product.id
@pytest.mark.asyncio
async def test_get_product_found_or_not(setup_data,test_session):
      with pytest.raises(HTTPException) as exc:
           await get_product(999,test_session)
      assert exc.value.status_code==404
      assert exc.value.detail=="Product not found"


@pytest.mark.asyncio
async def test_update_product(setup_data,test_session:AsyncSession):
      product_data = ProductUpdate(
             title="Update Product",
             price=300.0,
             stock=10
            )
      product= await create_product(test_session,product_data)
      fetch_product= await update_product(product.id,product_data,test_session)
      assert fetch_product.title=="Update Product"
      assert fetch_product.id==product.id
@pytest.mark.asyncio
async def test_update_product_not_found(setup_data,test_session:AsyncSession):
     update_product=ProductUpdate(title="Update Product",
                  price=100.0,
                  stock=10)
     with pytest.raises(HTTPException) as exc:
          await get_product(999,test_session)
     assert exc.value.status_code==404
     assert exc.value.detail=="Product not found"
@pytest.mark.asyncio
async def test_delete_product(setup_data,test_session:AsyncSession):
     product_data = ProductBase(
                  title="Test Product",
                  price=100.0,
                  stock=10
                 )
     product= await create_product(test_session,product_data)
     result=await delete_product(product.id,test_session)
     assert result== {"detail": "Product deleted successfully"}
     with pytest.raises(HTTPException) as exc:
          await get_product(product.id,test_session)
     assert exc.value.status_code==404
#API endpoints testing(Integaration testing)
# These verfiy integartion  between rounting, services, and database
#These test the full request request-response cycle of Fastapi endpoints in app/product/routers.py

@pytest.mark.asyncio
async def test_create_product_endpoints(setup_data,test_client):
     """
     Integaration test  for the Post /product/create_product API endpoint.
     -Send a Post request create Poduct with "title":"Test Product","price":10,"stock":12
     -verifies the response status is 201 and return data is matched input.
     -Testing,Routing,service layer and data interagation


     """
     response=test_client.post("/product/create_product",json={"title":"Test Product","price":10,"stock":12})
     assert response.status_code==201
     data=response.json()
     assert data["title"]=="Test Product"
     assert "id" in data
@pytest.mark.asyncio
async def test_get_all_product_endpoint(setup_data,test_client):
     """
     Integaration test  for the get /product/get_all_the_product API endpoint.
     -Create the product via post ,then retrives all products via get
     -Verifie the response status is 201 
     """
     response=test_client.post("/product/create_product",json={"title":"Test Product","price":10,"stock":12})
     assert response.status_code==201
     response=test_client.get("/product/")
     assert response.status_code==200
     data=response.json()
     assert len(data)==1
     assert data[0]["title"]=="Test Product"
@pytest.mark.asyncio
async def test_get_product_endpoint(setup_data,test_client):
     response=test_client.post("/product/create_product",json={"title":"Test Product","price":10,"stock":12})
     assert response.status_code==201
     product_id=response.json()['id']
     response= test_client.get(f"/product/{product_id}")
     assert response.status_code==200
     data=response.json()
     assert data["title"]=="Test Product"
     assert data["id"]==product_id
@pytest.mark.asyncio
async def test_update_endpoint(setup_data,test_client):
     response=test_client.post("/product/create_product",json={"title":"Updated Product","price":10,"stock":12})
     assert response.status_code==201
     product_id=response.json()["id"]
     response=test_client.put(f"/product/{product_id}",json={"title":"Updated Product","price":10,"stock":13})
     assert response.status_code==201


     data=response.json()
     assert data["title"]=="Updated Product"
     assert data["id"]==product_id
@pytest.mark.asyncio
async def test_update_not_found_endpoint(setup_data,test_client):
     response=test_client.put("/product/999",json={"title":"Updated Product","price":20,"stock":30})
     assert response.status_code==404
     assert response.json()=={
          "detail":"Product not found"
     }
@pytest.mark.asyncio
async def test_delete_endpoint(setup_data,test_client):
     response=test_client.post("/product/create_product",json={"title":"Updated Product","price":10,"stock":12})
     assert response.status_code==201
     product_id=response.json()["id"]
     response=test_client.delete(f"/product/delete/{product_id}")
     assert response.status_code==200
     assert response.json()=={
               "detail":"Product deleted successfully"
          }
