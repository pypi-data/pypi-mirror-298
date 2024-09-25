from google.protobuf import timestamp_pb2 as _timestamp_pb2
from tecton_proto.common import container_image__client_pb2 as _container_image__client_pb2
from tecton_proto.common import id__client_pb2 as _id__client_pb2
from tecton_proto.common import server_group_status__client_pb2 as _server_group_status__client_pb2
from tecton_proto.common import server_group_type__client_pb2 as _server_group_type__client_pb2
from tecton_proto.realtime import instance_group__client_pb2 as _instance_group__client_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AutoscalingPolicy(_message.Message):
    __slots__ = ["autoscaling_enabled", "name", "target_tracking_policy"]
    AUTOSCALING_ENABLED_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TARGET_TRACKING_POLICY_FIELD_NUMBER: ClassVar[int]
    autoscaling_enabled: bool
    name: str
    target_tracking_policy: TargetTrackingPolicy
    def __init__(self, name: Optional[str] = ..., autoscaling_enabled: bool = ..., target_tracking_policy: Optional[Union[TargetTrackingPolicy, Mapping]] = ...) -> None: ...

class CustomMetric(_message.Message):
    __slots__ = ["name", "statistic", "unit"]
    NAME_FIELD_NUMBER: ClassVar[int]
    STATISTIC_FIELD_NUMBER: ClassVar[int]
    UNIT_FIELD_NUMBER: ClassVar[int]
    name: str
    statistic: str
    unit: str
    def __init__(self, name: Optional[str] = ..., statistic: Optional[str] = ..., unit: Optional[str] = ...) -> None: ...

class FeatureServerGroupState(_message.Message):
    __slots__ = ["instance_type"]
    INSTANCE_TYPE_FIELD_NUMBER: ClassVar[int]
    instance_type: str
    def __init__(self, instance_type: Optional[str] = ...) -> None: ...

class PredefinedMetric(_message.Message):
    __slots__ = ["type"]
    TYPE_FIELD_NUMBER: ClassVar[int]
    type: str
    def __init__(self, type: Optional[str] = ...) -> None: ...

class ServerGroupState(_message.Message):
    __slots__ = ["autoscaling_policy", "created_at", "desired_nodes", "feature_server_group_state", "last_updated_at", "max_nodes", "min_nodes", "name", "server_group_id", "server_group_state_id", "status", "status_details", "transform_server_group_state", "type", "workspace", "workspace_state_id"]
    AUTOSCALING_POLICY_FIELD_NUMBER: ClassVar[int]
    CREATED_AT_FIELD_NUMBER: ClassVar[int]
    DESIRED_NODES_FIELD_NUMBER: ClassVar[int]
    FEATURE_SERVER_GROUP_STATE_FIELD_NUMBER: ClassVar[int]
    LAST_UPDATED_AT_FIELD_NUMBER: ClassVar[int]
    MAX_NODES_FIELD_NUMBER: ClassVar[int]
    MIN_NODES_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    SERVER_GROUP_ID_FIELD_NUMBER: ClassVar[int]
    SERVER_GROUP_STATE_ID_FIELD_NUMBER: ClassVar[int]
    STATUS_DETAILS_FIELD_NUMBER: ClassVar[int]
    STATUS_FIELD_NUMBER: ClassVar[int]
    TRANSFORM_SERVER_GROUP_STATE_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_FIELD_NUMBER: ClassVar[int]
    WORKSPACE_STATE_ID_FIELD_NUMBER: ClassVar[int]
    autoscaling_policy: AutoscalingPolicy
    created_at: _timestamp_pb2.Timestamp
    desired_nodes: int
    feature_server_group_state: FeatureServerGroupState
    last_updated_at: _timestamp_pb2.Timestamp
    max_nodes: int
    min_nodes: int
    name: str
    server_group_id: _id__client_pb2.Id
    server_group_state_id: _id__client_pb2.Id
    status: _server_group_status__client_pb2.ServerGroupStatus
    status_details: str
    transform_server_group_state: TransformServerGroupState
    type: _server_group_type__client_pb2.ServerGroupType
    workspace: str
    workspace_state_id: _id__client_pb2.Id
    def __init__(self, server_group_state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., server_group_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ..., name: Optional[str] = ..., status: Optional[Union[_server_group_status__client_pb2.ServerGroupStatus, str]] = ..., type: Optional[Union[_server_group_type__client_pb2.ServerGroupType, str]] = ..., autoscaling_policy: Optional[Union[AutoscalingPolicy, Mapping]] = ..., status_details: Optional[str] = ..., created_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., last_updated_at: Optional[Union[_timestamp_pb2.Timestamp, Mapping]] = ..., min_nodes: Optional[int] = ..., max_nodes: Optional[int] = ..., desired_nodes: Optional[int] = ..., transform_server_group_state: Optional[Union[TransformServerGroupState, Mapping]] = ..., feature_server_group_state: Optional[Union[FeatureServerGroupState, Mapping]] = ..., workspace: Optional[str] = ..., workspace_state_id: Optional[Union[_id__client_pb2.Id, Mapping]] = ...) -> None: ...

class TargetTrackingPolicy(_message.Message):
    __slots__ = ["custom_metric", "predefined_metric", "scale_in_disabled", "target_value"]
    CUSTOM_METRIC_FIELD_NUMBER: ClassVar[int]
    PREDEFINED_METRIC_FIELD_NUMBER: ClassVar[int]
    SCALE_IN_DISABLED_FIELD_NUMBER: ClassVar[int]
    TARGET_VALUE_FIELD_NUMBER: ClassVar[int]
    custom_metric: CustomMetric
    predefined_metric: PredefinedMetric
    scale_in_disabled: bool
    target_value: float
    def __init__(self, target_value: Optional[float] = ..., scale_in_disabled: bool = ..., predefined_metric: Optional[Union[PredefinedMetric, Mapping]] = ..., custom_metric: Optional[Union[CustomMetric, Mapping]] = ...) -> None: ...

class TransformServerGroupState(_message.Message):
    __slots__ = ["autoscaling_policy", "environment_id", "environment_name", "environment_variables", "image_info", "instance_group_handle"]
    class EnvironmentVariablesEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        key: str
        value: str
        def __init__(self, key: Optional[str] = ..., value: Optional[str] = ...) -> None: ...
    AUTOSCALING_POLICY_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_ID_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_NAME_FIELD_NUMBER: ClassVar[int]
    ENVIRONMENT_VARIABLES_FIELD_NUMBER: ClassVar[int]
    IMAGE_INFO_FIELD_NUMBER: ClassVar[int]
    INSTANCE_GROUP_HANDLE_FIELD_NUMBER: ClassVar[int]
    autoscaling_policy: AutoscalingPolicy
    environment_id: str
    environment_name: str
    environment_variables: _containers.ScalarMap[str, str]
    image_info: _container_image__client_pb2.ContainerImage
    instance_group_handle: _instance_group__client_pb2.InstanceGroupHandle
    def __init__(self, environment_id: Optional[str] = ..., environment_name: Optional[str] = ..., image_info: Optional[Union[_container_image__client_pb2.ContainerImage, Mapping]] = ..., environment_variables: Optional[Mapping[str, str]] = ..., autoscaling_policy: Optional[Union[AutoscalingPolicy, Mapping]] = ..., instance_group_handle: Optional[Union[_instance_group__client_pb2.InstanceGroupHandle, Mapping]] = ...) -> None: ...
