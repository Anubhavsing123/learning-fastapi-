from app.main import add,divide
import pytest
# @pytest.fixture
# def data():
#     return {"a":10,"b":0}
# def test_add_fix(data):
#     assert add(data["a"],data["b"])==5
#     assert add(data["a"],data["b"])==15
@pytest.mark.parametrize('a,b,expected',[
        (2, 3, 5),
        (1, -1, 0),
        (0, 0, 0),
    ])
def test_add_mark(a,b,expected):
    assert add(a,b)==expected

@pytest.mark.skip(reason="Not implemented yet")
def test_future_value():
    pass

