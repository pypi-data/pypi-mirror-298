from google.protobuf import timestamp_pb2 as _timestamp_pb2
from zepben.protobuf.ns.data import change_events_pb2 as _change_events_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class SetCurrentStatesRequest(_message.Message):
    __slots__ = ["messageId", "event"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    EVENT_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    event: _containers.RepeatedCompositeFieldContainer[_change_events_pb2.CurrentStateEvent]
    def __init__(self, messageId: _Optional[int] = ..., event: _Optional[_Iterable[_Union[_change_events_pb2.CurrentStateEvent, _Mapping]]] = ...) -> None: ...

class GetCurrentStatesRequest(_message.Message):
    __slots__ = ["messageId", "to"]
    MESSAGEID_FIELD_NUMBER: _ClassVar[int]
    FROM_FIELD_NUMBER: _ClassVar[int]
    TO_FIELD_NUMBER: _ClassVar[int]
    messageId: int
    to: _timestamp_pb2.Timestamp
    def __init__(self, messageId: _Optional[int] = ..., to: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., **kwargs) -> None: ...
