from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Integration(_message.Message):
    __slots__ = ("id", "integration_id", "access_token", "name", "active")
    ID_FIELD_NUMBER: _ClassVar[int]
    INTEGRATION_ID_FIELD_NUMBER: _ClassVar[int]
    ACCESS_TOKEN_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACTIVE_FIELD_NUMBER: _ClassVar[int]
    id: str
    integration_id: str
    access_token: str
    name: str
    active: bool
    def __init__(self, id: _Optional[str] = ..., integration_id: _Optional[str] = ..., access_token: _Optional[str] = ..., name: _Optional[str] = ..., active: bool = ...) -> None: ...

class IntegrationsResponse(_message.Message):
    __slots__ = ("integrations",)
    INTEGRATIONS_FIELD_NUMBER: _ClassVar[int]
    integrations: _containers.RepeatedCompositeFieldContainer[Integration]
    def __init__(self, integrations: _Optional[_Iterable[_Union[Integration, _Mapping]]] = ...) -> None: ...

class IntegrationResponse(_message.Message):
    __slots__ = ("github", "benchling")
    GITHUB_FIELD_NUMBER: _ClassVar[int]
    BENCHLING_FIELD_NUMBER: _ClassVar[int]
    github: GithubIntegration
    benchling: BenchlingIntegration
    def __init__(self, github: _Optional[_Union[GithubIntegration, _Mapping]] = ..., benchling: _Optional[_Union[BenchlingIntegration, _Mapping]] = ...) -> None: ...

class PostIntegrationRequest(_message.Message):
    __slots__ = ("github", "benchling")
    GITHUB_FIELD_NUMBER: _ClassVar[int]
    BENCHLING_FIELD_NUMBER: _ClassVar[int]
    github: PostGithubIntegration
    benchling: PostBenchlingIntegration
    def __init__(self, github: _Optional[_Union[PostGithubIntegration, _Mapping]] = ..., benchling: _Optional[_Union[PostBenchlingIntegration, _Mapping]] = ...) -> None: ...

class PostGithubIntegration(_message.Message):
    __slots__ = ("name", "repo", "token")
    NAME_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    TOKEN_FIELD_NUMBER: _ClassVar[int]
    name: str
    repo: str
    token: str
    def __init__(self, name: _Optional[str] = ..., repo: _Optional[str] = ..., token: _Optional[str] = ...) -> None: ...

class GithubIntegration(_message.Message):
    __slots__ = ("id", "name", "repo")
    ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    REPO_FIELD_NUMBER: _ClassVar[int]
    id: str
    name: str
    repo: str
    def __init__(self, id: _Optional[str] = ..., name: _Optional[str] = ..., repo: _Optional[str] = ...) -> None: ...

class GithubIntegrationsResponse(_message.Message):
    __slots__ = ("repos",)
    REPOS_FIELD_NUMBER: _ClassVar[int]
    repos: _containers.RepeatedCompositeFieldContainer[GithubIntegration]
    def __init__(self, repos: _Optional[_Iterable[_Union[GithubIntegration, _Mapping]]] = ...) -> None: ...

class PostBenchlingIntegration(_message.Message):
    __slots__ = ("benchling_tenant_id",)
    BENCHLING_TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    benchling_tenant_id: str
    def __init__(self, benchling_tenant_id: _Optional[str] = ...) -> None: ...

class BenchlingIntegration(_message.Message):
    __slots__ = ("id", "benchling_tenant_id", "benchling_url", "created_at")
    ID_FIELD_NUMBER: _ClassVar[int]
    BENCHLING_TENANT_ID_FIELD_NUMBER: _ClassVar[int]
    BENCHLING_URL_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    id: str
    benchling_tenant_id: str
    benchling_url: str
    created_at: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., benchling_tenant_id: _Optional[str] = ..., benchling_url: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class IntegrationUpdateRequest(_message.Message):
    __slots__ = ("add_benchling_schema",)
    ADD_BENCHLING_SCHEMA_FIELD_NUMBER: _ClassVar[int]
    add_benchling_schema: BenchlingSchema
    def __init__(self, add_benchling_schema: _Optional[_Union[BenchlingSchema, _Mapping]] = ...) -> None: ...

class BenchlingSchema(_message.Message):
    __slots__ = ("schema_type", "schema_id", "created_at", "last_synced", "data_type_unique_id", "name")
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        INVALID: _ClassVar[BenchlingSchema.Type]
        ENTITY: _ClassVar[BenchlingSchema.Type]
        ENTRY: _ClassVar[BenchlingSchema.Type]
    INVALID: BenchlingSchema.Type
    ENTITY: BenchlingSchema.Type
    ENTRY: BenchlingSchema.Type
    SCHEMA_TYPE_FIELD_NUMBER: _ClassVar[int]
    SCHEMA_ID_FIELD_NUMBER: _ClassVar[int]
    CREATED_AT_FIELD_NUMBER: _ClassVar[int]
    LAST_SYNCED_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPE_UNIQUE_ID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    schema_type: BenchlingSchema.Type
    schema_id: str
    created_at: _timestamp_pb2.Timestamp
    last_synced: _timestamp_pb2.Timestamp
    data_type_unique_id: str
    name: str
    def __init__(self, schema_type: _Optional[_Union[BenchlingSchema.Type, str]] = ..., schema_id: _Optional[str] = ..., created_at: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., last_synced: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ..., data_type_unique_id: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class BenchlingSchemaResponse(_message.Message):
    __slots__ = ("schemas",)
    SCHEMAS_FIELD_NUMBER: _ClassVar[int]
    schemas: _containers.RepeatedCompositeFieldContainer[BenchlingSchema]
    def __init__(self, schemas: _Optional[_Iterable[_Union[BenchlingSchema, _Mapping]]] = ...) -> None: ...
