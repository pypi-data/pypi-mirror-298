from datetime import datetime
from typing import Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    JsonFilterExpression,
    JsonPointer,
    SegmentationId,
    SourceId,
    ValidatorId,
    WindowId,
)

from .base_model import BaseModel
from .enums import (
    CategoricalDistributionMetric,
    ComparisonOperator,
    DecisionBoundsType,
    DifferenceOperator,
    DifferenceType,
    IncidentGroupPriority,
    IncidentStatus,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    VolumeMetric,
)
from .fragments import SegmentDetails


class GetIncidentGroup(BaseModel):
    incident_group: Optional["GetIncidentGroupIncidentGroup"] = Field(
        alias="incidentGroup"
    )


class GetIncidentGroupIncidentGroup(BaseModel):
    id: Any
    status: IncidentStatus
    priority: IncidentGroupPriority
    owner: Optional["GetIncidentGroupIncidentGroupOwner"]
    source: "GetIncidentGroupIncidentGroupSource"
    validator: Union[
        "GetIncidentGroupIncidentGroupValidatorValidator",
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidator",
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidator",
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidator",
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidator",
        "GetIncidentGroupIncidentGroupValidatorNumericValidator",
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidator",
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidator",
        "GetIncidentGroupIncidentGroupValidatorSqlValidator",
        "GetIncidentGroupIncidentGroupValidatorVolumeValidator",
    ] = Field(discriminator="typename__")
    segment: "GetIncidentGroupIncidentGroupSegment"
    severity_stats: "GetIncidentGroupIncidentGroupSeverityStats" = Field(
        alias="severityStats"
    )
    first_seen_at: datetime = Field(alias="firstSeenAt")
    last_seen_at: datetime = Field(alias="lastSeenAt")


class GetIncidentGroupIncidentGroupOwner(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")


class GetIncidentGroupIncidentGroupSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str


class GetIncidentGroupIncidentGroupValidatorValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorValidatorTags"]


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindowNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorNamespace"
    tags: List[
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorTags"
    ]
    config: (
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfig"
    )
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorFreshnessValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    sensitivity: float
    minimum_reference_datapoints: Optional[float] = Field(
        alias="minimumReferenceDatapoints"
    )
    minimum_absolute_difference: float = Field(alias="minimumAbsoluteDifference")
    minimum_relative_difference_percent: float = Field(
        alias="minimumRelativeDifferencePercent"
    )


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorNamespace"
    )
    tags: List["GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorNumericValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorNumericValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: (
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSource"
    )
    window: (
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindow"
    )
    segmentation: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorSqlValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSource(BaseModel):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindowNamespace"
    )


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorSqlValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupValidatorVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorNamespace"
    tags: List["GetIncidentGroupIncidentGroupValidatorVolumeValidatorTags"]
    config: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfig"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfig(BaseModel):
    source: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSource"
    window: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindow"
    segmentation: (
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSource(
    BaseModel
):
    typename__: Literal[
        "AwsAthenaSource",
        "AwsKinesisSource",
        "AwsRedshiftSource",
        "AwsS3Source",
        "AzureSynapseSource",
        "ClickHouseSource",
        "DatabricksSource",
        "DbtModelRunSource",
        "DbtTestResultSource",
        "DemoSource",
        "GcpBigQuerySource",
        "GcpPubSubLiteSource",
        "GcpPubSubSource",
        "GcpStorageSource",
        "KafkaSource",
        "PostgreSqlSource",
        "SnowflakeSource",
        "Source",
    ] = Field(alias="__typename")
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceNamespace"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindowNamespace"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorNamespace(BaseModel):
    id: Any


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorTags(BaseModel):
    key: str
    value: str


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetIncidentGroupIncidentGroupSegment(SegmentDetails):
    pass


class GetIncidentGroupIncidentGroupSeverityStats(BaseModel):
    high_count: int = Field(alias="highCount")
    medium_count: int = Field(alias="mediumCount")
    low_count: int = Field(alias="lowCount")
    total_count: int = Field(alias="totalCount")


GetIncidentGroup.model_rebuild()
GetIncidentGroupIncidentGroup.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorFreshnessValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorNumericValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeTimeValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorSqlValidatorConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidator.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfig.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSource.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetIncidentGroupIncidentGroupValidatorVolumeValidatorConfig.model_rebuild()
