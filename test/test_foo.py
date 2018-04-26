from main import get_kj


def test_get_kj():
    result = get_kj(1, True)

    assert result == 1
