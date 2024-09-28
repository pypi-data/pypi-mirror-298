from proto import entity_pb2 as _entity_pb2
from proto import data_type_pb2 as _data_type_pb2
from proto import analysis_pb2 as _analysis_pb2
from proto import pipeline_pb2 as _pipeline_pb2
from proto import pipeline_run_pb2 as _pipeline_run_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Template(_message.Message):
    __slots__ = ("name", "entities", "data_types", "analyses", "notebook_environments", "pipelines", "pipeline_runs", "description", "id")
    NAME_FIELD_NUMBER: _ClassVar[int]
    ENTITIES_FIELD_NUMBER: _ClassVar[int]
    DATA_TYPES_FIELD_NUMBER: _ClassVar[int]
    ANALYSES_FIELD_NUMBER: _ClassVar[int]
    NOTEBOOK_ENVIRONMENTS_FIELD_NUMBER: _ClassVar[int]
    PIPELINES_FIELD_NUMBER: _ClassVar[int]
    PIPELINE_RUNS_FIELD_NUMBER: _ClassVar[int]
    DESCRIPTION_FIELD_NUMBER: _ClassVar[int]
    ID_FIELD_NUMBER: _ClassVar[int]
    name: str
    entities: _containers.RepeatedCompositeFieldContainer[_entity_pb2.Entity]
    data_types: _containers.RepeatedCompositeFieldContainer[_data_type_pb2.DataType]
    analyses: _containers.RepeatedCompositeFieldContainer[_analysis_pb2.Analysis]
    notebook_environments: _containers.RepeatedCompositeFieldContainer[_analysis_pb2.NotebookEnvironment]
    pipelines: _containers.RepeatedCompositeFieldContainer[_pipeline_pb2.Pipeline]
    pipeline_runs: _containers.RepeatedCompositeFieldContainer[_pipeline_run_pb2.PipelineRun]
    description: str
    id: str
    def __init__(self, name: _Optional[str] = ..., entities: _Optional[_Iterable[_Union[_entity_pb2.Entity, _Mapping]]] = ..., data_types: _Optional[_Iterable[_Union[_data_type_pb2.DataType, _Mapping]]] = ..., analyses: _Optional[_Iterable[_Union[_analysis_pb2.Analysis, _Mapping]]] = ..., notebook_environments: _Optional[_Iterable[_Union[_analysis_pb2.NotebookEnvironment, _Mapping]]] = ..., pipelines: _Optional[_Iterable[_Union[_pipeline_pb2.Pipeline, _Mapping]]] = ..., pipeline_runs: _Optional[_Iterable[_Union[_pipeline_run_pb2.PipelineRun, _Mapping]]] = ..., description: _Optional[str] = ..., id: _Optional[str] = ...) -> None: ...

class ImportTemplateRequest(_message.Message):
    __slots__ = ("id",)
    ID_FIELD_NUMBER: _ClassVar[int]
    id: str
    def __init__(self, id: _Optional[str] = ...) -> None: ...

class TemplateListResponse(_message.Message):
    __slots__ = ("templates",)
    TEMPLATES_FIELD_NUMBER: _ClassVar[int]
    templates: _containers.RepeatedCompositeFieldContainer[Template]
    def __init__(self, templates: _Optional[_Iterable[_Union[Template, _Mapping]]] = ...) -> None: ...
