from collections import namedtuple
from typing import Type as T
from google.protobuf import descriptor
from google.protobuf import reflection
from google.protobuf import message
from enum import Enum

## Annotations
Field = namedtuple('Field', ['number', 'type', 'repeated', 'union'])


def field(tag, t, repeated=False, union=None):
    return Field(tag, t, repeated, union)


class Type(Enum):
    int32 = 1


class Message(object):
    def __repr__(self):
        name = self.__class__.__name__
        attrs = ["{}={}".format(k, repr(getattr(self, k))) for k in self.__annotations__.keys()]
        return "{}({})".format(name, ", ".join(attrs))


# Encode / Decode
def _pbmessage(msgcls: T[Message]) -> message.Message:
    full_name = '{}.{}'.format(msgcls.__module__, msgcls.__name__)
    fields = []

    for i, (k, field) in enumerate(msgcls.__annotations__.items()):
        fields.append(descriptor.FieldDescriptor(
            name=k, full_name='{}.{}'.format(full_name, k), index=i,
            number=field.number, type=9, cpp_type=9, label=field.number,
            has_default_value=False, default_value='',
            message_type=None, enum_type=None, containing_type=None,
            is_extension=False, extension_scope=None,
            options=None))

    hr = descriptor.Descriptor(
        name=msgcls.__name__,
        full_name=full_name,
        filename=None,
        containing_type=None,
        fields=fields,
        extensions=[
        ],
        nested_types=[],
        enum_types=[
        ],
        options=None,
        is_extendable=False,
        syntax='proto3',
        extension_ranges=[],
    )
    
    return reflection.GeneratedProtocolMessageType('pb{}'.format(msgcls.__name__), (message.Message,), dict(
      DESCRIPTOR = hr,
      __module__ = msgcls.__module__
    ))()


def decode(msg: bytes, t: T[Message]) -> Message:
    m = _pbmessage(t)
    m.ParseFromString(msg)
    params = {}
    for k, field in t.__annotations__.items():
        params[k] = getattr(m, k)
    return t(**params)


def encode(msg: Message) -> bytes:
    m = _pbmessage(msg.__class__)
    for k, field in msg.__annotations__.items():
        setattr(m, k, getattr(msg, k))
    return m.SerializeToString()



