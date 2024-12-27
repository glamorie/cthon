import ctypes

type Fields = list[tuple[str, type]]


def from_namespace(namespace: dict[str, object]):
    for key, value in namespace.items():
        if isinstance(value, type):
            yield key, value


class StructType(type(ctypes.Structure)):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, object]):
        annotations = cls.__annotations__
        if annotations:
            fields: Fields = [] * len(annotations)
            fields.extend(annotations.items())
        else:
            fields = list(from_namespace(namespace))
        namespace["_fields_"] = fields
        return super().__new__(cls, name, bases, namespace)


class UnionType(type(ctypes.Union)):
    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, object]):
        annotations = cls.__annotations__
        if annotations:
            fields: Fields = [] * len(annotations)
            fields.extend(annotations.items())
        else:
            fields = list(from_namespace(namespace))
        namespace["_fields_"] = fields
        return super().__new__(cls, name, bases, namespace)


class Struct(ctypes.Structure, metaclass=StructType):
    pass


class Union(ctypes.Union, metaclass=UnionType):
    pass
