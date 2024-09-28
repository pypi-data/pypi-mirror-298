class Class:
    def m(self, x: int) -> str:
        return str(x)

    @staticmethod
    def s(x: int) -> str:
        return str(x)

    @classmethod
    def c_int(cls, x: int) -> int:
        return x

    @classmethod
    def c_str(cls, x: int) -> str:
        return str(x)

    @classmethod
    def c_none(cls, x: int) -> None:
        return

    @classmethod
    def c_noann(cls, x: int):
        return

    @classmethod
    def c_two(cls, x: int, y: int) -> int:
        return x + y


def test_is_template_method_normal():
    from jinjaconf.config import is_template_method

    assert not is_template_method(Class.m)


def test_is_template_method_static():
    from jinjaconf.config import is_template_method

    assert not is_template_method(Class.s)


def test_is_template_method_int():
    from jinjaconf.config import is_template_method

    assert is_template_method(Class.c_int)


def test_is_template_method_str():
    from jinjaconf.config import is_template_method

    assert is_template_method(Class.c_str)


def test_is_template_method_none():
    from jinjaconf.config import is_template_method

    assert not is_template_method(Class.c_none)


def test_is_template_method_noann():
    from jinjaconf.config import is_template_method

    assert not is_template_method(Class.c_noann)


def test_is_template_method_two():
    from jinjaconf.config import is_template_method

    assert not is_template_method(Class.c_two)


def test_iter_template_methods():
    from jinjaconf.config import iter_template_methods

    it = iter_template_methods(Class)
    assert next(it) == ("c_int", Class.c_int)
    assert next(it) == ("c_str", Class.c_str)
    assert len(list(iter_template_methods(Class))) == 2
