from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClassEnum(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
    LIVEL_KNOT: _ClassVar[ClassEnum]
    DEATH_KNOT: _ClassVar[ClassEnum]
    KNOT_MISSING: _ClassVar[ClassEnum]
    KNOT_WITH_CRACK: _ClassVar[ClassEnum]
    CRACK: _ClassVar[ClassEnum]
    QUARTZITY: _ClassVar[ClassEnum]
    RESIN: _ClassVar[ClassEnum]
    MARROW: _ClassVar[ClassEnum]
    BLUE_STAIN: _ClassVar[ClassEnum]
    OVERGROWN: _ClassVar[ClassEnum]
LIVEL_KNOT: ClassEnum
DEATH_KNOT: ClassEnum
KNOT_MISSING: ClassEnum
KNOT_WITH_CRACK: ClassEnum
CRACK: ClassEnum
QUARTZITY: ClassEnum
RESIN: ClassEnum
MARROW: ClassEnum
BLUE_STAIN: ClassEnum
OVERGROWN: ClassEnum

class BoundingBox(_message.Message):
    __slots__ = ["x_min", "y_min", "x_max", "y_max"]
    X_MIN_FIELD_NUMBER: _ClassVar[int]
    Y_MIN_FIELD_NUMBER: _ClassVar[int]
    X_MAX_FIELD_NUMBER: _ClassVar[int]
    Y_MAX_FIELD_NUMBER: _ClassVar[int]
    x_min: float
    y_min: float
    x_max: float
    y_max: float
    def __init__(self, x_min: _Optional[float] = ..., y_min: _Optional[float] = ..., x_max: _Optional[float] = ..., y_max: _Optional[float] = ...) -> None: ...

class DetectBatchRequest(_message.Message):
    __slots__ = ["batch"]
    BATCH_FIELD_NUMBER: _ClassVar[int]
    batch: _containers.RepeatedScalarFieldContainer[bytes]
    def __init__(self, batch: _Optional[_Iterable[bytes]] = ...) -> None: ...

class DetectResponse(_message.Message):
    __slots__ = ["objects"]
    OBJECTS_FIELD_NUMBER: _ClassVar[int]
    objects: _containers.RepeatedCompositeFieldContainer[ObjectDetection]
    def __init__(self, objects: _Optional[_Iterable[_Union[ObjectDetection, _Mapping]]] = ...) -> None: ...

class DetectBatchResponse(_message.Message):
    __slots__ = ["requests"]
    REQUESTS_FIELD_NUMBER: _ClassVar[int]
    requests: _containers.RepeatedCompositeFieldContainer[DetectResponse]
    def __init__(self, requests: _Optional[_Iterable[_Union[DetectResponse, _Mapping]]] = ...) -> None: ...

class ObjectDetection(_message.Message):
    __slots__ = ["confidence", "bounding_box"]
    CLASS_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_FIELD_NUMBER: _ClassVar[int]
    confidence: float
    bounding_box: BoundingBox
    def __init__(self, confidence: _Optional[float] = ..., bounding_box: _Optional[_Union[BoundingBox, _Mapping]] = ..., **kwargs) -> None: ...
