from collections import namedtuple
from dataclasses import dataclass
import typing
import sys


def attributes_in_class():
    class Pet:
        legs: int
        noise: str

        def __init__(self, legs, noise) -> None:
            self.legs = legs
            self.noise = noise

        def __repr__(self):
            return f"<Pet legs={self.legs} noise='{self.noise}'>"

    for _ in range(100000):
        dog = Pet(4, "woof")
        str(dog)


def attributes_in_class_with_slots():
    class Pet:
        legs: int
        noise: str
        __slots__ = "legs", "noise"

        def __init__(self, legs, noise) -> None:
            self.legs = legs
            self.noise = noise

        def __repr__(self):
            return f"<Pet legs={self.legs} noise='{self.noise}'>"

    for _ in range(100000):
        dog = Pet(4, "woof")
        str(dog)


def attributes_in_class_with_slots_factory():
    lb = "\n        "

    def class_factory(*attrs):
        class_string = f"""
global Klass
class Klass:
    __slots__ = {attrs}

    def __init__(self, {', '.join(attrs)}):
        {lb.join(f'self.{attr}={attr}' for attr in attrs)}

    def __repr__(self):
        return (
            f'<{{self.__class__.__name__}}' 
            + "{' '.join(f'{attr}={{getattr(self, {attr})}}' for attr in attrs)}"
        )
"""
        exec(class_string)
        return Klass

    Pet = class_factory("legs", "noise")

    for _ in range(100000):
        dog = Pet(4, "woof")
        str(dog)


def attributes_in_dataclass():
    @dataclass
    class Pet:
        legs: int
        noise: str

    for _ in range(100000):
        dog = Pet(4, "woof")
        str(dog)


attributes_in_dataclass_with_slots = None
if sys.version_info.minor >= 10:

    def attributes_in_dataclass_with_slots():
        @dataclass(slots=True)
        class Pet:
            legs: int
            noise: str

        for _ in range(100000):
            dog = Pet(4, "woof")
            str(dog)


def attributes_in_namedtuple():
    Pet = namedtuple("Pet", "legs noise")
    for _ in range(100000):
        dog = Pet(4, "woof")
        str(dog)


def attributes_in_namedtuple_type():
    class Pet(typing.NamedTuple):
        legs: int
        noise: str

    for _ in range(100000):
        dog = Pet(4, "woof")
        str(dog)


def attributes_in_dict():
    for _ in range(100000):
        dog = {"legs": 4, "noise": "woof"}
        str(dog)


__benchmarks__ = [
    (attributes_in_dataclass, attributes_in_class, "Class instead of dataclass"),
    (
        attributes_in_dataclass,
        attributes_in_namedtuple,
        "Namedtuple instead of dataclass",
    ),
    (attributes_in_namedtuple, attributes_in_class, "class instead of namedtuple"),
    (
        attributes_in_namedtuple,
        attributes_in_namedtuple_type,
        "namedtuple class instead of namedtuple",
    ),
    (attributes_in_class, attributes_in_dict, "dict instead of class"),
    (
        attributes_in_class,
        attributes_in_class_with_slots,
        "class with slots instead of class",
    ),
    (
        attributes_in_class_with_slots,
        attributes_in_class_with_slots_factory,
        "class with slots factory instead of class with slots",
    ),
    (
        attributes_in_dict,
        attributes_in_class_with_slots_factory,
        "class with slots factory instead of dict",
    ),
]
if attributes_in_dataclass_with_slots:
    __benchmarks__.append(
        (
            attributes_in_dataclass,
            attributes_in_dataclass_with_slots,
            "dataclass with slots instead of dataclass",
        )
    )
