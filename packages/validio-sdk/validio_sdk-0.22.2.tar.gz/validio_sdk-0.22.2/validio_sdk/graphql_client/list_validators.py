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


class ListValidators(BaseModel):
    validators_list: List[
        Annotated[
            Union[
                "ListValidatorsValidatorsListValidator",
                "ListValidatorsValidatorsListCategoricalDistributionValidator",
                "ListValidatorsValidatorsListFreshnessValidator",
                "ListValidatorsValidatorsListNumericAnomalyValidator",
                "ListValidatorsValidatorsListNumericDistributionValidator",
                "ListValidatorsValidatorsListNumericValidator",
                "ListValidatorsValidatorsListRelativeTimeValidator",
                "ListValidatorsValidatorsListRelativeVolumeValidator",
                "ListValidatorsValidatorsListSqlValidator",
                "ListValidatorsValidatorsListVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="validatorsList")


class ListValidatorsValidatorsListValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListValidatorNamespace"
    tags: List["ListValidatorsValidatorsListValidatorTags"]


class ListValidatorsValidatorsListValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListValidatorSourceConfigSource(BaseModel):
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
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorNamespace"
    tags: List["ListValidatorsValidatorsListCategoricalDistributionValidatorTags"]
    config: "ListValidatorsValidatorsListCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfig(
    BaseModel
):
    source: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSource"
    )
    window: (
        "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindow"
    )
    segmentation: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListFreshnessValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorNamespace"
    tags: List["ListValidatorsValidatorsListFreshnessValidatorTags"]
    config: "ListValidatorsValidatorsListFreshnessValidatorConfig"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSource(BaseModel):
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
        "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListFreshnessValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorNamespace"
    tags: List["ListValidatorsValidatorsListNumericAnomalyValidatorTags"]
    config: "ListValidatorsValidatorsListNumericAnomalyValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSource(BaseModel):
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
        "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfig(
    BaseModel
):
    source: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSource"
    )
    window: (
        "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorNamespace"
    tags: List["ListValidatorsValidatorsListNumericDistributionValidatorTags"]
    config: "ListValidatorsValidatorsListNumericDistributionValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListNumericDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericValidatorNamespace"
    tags: List["ListValidatorsValidatorsListNumericValidatorTags"]
    config: "ListValidatorsValidatorsListNumericValidatorConfig"


class ListValidatorsValidatorsListNumericValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListNumericValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListNumericValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListNumericValidatorSourceConfigSource(BaseModel):
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
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListNumericValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListNumericValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListNumericValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentationNamespace"
    )


class ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListNumericValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListNumericValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListNumericValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListNumericValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorNamespace"
    tags: List["ListValidatorsValidatorsListRelativeTimeValidatorTags"]
    config: "ListValidatorsValidatorsListRelativeTimeValidatorConfig"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSource(BaseModel):
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
        "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListRelativeTimeValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorNamespace"
    tags: List["ListValidatorsValidatorsListRelativeVolumeValidatorTags"]
    config: "ListValidatorsValidatorsListRelativeVolumeValidatorConfig"
    reference_source_config: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindow"
    segmentation: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSource(BaseModel):
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
        "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceNamespace"
    )


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindowNamespace"
    )


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfig(
    BaseModel
):
    source: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSource"
    )
    window: (
        "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListSqlValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListSqlValidatorNamespace"
    tags: List["ListValidatorsValidatorsListSqlValidatorTags"]
    config: "ListValidatorsValidatorsListSqlValidatorConfig"


class ListValidatorsValidatorsListSqlValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListSqlValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListSqlValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListSqlValidatorSourceConfigSource(BaseModel):
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
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListSqlValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListSqlValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListSqlValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentationNamespace"
    )


class ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListSqlValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListSqlValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "ListValidatorsValidatorsListSqlValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListSqlValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class ListValidatorsValidatorsListSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListSqlValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListSqlValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ListValidatorsValidatorsListVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ListValidatorsValidatorsListVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListVolumeValidatorNamespace"
    tags: List["ListValidatorsValidatorsListVolumeValidatorTags"]
    config: "ListValidatorsValidatorsListVolumeValidatorConfig"


class ListValidatorsValidatorsListVolumeValidatorSourceConfig(BaseModel):
    source: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSource"
    window: "ListValidatorsValidatorsListVolumeValidatorSourceConfigWindow"
    segmentation: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSource(BaseModel):
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
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceNamespace"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ListValidatorsValidatorsListVolumeValidatorSourceConfigWindowNamespace"


class ListValidatorsValidatorsListVolumeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentationNamespace"
    )


class ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorNamespace(BaseModel):
    id: Any


class ListValidatorsValidatorsListVolumeValidatorTags(BaseModel):
    key: str
    value: str


class ListValidatorsValidatorsListVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ListValidatorsValidatorsListVolumeValidatorConfigThresholdDifferenceThreshold",
        "ListValidatorsValidatorsListVolumeValidatorConfigThresholdDynamicThreshold",
        "ListValidatorsValidatorsListVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ListValidatorsValidatorsListVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ListValidatorsValidatorsListVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ListValidatorsValidatorsListVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


ListValidators.model_rebuild()
ListValidatorsValidatorsListValidator.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidator.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorConfig.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListCategoricalDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListFreshnessValidator.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListFreshnessValidatorConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidator.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericAnomalyValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidator.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorConfig.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericDistributionValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericValidator.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListNumericValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListNumericValidatorConfig.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidator.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListRelativeTimeValidatorConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidator.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfig.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListRelativeVolumeValidatorReferenceSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListSqlValidator.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListSqlValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListSqlValidatorConfig.model_rebuild()
ListValidatorsValidatorsListVolumeValidator.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfig.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSource.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigWindow.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorSourceConfigSegmentation.model_rebuild()
ListValidatorsValidatorsListVolumeValidatorConfig.model_rebuild()
