from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Error(_message.Message):
    __slots__ = ("error",)
    ERROR_FIELD_NUMBER: _ClassVar[int]
    error: str
    def __init__(self, error: _Optional[str] = ...) -> None: ...

class InviteUser(_message.Message):
    __slots__ = ("email", "name")
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    email: str
    name: str
    def __init__(self, email: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class User(_message.Message):
    __slots__ = ("id", "email", "name", "access_token", "tenants", "state")
    ID_FIELD_NUMBER: _ClassVar[int]
    EMAIL_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    TENANTS_FIELD_NUMBER: _ClassVar[int]
    STATE_FIELD_NUMBER: _ClassVar[int]
    id: str
    email: str
    name: str
    access_token: str
    tenants: _containers.RepeatedScalarFieldContainer[str]
    state: UserState
    def __init__(self, id: _Optional[str] = ..., email: _Optional[str] = ..., name: _Optional[str] = ..., access_token: _Optional[str] = ..., tenants: _Optional[_Iterable[str]] = ..., state: _Optional[_Union[UserState, _Mapping]] = ...) -> None: ...

class UserState(_message.Message):
    __slots__ = ("tour_completed",)
    TOUR_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    tour_completed: bool
    def __init__(self, tour_completed: bool = ...) -> None: ...

class UpdateuserStateRequest(_message.Message):
    __slots__ = ("tour_completed",)
    TOUR_COMPLETED_FIELD_NUMBER: _ClassVar[int]
    tour_completed: bool
    def __init__(self, tour_completed: bool = ...) -> None: ...

class Message(_message.Message):
    __slots__ = ("message",)
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    message: str
    def __init__(self, message: _Optional[str] = ...) -> None: ...
