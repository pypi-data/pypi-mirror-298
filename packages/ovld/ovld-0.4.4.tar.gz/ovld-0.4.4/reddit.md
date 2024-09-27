## What My Project Does

[ovld](https://github.com/breuleux/ovld) implements multiple dispatch in Python. This lets you define multiple versions of the same function with different type signatures.

For example:

```python
import math
from typing import Literal
from ovld import ovld

@ovld
def div(x: int, y: int):
    return x / y

@ovld
def div(x: str, y: str):
    return f"{x}/{y}"

@ovld
def div(x: int, y: Literal[0]):
    return math.inf

assert div(8, 2) == 4
assert div("/home", "user") == "/home/user"
assert div(10, 0) == math.inf
```


## Target Audience

Ovld is pretty generally applicable: multiple dispatch is a central feature of several programming languages, e.g. Julia. I find it particularly useful when doing work on complex heterogeneous data structures, for instance walking an AST, serializing/deserializing data, generating HTML representations of data, etc.


## Features

* Wide range of supported annotations: normal types, protocols, Union, Literal, [custom types](https://ovld.readthedocs.io/en/latest/types/#defining-new-types) such as HasMethod, Intersection and arbitrary user-defined types.
* Intersection type, so you can write types like `Shape[Any, 3] & Int8 & OnGPU`
* Support for [dependent types](https://ovld.readthedocs.io/en/latest/dependent/), by which I mean "types" that depend on the values of the arguments. For example you can easily implement a `Regexp[regex]` type that matches string arguments based on regular expressions, or a type that only matches 2x2 torch.Tensor with int8 dtype.
* Dispatch on keyword arguments (with a few limitations).
* Define numeric priority levels for disambiguation.
* Define [variants](https://ovld.readthedocs.io/en/latest/usage/#variants) of existing functions (copies of existing overloads with additional functionality)
* Special `recurse()` function for recursive calls that also work with variants.
* Special `call_next()` function to call the next dispatch.


## Comparison

There already exist a few multiple dispatch libraries: plum, multimethod, multipledispatch, runtype, fastcore, and the builtin functools.singledispatch (single argument).

Ovld is faster than all of them. From 1.5x to 100x faster depending on use case, and in the ballpark of isinstance/match. It is also generally more featureful: no other library supports dispatch on keyword arguments, and only a few support `Literal` annotations, but with massive performance penalties.

You can also do many things ovld does with the `match` statement, except you cannot extend existing `match` statements with more signatures.

[Whole comparison section, with benchmarks, can be found here.](https://ovld.readthedocs.io/en/latest/compare/)
