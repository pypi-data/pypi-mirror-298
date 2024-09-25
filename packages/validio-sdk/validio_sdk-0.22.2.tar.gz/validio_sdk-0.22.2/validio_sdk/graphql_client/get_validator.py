from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

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
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    VolumeMetric,
)


class GetValidator(BaseModel):
    validator: Optional[
        Annotated[
            Union[
                "GetValidatorValidatorValidator",
                "GetValidatorValidatorCategoricalDistributionValidator",
                "GetValidatorValidatorFreshnessValidator",
                "GetValidatorValidatorNumericAnomalyValidator",
                "GetValidatorValidatorNumericDistributionValidator",
                "GetValidatorValidatorNumericValidator",
                "GetValidatorValidatorRelativeTimeValidator",
                "GetValidatorValidatorRelativeVolumeValidator",
                "GetValidatorValidatorSqlValidator",
                "GetValidatorValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class GetValidatorValidatorValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorValidatorNamespace"
    tags: List["GetValidatorValidatorValidatorTags"]


class GetValidatorValidatorValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorValidatorSourceConfigSource"
    window: "GetValidatorValidatorValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorNamespace"
    tags: List["GetValidatorValidatorCategoricalDistributionValidatorTags"]
    config: "GetValidatorValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: (
        "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorCategoricalDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorFreshnessValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorFreshnessValidatorNamespace"
    tags: List["GetValidatorValidatorFreshnessValidatorTags"]
    config: "GetValidatorValidatorFreshnessValidatorConfig"


class GetValidatorValidatorFreshnessValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorFreshnessValidatorSourceConfigSource"
    window: "GetValidatorValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorFreshnessValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorFreshnessValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorFreshnessValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorFreshnessValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorFreshnessValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorFreshnessValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorFreshnessValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorFreshnessValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "GetValidatorValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorFreshnessValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorFreshnessValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorNumericAnomalyValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorNamespace"
    tags: List["GetValidatorValidatorNumericAnomalyValidatorTags"]
    config: "GetValidatorValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorNumericAnomalyValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorNumericDistributionValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericDistributionValidatorNamespace"
    tags: List["GetValidatorValidatorNumericDistributionValidatorTags"]
    config: "GetValidatorValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorNumericDistributionValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSource"
    window: "GetValidatorValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: (
        "GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSource(BaseModel):
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
        "GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceNamespace"
    )


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorNumericDistributionValidatorSourceConfigWindowNamespace"
    )


class GetValidatorValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorNumericDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfig(BaseModel):
    source: (
        "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    )
    window: (
        "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericValidatorNamespace"
    tags: List["GetValidatorValidatorNumericValidatorTags"]
    config: "GetValidatorValidatorNumericValidatorConfig"


class GetValidatorValidatorNumericValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorNumericValidatorSourceConfigSource"
    window: "GetValidatorValidatorNumericValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorNumericValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorNumericValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorNumericValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorNumericValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorNumericValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorNumericValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorNumericValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorNumericValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorRelativeTimeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeTimeValidatorNamespace"
    tags: List["GetValidatorValidatorRelativeTimeValidatorTags"]
    config: "GetValidatorValidatorRelativeTimeValidatorConfig"


class GetValidatorValidatorRelativeTimeValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSource"
    window: "GetValidatorValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorRelativeTimeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeTimeValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorRelativeVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorNamespace"
    tags: List["GetValidatorValidatorRelativeVolumeValidatorTags"]
    config: "GetValidatorValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorValidatorRelativeVolumeValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"
    )


class GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfig(BaseModel):
    source: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorValidatorSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorSqlValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorSqlValidatorNamespace"
    tags: List["GetValidatorValidatorSqlValidatorTags"]
    config: "GetValidatorValidatorSqlValidatorConfig"


class GetValidatorValidatorSqlValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorSqlValidatorSourceConfigSource"
    window: "GetValidatorValidatorSqlValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorSqlValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorSqlValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorSqlValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorSqlValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorSqlValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorSqlValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "GetValidatorValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class GetValidatorValidatorSqlValidatorConfigThresholdDifferenceThreshold(BaseModel):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorSqlValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorSqlValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorValidatorVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "GetValidatorValidatorVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorVolumeValidatorNamespace"
    tags: List["GetValidatorValidatorVolumeValidatorTags"]
    config: "GetValidatorValidatorVolumeValidatorConfig"


class GetValidatorValidatorVolumeValidatorSourceConfig(BaseModel):
    source: "GetValidatorValidatorVolumeValidatorSourceConfigSource"
    window: "GetValidatorValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorValidatorVolumeValidatorSourceConfigSource(BaseModel):
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
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorValidatorVolumeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorValidatorVolumeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class GetValidatorValidatorVolumeValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorNamespace(BaseModel):
    id: Any


class GetValidatorValidatorVolumeValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorValidatorVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorValidatorVolumeValidatorConfigThresholdDifferenceThreshold(BaseModel):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorValidatorVolumeValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorValidatorVolumeValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


GetValidator.model_rebuild()
GetValidatorValidatorValidator.model_rebuild()
GetValidatorValidatorValidatorSourceConfig.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidator.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorConfig.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorFreshnessValidator.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfig.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorFreshnessValidatorConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidator.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericDistributionValidator.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorConfig.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericValidator.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfig.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorNumericValidatorConfig.model_rebuild()
GetValidatorValidatorRelativeTimeValidator.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorRelativeTimeValidatorConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidator.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorValidatorSqlValidator.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfig.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorSqlValidatorConfig.model_rebuild()
GetValidatorValidatorVolumeValidator.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfig.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorValidatorVolumeValidatorConfig.model_rebuild()
