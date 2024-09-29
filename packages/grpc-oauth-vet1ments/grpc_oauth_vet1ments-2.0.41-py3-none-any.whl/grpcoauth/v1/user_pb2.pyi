from buf.validate import validate_pb2 as _validate_pb2
from google.api import annotations_pb2 as _annotations_pb2
from google.protobuf import empty_pb2 as _empty_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class User(_message.Message):
    __slots__ = ("id", "name", "phone_number", "nickname", "thumbnail")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    THUMBNAIL_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    phone_number: str
    nickname: str
    thumbnail: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., phone_number: _Optional[str] = ..., nickname: _Optional[str] = ..., thumbnail: _Optional[str] = ...) -> None: ...

class test(_message.Message):
    __slots__ = ("test",)
    TEST_FIELD_NUMBER: _ClassVar[int]
    test: str
    def __init__(self, test: _Optional[str] = ...) -> None: ...

class GetAccessTokenInfoResponse(_message.Message):
    __slots__ = ("id", "expires_in", "app_id")
    ID_FIELD_NUMBER: _ClassVar[int]
    EXPIRES_IN_FIELD_NUMBER: _ClassVar[int]
    APP_ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    expires_in: int
    app_id: str
    def __init__(self, id: _Optional[str] = ..., expires_in: _Optional[int] = ..., app_id: _Optional[str] = ...) -> None: ...

class GetUserMeResponse(_message.Message):
    __slots__ = ("id", "name", "phone_number", "nickname")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PHONE_NUMBER_FIELD_NUMBER: _ClassVar[int]
    NICKNAME_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    phone_number: str
    nickname: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., phone_number: _Optional[str] = ..., nickname: _Optional[str] = ...) -> None: ...

class UserLogoutResponse(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...
