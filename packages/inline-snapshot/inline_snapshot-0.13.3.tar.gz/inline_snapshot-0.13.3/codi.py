from dirty_equals import DirtyEquals
from inline_snapshot import snapshot,Is





def get_data(i):
     return {"num": i, "data": "some data", "with_i": f"some data with {i}" }

def test_is():
    for i in range(5):
        assert get_data(i) == snapshot({"num": Is(i), "data": "some data", "with_i": Is(f"some data with {i}")})



def foo(version,list):
    assert list == snapshot([1, snapshot(5) if version == 1 else snapshot(), 8])

def test_snapshot():

    foo(1,[1,5,8])
    foo(2,[1,7,8])

