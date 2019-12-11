from .first import check_password1
from .second import check_password2

def test_check_password1():
    assert check_password1(111111)
    assert not check_password1(223450)
    assert not check_password1(123789)
    assert check_password1(455667)

def test_check_password2():
    assert not check_password2(111111)
    assert not check_password2(223450)
    assert not check_password2(123789)
    assert check_password2(455667)

    assert check_password2(112233)
    assert not check_password2(123444)
    assert check_password2(111122)
