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
from .fragments import ErrorDetails


class UpdateValidatorWithDifferenceThreshold(BaseModel):
    validator_with_difference_threshold_update: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdate"
    ) = Field(alias="validatorWithDifferenceThresholdUpdate")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdate(
    BaseModel
):
    errors: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateErrors"
    ]
    validator: Optional[
        Annotated[
            Union[
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidator",
                "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateErrors(
    ErrorDetails
):
    pass


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidator(
    BaseModel
):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorTags"
    ]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidator(
    BaseModel
):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidator(
    BaseModel
):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfig(
    BaseModel
):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidator(
    BaseModel
):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidator(
    BaseModel
):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidator(
    BaseModel
):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfig(
    BaseModel
):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidator(
    BaseModel
):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfig(
    BaseModel
):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidator(
    BaseModel
):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidator(
    BaseModel
):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfig(
    BaseModel
):
    query: str
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidator(
    BaseModel
):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorNamespace"
    tags: List[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorTags"
    ]
    config: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfig"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfig(
    BaseModel
):
    source: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSource"
    window: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSource(
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
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace"


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorNamespace(
    BaseModel
):
    id: Any


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorTags(
    BaseModel
):
    key: str
    value: str


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfig(
    BaseModel
):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


UpdateValidatorWithDifferenceThreshold.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdate.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorFreshnessValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorNumericValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeTimeValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorSqlValidatorConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidator.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfig.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSource.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigWindow.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorSourceConfigSegmentation.model_rebuild()
UpdateValidatorWithDifferenceThresholdValidatorWithDifferenceThresholdUpdateValidatorVolumeValidatorConfig.model_rebuild()
