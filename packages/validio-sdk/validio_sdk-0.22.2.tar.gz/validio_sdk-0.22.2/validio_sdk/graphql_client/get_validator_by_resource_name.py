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


class GetValidatorByResourceName(BaseModel):
    validator_by_resource_name: Optional[
        Annotated[
            Union[
                "GetValidatorByResourceNameValidatorByResourceNameValidator",
                "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidator",
                "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidator",
                "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidator",
                "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidator",
                "GetValidatorByResourceNameValidatorByResourceNameNumericValidator",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidator",
                "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidator",
                "GetValidatorByResourceNameValidatorByResourceNameSqlValidator",
                "GetValidatorByResourceNameValidatorByResourceNameVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="validatorByResourceName")


class GetValidatorByResourceNameValidatorByResourceNameValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorNamespace"
    tags: List["GetValidatorByResourceNameValidatorByResourceNameValidatorTags"]


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfig(BaseModel):
    source: (
        "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSource"
    )
    window: (
        "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindow"
    )
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorNamespace(BaseModel):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidator(
    BaseModel
):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorTags"
    ]
    config: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorNamespace"
    )
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorTags"
    ]
    config: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorTags(
    BaseModel
):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfig(
    BaseModel
):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidator(
    BaseModel
):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorTags"
    ]
    config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfig"
    )
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorTags(
    BaseModel
):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidator(
    BaseModel
):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorTags"
    ]
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfig"
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorTags(
    BaseModel
):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorNamespace"
    )
    tags: List["GetValidatorByResourceNameValidatorByResourceNameNumericValidatorTags"]
    config: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorTags"
    ]
    config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfig"
    )


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorTags(
    BaseModel
):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfig(
    BaseModel
):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidator(
    BaseModel
):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorNamespace"
    tags: List[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorTags"
    ]
    config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfig"
    )
    reference_source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorTags(
    BaseModel
):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorNamespace"
    tags: List["GetValidatorByResourceNameValidatorByResourceNameSqlValidatorTags"]
    config: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorNamespace(BaseModel):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorNamespace"
    )
    tags: List["GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorTags"]
    config: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfig"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfig(
    BaseModel
):
    source: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSource"
    window: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindow"
    segmentation: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSource(
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
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceNamespace"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindowNamespace"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentationNamespace"


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorTags(BaseModel):
    key: str
    value: str


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDifferenceThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDynamicThreshold",
        "GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


GetValidatorByResourceName.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameFreshnessValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameNumericValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeTimeValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameSqlValidatorConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidator.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfig.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSource.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigWindow.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorSourceConfigSegmentation.model_rebuild()
GetValidatorByResourceNameValidatorByResourceNameVolumeValidatorConfig.model_rebuild()
