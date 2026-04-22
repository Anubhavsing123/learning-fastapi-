from app.main import add,divide
import pytest,asyncio
@pytest.fixture

async def data():
    await asyncio.sleep(1)
    return {"a":3,"b":5}
@pytest.mark.asyncio
async def test_add(data):
    assert await add(data["a"],data["b"])==8
@pytest.mark.parametrize('a,b,excepted',[(2,3,5),(-1,1,0),(0,0,0)])
@pytest.mark.asyncio
async def test_add(a,b,excepted):
    assert await add(a,b)==excepted

