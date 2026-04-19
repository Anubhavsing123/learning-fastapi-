from app.main import add,divide
import pytest
def test_add():
    assert add(2,3)==5
    assert add(-1,1)==0
    assert add(0,0)==0
def test_divide():
    assert divide(6,3)==2
    assert divide(5,2)==2.5
    #m-1 one better way
# def test_divide_by_zero():
#     try:
#         divide(10,0)
#         assert False,"Expeceted ValueError"
#     except ValueError:
#         assert True
#m2
def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10,0)

