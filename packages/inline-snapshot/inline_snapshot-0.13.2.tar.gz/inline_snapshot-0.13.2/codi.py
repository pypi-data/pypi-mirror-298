from dirty_equals import DirtyEquals
from inline_snapshot import snapshot


def test_time_like_ditry_equal():

    assert [5] == snapshot([*[5]])

