from datetime import datetime
from typing import Annotated, Any, List, Literal, Optional, Union

from pydantic import Field

from validio_sdk.scalars import (
    CredentialId,
    CronExpression,
    JsonFilterExpression,
    JsonPointer,
    JsonTypeDefinition,
    SegmentationId,
    SourceId,
    ValidatorId,
    WindowId,
)

from .base_model import BaseModel
from .enums import (
    ApiErrorCode,
    AzureSynapseBackendType,
    CatalogAssetDescriptionOrigin,
    CatalogAssetType,
    CategoricalDistributionMetric,
    ClickHouseProtocol,
    ComparisonOperator,
    DecisionBoundsType,
    DifferenceOperator,
    DifferenceType,
    FileFormat,
    IdentityDeleteErrorCode,
    IdentityProviderCreateErrorCode,
    IdentityProviderDeleteErrorCode,
    IdentityProviderUpdateErrorCode,
    IncidentSeverity,
    IssueTypename,
    LoginType,
    NumericAnomalyMetric,
    NumericDistributionMetric,
    NumericMetric,
    RelativeTimeMetric,
    RelativeVolumeMetric,
    Role,
    SourceState,
    StreamingSourceMessageFormat,
    UserDeleteErrorCode,
    UserStatus,
    UserUpdateErrorCode,
    VolumeMetric,
    WindowTimeUnit,
)


class ApiKeyDetails(BaseModel):
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    last_used_at: Optional[datetime] = Field(alias="lastUsedAt")
    global_role: Role = Field(alias="globalRole")


class CatalogAssetDescriptionDetails(BaseModel):
    typename__: str = Field(alias="__typename")
    description: str
    origin: CatalogAssetDescriptionOrigin


class CatalogAssetStatsDetails(BaseModel):
    utilization: Optional[float]
    n_reads: Optional[int] = Field(alias="nReads")
    n_writes: Optional[int] = Field(alias="nWrites")


class ErrorDetails(BaseModel):
    typename__: str = Field(alias="__typename")
    code: ApiErrorCode
    message: str


class ChannelCreation(BaseModel):
    errors: List["ChannelCreationErrors"]
    channel: Optional[
        Annotated[
            Union[
                "ChannelCreationChannelChannel",
                "ChannelCreationChannelMsTeamsChannel",
                "ChannelCreationChannelSlackChannel",
                "ChannelCreationChannelWebhookChannel",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class ChannelCreationErrors(ErrorDetails):
    pass


class ChannelCreationChannelChannel(BaseModel):
    typename__: Literal["Channel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelCreationChannelChannelNamespace"
    notification_rules: List["ChannelCreationChannelChannelNotificationRules"] = Field(
        alias="notificationRules"
    )


class ChannelCreationChannelChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelCreationChannelChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelCreationChannelMsTeamsChannel(BaseModel):
    typename__: Literal["MsTeamsChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelCreationChannelMsTeamsChannelNamespace"
    notification_rules: List[
        "ChannelCreationChannelMsTeamsChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "ChannelCreationChannelMsTeamsChannelConfig"


class ChannelCreationChannelMsTeamsChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelCreationChannelMsTeamsChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelCreationChannelMsTeamsChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class ChannelCreationChannelSlackChannel(BaseModel):
    typename__: Literal["SlackChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelCreationChannelSlackChannelNamespace"
    notification_rules: List["ChannelCreationChannelSlackChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )
    config: "ChannelCreationChannelSlackChannelConfig"


class ChannelCreationChannelSlackChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelCreationChannelSlackChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelCreationChannelSlackChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class ChannelCreationChannelWebhookChannel(BaseModel):
    typename__: Literal["WebhookChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelCreationChannelWebhookChannelNamespace"
    notification_rules: List[
        "ChannelCreationChannelWebhookChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "ChannelCreationChannelWebhookChannelConfig"


class ChannelCreationChannelWebhookChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelCreationChannelWebhookChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelCreationChannelWebhookChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader")


class ChannelDeletion(BaseModel):
    errors: List["ChannelDeletionErrors"]
    channel: Optional["ChannelDeletionChannel"]


class ChannelDeletionErrors(BaseModel):
    code: ApiErrorCode
    message: str


class ChannelDeletionChannel(BaseModel):
    typename__: Literal[
        "Channel", "MsTeamsChannel", "SlackChannel", "WebhookChannel"
    ] = Field(alias="__typename")
    id: Any
    name: str


class ChannelUpdate(BaseModel):
    errors: List["ChannelUpdateErrors"]
    channel: Optional[
        Annotated[
            Union[
                "ChannelUpdateChannelChannel",
                "ChannelUpdateChannelMsTeamsChannel",
                "ChannelUpdateChannelSlackChannel",
                "ChannelUpdateChannelWebhookChannel",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class ChannelUpdateErrors(BaseModel):
    code: ApiErrorCode
    message: str


class ChannelUpdateChannelChannel(BaseModel):
    typename__: Literal["Channel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelUpdateChannelChannelNamespace"
    notification_rules: List["ChannelUpdateChannelChannelNotificationRules"] = Field(
        alias="notificationRules"
    )


class ChannelUpdateChannelChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelUpdateChannelChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelUpdateChannelMsTeamsChannel(BaseModel):
    typename__: Literal["MsTeamsChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelUpdateChannelMsTeamsChannelNamespace"
    notification_rules: List["ChannelUpdateChannelMsTeamsChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )
    config: "ChannelUpdateChannelMsTeamsChannelConfig"


class ChannelUpdateChannelMsTeamsChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelUpdateChannelMsTeamsChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelUpdateChannelMsTeamsChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class ChannelUpdateChannelSlackChannel(BaseModel):
    typename__: Literal["SlackChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelUpdateChannelSlackChannelNamespace"
    notification_rules: List["ChannelUpdateChannelSlackChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )
    config: "ChannelUpdateChannelSlackChannelConfig"


class ChannelUpdateChannelSlackChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelUpdateChannelSlackChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelUpdateChannelSlackChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class ChannelUpdateChannelWebhookChannel(BaseModel):
    typename__: Literal["WebhookChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ChannelUpdateChannelWebhookChannelNamespace"
    notification_rules: List["ChannelUpdateChannelWebhookChannelNotificationRules"] = (
        Field(alias="notificationRules")
    )
    config: "ChannelUpdateChannelWebhookChannelConfig"


class ChannelUpdateChannelWebhookChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class ChannelUpdateChannelWebhookChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class ChannelUpdateChannelWebhookChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader")


class CredentialBase(BaseModel):
    id: CredentialId
    typename__: str = Field(alias="__typename")
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialBaseNamespace"


class CredentialBaseNamespace(BaseModel):
    id: Any


class CredentialCreation(BaseModel):
    typename__: str = Field(alias="__typename")
    errors: List["CredentialCreationErrors"]
    credential: Optional[
        Annotated[
            Union[
                "CredentialCreationCredentialCredential",
                "CredentialCreationCredentialAwsAthenaCredential",
                "CredentialCreationCredentialAwsCredential",
                "CredentialCreationCredentialAwsRedshiftCredential",
                "CredentialCreationCredentialAzureSynapseEntraIdCredential",
                "CredentialCreationCredentialAzureSynapseSqlCredential",
                "CredentialCreationCredentialClickHouseCredential",
                "CredentialCreationCredentialDatabricksCredential",
                "CredentialCreationCredentialDbtCloudCredential",
                "CredentialCreationCredentialDbtCoreCredential",
                "CredentialCreationCredentialGcpCredential",
                "CredentialCreationCredentialKafkaSaslSslPlainCredential",
                "CredentialCreationCredentialKafkaSslCredential",
                "CredentialCreationCredentialLookerCredential",
                "CredentialCreationCredentialPostgreSqlCredential",
                "CredentialCreationCredentialSnowflakeCredential",
                "CredentialCreationCredentialTableauConnectedAppCredential",
                "CredentialCreationCredentialTableauPersonalAccessTokenCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class CredentialCreationErrors(ErrorDetails):
    pass


class CredentialCreationCredentialCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialCredentialNamespace"


class CredentialCreationCredentialCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialAwsAthenaCredentialNamespace"
    config: "CredentialCreationCredentialAwsAthenaCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialAwsAthenaCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialAwsAthenaCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class CredentialCreationCredentialAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialAwsCredentialNamespace"
    config: "CredentialCreationCredentialAwsCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialAwsCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class CredentialCreationCredentialAwsRedshiftCredential(BaseModel):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialAwsRedshiftCredentialNamespace"
    config: "CredentialCreationCredentialAwsRedshiftCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialAwsRedshiftCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialAwsRedshiftCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class CredentialCreationCredentialAzureSynapseEntraIdCredential(BaseModel):
    typename__: Literal["AzureSynapseEntraIdCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialAzureSynapseEntraIdCredentialNamespace"
    config: "CredentialCreationCredentialAzureSynapseEntraIdCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialAzureSynapseEntraIdCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialAzureSynapseEntraIdCredentialConfig(BaseModel):
    client_id: str = Field(alias="clientId")
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class CredentialCreationCredentialAzureSynapseSqlCredential(BaseModel):
    typename__: Literal["AzureSynapseSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialAzureSynapseSqlCredentialNamespace"
    config: "CredentialCreationCredentialAzureSynapseSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialAzureSynapseSqlCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialAzureSynapseSqlCredentialConfig(BaseModel):
    username: str
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class CredentialCreationCredentialClickHouseCredential(BaseModel):
    typename__: Literal["ClickHouseCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialClickHouseCredentialNamespace"
    config: "CredentialCreationCredentialClickHouseCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialClickHouseCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialClickHouseCredentialConfig(BaseModel):
    protocol: ClickHouseProtocol
    host: str
    port: int
    username: str
    default_database: str = Field(alias="defaultDatabase")


class CredentialCreationCredentialDatabricksCredential(BaseModel):
    typename__: Literal["DatabricksCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialDatabricksCredentialNamespace"
    config: "CredentialCreationCredentialDatabricksCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialDatabricksCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialDatabricksCredentialConfig(BaseModel):
    host: str
    port: int
    http_path: str = Field(alias="httpPath")


class CredentialCreationCredentialDbtCloudCredential(BaseModel):
    typename__: Literal["DbtCloudCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialDbtCloudCredentialNamespace"
    config: "CredentialCreationCredentialDbtCloudCredentialConfig"


class CredentialCreationCredentialDbtCloudCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialDbtCloudCredentialConfig(BaseModel):
    warehouse_credential: (
        "CredentialCreationCredentialDbtCloudCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")
    account_id: str = Field(alias="accountId")
    api_base_url: Optional[str] = Field(alias="apiBaseUrl")


class CredentialCreationCredentialDbtCloudCredentialConfigWarehouseCredential(
    CredentialBase
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")


class CredentialCreationCredentialDbtCoreCredential(BaseModel):
    typename__: Literal["DbtCoreCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialDbtCoreCredentialNamespace"
    config: "CredentialCreationCredentialDbtCoreCredentialConfig"


class CredentialCreationCredentialDbtCoreCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialDbtCoreCredentialConfig(BaseModel):
    warehouse_credential: (
        "CredentialCreationCredentialDbtCoreCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")


class CredentialCreationCredentialDbtCoreCredentialConfigWarehouseCredential(
    CredentialBase
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")


class CredentialCreationCredentialGcpCredential(BaseModel):
    typename__: Literal["GcpCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialGcpCredentialNamespace"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialGcpCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialKafkaSaslSslPlainCredential(BaseModel):
    typename__: Literal["KafkaSaslSslPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialKafkaSaslSslPlainCredentialNamespace"
    config: "CredentialCreationCredentialKafkaSaslSslPlainCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialKafkaSaslSslPlainCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialKafkaSaslSslPlainCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


class CredentialCreationCredentialKafkaSslCredential(BaseModel):
    typename__: Literal["KafkaSslCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialKafkaSslCredentialNamespace"
    config: "CredentialCreationCredentialKafkaSslCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialKafkaSslCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialKafkaSslCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class CredentialCreationCredentialLookerCredential(BaseModel):
    typename__: Literal["LookerCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialLookerCredentialNamespace"
    config: "CredentialCreationCredentialLookerCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialLookerCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialLookerCredentialConfig(BaseModel):
    base_url: str = Field(alias="baseUrl")
    client_id: str = Field(alias="clientId")


class CredentialCreationCredentialPostgreSqlCredential(BaseModel):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialPostgreSqlCredentialNamespace"
    config: "CredentialCreationCredentialPostgreSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialPostgreSqlCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialPostgreSqlCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class CredentialCreationCredentialSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialSnowflakeCredentialNamespace"
    config: "CredentialCreationCredentialSnowflakeCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialSnowflakeCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialSnowflakeCredentialConfig(BaseModel):
    account: str
    user: str
    role: Optional[str]
    warehouse: Optional[str]
    auth: Optional[
        Annotated[
            Union[
                "CredentialCreationCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair",
                "CredentialCreationCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class CredentialCreationCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialKeyPair"] = Field(alias="__typename")
    user: str


class CredentialCreationCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialUserPassword"] = Field(alias="__typename")
    user: str


class CredentialCreationCredentialTableauConnectedAppCredential(BaseModel):
    typename__: Literal["TableauConnectedAppCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialCreationCredentialTableauConnectedAppCredentialNamespace"
    config: "CredentialCreationCredentialTableauConnectedAppCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialTableauConnectedAppCredentialNamespace(BaseModel):
    id: Any


class CredentialCreationCredentialTableauConnectedAppCredentialConfig(BaseModel):
    host: str
    site: Optional[str]
    user: str
    client_id: str = Field(alias="clientId")
    secret_id: str = Field(alias="secretId")


class CredentialCreationCredentialTableauPersonalAccessTokenCredential(BaseModel):
    typename__: Literal["TableauPersonalAccessTokenCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "CredentialCreationCredentialTableauPersonalAccessTokenCredentialNamespace"
    )
    config: "CredentialCreationCredentialTableauPersonalAccessTokenCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialCreationCredentialTableauPersonalAccessTokenCredentialNamespace(
    BaseModel
):
    id: Any


class CredentialCreationCredentialTableauPersonalAccessTokenCredentialConfig(BaseModel):
    host: str
    site: Optional[str]
    token_name: str = Field(alias="tokenName")


class CredentialSecretChanged(BaseModel):
    errors: List["CredentialSecretChangedErrors"]
    has_changed: Optional[bool] = Field(alias="hasChanged")


class CredentialSecretChangedErrors(ErrorDetails):
    pass


class CredentialUpdate(BaseModel):
    errors: List["CredentialUpdateErrors"]
    credential: Optional[
        Annotated[
            Union[
                "CredentialUpdateCredentialCredential",
                "CredentialUpdateCredentialAwsAthenaCredential",
                "CredentialUpdateCredentialAwsCredential",
                "CredentialUpdateCredentialAwsRedshiftCredential",
                "CredentialUpdateCredentialAzureSynapseEntraIdCredential",
                "CredentialUpdateCredentialAzureSynapseSqlCredential",
                "CredentialUpdateCredentialClickHouseCredential",
                "CredentialUpdateCredentialDatabricksCredential",
                "CredentialUpdateCredentialDbtCloudCredential",
                "CredentialUpdateCredentialDbtCoreCredential",
                "CredentialUpdateCredentialGcpCredential",
                "CredentialUpdateCredentialKafkaSaslSslPlainCredential",
                "CredentialUpdateCredentialKafkaSslCredential",
                "CredentialUpdateCredentialLookerCredential",
                "CredentialUpdateCredentialPostgreSqlCredential",
                "CredentialUpdateCredentialSnowflakeCredential",
                "CredentialUpdateCredentialTableauConnectedAppCredential",
                "CredentialUpdateCredentialTableauPersonalAccessTokenCredential",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class CredentialUpdateErrors(ErrorDetails):
    pass


class CredentialUpdateCredentialCredential(BaseModel):
    typename__: Literal["Credential", "DemoCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialCredentialNamespace"


class CredentialUpdateCredentialCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialAwsAthenaCredential(BaseModel):
    typename__: Literal["AwsAthenaCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialAwsAthenaCredentialNamespace"
    config: "CredentialUpdateCredentialAwsAthenaCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialAwsAthenaCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialAwsAthenaCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")
    region: str
    query_result_location: str = Field(alias="queryResultLocation")


class CredentialUpdateCredentialAwsCredential(BaseModel):
    typename__: Literal["AwsCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialAwsCredentialNamespace"
    config: "CredentialUpdateCredentialAwsCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialAwsCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialAwsCredentialConfig(BaseModel):
    access_key: str = Field(alias="accessKey")


class CredentialUpdateCredentialAwsRedshiftCredential(BaseModel):
    typename__: Literal["AwsRedshiftCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialAwsRedshiftCredentialNamespace"
    config: "CredentialUpdateCredentialAwsRedshiftCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialAwsRedshiftCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialAwsRedshiftCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class CredentialUpdateCredentialAzureSynapseEntraIdCredential(BaseModel):
    typename__: Literal["AzureSynapseEntraIdCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialAzureSynapseEntraIdCredentialNamespace"
    config: "CredentialUpdateCredentialAzureSynapseEntraIdCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialAzureSynapseEntraIdCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialAzureSynapseEntraIdCredentialConfig(BaseModel):
    client_id: str = Field(alias="clientId")
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class CredentialUpdateCredentialAzureSynapseSqlCredential(BaseModel):
    typename__: Literal["AzureSynapseSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialAzureSynapseSqlCredentialNamespace"
    config: "CredentialUpdateCredentialAzureSynapseSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialAzureSynapseSqlCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialAzureSynapseSqlCredentialConfig(BaseModel):
    username: str
    host: str
    port: int
    database: Optional[str]
    backend_type: AzureSynapseBackendType = Field(alias="backendType")


class CredentialUpdateCredentialClickHouseCredential(BaseModel):
    typename__: Literal["ClickHouseCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialClickHouseCredentialNamespace"
    config: "CredentialUpdateCredentialClickHouseCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialClickHouseCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialClickHouseCredentialConfig(BaseModel):
    protocol: ClickHouseProtocol
    host: str
    port: int
    username: str
    default_database: str = Field(alias="defaultDatabase")


class CredentialUpdateCredentialDatabricksCredential(BaseModel):
    typename__: Literal["DatabricksCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialDatabricksCredentialNamespace"
    config: "CredentialUpdateCredentialDatabricksCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialDatabricksCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialDatabricksCredentialConfig(BaseModel):
    host: str
    port: int
    http_path: str = Field(alias="httpPath")


class CredentialUpdateCredentialDbtCloudCredential(BaseModel):
    typename__: Literal["DbtCloudCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialDbtCloudCredentialNamespace"
    config: "CredentialUpdateCredentialDbtCloudCredentialConfig"


class CredentialUpdateCredentialDbtCloudCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialDbtCloudCredentialConfig(BaseModel):
    warehouse_credential: (
        "CredentialUpdateCredentialDbtCloudCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")
    account_id: str = Field(alias="accountId")
    api_base_url: Optional[str] = Field(alias="apiBaseUrl")


class CredentialUpdateCredentialDbtCloudCredentialConfigWarehouseCredential(
    CredentialBase
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")


class CredentialUpdateCredentialDbtCoreCredential(BaseModel):
    typename__: Literal["DbtCoreCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialDbtCoreCredentialNamespace"
    config: "CredentialUpdateCredentialDbtCoreCredentialConfig"


class CredentialUpdateCredentialDbtCoreCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialDbtCoreCredentialConfig(BaseModel):
    warehouse_credential: (
        "CredentialUpdateCredentialDbtCoreCredentialConfigWarehouseCredential"
    ) = Field(alias="warehouseCredential")


class CredentialUpdateCredentialDbtCoreCredentialConfigWarehouseCredential(
    CredentialBase
):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")


class CredentialUpdateCredentialGcpCredential(BaseModel):
    typename__: Literal["GcpCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialGcpCredentialNamespace"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialGcpCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialKafkaSaslSslPlainCredential(BaseModel):
    typename__: Literal["KafkaSaslSslPlainCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialKafkaSaslSslPlainCredentialNamespace"
    config: "CredentialUpdateCredentialKafkaSaslSslPlainCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialKafkaSaslSslPlainCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialKafkaSaslSslPlainCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    username: str


class CredentialUpdateCredentialKafkaSslCredential(BaseModel):
    typename__: Literal["KafkaSslCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialKafkaSslCredentialNamespace"
    config: "CredentialUpdateCredentialKafkaSslCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialKafkaSslCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialKafkaSslCredentialConfig(BaseModel):
    bootstrap_servers: List[str] = Field(alias="bootstrapServers")
    ca_certificate: str = Field(alias="caCertificate")


class CredentialUpdateCredentialLookerCredential(BaseModel):
    typename__: Literal["LookerCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialLookerCredentialNamespace"
    config: "CredentialUpdateCredentialLookerCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialLookerCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialLookerCredentialConfig(BaseModel):
    base_url: str = Field(alias="baseUrl")
    client_id: str = Field(alias="clientId")


class CredentialUpdateCredentialPostgreSqlCredential(BaseModel):
    typename__: Literal["PostgreSqlCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialPostgreSqlCredentialNamespace"
    config: "CredentialUpdateCredentialPostgreSqlCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialPostgreSqlCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialPostgreSqlCredentialConfig(BaseModel):
    host: str
    port: int
    user: str
    default_database: str = Field(alias="defaultDatabase")


class CredentialUpdateCredentialSnowflakeCredential(BaseModel):
    typename__: Literal["SnowflakeCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialSnowflakeCredentialNamespace"
    config: "CredentialUpdateCredentialSnowflakeCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialSnowflakeCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialSnowflakeCredentialConfig(BaseModel):
    account: str
    user: str
    role: Optional[str]
    warehouse: Optional[str]
    auth: Optional[
        Annotated[
            Union[
                "CredentialUpdateCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair",
                "CredentialUpdateCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class CredentialUpdateCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialKeyPair(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialKeyPair"] = Field(alias="__typename")
    user: str


class CredentialUpdateCredentialSnowflakeCredentialConfigAuthSnowflakeCredentialUserPassword(
    BaseModel
):
    typename__: Literal["SnowflakeCredentialUserPassword"] = Field(alias="__typename")
    user: str


class CredentialUpdateCredentialTableauConnectedAppCredential(BaseModel):
    typename__: Literal["TableauConnectedAppCredential"] = Field(alias="__typename")
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialTableauConnectedAppCredentialNamespace"
    config: "CredentialUpdateCredentialTableauConnectedAppCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialTableauConnectedAppCredentialNamespace(BaseModel):
    id: Any


class CredentialUpdateCredentialTableauConnectedAppCredentialConfig(BaseModel):
    host: str
    site: Optional[str]
    user: str
    client_id: str = Field(alias="clientId")
    secret_id: str = Field(alias="secretId")


class CredentialUpdateCredentialTableauPersonalAccessTokenCredential(BaseModel):
    typename__: Literal["TableauPersonalAccessTokenCredential"] = Field(
        alias="__typename"
    )
    id: CredentialId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "CredentialUpdateCredentialTableauPersonalAccessTokenCredentialNamespace"
    config: "CredentialUpdateCredentialTableauPersonalAccessTokenCredentialConfig"
    enable_catalog: bool = Field(alias="enableCatalog")


class CredentialUpdateCredentialTableauPersonalAccessTokenCredentialNamespace(
    BaseModel
):
    id: Any


class CredentialUpdateCredentialTableauPersonalAccessTokenCredentialConfig(BaseModel):
    host: str
    site: Optional[str]
    token_name: str = Field(alias="tokenName")


class IdentityDeletion(BaseModel):
    errors: List["IdentityDeletionErrors"]


class IdentityDeletionErrors(BaseModel):
    code: IdentityDeleteErrorCode
    message: str


class IdentityProviderCreation(BaseModel):
    errors: List["IdentityProviderCreationErrors"]
    identity_provider: Optional[
        Annotated[
            Union[
                "IdentityProviderCreationIdentityProviderIdentityProvider",
                "IdentityProviderCreationIdentityProviderSamlIdentityProvider",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="identityProvider")


class IdentityProviderCreationErrors(BaseModel):
    code: IdentityProviderCreateErrorCode
    message: Optional[str]


class IdentityProviderCreationIdentityProviderIdentityProvider(BaseModel):
    typename__: Literal["IdentityProvider", "LocalIdentityProvider"] = Field(
        alias="__typename"
    )
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")


class IdentityProviderCreationIdentityProviderSamlIdentityProvider(BaseModel):
    typename__: Literal["SamlIdentityProvider"] = Field(alias="__typename")
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    config: "IdentityProviderCreationIdentityProviderSamlIdentityProviderConfig"


class IdentityProviderCreationIdentityProviderSamlIdentityProviderConfig(BaseModel):
    entry_point: str = Field(alias="entryPoint")
    entity_id: str = Field(alias="entityId")
    cert: str


class IdentityProviderDeletion(BaseModel):
    errors: List["IdentityProviderDeletionErrors"]


class IdentityProviderDeletionErrors(BaseModel):
    code: IdentityProviderDeleteErrorCode
    message: Optional[str]


class IdentityProviderUpdate(BaseModel):
    errors: List["IdentityProviderUpdateErrors"]
    identity_provider: Optional[
        Annotated[
            Union[
                "IdentityProviderUpdateIdentityProviderIdentityProvider",
                "IdentityProviderUpdateIdentityProviderSamlIdentityProvider",
            ],
            Field(discriminator="typename__"),
        ]
    ] = Field(alias="identityProvider")


class IdentityProviderUpdateErrors(BaseModel):
    code: IdentityProviderUpdateErrorCode
    message: Optional[str]


class IdentityProviderUpdateIdentityProviderIdentityProvider(BaseModel):
    typename__: Literal["IdentityProvider", "LocalIdentityProvider"] = Field(
        alias="__typename"
    )
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")


class IdentityProviderUpdateIdentityProviderSamlIdentityProvider(BaseModel):
    typename__: Literal["SamlIdentityProvider"] = Field(alias="__typename")
    id: str
    name: str
    disabled: bool
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    config: "IdentityProviderUpdateIdentityProviderSamlIdentityProviderConfig"


class IdentityProviderUpdateIdentityProviderSamlIdentityProviderConfig(BaseModel):
    entry_point: str = Field(alias="entryPoint")
    entity_id: str = Field(alias="entityId")
    cert: str


class LineageEdgeDetails(BaseModel):
    typename__: str = Field(alias="__typename")
    id: Any
    upstream: "LineageEdgeDetailsUpstream"
    downstream: "LineageEdgeDetailsDownstream"
    sql_query: Optional[str] = Field(alias="sqlQuery")


class LineageEdgeDetailsUpstream(BaseModel):
    catalog_asset: "LineageEdgeDetailsUpstreamCatalogAsset" = Field(
        alias="catalogAsset"
    )
    field: Optional[JsonPointer]


class LineageEdgeDetailsUpstreamCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    name: str


class LineageEdgeDetailsDownstream(BaseModel):
    catalog_asset: "LineageEdgeDetailsDownstreamCatalogAsset" = Field(
        alias="catalogAsset"
    )
    field: Optional[JsonPointer]


class LineageEdgeDetailsDownstreamCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    name: str


class LineageEdgeCreation(BaseModel):
    errors: List["LineageEdgeCreationErrors"]
    edge: Optional["LineageEdgeCreationEdge"]


class LineageEdgeCreationErrors(ErrorDetails):
    pass


class LineageEdgeCreationEdge(LineageEdgeDetails):
    pass


class LineageEdgeSummary(BaseModel):
    id: Any
    upstream: "LineageEdgeSummaryUpstream"
    downstream: "LineageEdgeSummaryDownstream"


class LineageEdgeSummaryUpstream(BaseModel):
    catalog_asset: "LineageEdgeSummaryUpstreamCatalogAsset" = Field(
        alias="catalogAsset"
    )
    field: Optional[JsonPointer]


class LineageEdgeSummaryUpstreamCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any


class LineageEdgeSummaryDownstream(BaseModel):
    catalog_asset: "LineageEdgeSummaryDownstreamCatalogAsset" = Field(
        alias="catalogAsset"
    )
    field: Optional[JsonPointer]


class LineageEdgeSummaryDownstreamCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any


class LineageGraphDetails(BaseModel):
    nodes: List[
        Annotated[
            Union[
                "LineageGraphDetailsNodesCatalogAsset",
                "LineageGraphDetailsNodesDbtModelCatalogAsset",
                "LineageGraphDetailsNodesSourcesCatalogAsset",
            ],
            Field(discriminator="typename__"),
        ]
    ]
    edges: List["LineageGraphDetailsEdges"]
    stats: "LineageGraphDetailsStats"


class LineageGraphDetailsNodesCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    name: str
    stats: Optional["LineageGraphDetailsNodesCatalogAssetStats"]


class LineageGraphDetailsNodesCatalogAssetStats(BaseModel):
    n_reads: Optional[int] = Field(alias="nReads")
    n_writes: Optional[int] = Field(alias="nWrites")
    utilization: Optional[float]


class LineageGraphDetailsNodesDbtModelCatalogAsset(BaseModel):
    typename__: Literal["DbtModelCatalogAsset"] = Field(alias="__typename")


class LineageGraphDetailsNodesSourcesCatalogAsset(BaseModel):
    typename__: Literal["SourcesCatalogAsset"] = Field(alias="__typename")


class LineageGraphDetailsEdges(LineageEdgeSummary):
    pass


class LineageGraphDetailsStats(BaseModel):
    total_asset_count: int = Field(alias="totalAssetCount")
    total_edge_count: int = Field(alias="totalEdgeCount")
    total_source_count: int = Field(alias="totalSourceCount")


class UserSummary(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")
    full_name: Optional[str] = Field(alias="fullName")
    email: Optional[str]
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")
    status: UserStatus
    global_role: Role = Field(alias="globalRole")
    login_type: LoginType = Field(alias="loginType")


class TeamDetails(BaseModel):
    id: Any
    name: str
    description: Optional[str]
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")
    avatar: Any
    members: List["TeamDetailsMembers"]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class TeamDetailsMembers(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")
    status: UserStatus
    email: Optional[str]
    last_login_at: Optional[datetime] = Field(alias="lastLoginAt")


class NamespaceDetails(BaseModel):
    id: Any
    name: str
    description: Optional[str]
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")
    members: List["NamespaceDetailsMembers"]
    teams: List["NamespaceDetailsTeams"]
    api_keys: List["NamespaceDetailsApiKeys"] = Field(alias="apiKeys")
    users: List["NamespaceDetailsUsers"]


class NamespaceDetailsMembers(BaseModel):
    role: Role
    user: "NamespaceDetailsMembersUser"


class NamespaceDetailsMembersUser(UserSummary):
    pass


class NamespaceDetailsTeams(BaseModel):
    role: Role
    team: "NamespaceDetailsTeamsTeam"


class NamespaceDetailsTeamsTeam(TeamDetails):
    pass


class NamespaceDetailsApiKeys(BaseModel):
    role: Role
    api_key: "NamespaceDetailsApiKeysApiKey" = Field(alias="apiKey")


class NamespaceDetailsApiKeysApiKey(ApiKeyDetails):
    pass


class NamespaceDetailsUsers(BaseModel):
    role: Role
    user: "NamespaceDetailsUsersUser"


class NamespaceDetailsUsersUser(UserSummary):
    pass


class NamespaceDetailsWithFullAvatar(BaseModel):
    id: Any
    name: str
    description: Optional[str]
    avatar: Any
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")
    members: List["NamespaceDetailsWithFullAvatarMembers"]
    teams: List["NamespaceDetailsWithFullAvatarTeams"]
    api_keys: List["NamespaceDetailsWithFullAvatarApiKeys"] = Field(alias="apiKeys")
    users: List["NamespaceDetailsWithFullAvatarUsers"]


class NamespaceDetailsWithFullAvatarMembers(BaseModel):
    role: Role
    user: "NamespaceDetailsWithFullAvatarMembersUser"


class NamespaceDetailsWithFullAvatarMembersUser(UserSummary):
    pass


class NamespaceDetailsWithFullAvatarTeams(BaseModel):
    role: Role
    team: "NamespaceDetailsWithFullAvatarTeamsTeam"


class NamespaceDetailsWithFullAvatarTeamsTeam(TeamDetails):
    pass


class NamespaceDetailsWithFullAvatarApiKeys(BaseModel):
    role: Role
    api_key: "NamespaceDetailsWithFullAvatarApiKeysApiKey" = Field(alias="apiKey")


class NamespaceDetailsWithFullAvatarApiKeysApiKey(ApiKeyDetails):
    pass


class NamespaceDetailsWithFullAvatarUsers(BaseModel):
    role: Role
    user: "NamespaceDetailsWithFullAvatarUsersUser"


class NamespaceDetailsWithFullAvatarUsersUser(UserSummary):
    pass


class NamespaceUpdate(BaseModel):
    errors: List["NamespaceUpdateErrors"]
    resource_name: Optional[str] = Field(alias="resourceName")
    namespace_id: Optional[Any] = Field(alias="namespaceId")


class NamespaceUpdateErrors(ErrorDetails):
    pass


class NotificationRuleConditionCreation(BaseModel):
    errors: List["NotificationRuleConditionCreationErrors"]


class NotificationRuleConditionCreationErrors(BaseModel):
    code: ApiErrorCode
    message: str


class NotificationRuleDetails(BaseModel):
    typename__: str = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    conditions: List[
        Annotated[
            Union[
                "NotificationRuleDetailsConditionsNotificationRuleCondition",
                "NotificationRuleDetailsConditionsOwnerNotificationRuleCondition",
                "NotificationRuleDetailsConditionsSegmentNotificationRuleCondition",
                "NotificationRuleDetailsConditionsSeverityNotificationRuleCondition",
                "NotificationRuleDetailsConditionsSourceNotificationRuleCondition",
                "NotificationRuleDetailsConditionsTagNotificationRuleCondition",
                "NotificationRuleDetailsConditionsTypeNotificationRuleCondition",
            ],
            Field(discriminator="typename__"),
        ]
    ]
    channel: Union[
        "NotificationRuleDetailsChannelChannel",
        "NotificationRuleDetailsChannelMsTeamsChannel",
        "NotificationRuleDetailsChannelSlackChannel",
        "NotificationRuleDetailsChannelWebhookChannel",
    ] = Field(discriminator="typename__")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "NotificationRuleDetailsNamespace"


class NotificationRuleDetailsConditionsNotificationRuleCondition(BaseModel):
    typename__: Literal["NotificationRuleCondition"] = Field(alias="__typename")
    id: str
    notification_rule_id: Any = Field(alias="notificationRuleId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class NotificationRuleDetailsConditionsOwnerNotificationRuleCondition(BaseModel):
    typename__: Literal["OwnerNotificationRuleCondition"] = Field(alias="__typename")
    id: str
    notification_rule_id: Any = Field(alias="notificationRuleId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "NotificationRuleDetailsConditionsOwnerNotificationRuleConditionConfig"


class NotificationRuleDetailsConditionsOwnerNotificationRuleConditionConfig(BaseModel):
    owners: List[
        "NotificationRuleDetailsConditionsOwnerNotificationRuleConditionConfigOwners"
    ]


class NotificationRuleDetailsConditionsOwnerNotificationRuleConditionConfigOwners(
    BaseModel
):
    id: Any
    display_name: str = Field(alias="displayName")


class NotificationRuleDetailsConditionsSegmentNotificationRuleCondition(BaseModel):
    typename__: Literal["SegmentNotificationRuleCondition"] = Field(alias="__typename")
    id: str
    notification_rule_id: Any = Field(alias="notificationRuleId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "NotificationRuleDetailsConditionsSegmentNotificationRuleConditionConfig"


class NotificationRuleDetailsConditionsSegmentNotificationRuleConditionConfig(
    BaseModel
):
    segments: List[
        "NotificationRuleDetailsConditionsSegmentNotificationRuleConditionConfigSegments"
    ]


class NotificationRuleDetailsConditionsSegmentNotificationRuleConditionConfigSegments(
    BaseModel
):
    field: JsonPointer
    value: str


class NotificationRuleDetailsConditionsSeverityNotificationRuleCondition(BaseModel):
    typename__: Literal["SeverityNotificationRuleCondition"] = Field(alias="__typename")
    id: str
    notification_rule_id: Any = Field(alias="notificationRuleId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "NotificationRuleDetailsConditionsSeverityNotificationRuleConditionConfig"


class NotificationRuleDetailsConditionsSeverityNotificationRuleConditionConfig(
    BaseModel
):
    severities: List[IncidentSeverity]


class NotificationRuleDetailsConditionsSourceNotificationRuleCondition(BaseModel):
    typename__: Literal["SourceNotificationRuleCondition"] = Field(alias="__typename")
    id: str
    notification_rule_id: Any = Field(alias="notificationRuleId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "NotificationRuleDetailsConditionsSourceNotificationRuleConditionConfig"


class NotificationRuleDetailsConditionsSourceNotificationRuleConditionConfig(BaseModel):
    sources: List[
        Optional[
            "NotificationRuleDetailsConditionsSourceNotificationRuleConditionConfigSources"
        ]
    ]


class NotificationRuleDetailsConditionsSourceNotificationRuleConditionConfigSources(
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


class NotificationRuleDetailsConditionsTagNotificationRuleCondition(BaseModel):
    typename__: Literal["TagNotificationRuleCondition"] = Field(alias="__typename")
    id: str
    notification_rule_id: Any = Field(alias="notificationRuleId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "NotificationRuleDetailsConditionsTagNotificationRuleConditionConfig"


class NotificationRuleDetailsConditionsTagNotificationRuleConditionConfig(BaseModel):
    tags: List[
        "NotificationRuleDetailsConditionsTagNotificationRuleConditionConfigTags"
    ]


class NotificationRuleDetailsConditionsTagNotificationRuleConditionConfigTags(
    BaseModel
):
    id: Any
    key: str
    value: str


class NotificationRuleDetailsConditionsTypeNotificationRuleCondition(BaseModel):
    typename__: Literal["TypeNotificationRuleCondition"] = Field(alias="__typename")
    id: str
    notification_rule_id: Any = Field(alias="notificationRuleId")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    config: "NotificationRuleDetailsConditionsTypeNotificationRuleConditionConfig"


class NotificationRuleDetailsConditionsTypeNotificationRuleConditionConfig(BaseModel):
    types: List[IssueTypename]


class NotificationRuleDetailsChannelChannel(BaseModel):
    typename__: Literal["Channel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "NotificationRuleDetailsChannelChannelNamespace"
    notification_rules: List[
        "NotificationRuleDetailsChannelChannelNotificationRules"
    ] = Field(alias="notificationRules")


class NotificationRuleDetailsChannelChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class NotificationRuleDetailsChannelChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class NotificationRuleDetailsChannelMsTeamsChannel(BaseModel):
    typename__: Literal["MsTeamsChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "NotificationRuleDetailsChannelMsTeamsChannelNamespace"
    notification_rules: List[
        "NotificationRuleDetailsChannelMsTeamsChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "NotificationRuleDetailsChannelMsTeamsChannelConfig"


class NotificationRuleDetailsChannelMsTeamsChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class NotificationRuleDetailsChannelMsTeamsChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class NotificationRuleDetailsChannelMsTeamsChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class NotificationRuleDetailsChannelSlackChannel(BaseModel):
    typename__: Literal["SlackChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "NotificationRuleDetailsChannelSlackChannelNamespace"
    notification_rules: List[
        "NotificationRuleDetailsChannelSlackChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "NotificationRuleDetailsChannelSlackChannelConfig"


class NotificationRuleDetailsChannelSlackChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class NotificationRuleDetailsChannelSlackChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class NotificationRuleDetailsChannelSlackChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    timezone: Optional[str]
    application_link_url: str = Field(alias="applicationLinkUrl")


class NotificationRuleDetailsChannelWebhookChannel(BaseModel):
    typename__: Literal["WebhookChannel"] = Field(alias="__typename")
    id: Any
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "NotificationRuleDetailsChannelWebhookChannelNamespace"
    notification_rules: List[
        "NotificationRuleDetailsChannelWebhookChannelNotificationRules"
    ] = Field(alias="notificationRules")
    config: "NotificationRuleDetailsChannelWebhookChannelConfig"


class NotificationRuleDetailsChannelWebhookChannelNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class NotificationRuleDetailsChannelWebhookChannelNotificationRules(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class NotificationRuleDetailsChannelWebhookChannelConfig(BaseModel):
    webhook_url: str = Field(alias="webhookUrl")
    application_link_url: str = Field(alias="applicationLinkUrl")
    auth_header: Optional[str] = Field(alias="authHeader")


class NotificationRuleDetailsNamespace(BaseModel):
    id: Any
    name: str
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class NotificationRuleCreation(BaseModel):
    errors: List["NotificationRuleCreationErrors"]
    notification_rule: Optional["NotificationRuleCreationNotificationRule"] = Field(
        alias="notificationRule"
    )


class NotificationRuleCreationErrors(BaseModel):
    code: ApiErrorCode
    message: str


class NotificationRuleCreationNotificationRule(NotificationRuleDetails):
    pass


class NotificationRuleDeletion(BaseModel):
    errors: List["NotificationRuleDeletionErrors"]
    notification_rule: Optional["NotificationRuleDeletionNotificationRule"] = Field(
        alias="notificationRule"
    )


class NotificationRuleDeletionErrors(BaseModel):
    code: ApiErrorCode
    message: str


class NotificationRuleDeletionNotificationRule(BaseModel):
    typename__: Literal["NotificationRule"] = Field(alias="__typename")
    id: Any
    name: str


class NotificationRuleUpdate(BaseModel):
    errors: List["NotificationRuleUpdateErrors"]
    notification_rule: Optional["NotificationRuleUpdateNotificationRule"] = Field(
        alias="notificationRule"
    )


class NotificationRuleUpdateErrors(BaseModel):
    code: ApiErrorCode
    message: str


class NotificationRuleUpdateNotificationRule(NotificationRuleDetails):
    pass


class ReferenceSourceConfigDetails(BaseModel):
    source: "ReferenceSourceConfigDetailsSource"
    window: "ReferenceSourceConfigDetailsWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ReferenceSourceConfigDetailsSource(BaseModel):
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
    namespace: "ReferenceSourceConfigDetailsSourceNamespace"


class ReferenceSourceConfigDetailsSourceNamespace(BaseModel):
    id: Any


class ReferenceSourceConfigDetailsWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ReferenceSourceConfigDetailsWindowNamespace"


class ReferenceSourceConfigDetailsWindowNamespace(BaseModel):
    id: Any


class SegmentDetails(BaseModel):
    typename__: str = Field(alias="__typename")
    id: Any
    muted: bool
    fields: List["SegmentDetailsFields"]
    data_quality: Optional["SegmentDetailsDataQuality"] = Field(alias="dataQuality")


class SegmentDetailsFields(BaseModel):
    field: JsonPointer
    value: str


class SegmentDetailsDataQuality(BaseModel):
    incident_count: int = Field(alias="incidentCount")
    total_count: int = Field(alias="totalCount")
    quality: float
    quality_diff: float = Field(alias="qualityDiff")


class SegmentationDetails(BaseModel):
    typename__: str = Field(alias="__typename")
    id: SegmentationId
    name: str
    source: "SegmentationDetailsSource"
    fields: List[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SegmentationDetailsNamespace"


class SegmentationDetailsSource(BaseModel):
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
    namespace: "SegmentationDetailsSourceNamespace"


class SegmentationDetailsSourceNamespace(BaseModel):
    id: Any


class SegmentationDetailsNamespace(BaseModel):
    id: Any


class SegmentationCreation(BaseModel):
    errors: List["SegmentationCreationErrors"]
    segmentation: Optional["SegmentationCreationSegmentation"]


class SegmentationCreationErrors(ErrorDetails):
    pass


class SegmentationCreationSegmentation(SegmentationDetails):
    pass


class SegmentationSummary(BaseModel):
    typename__: str = Field(alias="__typename")
    id: SegmentationId
    name: str
    fields: List[str]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class SourceBase(BaseModel):
    id: SourceId
    typename__: str = Field(alias="__typename")
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace: "SourceBaseNamespace"


class SourceBaseNamespace(BaseModel):
    id: Any


class SourceCreation(BaseModel):
    errors: List["SourceCreationErrors"]
    source: Optional[
        Annotated[
            Union[
                "SourceCreationSourceSource",
                "SourceCreationSourceAwsAthenaSource",
                "SourceCreationSourceAwsKinesisSource",
                "SourceCreationSourceAwsRedshiftSource",
                "SourceCreationSourceAwsS3Source",
                "SourceCreationSourceAzureSynapseSource",
                "SourceCreationSourceClickHouseSource",
                "SourceCreationSourceDatabricksSource",
                "SourceCreationSourceDbtModelRunSource",
                "SourceCreationSourceDbtTestResultSource",
                "SourceCreationSourceGcpBigQuerySource",
                "SourceCreationSourceGcpPubSubLiteSource",
                "SourceCreationSourceGcpPubSubSource",
                "SourceCreationSourceGcpStorageSource",
                "SourceCreationSourceKafkaSource",
                "SourceCreationSourcePostgreSqlSource",
                "SourceCreationSourceSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class SourceCreationErrors(ErrorDetails):
    pass


class SourceCreationSourceSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceSourceCredential"
    windows: List["SourceCreationSourceSourceWindows"]
    segmentations: List["SourceCreationSourceSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSourceNamespace"
    tags: List["SourceCreationSourceSourceTags"]


class SourceCreationSourceSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSourceCredentialNamespace"


class SourceCreationSourceSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSourceWindowsNamespace"


class SourceCreationSourceSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSourceSegmentationsNamespace"


class SourceCreationSourceSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceAwsAthenaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceAwsAthenaSourceCredential"
    windows: List["SourceCreationSourceAwsAthenaSourceWindows"]
    segmentations: List["SourceCreationSourceAwsAthenaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsAthenaSourceNamespace"
    tags: List["SourceCreationSourceAwsAthenaSourceTags"]
    config: "SourceCreationSourceAwsAthenaSourceConfig"


class SourceCreationSourceAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceAwsAthenaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsAthenaSourceCredentialNamespace"


class SourceCreationSourceAwsAthenaSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsAthenaSourceWindowsNamespace"


class SourceCreationSourceAwsAthenaSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsAthenaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsAthenaSourceSegmentationsNamespace"


class SourceCreationSourceAwsAthenaSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsAthenaSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsAthenaSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceCreationSourceAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceAwsKinesisSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceAwsKinesisSourceCredential"
    windows: List["SourceCreationSourceAwsKinesisSourceWindows"]
    segmentations: List["SourceCreationSourceAwsKinesisSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsKinesisSourceNamespace"
    tags: List["SourceCreationSourceAwsKinesisSourceTags"]
    config: "SourceCreationSourceAwsKinesisSourceConfig"


class SourceCreationSourceAwsKinesisSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceAwsKinesisSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsKinesisSourceCredentialNamespace"


class SourceCreationSourceAwsKinesisSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsKinesisSourceWindowsNamespace"


class SourceCreationSourceAwsKinesisSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsKinesisSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsKinesisSourceSegmentationsNamespace"


class SourceCreationSourceAwsKinesisSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsKinesisSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsKinesisSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "SourceCreationSourceAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class SourceCreationSourceAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceCreationSourceAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceAwsRedshiftSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceCreationSourceAwsRedshiftSourceCredential"
    windows: List["SourceCreationSourceAwsRedshiftSourceWindows"]
    segmentations: List["SourceCreationSourceAwsRedshiftSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsRedshiftSourceNamespace"
    tags: List["SourceCreationSourceAwsRedshiftSourceTags"]
    config: "SourceCreationSourceAwsRedshiftSourceConfig"


class SourceCreationSourceAwsRedshiftSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceAwsRedshiftSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsRedshiftSourceCredentialNamespace"


class SourceCreationSourceAwsRedshiftSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsRedshiftSourceWindowsNamespace"


class SourceCreationSourceAwsRedshiftSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsRedshiftSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsRedshiftSourceSegmentationsNamespace"


class SourceCreationSourceAwsRedshiftSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsRedshiftSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsRedshiftSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceCreationSourceAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceAwsS3SourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceAwsS3SourceCredential"
    windows: List["SourceCreationSourceAwsS3SourceWindows"]
    segmentations: List["SourceCreationSourceAwsS3SourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsS3SourceNamespace"
    tags: List["SourceCreationSourceAwsS3SourceTags"]
    config: "SourceCreationSourceAwsS3SourceConfig"


class SourceCreationSourceAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceAwsS3SourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsS3SourceCredentialNamespace"


class SourceCreationSourceAwsS3SourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsS3SourceWindowsNamespace"


class SourceCreationSourceAwsS3SourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAwsS3SourceSegmentationsNamespace"


class SourceCreationSourceAwsS3SourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsS3SourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceAwsS3SourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["SourceCreationSourceAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class SourceCreationSourceAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class SourceCreationSourceAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceAzureSynapseSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceCreationSourceAzureSynapseSourceCredential"
    windows: List["SourceCreationSourceAzureSynapseSourceWindows"]
    segmentations: List["SourceCreationSourceAzureSynapseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAzureSynapseSourceNamespace"
    tags: List["SourceCreationSourceAzureSynapseSourceTags"]
    config: "SourceCreationSourceAzureSynapseSourceConfig"


class SourceCreationSourceAzureSynapseSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceAzureSynapseSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAzureSynapseSourceCredentialNamespace"


class SourceCreationSourceAzureSynapseSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAzureSynapseSourceWindowsNamespace"


class SourceCreationSourceAzureSynapseSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAzureSynapseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceAzureSynapseSourceSegmentationsNamespace"


class SourceCreationSourceAzureSynapseSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceAzureSynapseSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceAzureSynapseSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceCreationSourceClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceClickHouseSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceClickHouseSourceCredential"
    windows: List["SourceCreationSourceClickHouseSourceWindows"]
    segmentations: List["SourceCreationSourceClickHouseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceClickHouseSourceNamespace"
    tags: List["SourceCreationSourceClickHouseSourceTags"]
    config: "SourceCreationSourceClickHouseSourceConfig"


class SourceCreationSourceClickHouseSourceCatalogAsset(BaseModel):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceClickHouseSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceClickHouseSourceCredentialNamespace"


class SourceCreationSourceClickHouseSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceClickHouseSourceWindowsNamespace"


class SourceCreationSourceClickHouseSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceClickHouseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceClickHouseSourceSegmentationsNamespace"


class SourceCreationSourceClickHouseSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceClickHouseSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceClickHouseSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceCreationSourceDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceDatabricksSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceDatabricksSourceCredential"
    windows: List["SourceCreationSourceDatabricksSourceWindows"]
    segmentations: List["SourceCreationSourceDatabricksSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDatabricksSourceNamespace"
    tags: List["SourceCreationSourceDatabricksSourceTags"]
    config: "SourceCreationSourceDatabricksSourceConfig"


class SourceCreationSourceDatabricksSourceCatalogAsset(BaseModel):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceDatabricksSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDatabricksSourceCredentialNamespace"


class SourceCreationSourceDatabricksSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDatabricksSourceWindowsNamespace"


class SourceCreationSourceDatabricksSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceDatabricksSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDatabricksSourceSegmentationsNamespace"


class SourceCreationSourceDatabricksSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceDatabricksSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceDatabricksSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class SourceCreationSourceDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceDbtModelRunSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceCreationSourceDbtModelRunSourceCredential"
    windows: List["SourceCreationSourceDbtModelRunSourceWindows"]
    segmentations: List["SourceCreationSourceDbtModelRunSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtModelRunSourceNamespace"
    tags: List["SourceCreationSourceDbtModelRunSourceTags"]
    config: "SourceCreationSourceDbtModelRunSourceConfig"


class SourceCreationSourceDbtModelRunSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceDbtModelRunSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtModelRunSourceCredentialNamespace"


class SourceCreationSourceDbtModelRunSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtModelRunSourceWindowsNamespace"


class SourceCreationSourceDbtModelRunSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtModelRunSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtModelRunSourceSegmentationsNamespace"


class SourceCreationSourceDbtModelRunSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtModelRunSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtModelRunSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class SourceCreationSourceDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceDbtTestResultSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceCreationSourceDbtTestResultSourceCredential"
    windows: List["SourceCreationSourceDbtTestResultSourceWindows"]
    segmentations: List["SourceCreationSourceDbtTestResultSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtTestResultSourceNamespace"
    tags: List["SourceCreationSourceDbtTestResultSourceTags"]
    config: "SourceCreationSourceDbtTestResultSourceConfig"


class SourceCreationSourceDbtTestResultSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceDbtTestResultSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtTestResultSourceCredentialNamespace"


class SourceCreationSourceDbtTestResultSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtTestResultSourceWindowsNamespace"


class SourceCreationSourceDbtTestResultSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtTestResultSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceDbtTestResultSourceSegmentationsNamespace"


class SourceCreationSourceDbtTestResultSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtTestResultSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceDbtTestResultSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class SourceCreationSourceGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceGcpBigQuerySourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceCreationSourceGcpBigQuerySourceCredential"
    windows: List["SourceCreationSourceGcpBigQuerySourceWindows"]
    segmentations: List["SourceCreationSourceGcpBigQuerySourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpBigQuerySourceNamespace"
    tags: List["SourceCreationSourceGcpBigQuerySourceTags"]
    config: "SourceCreationSourceGcpBigQuerySourceConfig"


class SourceCreationSourceGcpBigQuerySourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceGcpBigQuerySourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpBigQuerySourceCredentialNamespace"


class SourceCreationSourceGcpBigQuerySourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpBigQuerySourceWindowsNamespace"


class SourceCreationSourceGcpBigQuerySourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpBigQuerySourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpBigQuerySourceSegmentationsNamespace"


class SourceCreationSourceGcpBigQuerySourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpBigQuerySourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpBigQuerySourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceCreationSourceGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceGcpPubSubLiteSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceCreationSourceGcpPubSubLiteSourceCredential"
    windows: List["SourceCreationSourceGcpPubSubLiteSourceWindows"]
    segmentations: List["SourceCreationSourceGcpPubSubLiteSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubLiteSourceNamespace"
    tags: List["SourceCreationSourceGcpPubSubLiteSourceTags"]
    config: "SourceCreationSourceGcpPubSubLiteSourceConfig"


class SourceCreationSourceGcpPubSubLiteSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceGcpPubSubLiteSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubLiteSourceCredentialNamespace"


class SourceCreationSourceGcpPubSubLiteSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubLiteSourceWindowsNamespace"


class SourceCreationSourceGcpPubSubLiteSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubLiteSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubLiteSourceSegmentationsNamespace"


class SourceCreationSourceGcpPubSubLiteSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubLiteSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "SourceCreationSourceGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class SourceCreationSourceGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceCreationSourceGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceGcpPubSubSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceGcpPubSubSourceCredential"
    windows: List["SourceCreationSourceGcpPubSubSourceWindows"]
    segmentations: List["SourceCreationSourceGcpPubSubSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubSourceNamespace"
    tags: List["SourceCreationSourceGcpPubSubSourceTags"]
    config: "SourceCreationSourceGcpPubSubSourceConfig"


class SourceCreationSourceGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceGcpPubSubSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubSourceCredentialNamespace"


class SourceCreationSourceGcpPubSubSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubSourceWindowsNamespace"


class SourceCreationSourceGcpPubSubSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpPubSubSourceSegmentationsNamespace"


class SourceCreationSourceGcpPubSubSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpPubSubSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "SourceCreationSourceGcpPubSubSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class SourceCreationSourceGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceCreationSourceGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceGcpStorageSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceGcpStorageSourceCredential"
    windows: List["SourceCreationSourceGcpStorageSourceWindows"]
    segmentations: List["SourceCreationSourceGcpStorageSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpStorageSourceNamespace"
    tags: List["SourceCreationSourceGcpStorageSourceTags"]
    config: "SourceCreationSourceGcpStorageSourceConfig"


class SourceCreationSourceGcpStorageSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceGcpStorageSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpStorageSourceCredentialNamespace"


class SourceCreationSourceGcpStorageSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpStorageSourceWindowsNamespace"


class SourceCreationSourceGcpStorageSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpStorageSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceGcpStorageSourceSegmentationsNamespace"


class SourceCreationSourceGcpStorageSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpStorageSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceGcpStorageSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["SourceCreationSourceGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class SourceCreationSourceGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class SourceCreationSourceKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceKafkaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceKafkaSourceCredential"
    windows: List["SourceCreationSourceKafkaSourceWindows"]
    segmentations: List["SourceCreationSourceKafkaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceKafkaSourceNamespace"
    tags: List["SourceCreationSourceKafkaSourceTags"]
    config: "SourceCreationSourceKafkaSourceConfig"


class SourceCreationSourceKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceKafkaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceKafkaSourceCredentialNamespace"


class SourceCreationSourceKafkaSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceKafkaSourceWindowsNamespace"


class SourceCreationSourceKafkaSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceKafkaSourceSegmentationsNamespace"


class SourceCreationSourceKafkaSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceKafkaSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceKafkaSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional["SourceCreationSourceKafkaSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class SourceCreationSourceKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceCreationSourcePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourcePostgreSqlSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourcePostgreSqlSourceCredential"
    windows: List["SourceCreationSourcePostgreSqlSourceWindows"]
    segmentations: List["SourceCreationSourcePostgreSqlSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourcePostgreSqlSourceNamespace"
    tags: List["SourceCreationSourcePostgreSqlSourceTags"]
    config: "SourceCreationSourcePostgreSqlSourceConfig"


class SourceCreationSourcePostgreSqlSourceCatalogAsset(BaseModel):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourcePostgreSqlSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourcePostgreSqlSourceCredentialNamespace"


class SourceCreationSourcePostgreSqlSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourcePostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourcePostgreSqlSourceWindowsNamespace"


class SourceCreationSourcePostgreSqlSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourcePostgreSqlSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourcePostgreSqlSourceSegmentationsNamespace"


class SourceCreationSourcePostgreSqlSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourcePostgreSqlSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourcePostgreSqlSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourcePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceCreationSourceSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceCreationSourceSnowflakeSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceCreationSourceSnowflakeSourceCredential"
    windows: List["SourceCreationSourceSnowflakeSourceWindows"]
    segmentations: List["SourceCreationSourceSnowflakeSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSnowflakeSourceNamespace"
    tags: List["SourceCreationSourceSnowflakeSourceTags"]
    config: "SourceCreationSourceSnowflakeSourceConfig"


class SourceCreationSourceSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceCreationSourceSnowflakeSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSnowflakeSourceCredentialNamespace"


class SourceCreationSourceSnowflakeSourceCredentialNamespace(BaseModel):
    id: Any


class SourceCreationSourceSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSnowflakeSourceWindowsNamespace"


class SourceCreationSourceSnowflakeSourceWindowsNamespace(BaseModel):
    id: Any


class SourceCreationSourceSnowflakeSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceCreationSourceSnowflakeSourceSegmentationsNamespace"


class SourceCreationSourceSnowflakeSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceCreationSourceSnowflakeSourceNamespace(BaseModel):
    id: Any


class SourceCreationSourceSnowflakeSourceTags(BaseModel):
    key: str
    value: str


class SourceCreationSourceSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceUpdate(BaseModel):
    errors: List["SourceUpdateErrors"]
    source: Optional[
        Annotated[
            Union[
                "SourceUpdateSourceSource",
                "SourceUpdateSourceAwsAthenaSource",
                "SourceUpdateSourceAwsKinesisSource",
                "SourceUpdateSourceAwsRedshiftSource",
                "SourceUpdateSourceAwsS3Source",
                "SourceUpdateSourceAzureSynapseSource",
                "SourceUpdateSourceClickHouseSource",
                "SourceUpdateSourceDatabricksSource",
                "SourceUpdateSourceDbtModelRunSource",
                "SourceUpdateSourceDbtTestResultSource",
                "SourceUpdateSourceGcpBigQuerySource",
                "SourceUpdateSourceGcpPubSubLiteSource",
                "SourceUpdateSourceGcpPubSubSource",
                "SourceUpdateSourceGcpStorageSource",
                "SourceUpdateSourceKafkaSource",
                "SourceUpdateSourcePostgreSqlSource",
                "SourceUpdateSourceSnowflakeSource",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class SourceUpdateErrors(ErrorDetails):
    pass


class SourceUpdateSourceSource(BaseModel):
    typename__: Literal["DemoSource", "Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceSourceCredential"
    windows: List["SourceUpdateSourceSourceWindows"]
    segmentations: List["SourceUpdateSourceSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSourceNamespace"
    tags: List["SourceUpdateSourceSourceTags"]


class SourceUpdateSourceSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSourceCredentialNamespace"


class SourceUpdateSourceSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSourceWindowsNamespace"


class SourceUpdateSourceSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSourceSegmentationsNamespace"


class SourceUpdateSourceSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceAwsAthenaSource(BaseModel):
    typename__: Literal["AwsAthenaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceAwsAthenaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceAwsAthenaSourceCredential"
    windows: List["SourceUpdateSourceAwsAthenaSourceWindows"]
    segmentations: List["SourceUpdateSourceAwsAthenaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsAthenaSourceNamespace"
    tags: List["SourceUpdateSourceAwsAthenaSourceTags"]
    config: "SourceUpdateSourceAwsAthenaSourceConfig"


class SourceUpdateSourceAwsAthenaSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsAthenaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceAwsAthenaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsAthenaSourceCredentialNamespace"


class SourceUpdateSourceAwsAthenaSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsAthenaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsAthenaSourceWindowsNamespace"


class SourceUpdateSourceAwsAthenaSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsAthenaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsAthenaSourceSegmentationsNamespace"


class SourceUpdateSourceAwsAthenaSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsAthenaSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsAthenaSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceAwsAthenaSourceConfig(BaseModel):
    catalog: str
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceUpdateSourceAwsKinesisSource(BaseModel):
    typename__: Literal["AwsKinesisSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceAwsKinesisSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceAwsKinesisSourceCredential"
    windows: List["SourceUpdateSourceAwsKinesisSourceWindows"]
    segmentations: List["SourceUpdateSourceAwsKinesisSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsKinesisSourceNamespace"
    tags: List["SourceUpdateSourceAwsKinesisSourceTags"]
    config: "SourceUpdateSourceAwsKinesisSourceConfig"


class SourceUpdateSourceAwsKinesisSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsKinesisCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceAwsKinesisSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsKinesisSourceCredentialNamespace"


class SourceUpdateSourceAwsKinesisSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsKinesisSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsKinesisSourceWindowsNamespace"


class SourceUpdateSourceAwsKinesisSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsKinesisSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsKinesisSourceSegmentationsNamespace"


class SourceUpdateSourceAwsKinesisSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsKinesisSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsKinesisSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceAwsKinesisSourceConfig(BaseModel):
    region: str
    stream_name: str = Field(alias="streamName")
    message_format: Optional[
        "SourceUpdateSourceAwsKinesisSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class SourceUpdateSourceAwsKinesisSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceUpdateSourceAwsRedshiftSource(BaseModel):
    typename__: Literal["AwsRedshiftSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceAwsRedshiftSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceAwsRedshiftSourceCredential"
    windows: List["SourceUpdateSourceAwsRedshiftSourceWindows"]
    segmentations: List["SourceUpdateSourceAwsRedshiftSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsRedshiftSourceNamespace"
    tags: List["SourceUpdateSourceAwsRedshiftSourceTags"]
    config: "SourceUpdateSourceAwsRedshiftSourceConfig"


class SourceUpdateSourceAwsRedshiftSourceCatalogAsset(BaseModel):
    typename__: Literal["AwsRedshiftCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceAwsRedshiftSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsRedshiftSourceCredentialNamespace"


class SourceUpdateSourceAwsRedshiftSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsRedshiftSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsRedshiftSourceWindowsNamespace"


class SourceUpdateSourceAwsRedshiftSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsRedshiftSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsRedshiftSourceSegmentationsNamespace"


class SourceUpdateSourceAwsRedshiftSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsRedshiftSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsRedshiftSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceAwsRedshiftSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceUpdateSourceAwsS3Source(BaseModel):
    typename__: Literal["AwsS3Source"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceAwsS3SourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceAwsS3SourceCredential"
    windows: List["SourceUpdateSourceAwsS3SourceWindows"]
    segmentations: List["SourceUpdateSourceAwsS3SourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsS3SourceNamespace"
    tags: List["SourceUpdateSourceAwsS3SourceTags"]
    config: "SourceUpdateSourceAwsS3SourceConfig"


class SourceUpdateSourceAwsS3SourceCatalogAsset(BaseModel):
    typename__: Literal["AwsS3CatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceAwsS3SourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsS3SourceCredentialNamespace"


class SourceUpdateSourceAwsS3SourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsS3SourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsS3SourceWindowsNamespace"


class SourceUpdateSourceAwsS3SourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsS3SourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAwsS3SourceSegmentationsNamespace"


class SourceUpdateSourceAwsS3SourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsS3SourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAwsS3SourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceAwsS3SourceConfig(BaseModel):
    bucket: str
    prefix: str
    csv: Optional["SourceUpdateSourceAwsS3SourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class SourceUpdateSourceAwsS3SourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class SourceUpdateSourceAzureSynapseSource(BaseModel):
    typename__: Literal["AzureSynapseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceAzureSynapseSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceAzureSynapseSourceCredential"
    windows: List["SourceUpdateSourceAzureSynapseSourceWindows"]
    segmentations: List["SourceUpdateSourceAzureSynapseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAzureSynapseSourceNamespace"
    tags: List["SourceUpdateSourceAzureSynapseSourceTags"]
    config: "SourceUpdateSourceAzureSynapseSourceConfig"


class SourceUpdateSourceAzureSynapseSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceAzureSynapseSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAzureSynapseSourceCredentialNamespace"


class SourceUpdateSourceAzureSynapseSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAzureSynapseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAzureSynapseSourceWindowsNamespace"


class SourceUpdateSourceAzureSynapseSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAzureSynapseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceAzureSynapseSourceSegmentationsNamespace"


class SourceUpdateSourceAzureSynapseSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAzureSynapseSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceAzureSynapseSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceAzureSynapseSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceUpdateSourceClickHouseSource(BaseModel):
    typename__: Literal["ClickHouseSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceClickHouseSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceClickHouseSourceCredential"
    windows: List["SourceUpdateSourceClickHouseSourceWindows"]
    segmentations: List["SourceUpdateSourceClickHouseSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceClickHouseSourceNamespace"
    tags: List["SourceUpdateSourceClickHouseSourceTags"]
    config: "SourceUpdateSourceClickHouseSourceConfig"


class SourceUpdateSourceClickHouseSourceCatalogAsset(BaseModel):
    typename__: Literal["ClickHouseCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceClickHouseSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceClickHouseSourceCredentialNamespace"


class SourceUpdateSourceClickHouseSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceClickHouseSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceClickHouseSourceWindowsNamespace"


class SourceUpdateSourceClickHouseSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceClickHouseSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceClickHouseSourceSegmentationsNamespace"


class SourceUpdateSourceClickHouseSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceClickHouseSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceClickHouseSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceClickHouseSourceConfig(BaseModel):
    database: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceUpdateSourceDatabricksSource(BaseModel):
    typename__: Literal["DatabricksSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceDatabricksSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceDatabricksSourceCredential"
    windows: List["SourceUpdateSourceDatabricksSourceWindows"]
    segmentations: List["SourceUpdateSourceDatabricksSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDatabricksSourceNamespace"
    tags: List["SourceUpdateSourceDatabricksSourceTags"]
    config: "SourceUpdateSourceDatabricksSourceConfig"


class SourceUpdateSourceDatabricksSourceCatalogAsset(BaseModel):
    typename__: Literal["DatabricksCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceDatabricksSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDatabricksSourceCredentialNamespace"


class SourceUpdateSourceDatabricksSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDatabricksSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDatabricksSourceWindowsNamespace"


class SourceUpdateSourceDatabricksSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDatabricksSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDatabricksSourceSegmentationsNamespace"


class SourceUpdateSourceDatabricksSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDatabricksSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDatabricksSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceDatabricksSourceConfig(BaseModel):
    catalog: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]
    http_path: Optional[str] = Field(alias="httpPath")


class SourceUpdateSourceDbtModelRunSource(BaseModel):
    typename__: Literal["DbtModelRunSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceDbtModelRunSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceDbtModelRunSourceCredential"
    windows: List["SourceUpdateSourceDbtModelRunSourceWindows"]
    segmentations: List["SourceUpdateSourceDbtModelRunSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtModelRunSourceNamespace"
    tags: List["SourceUpdateSourceDbtModelRunSourceTags"]
    config: "SourceUpdateSourceDbtModelRunSourceConfig"


class SourceUpdateSourceDbtModelRunSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceDbtModelRunSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtModelRunSourceCredentialNamespace"


class SourceUpdateSourceDbtModelRunSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtModelRunSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtModelRunSourceWindowsNamespace"


class SourceUpdateSourceDbtModelRunSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtModelRunSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtModelRunSourceSegmentationsNamespace"


class SourceUpdateSourceDbtModelRunSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtModelRunSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtModelRunSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceDbtModelRunSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class SourceUpdateSourceDbtTestResultSource(BaseModel):
    typename__: Literal["DbtTestResultSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceDbtTestResultSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceUpdateSourceDbtTestResultSourceCredential"
    windows: List["SourceUpdateSourceDbtTestResultSourceWindows"]
    segmentations: List["SourceUpdateSourceDbtTestResultSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtTestResultSourceNamespace"
    tags: List["SourceUpdateSourceDbtTestResultSourceTags"]
    config: "SourceUpdateSourceDbtTestResultSourceConfig"


class SourceUpdateSourceDbtTestResultSourceCatalogAsset(BaseModel):
    typename__: Literal[
        "AwsAthenaCatalogAsset",
        "AwsKinesisCatalogAsset",
        "AwsRedshiftCatalogAsset",
        "AwsS3CatalogAsset",
        "AzureSynapseCatalogAsset",
        "CatalogAsset",
        "ClickHouseCatalogAsset",
        "DatabricksCatalogAsset",
        "DemoCatalogAsset",
        "GcpBigQueryCatalogAsset",
        "GcpPubSubCatalogAsset",
        "GcpPubSubLiteCatalogAsset",
        "GcpStorageCatalogAsset",
        "KafkaCatalogAsset",
        "LookerDashboardCatalogAsset",
        "LookerLookCatalogAsset",
        "PostgreSqlCatalogAsset",
        "SnowflakeCatalogAsset",
        "TableauCustomSQLTableCatalogAsset",
        "TableauDashboardCatalogAsset",
        "TableauDatasourceCatalogAsset",
        "TableauFlowCatalogAsset",
        "TableauWorkbookCatalogAsset",
        "TableauWorksheetCatalogAsset",
    ] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceDbtTestResultSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtTestResultSourceCredentialNamespace"


class SourceUpdateSourceDbtTestResultSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtTestResultSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtTestResultSourceWindowsNamespace"


class SourceUpdateSourceDbtTestResultSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtTestResultSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceDbtTestResultSourceSegmentationsNamespace"


class SourceUpdateSourceDbtTestResultSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtTestResultSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceDbtTestResultSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceDbtTestResultSourceConfig(BaseModel):
    job_name: str = Field(alias="jobName")
    project_name: str = Field(alias="projectName")
    schedule: Optional[CronExpression]


class SourceUpdateSourceGcpBigQuerySource(BaseModel):
    typename__: Literal["GcpBigQuerySource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceGcpBigQuerySourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceGcpBigQuerySourceCredential"
    windows: List["SourceUpdateSourceGcpBigQuerySourceWindows"]
    segmentations: List["SourceUpdateSourceGcpBigQuerySourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpBigQuerySourceNamespace"
    tags: List["SourceUpdateSourceGcpBigQuerySourceTags"]
    config: "SourceUpdateSourceGcpBigQuerySourceConfig"


class SourceUpdateSourceGcpBigQuerySourceCatalogAsset(BaseModel):
    typename__: Literal["GcpBigQueryCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceGcpBigQuerySourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpBigQuerySourceCredentialNamespace"


class SourceUpdateSourceGcpBigQuerySourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpBigQuerySourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpBigQuerySourceWindowsNamespace"


class SourceUpdateSourceGcpBigQuerySourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpBigQuerySourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpBigQuerySourceSegmentationsNamespace"


class SourceUpdateSourceGcpBigQuerySourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpBigQuerySourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpBigQuerySourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceGcpBigQuerySourceConfig(BaseModel):
    project: str
    dataset: str
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceUpdateSourceGcpPubSubLiteSource(BaseModel):
    typename__: Literal["GcpPubSubLiteSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceGcpPubSubLiteSourceCatalogAsset"] = (
        Field(alias="catalogAsset")
    )
    credential: "SourceUpdateSourceGcpPubSubLiteSourceCredential"
    windows: List["SourceUpdateSourceGcpPubSubLiteSourceWindows"]
    segmentations: List["SourceUpdateSourceGcpPubSubLiteSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubLiteSourceNamespace"
    tags: List["SourceUpdateSourceGcpPubSubLiteSourceTags"]
    config: "SourceUpdateSourceGcpPubSubLiteSourceConfig"


class SourceUpdateSourceGcpPubSubLiteSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubLiteCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceGcpPubSubLiteSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubLiteSourceCredentialNamespace"


class SourceUpdateSourceGcpPubSubLiteSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubLiteSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubLiteSourceWindowsNamespace"


class SourceUpdateSourceGcpPubSubLiteSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubLiteSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubLiteSourceSegmentationsNamespace"


class SourceUpdateSourceGcpPubSubLiteSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubLiteSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubLiteSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceGcpPubSubLiteSourceConfig(BaseModel):
    location: str
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional[
        "SourceUpdateSourceGcpPubSubLiteSourceConfigMessageFormat"
    ] = Field(alias="messageFormat")


class SourceUpdateSourceGcpPubSubLiteSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceUpdateSourceGcpPubSubSource(BaseModel):
    typename__: Literal["GcpPubSubSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceGcpPubSubSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceGcpPubSubSourceCredential"
    windows: List["SourceUpdateSourceGcpPubSubSourceWindows"]
    segmentations: List["SourceUpdateSourceGcpPubSubSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubSourceNamespace"
    tags: List["SourceUpdateSourceGcpPubSubSourceTags"]
    config: "SourceUpdateSourceGcpPubSubSourceConfig"


class SourceUpdateSourceGcpPubSubSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpPubSubCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceGcpPubSubSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubSourceCredentialNamespace"


class SourceUpdateSourceGcpPubSubSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubSourceWindowsNamespace"


class SourceUpdateSourceGcpPubSubSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpPubSubSourceSegmentationsNamespace"


class SourceUpdateSourceGcpPubSubSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpPubSubSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceGcpPubSubSourceConfig(BaseModel):
    project: str
    subscription_id: str = Field(alias="subscriptionId")
    message_format: Optional["SourceUpdateSourceGcpPubSubSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class SourceUpdateSourceGcpPubSubSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceUpdateSourceGcpStorageSource(BaseModel):
    typename__: Literal["GcpStorageSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceGcpStorageSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceGcpStorageSourceCredential"
    windows: List["SourceUpdateSourceGcpStorageSourceWindows"]
    segmentations: List["SourceUpdateSourceGcpStorageSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpStorageSourceNamespace"
    tags: List["SourceUpdateSourceGcpStorageSourceTags"]
    config: "SourceUpdateSourceGcpStorageSourceConfig"


class SourceUpdateSourceGcpStorageSourceCatalogAsset(BaseModel):
    typename__: Literal["GcpStorageCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceGcpStorageSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpStorageSourceCredentialNamespace"


class SourceUpdateSourceGcpStorageSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpStorageSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpStorageSourceWindowsNamespace"


class SourceUpdateSourceGcpStorageSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpStorageSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceGcpStorageSourceSegmentationsNamespace"


class SourceUpdateSourceGcpStorageSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpStorageSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceGcpStorageSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceGcpStorageSourceConfig(BaseModel):
    project: str
    bucket: str
    folder: str
    csv: Optional["SourceUpdateSourceGcpStorageSourceConfigCsv"]
    schedule: Optional[CronExpression]
    file_pattern: Optional[str] = Field(alias="filePattern")
    file_format: Optional[FileFormat] = Field(alias="fileFormat")


class SourceUpdateSourceGcpStorageSourceConfigCsv(BaseModel):
    null_marker: Optional[str] = Field(alias="nullMarker")
    delimiter: str


class SourceUpdateSourceKafkaSource(BaseModel):
    typename__: Literal["KafkaSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceKafkaSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceKafkaSourceCredential"
    windows: List["SourceUpdateSourceKafkaSourceWindows"]
    segmentations: List["SourceUpdateSourceKafkaSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceKafkaSourceNamespace"
    tags: List["SourceUpdateSourceKafkaSourceTags"]
    config: "SourceUpdateSourceKafkaSourceConfig"


class SourceUpdateSourceKafkaSourceCatalogAsset(BaseModel):
    typename__: Literal["KafkaCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceKafkaSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceKafkaSourceCredentialNamespace"


class SourceUpdateSourceKafkaSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceKafkaSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceKafkaSourceWindowsNamespace"


class SourceUpdateSourceKafkaSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceKafkaSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceKafkaSourceSegmentationsNamespace"


class SourceUpdateSourceKafkaSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceKafkaSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceKafkaSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceKafkaSourceConfig(BaseModel):
    topic: str
    message_format: Optional["SourceUpdateSourceKafkaSourceConfigMessageFormat"] = (
        Field(alias="messageFormat")
    )


class SourceUpdateSourceKafkaSourceConfigMessageFormat(BaseModel):
    format: StreamingSourceMessageFormat
    db_schema: Optional[str] = Field(alias="schema")


class SourceUpdateSourcePostgreSqlSource(BaseModel):
    typename__: Literal["PostgreSqlSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourcePostgreSqlSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourcePostgreSqlSourceCredential"
    windows: List["SourceUpdateSourcePostgreSqlSourceWindows"]
    segmentations: List["SourceUpdateSourcePostgreSqlSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourcePostgreSqlSourceNamespace"
    tags: List["SourceUpdateSourcePostgreSqlSourceTags"]
    config: "SourceUpdateSourcePostgreSqlSourceConfig"


class SourceUpdateSourcePostgreSqlSourceCatalogAsset(BaseModel):
    typename__: Literal["PostgreSqlCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourcePostgreSqlSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourcePostgreSqlSourceCredentialNamespace"


class SourceUpdateSourcePostgreSqlSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourcePostgreSqlSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourcePostgreSqlSourceWindowsNamespace"


class SourceUpdateSourcePostgreSqlSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourcePostgreSqlSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourcePostgreSqlSourceSegmentationsNamespace"


class SourceUpdateSourcePostgreSqlSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourcePostgreSqlSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourcePostgreSqlSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourcePostgreSqlSourceConfig(BaseModel):
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class SourceUpdateSourceSnowflakeSource(BaseModel):
    typename__: Literal["SnowflakeSource"] = Field(alias="__typename")
    id: SourceId
    name: str
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    catalog_asset: Optional["SourceUpdateSourceSnowflakeSourceCatalogAsset"] = Field(
        alias="catalogAsset"
    )
    credential: "SourceUpdateSourceSnowflakeSourceCredential"
    windows: List["SourceUpdateSourceSnowflakeSourceWindows"]
    segmentations: List["SourceUpdateSourceSnowflakeSourceSegmentations"]
    jtd_schema: JsonTypeDefinition = Field(alias="jtdSchema")
    state: SourceState
    state_updated_at: datetime = Field(alias="stateUpdatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSnowflakeSourceNamespace"
    tags: List["SourceUpdateSourceSnowflakeSourceTags"]
    config: "SourceUpdateSourceSnowflakeSourceConfig"


class SourceUpdateSourceSnowflakeSourceCatalogAsset(BaseModel):
    typename__: Literal["SnowflakeCatalogAsset"] = Field(alias="__typename")
    id: Any
    asset_type: CatalogAssetType = Field(alias="assetType")


class SourceUpdateSourceSnowflakeSourceCredential(BaseModel):
    typename__: Literal[
        "AwsAthenaCredential",
        "AwsCredential",
        "AwsRedshiftCredential",
        "AzureSynapseEntraIdCredential",
        "AzureSynapseSqlCredential",
        "ClickHouseCredential",
        "Credential",
        "DatabricksCredential",
        "DbtCloudCredential",
        "DbtCoreCredential",
        "DemoCredential",
        "GcpCredential",
        "KafkaSaslSslPlainCredential",
        "KafkaSslCredential",
        "LookerCredential",
        "PostgreSqlCredential",
        "SnowflakeCredential",
        "TableauConnectedAppCredential",
        "TableauPersonalAccessTokenCredential",
    ] = Field(alias="__typename")
    id: CredentialId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSnowflakeSourceCredentialNamespace"


class SourceUpdateSourceSnowflakeSourceCredentialNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSnowflakeSourceWindows(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSnowflakeSourceWindowsNamespace"


class SourceUpdateSourceSnowflakeSourceWindowsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSnowflakeSourceSegmentations(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "SourceUpdateSourceSnowflakeSourceSegmentationsNamespace"


class SourceUpdateSourceSnowflakeSourceSegmentationsNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSnowflakeSourceNamespace(BaseModel):
    id: Any


class SourceUpdateSourceSnowflakeSourceTags(BaseModel):
    key: str
    value: str


class SourceUpdateSourceSnowflakeSourceConfig(BaseModel):
    role: Optional[str]
    warehouse: Optional[str]
    database: str
    db_schema: str = Field(alias="schema")
    table: str
    cursor_field: Optional[str] = Field(alias="cursorField")
    lookback_days: int = Field(alias="lookbackDays")
    schedule: Optional[CronExpression]


class TagDetails(BaseModel):
    id: Any
    key: str
    value: str
    is_imported: bool = Field(alias="isImported")
    is_system_tag: bool = Field(alias="isSystemTag")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")


class TagCreation(BaseModel):
    errors: List["TagCreationErrors"]
    tag: Optional["TagCreationTag"]


class TagCreationErrors(ErrorDetails):
    pass


class TagCreationTag(TagDetails):
    pass


class TagUpdate(BaseModel):
    errors: List["TagUpdateErrors"]
    tag: Optional["TagUpdateTag"]


class TagUpdateErrors(ErrorDetails):
    pass


class TagUpdateTag(TagDetails):
    pass


class TeamSummary(BaseModel):
    id: Any
    name: str
    description: Optional[str]
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")


class UserDetails(BaseModel):
    id: Any
    display_name: str = Field(alias="displayName")
    full_name: Optional[str] = Field(alias="fullName")
    email: Optional[str]
    status: UserStatus
    avatar: Any
    avatar_thumbnail: Any = Field(alias="avatarThumbnail")
    login_type: LoginType = Field(alias="loginType")
    global_role: Role = Field(alias="globalRole")
    identities: List[
        Annotated[
            Union[
                "UserDetailsIdentitiesFederatedIdentity",
                "UserDetailsIdentitiesLocalIdentity",
            ],
            Field(discriminator="typename__"),
        ]
    ]
    teams: List["UserDetailsTeams"]
    namespaces: List["UserDetailsNamespaces"]
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    last_login_at: Optional[datetime] = Field(alias="lastLoginAt")
    resource_name: str = Field(alias="resourceName")


class UserDetailsIdentitiesFederatedIdentity(BaseModel):
    typename__: Literal["FederatedIdentity"] = Field(alias="__typename")
    id: str
    user_id: Optional[Any] = Field(alias="userId")
    idp: "UserDetailsIdentitiesFederatedIdentityIdp"
    created_at: datetime = Field(alias="createdAt")


class UserDetailsIdentitiesFederatedIdentityIdp(BaseModel):
    typename__: Literal[
        "IdentityProvider", "LocalIdentityProvider", "SamlIdentityProvider"
    ] = Field(alias="__typename")
    id: str
    name: str


class UserDetailsIdentitiesLocalIdentity(BaseModel):
    typename__: Literal["LocalIdentity"] = Field(alias="__typename")
    id: str
    user_id: Optional[Any] = Field(alias="userId")
    username: str
    created_at: datetime = Field(alias="createdAt")


class UserDetailsTeams(TeamDetails):
    pass


class UserDetailsNamespaces(NamespaceDetails):
    pass


class UserCreation(BaseModel):
    errors: List["UserCreationErrors"]
    user: Optional["UserCreationUser"]


class UserCreationErrors(BaseModel):
    code: Optional[str]
    message: Optional[str]


class UserCreationUser(UserDetails):
    pass


class UserDeletion(BaseModel):
    errors: List["UserDeletionErrors"]
    user: Optional["UserDeletionUser"]


class UserDeletionErrors(BaseModel):
    code: UserDeleteErrorCode
    message: str


class UserDeletionUser(UserDetails):
    pass


class UserUpdate(BaseModel):
    errors: List["UserUpdateErrors"]
    user: Optional["UserUpdateUser"]


class UserUpdateErrors(BaseModel):
    code: UserUpdateErrorCode
    message: str


class UserUpdateUser(UserDetails):
    pass


class ValidatorCreation(BaseModel):
    errors: List["ValidatorCreationErrors"]
    validator: Optional[
        Annotated[
            Union[
                "ValidatorCreationValidatorValidator",
                "ValidatorCreationValidatorCategoricalDistributionValidator",
                "ValidatorCreationValidatorFreshnessValidator",
                "ValidatorCreationValidatorNumericAnomalyValidator",
                "ValidatorCreationValidatorNumericDistributionValidator",
                "ValidatorCreationValidatorNumericValidator",
                "ValidatorCreationValidatorRelativeTimeValidator",
                "ValidatorCreationValidatorRelativeVolumeValidator",
                "ValidatorCreationValidatorSqlValidator",
                "ValidatorCreationValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class ValidatorCreationErrors(ErrorDetails):
    pass


class ValidatorCreationValidatorValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorValidatorNamespace"
    tags: List["ValidatorCreationValidatorValidatorTags"]


class ValidatorCreationValidatorValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorValidatorSourceConfigWindow"
    segmentation: "ValidatorCreationValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorCreationValidatorValidatorSourceConfigSourceNamespace"


class ValidatorCreationValidatorValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorValidatorSourceConfigWindowNamespace"


class ValidatorCreationValidatorValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorValidatorSourceConfigSegmentationNamespace"


class ValidatorCreationValidatorValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorCategoricalDistributionValidatorNamespace"
    tags: List["ValidatorCreationValidatorCategoricalDistributionValidatorTags"]
    config: "ValidatorCreationValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfig(BaseModel):
    source: (
        "ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSource"
    )
    window: (
        "ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigWindow"
    )
    segmentation: "ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class ValidatorCreationValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorCategoricalDistributionValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorCategoricalDistributionValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorCategoricalDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorCreationValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorCreationValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class ValidatorCreationValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorFreshnessValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorFreshnessValidatorNamespace"
    tags: List["ValidatorCreationValidatorFreshnessValidatorTags"]
    config: "ValidatorCreationValidatorFreshnessValidatorConfig"


class ValidatorCreationValidatorFreshnessValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorFreshnessValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "ValidatorCreationValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorFreshnessValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorCreationValidatorFreshnessValidatorSourceConfigSourceNamespace"


class ValidatorCreationValidatorFreshnessValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorFreshnessValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorFreshnessValidatorSourceConfigWindowNamespace"


class ValidatorCreationValidatorFreshnessValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorFreshnessValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorCreationValidatorFreshnessValidatorSourceConfigSegmentationNamespace"
    )


class ValidatorCreationValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorFreshnessValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorFreshnessValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "ValidatorCreationValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorCreationValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorNumericAnomalyValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericAnomalyValidatorNamespace"
    tags: List["ValidatorCreationValidatorNumericAnomalyValidatorTags"]
    config: "ValidatorCreationValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorCreationValidatorNumericAnomalyValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSource(BaseModel):
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
        "ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"
    )


class ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"
    )


class ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class ValidatorCreationValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorCreationValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class ValidatorCreationValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfig(BaseModel):
    source: (
        "ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    )
    window: (
        "ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class ValidatorCreationValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "ValidatorCreationValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericDistributionValidatorNamespace"
    tags: List["ValidatorCreationValidatorNumericDistributionValidatorTags"]
    config: "ValidatorCreationValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorCreationValidatorNumericDistributionValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSource(
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
    namespace: "ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class ValidatorCreationValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class ValidatorCreationValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericDistributionValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorNumericDistributionValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorNumericDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorCreationValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorCreationValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class ValidatorCreationValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericValidatorNamespace"
    tags: List["ValidatorCreationValidatorNumericValidatorTags"]
    config: "ValidatorCreationValidatorNumericValidatorConfig"


class ValidatorCreationValidatorNumericValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorNumericValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorNumericValidatorSourceConfigWindow"
    segmentation: "ValidatorCreationValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorNumericValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorCreationValidatorNumericValidatorSourceConfigSourceNamespace"


class ValidatorCreationValidatorNumericValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorNumericValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorNumericValidatorSourceConfigWindowNamespace"


class ValidatorCreationValidatorNumericValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorNumericValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorCreationValidatorNumericValidatorSourceConfigSegmentationNamespace"
    )


class ValidatorCreationValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorNumericValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorNumericValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorCreationValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorCreationValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorNumericValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorRelativeTimeValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorRelativeTimeValidatorNamespace"
    tags: List["ValidatorCreationValidatorRelativeTimeValidatorTags"]
    config: "ValidatorCreationValidatorRelativeTimeValidatorConfig"


class ValidatorCreationValidatorRelativeTimeValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSource(BaseModel):
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
        "ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSourceNamespace"
    )


class ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorRelativeTimeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorCreationValidatorRelativeTimeValidatorSourceConfigWindowNamespace"
    )


class ValidatorCreationValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"


class ValidatorCreationValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorRelativeTimeValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorCreationValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorCreationValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorRelativeVolumeValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorRelativeVolumeValidatorNamespace"
    tags: List["ValidatorCreationValidatorRelativeVolumeValidatorTags"]
    config: "ValidatorCreationValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorCreationValidatorRelativeVolumeValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSource(BaseModel):
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
        "ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"
    )


class ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"
    )


class ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class ValidatorCreationValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorCreationValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorCreationValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfig(BaseModel):
    source: (
        "ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    )
    window: (
        "ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    )
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class ValidatorCreationValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorSqlValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorSqlValidatorNamespace"
    tags: List["ValidatorCreationValidatorSqlValidatorTags"]
    config: "ValidatorCreationValidatorSqlValidatorConfig"


class ValidatorCreationValidatorSqlValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorSqlValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorSqlValidatorSourceConfigWindow"
    segmentation: "ValidatorCreationValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorSqlValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorCreationValidatorSqlValidatorSourceConfigSourceNamespace"


class ValidatorCreationValidatorSqlValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorSqlValidatorSourceConfigWindowNamespace"


class ValidatorCreationValidatorSqlValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorSqlValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorSqlValidatorSourceConfigSegmentationNamespace"


class ValidatorCreationValidatorSqlValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorSqlValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorSqlValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "ValidatorCreationValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class ValidatorCreationValidatorSqlValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorSqlValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorSqlValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorCreationValidatorVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorCreationValidatorVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorVolumeValidatorNamespace"
    tags: List["ValidatorCreationValidatorVolumeValidatorTags"]
    config: "ValidatorCreationValidatorVolumeValidatorConfig"


class ValidatorCreationValidatorVolumeValidatorSourceConfig(BaseModel):
    source: "ValidatorCreationValidatorVolumeValidatorSourceConfigSource"
    window: "ValidatorCreationValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "ValidatorCreationValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorCreationValidatorVolumeValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorCreationValidatorVolumeValidatorSourceConfigSourceNamespace"


class ValidatorCreationValidatorVolumeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorCreationValidatorVolumeValidatorSourceConfigWindowNamespace"


class ValidatorCreationValidatorVolumeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorCreationValidatorVolumeValidatorSourceConfigSegmentationNamespace"
    )


class ValidatorCreationValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorCreationValidatorVolumeValidatorNamespace(BaseModel):
    id: Any


class ValidatorCreationValidatorVolumeValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorCreationValidatorVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorCreationValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "ValidatorCreationValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "ValidatorCreationValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorCreationValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorCreationValidatorVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorCreationValidatorVolumeValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorRecommendationApplication(BaseModel):
    typename__: str = Field(alias="__typename")
    failed_ids: List[Any] = Field(alias="failedIds")
    success_ids: List[str] = Field(alias="successIds")


class ValidatorRecommendationDismissal(BaseModel):
    typename__: str = Field(alias="__typename")
    errors: List["ValidatorRecommendationDismissalErrors"]
    recommendation_ids: List[str] = Field(alias="recommendationIds")


class ValidatorRecommendationDismissalErrors(ErrorDetails):
    pass


class ValidatorUpdate(BaseModel):
    errors: List["ValidatorUpdateErrors"]
    validator: Optional[
        Annotated[
            Union[
                "ValidatorUpdateValidatorValidator",
                "ValidatorUpdateValidatorCategoricalDistributionValidator",
                "ValidatorUpdateValidatorFreshnessValidator",
                "ValidatorUpdateValidatorNumericAnomalyValidator",
                "ValidatorUpdateValidatorNumericDistributionValidator",
                "ValidatorUpdateValidatorNumericValidator",
                "ValidatorUpdateValidatorRelativeTimeValidator",
                "ValidatorUpdateValidatorRelativeVolumeValidator",
                "ValidatorUpdateValidatorSqlValidator",
                "ValidatorUpdateValidatorVolumeValidator",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class ValidatorUpdateErrors(ErrorDetails):
    pass


class ValidatorUpdateValidatorValidator(BaseModel):
    typename__: Literal["Validator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorValidatorNamespace"
    tags: List["ValidatorUpdateValidatorValidatorTags"]


class ValidatorUpdateValidatorValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorValidatorSourceConfigWindow"
    segmentation: "ValidatorUpdateValidatorValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorUpdateValidatorValidatorSourceConfigSourceNamespace"


class ValidatorUpdateValidatorValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorValidatorSourceConfigWindowNamespace"


class ValidatorUpdateValidatorValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorValidatorSourceConfigSegmentationNamespace"


class ValidatorUpdateValidatorValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorCategoricalDistributionValidator(BaseModel):
    typename__: Literal["CategoricalDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorCategoricalDistributionValidatorNamespace"
    tags: List["ValidatorUpdateValidatorCategoricalDistributionValidatorTags"]
    config: "ValidatorUpdateValidatorCategoricalDistributionValidatorConfig"
    reference_source_config: (
        "ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow"
    segmentation: "ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSource(
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
    namespace: "ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace"


class ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace"


class ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace"


class ValidatorUpdateValidatorCategoricalDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorCategoricalDistributionValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorCategoricalDistributionValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorCategoricalDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: CategoricalDistributionMetric = Field(alias="categoricalDistributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorUpdateValidatorCategoricalDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorCategoricalDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorCategoricalDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource"
    window: "ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace"


class ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace"


class ValidatorUpdateValidatorCategoricalDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorFreshnessValidator(BaseModel):
    typename__: Literal["FreshnessValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorFreshnessValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorFreshnessValidatorNamespace"
    tags: List["ValidatorUpdateValidatorFreshnessValidatorTags"]
    config: "ValidatorUpdateValidatorFreshnessValidatorConfig"


class ValidatorUpdateValidatorFreshnessValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorFreshnessValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorFreshnessValidatorSourceConfigWindow"
    segmentation: "ValidatorUpdateValidatorFreshnessValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorFreshnessValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace"


class ValidatorUpdateValidatorFreshnessValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorFreshnessValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace"


class ValidatorUpdateValidatorFreshnessValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorFreshnessValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace"
    )


class ValidatorUpdateValidatorFreshnessValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorFreshnessValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorFreshnessValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorFreshnessValidatorConfig(BaseModel):
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    threshold: Union[
        "ValidatorUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorUpdateValidatorFreshnessValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorFreshnessValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorFreshnessValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorNumericAnomalyValidator(BaseModel):
    typename__: Literal["NumericAnomalyValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericAnomalyValidatorNamespace"
    tags: List["ValidatorUpdateValidatorNumericAnomalyValidatorTags"]
    config: "ValidatorUpdateValidatorNumericAnomalyValidatorConfig"
    reference_source_config: (
        "ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSource(BaseModel):
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
        "ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace"
    )


class ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace"
    )


class ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace"


class ValidatorUpdateValidatorNumericAnomalyValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericAnomalyValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorNumericAnomalyValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorNumericAnomalyValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericAnomalyMetric = Field(alias="numericAnomalyMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold",
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


class ValidatorUpdateValidatorNumericAnomalyValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorNumericAnomalyValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorNumericAnomalyValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource"
    window: "ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace"


class ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace"


class ValidatorUpdateValidatorNumericAnomalyValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericDistributionValidator(BaseModel):
    typename__: Literal["NumericDistributionValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: (
        "ValidatorUpdateValidatorNumericDistributionValidatorSourceConfig"
    ) = Field(alias="sourceConfig")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericDistributionValidatorNamespace"
    tags: List["ValidatorUpdateValidatorNumericDistributionValidatorTags"]
    config: "ValidatorUpdateValidatorNumericDistributionValidatorConfig"
    reference_source_config: (
        "ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorUpdateValidatorNumericDistributionValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace"


class ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace"


class ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace"


class ValidatorUpdateValidatorNumericDistributionValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericDistributionValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorNumericDistributionValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorNumericDistributionValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    reference_source_field: JsonPointer = Field(alias="referenceSourceField")
    metric: NumericDistributionMetric = Field(alias="distributionMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorUpdateValidatorNumericDistributionValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorNumericDistributionValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorNumericDistributionValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfig(
    BaseModel
):
    source: "ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource"
    window: "ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace"


class ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace"


class ValidatorUpdateValidatorNumericDistributionValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericValidator(BaseModel):
    typename__: Literal["NumericValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorNumericValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericValidatorNamespace"
    tags: List["ValidatorUpdateValidatorNumericValidatorTags"]
    config: "ValidatorUpdateValidatorNumericValidatorConfig"


class ValidatorUpdateValidatorNumericValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorNumericValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorNumericValidatorSourceConfigWindow"
    segmentation: "ValidatorUpdateValidatorNumericValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorNumericValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorUpdateValidatorNumericValidatorSourceConfigSourceNamespace"


class ValidatorUpdateValidatorNumericValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorNumericValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorNumericValidatorSourceConfigWindowNamespace"


class ValidatorUpdateValidatorNumericValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorNumericValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace"
    )


class ValidatorUpdateValidatorNumericValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorNumericValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorNumericValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorNumericValidatorConfig(BaseModel):
    source_field: JsonPointer = Field(alias="sourceField")
    metric: NumericMetric
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorNumericValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorUpdateValidatorNumericValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorNumericValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorNumericValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorRelativeTimeValidator(BaseModel):
    typename__: Literal["RelativeTimeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorRelativeTimeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorRelativeTimeValidatorNamespace"
    tags: List["ValidatorUpdateValidatorRelativeTimeValidatorTags"]
    config: "ValidatorUpdateValidatorRelativeTimeValidatorConfig"


class ValidatorUpdateValidatorRelativeTimeValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSource(BaseModel):
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
        "ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace"
    )


class ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace"
    )


class ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace"
    )


class ValidatorUpdateValidatorRelativeTimeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorRelativeTimeValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorRelativeTimeValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorRelativeTimeValidatorConfig(BaseModel):
    source_field_minuend: JsonPointer = Field(alias="sourceFieldMinuend")
    source_field_subtrahend: JsonPointer = Field(alias="sourceFieldSubtrahend")
    metric: RelativeTimeMetric = Field(alias="relativeTimeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorUpdateValidatorRelativeTimeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorRelativeTimeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorRelativeTimeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorRelativeVolumeValidator(BaseModel):
    typename__: Literal["RelativeVolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfig" = (
        Field(alias="sourceConfig")
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorRelativeVolumeValidatorNamespace"
    tags: List["ValidatorUpdateValidatorRelativeVolumeValidatorTags"]
    config: "ValidatorUpdateValidatorRelativeVolumeValidatorConfig"
    reference_source_config: (
        "ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig"
    ) = Field(alias="referenceSourceConfig")


class ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigWindow"
    segmentation: (
        "ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation"
    )
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSource(BaseModel):
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
        "ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace"
    )


class ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace"
    )


class ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentation(
    BaseModel
):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace"


class ValidatorUpdateValidatorRelativeVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorRelativeVolumeValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorRelativeVolumeValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorRelativeVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    reference_source_field: Optional[JsonPointer] = Field(
        alias="optionalReferenceSourceField"
    )
    metric: RelativeVolumeMetric = Field(alias="relativeVolumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorUpdateValidatorRelativeVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorRelativeVolumeValidatorConfigThresholdDynamicThreshold(
    BaseModel
):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorRelativeVolumeValidatorConfigThresholdFixedThreshold(
    BaseModel
):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource"
    window: "ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow"
    history: int
    offset: int
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSource(
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
    namespace: "ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace"


class ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigSourceNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindow(
    BaseModel
):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace"


class ValidatorUpdateValidatorRelativeVolumeValidatorReferenceSourceConfigWindowNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorSqlValidator(BaseModel):
    typename__: Literal["SqlValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorSqlValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorSqlValidatorNamespace"
    tags: List["ValidatorUpdateValidatorSqlValidatorTags"]
    config: "ValidatorUpdateValidatorSqlValidatorConfig"


class ValidatorUpdateValidatorSqlValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorSqlValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorSqlValidatorSourceConfigWindow"
    segmentation: "ValidatorUpdateValidatorSqlValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorSqlValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorUpdateValidatorSqlValidatorSourceConfigSourceNamespace"


class ValidatorUpdateValidatorSqlValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorSqlValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorSqlValidatorSourceConfigWindowNamespace"


class ValidatorUpdateValidatorSqlValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorSqlValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace"


class ValidatorUpdateValidatorSqlValidatorSourceConfigSegmentationNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorSqlValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorSqlValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorSqlValidatorConfig(BaseModel):
    query: str
    threshold: Union[
        "ValidatorUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorSqlValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")


class ValidatorUpdateValidatorSqlValidatorConfigThresholdDifferenceThreshold(BaseModel):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorSqlValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorSqlValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class ValidatorUpdateValidatorVolumeValidator(BaseModel):
    typename__: Literal["VolumeValidator"] = Field(alias="__typename")
    id: ValidatorId
    name: str
    has_custom_name: bool = Field(alias="hasCustomName")
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    source_config: "ValidatorUpdateValidatorVolumeValidatorSourceConfig" = Field(
        alias="sourceConfig"
    )
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorVolumeValidatorNamespace"
    tags: List["ValidatorUpdateValidatorVolumeValidatorTags"]
    config: "ValidatorUpdateValidatorVolumeValidatorConfig"


class ValidatorUpdateValidatorVolumeValidatorSourceConfig(BaseModel):
    source: "ValidatorUpdateValidatorVolumeValidatorSourceConfigSource"
    window: "ValidatorUpdateValidatorVolumeValidatorSourceConfigWindow"
    segmentation: "ValidatorUpdateValidatorVolumeValidatorSourceConfigSegmentation"
    filter: Optional[JsonFilterExpression]


class ValidatorUpdateValidatorVolumeValidatorSourceConfigSource(BaseModel):
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
    namespace: "ValidatorUpdateValidatorVolumeValidatorSourceConfigSourceNamespace"


class ValidatorUpdateValidatorVolumeValidatorSourceConfigSourceNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorVolumeValidatorSourceConfigWindow(BaseModel):
    typename__: Literal[
        "FileWindow", "FixedBatchWindow", "GlobalWindow", "TumblingWindow", "Window"
    ] = Field(alias="__typename")
    id: WindowId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "ValidatorUpdateValidatorVolumeValidatorSourceConfigWindowNamespace"


class ValidatorUpdateValidatorVolumeValidatorSourceConfigWindowNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorVolumeValidatorSourceConfigSegmentation(BaseModel):
    typename__: Literal["Segmentation"] = Field(alias="__typename")
    id: SegmentationId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: (
        "ValidatorUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace"
    )


class ValidatorUpdateValidatorVolumeValidatorSourceConfigSegmentationNamespace(
    BaseModel
):
    id: Any


class ValidatorUpdateValidatorVolumeValidatorNamespace(BaseModel):
    id: Any


class ValidatorUpdateValidatorVolumeValidatorTags(BaseModel):
    key: str
    value: str


class ValidatorUpdateValidatorVolumeValidatorConfig(BaseModel):
    source_field: Optional[JsonPointer] = Field(alias="optionalSourceField")
    source_fields: List[JsonPointer] = Field(alias="sourceFields")
    metric: VolumeMetric = Field(alias="volumeMetric")
    initialize_with_backfill: bool = Field(alias="initializeWithBackfill")
    threshold: Union[
        "ValidatorUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold",
        "ValidatorUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold",
        "ValidatorUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold",
    ] = Field(discriminator="typename__")


class ValidatorUpdateValidatorVolumeValidatorConfigThresholdDifferenceThreshold(
    BaseModel
):
    typename__: Literal["DifferenceThreshold"] = Field(alias="__typename")
    operator: DifferenceOperator = Field(alias="differenceOperator")
    difference_type: DifferenceType = Field(alias="differenceType")
    number_of_windows: int = Field(alias="numberOfWindows")
    value: float


class ValidatorUpdateValidatorVolumeValidatorConfigThresholdDynamicThreshold(BaseModel):
    typename__: Literal["DynamicThreshold"] = Field(alias="__typename")
    sensitivity: float
    decision_bounds_type: Optional[DecisionBoundsType] = Field(
        alias="decisionBoundsType"
    )


class ValidatorUpdateValidatorVolumeValidatorConfigThresholdFixedThreshold(BaseModel):
    typename__: Literal["FixedThreshold"] = Field(alias="__typename")
    operator: ComparisonOperator
    value: float


class WindowCreation(BaseModel):
    errors: List["WindowCreationErrors"]
    window: Optional[
        Annotated[
            Union[
                "WindowCreationWindowWindow",
                "WindowCreationWindowFileWindow",
                "WindowCreationWindowFixedBatchWindow",
                "WindowCreationWindowTumblingWindow",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class WindowCreationErrors(ErrorDetails):
    pass


class WindowCreationWindowWindow(BaseModel):
    typename__: Literal["GlobalWindow", "Window"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowCreationWindowWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowWindowNamespace"


class WindowCreationWindowWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowWindowSourceNamespace"
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


class WindowCreationWindowWindowSourceNamespace(BaseModel):
    id: Any


class WindowCreationWindowWindowNamespace(BaseModel):
    id: Any


class WindowCreationWindowFileWindow(BaseModel):
    typename__: Literal["FileWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowCreationWindowFileWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowFileWindowNamespace"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class WindowCreationWindowFileWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowFileWindowSourceNamespace"
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


class WindowCreationWindowFileWindowSourceNamespace(BaseModel):
    id: Any


class WindowCreationWindowFileWindowNamespace(BaseModel):
    id: Any


class WindowCreationWindowFixedBatchWindow(BaseModel):
    typename__: Literal["FixedBatchWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowCreationWindowFixedBatchWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowFixedBatchWindowNamespace"
    config: "WindowCreationWindowFixedBatchWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class WindowCreationWindowFixedBatchWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowFixedBatchWindowSourceNamespace"
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


class WindowCreationWindowFixedBatchWindowSourceNamespace(BaseModel):
    id: Any


class WindowCreationWindowFixedBatchWindowNamespace(BaseModel):
    id: Any


class WindowCreationWindowFixedBatchWindowConfig(BaseModel):
    batch_size: int = Field(alias="batchSize")
    segmented_batching: bool = Field(alias="segmentedBatching")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs")


class WindowCreationWindowTumblingWindow(BaseModel):
    typename__: Literal["TumblingWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowCreationWindowTumblingWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowTumblingWindowNamespace"
    config: "WindowCreationWindowTumblingWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class WindowCreationWindowTumblingWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowCreationWindowTumblingWindowSourceNamespace"
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


class WindowCreationWindowTumblingWindowSourceNamespace(BaseModel):
    id: Any


class WindowCreationWindowTumblingWindowNamespace(BaseModel):
    id: Any


class WindowCreationWindowTumblingWindowConfig(BaseModel):
    window_size: int = Field(alias="windowSize")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_timeout_disabled: bool = Field(alias="windowTimeoutDisabled")


class WindowUpdate(BaseModel):
    errors: List["WindowUpdateErrors"]
    window: Optional[
        Annotated[
            Union[
                "WindowUpdateWindowWindow",
                "WindowUpdateWindowFileWindow",
                "WindowUpdateWindowFixedBatchWindow",
                "WindowUpdateWindowTumblingWindow",
            ],
            Field(discriminator="typename__"),
        ]
    ]


class WindowUpdateErrors(ErrorDetails):
    pass


class WindowUpdateWindowWindow(BaseModel):
    typename__: Literal["GlobalWindow", "Window"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowUpdateWindowWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowWindowNamespace"


class WindowUpdateWindowWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowWindowSourceNamespace"
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


class WindowUpdateWindowWindowSourceNamespace(BaseModel):
    id: Any


class WindowUpdateWindowWindowNamespace(BaseModel):
    id: Any


class WindowUpdateWindowFileWindow(BaseModel):
    typename__: Literal["FileWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowUpdateWindowFileWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowFileWindowNamespace"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class WindowUpdateWindowFileWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowFileWindowSourceNamespace"
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


class WindowUpdateWindowFileWindowSourceNamespace(BaseModel):
    id: Any


class WindowUpdateWindowFileWindowNamespace(BaseModel):
    id: Any


class WindowUpdateWindowFixedBatchWindow(BaseModel):
    typename__: Literal["FixedBatchWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowUpdateWindowFixedBatchWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowFixedBatchWindowNamespace"
    config: "WindowUpdateWindowFixedBatchWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class WindowUpdateWindowFixedBatchWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowFixedBatchWindowSourceNamespace"
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


class WindowUpdateWindowFixedBatchWindowSourceNamespace(BaseModel):
    id: Any


class WindowUpdateWindowFixedBatchWindowNamespace(BaseModel):
    id: Any


class WindowUpdateWindowFixedBatchWindowConfig(BaseModel):
    batch_size: int = Field(alias="batchSize")
    segmented_batching: bool = Field(alias="segmentedBatching")
    batch_timeout_secs: Optional[int] = Field(alias="batchTimeoutSecs")


class WindowUpdateWindowTumblingWindow(BaseModel):
    typename__: Literal["TumblingWindow"] = Field(alias="__typename")
    id: WindowId
    name: str
    source: "WindowUpdateWindowTumblingWindowSource"
    created_at: datetime = Field(alias="createdAt")
    updated_at: datetime = Field(alias="updatedAt")
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowTumblingWindowNamespace"
    config: "WindowUpdateWindowTumblingWindowConfig"
    data_time_field: JsonPointer = Field(alias="dataTimeField")


class WindowUpdateWindowTumblingWindowSource(BaseModel):
    id: SourceId
    name: str
    resource_name: str = Field(alias="resourceName")
    namespace_id: Any = Field(alias="namespaceId")
    namespace: "WindowUpdateWindowTumblingWindowSourceNamespace"
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


class WindowUpdateWindowTumblingWindowSourceNamespace(BaseModel):
    id: Any


class WindowUpdateWindowTumblingWindowNamespace(BaseModel):
    id: Any


class WindowUpdateWindowTumblingWindowConfig(BaseModel):
    window_size: int = Field(alias="windowSize")
    time_unit: WindowTimeUnit = Field(alias="timeUnit")
    window_timeout_disabled: bool = Field(alias="windowTimeoutDisabled")


ApiKeyDetails.model_rebuild()
CatalogAssetDescriptionDetails.model_rebuild()
CatalogAssetStatsDetails.model_rebuild()
ErrorDetails.model_rebuild()
ChannelCreation.model_rebuild()
ChannelDeletion.model_rebuild()
ChannelUpdate.model_rebuild()
CredentialBase.model_rebuild()
CredentialCreation.model_rebuild()
CredentialSecretChanged.model_rebuild()
CredentialUpdate.model_rebuild()
IdentityDeletion.model_rebuild()
IdentityProviderCreation.model_rebuild()
IdentityProviderDeletion.model_rebuild()
IdentityProviderUpdate.model_rebuild()
LineageEdgeDetails.model_rebuild()
LineageEdgeCreation.model_rebuild()
LineageEdgeSummary.model_rebuild()
LineageGraphDetails.model_rebuild()
UserSummary.model_rebuild()
TeamDetails.model_rebuild()
NamespaceDetails.model_rebuild()
NamespaceDetailsWithFullAvatar.model_rebuild()
NamespaceUpdate.model_rebuild()
NotificationRuleConditionCreation.model_rebuild()
NotificationRuleDetails.model_rebuild()
NotificationRuleCreation.model_rebuild()
NotificationRuleDeletion.model_rebuild()
NotificationRuleUpdate.model_rebuild()
ReferenceSourceConfigDetails.model_rebuild()
SegmentDetails.model_rebuild()
SegmentationDetails.model_rebuild()
SegmentationCreation.model_rebuild()
SegmentationSummary.model_rebuild()
SourceBase.model_rebuild()
SourceCreation.model_rebuild()
SourceUpdate.model_rebuild()
TagDetails.model_rebuild()
TagCreation.model_rebuild()
TagUpdate.model_rebuild()
TeamSummary.model_rebuild()
UserDetails.model_rebuild()
UserCreation.model_rebuild()
UserDeletion.model_rebuild()
UserUpdate.model_rebuild()
ValidatorCreation.model_rebuild()
ValidatorRecommendationApplication.model_rebuild()
ValidatorRecommendationDismissal.model_rebuild()
ValidatorUpdate.model_rebuild()
WindowCreation.model_rebuild()
WindowUpdate.model_rebuild()
