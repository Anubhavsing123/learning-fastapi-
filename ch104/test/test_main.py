from app.main import add,divide
import pytest
@pytest.mark.asyncio
async def test_add():
    assert await add(2,3)==5
    assert await add(1,-1)==0
@pytest.mark.asyncio
async def test_divide():
    assert await divide(6,3)==2
    assert await divide (8,4)==2
@pytest.mark.asyncio
async def test_divde_by_zero():
    with pytest.raises(ValueError):
        await divide(10,0)
    