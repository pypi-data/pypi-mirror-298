import timeit
from typing import Literal
from beartype import BeartypeConf                              # <-- this isn't your fault
from beartype.claw import beartype_all, beartype_this_package  # <-- you didn't sign up for this
from beartype import beartype
from ovld import ovld
from strongtyping.strong_typing import match_typing

beartype_all(conf=BeartypeConf())
# beartype_this_package()                                        # <-- raise exceptions in your code
# beartype_all(conf=BeartypeConf(violation_type=UserWarning))

@match_typing
def f1(x: int, y: int):
    return x + y


@ovld
def f2(x: int, y: int):
    return x + y


def f3(x: int, y: int):
    assert isinstance(x, int) and isinstance(y, int)
    return x + y


print(timeit.timeit(stmt=lambda: f1(3, 4), number=100000))
print(timeit.timeit(stmt=lambda: f2(3, 4), number=100000))
print(timeit.timeit(stmt=lambda: f3(3, 4), number=100000))
