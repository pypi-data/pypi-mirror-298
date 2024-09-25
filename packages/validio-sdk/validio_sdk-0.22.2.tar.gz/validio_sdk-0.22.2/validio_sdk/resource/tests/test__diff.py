import pytest

from validio_sdk.graphql_client.input_types import (
    NumericDistributionMetric,
    NumericMetric,
    WindowTimeUnit,
)
from validio_sdk.resource import FieldSelector
from validio_sdk.resource._diff import (
    CascadeReplacementReason,
    DiffContext,
    GraphDiff,
    ReplacementContext,
    ResourceUpdate,
    ResourceUpdates,
    _compute_replacements,
    _diff_resource_graph,
)
from validio_sdk.resource._resource import ResourceGraph
from validio_sdk.resource.channels import Channel, SlackChannel, WebhookChannel
from validio_sdk.resource.credentials import (
    AwsCredential,
    Credential,
    DemoCredential,
)
from validio_sdk.resource.filters import NullFilter
from validio_sdk.resource.notification_rules import (
    Conditions,
    NotificationRule,
    SourceNotificationRuleCondition,
    TagNotificationRuleCondition,
)
from validio_sdk.resource.replacement import ImmutableFieldReplacementReason
from validio_sdk.resource.segmentations import Segmentation
from validio_sdk.resource.sources import (
    DemoSource,
    Source,
)
from validio_sdk.resource.thresholds import (
    ComparisonOperator,
    DynamicThreshold,
    FixedThreshold,
)
from validio_sdk.resource.validators import (
    NumericDistributionValidator,
    NumericValidator,
    Reference,
    Validator,
)
from validio_sdk.resource.windows import TumblingWindow, Window


def _add_namespace(namespace: str, ctx: DiffContext) -> None:
    for f in DiffContext.fields():
        for r in getattr(ctx, f).values():
            r._namespace = namespace


def create_diff_context(
    credentials: dict[str, Credential] | None = None,
    channels: dict[str, Channel] | None = None,
    sources: dict[str, Source] | None = None,
    windows: dict[str, Window] | None = None,
    segmentations: dict[str, Segmentation] | None = None,
    validators: dict[str, Validator] | None = None,
    notification_rules: dict[str, NotificationRule] | None = None,
) -> DiffContext:
    return DiffContext(
        credentials=credentials or {},
        channels=channels or {},
        sources=sources or {},
        windows=windows or {},
        segmentations=segmentations or {},
        validators=validators or {},
        notification_rules=notification_rules or {},
    )


def create_resource_updates(
    credentials: dict[str, ResourceUpdate] | None = None,
    channels: dict[str, ResourceUpdate] | None = None,
    sources: dict[str, ResourceUpdate] | None = None,
    windows: dict[str, ResourceUpdate] | None = None,
    segmentations: dict[str, ResourceUpdate] | None = None,
    validators: dict[str, ResourceUpdate] | None = None,
    notification_rules: dict[str, ResourceUpdate] | None = None,
) -> ResourceUpdates:
    return ResourceUpdates(
        credentials=credentials or {},
        channels=channels or {},
        sources=sources or {},
        windows=windows or {},
        segmentations=segmentations or {},
        validators=validators or {},
        notification_rules=notification_rules or {},
    )


def create_graph_diff(
    to_create: DiffContext | None = None,
    to_delete: DiffContext | None = None,
    to_update: ResourceUpdates | None = None,
    replacement_ctx: ReplacementContext | None = None,
) -> GraphDiff:
    return GraphDiff(
        to_create=to_create or DiffContext(),
        to_delete=to_delete or DiffContext(),
        to_update=to_update or create_resource_updates(),
        replacement_ctx=replacement_ctx or ReplacementContext(),
    )


# ruff: noqa: PLR0915
def test_diff_should_detect_create_update_delete_operations_on_resources() -> None:
    namespace = "my_namespace"
    manifest_g = ResourceGraph()
    server_g = ResourceGraph()

    manifest_c1 = DemoCredential("c1", __internal__=manifest_g)
    manifest_s1 = DemoSource("s1", manifest_c1)
    manifest_s2 = DemoSource("s2", manifest_c1)  # To be created
    manifest_seg1 = Segmentation("seg1", manifest_s1, ["city"])
    manifest_seg2 = Segmentation("seg2", manifest_s1, ["gender"])  # To be created
    manifest_w1 = TumblingWindow("w1", manifest_s1, "d", 1, WindowTimeUnit.DAY)
    manifest_w2 = TumblingWindow(
        "w2", manifest_s1, "d", 2, WindowTimeUnit.DAY
    )  # To be created
    manifest_w3 = TumblingWindow(
        "w3",
        manifest_s1,
        "d",
        3,
        WindowTimeUnit.DAY,
    )  # Update
    manifest_v1 = NumericValidator(
        "v1", manifest_w1, manifest_seg1, NumericMetric.MAX, "a"
    )
    manifest_v2 = NumericValidator(
        "v2",
        manifest_w1,
        manifest_seg1,
        NumericMetric.MEAN,
        "b",
    )  # To be created
    manifest_ch1 = SlackChannel(
        "ch1",
        "app",
        "web",
        "tz",
        __internal__=manifest_g,
    )
    manifest_ch2 = SlackChannel(
        "ch2",
        "app",
        "web",
        "tz",
        __internal__=manifest_g,
    )  # To be created
    manifest_ch3 = SlackChannel(
        "ch3",
        "app",
        "web",
        None,
        __internal__=manifest_g,
    )  # To be updated
    manifest_cond1 = Conditions(
        source_condition=SourceNotificationRuleCondition([manifest_s1])
    )
    manifest_r1 = NotificationRule("r1", manifest_ch1, conditions=manifest_cond1)
    manifest_r2 = NotificationRule(
        "r2", manifest_ch1, conditions=manifest_cond1
    )  # To be created
    manifest_r3 = NotificationRule(
        "r3", manifest_ch1, conditions=manifest_cond1
    )  # To be updated

    server_c1 = DemoCredential("c1", __internal__=server_g)
    server_s1 = DemoSource("s1", server_c1)
    server_s3 = DemoSource("s3", server_c1)  # To be deleted
    server_seg1 = Segmentation("seg1", server_s1, ["city"])
    server_seg3 = Segmentation("seg3", server_s1, ["country"])  # To be deleted
    server_w1 = TumblingWindow("w1", server_s1, "d", 1, WindowTimeUnit.DAY)
    server_w3 = TumblingWindow("w3", server_s1, "d", 4, WindowTimeUnit.DAY)
    server_w4 = TumblingWindow(
        "w4", server_s1, "d", 5, WindowTimeUnit.DAY
    )  # To be deleted
    server_v1 = NumericValidator("v1", server_w1, server_seg1, NumericMetric.MAX, "a")
    server_v3 = NumericValidator(
        "v3", server_w1, server_seg1, NumericMetric.MAX, "d"
    )  # Delete
    server_ch1 = SlackChannel("ch1", "app", "web", "tz", __internal__=server_g)
    server_ch3 = SlackChannel("ch3", "app", "web", "tz", __internal__=server_g)
    server_ch4 = SlackChannel(
        "ch4",
        "app",
        "web",
        "tz",
        __internal__=server_g,
    )  # To be deleted
    server_cond1 = Conditions(
        source_condition=SourceNotificationRuleCondition([manifest_s1])
    )
    server_r1 = NotificationRule("r1", server_ch1, conditions=server_cond1)
    server_r3 = NotificationRule("r3", server_ch1)
    server_r4 = NotificationRule(
        "r4", server_ch1, conditions=server_cond1
    )  # To be deleted

    manifest_ctx = create_diff_context(
        credentials={manifest_c1.name: manifest_c1},
        sources={
            manifest_s1.name: manifest_s1,
            manifest_s2.name: manifest_s2,
        },
        segmentations={
            manifest_seg1.name: manifest_seg1,
            manifest_seg2.name: manifest_seg2,
        },
        windows={
            manifest_w1.name: manifest_w1,
            manifest_w2.name: manifest_w2,
            manifest_w3.name: manifest_w3,
        },
        validators={
            manifest_v1.name: manifest_v1,
            manifest_v2.name: manifest_v2,
        },
        channels={
            manifest_ch1.name: manifest_ch1,
            manifest_ch2.name: manifest_ch2,
            manifest_ch3.name: manifest_ch3,
        },
        notification_rules={
            manifest_r1.name: manifest_r1,
            manifest_r2.name: manifest_r2,
            manifest_r3.name: manifest_r3,
        },
    )

    server_ctx = create_diff_context(
        credentials={server_c1.name: server_c1},
        sources={
            server_s1.name: server_s1,
            server_s3.name: server_s3,
        },
        segmentations={
            server_seg1.name: server_seg1,
            server_seg3.name: server_seg3,
        },
        windows={
            server_w1.name: server_w1,
            server_w3.name: server_w3,
            server_w4.name: server_w4,
        },
        validators={
            server_v1.name: server_v1,
            server_v3.name: server_v3,
        },
        channels={
            server_ch1.name: server_ch1,
            server_ch3.name: server_ch3,
            server_ch4.name: server_ch4,
        },
        notification_rules={
            server_r1.name: server_r1,
            server_r3.name: server_r3,
            server_r4.name: server_r4,
        },
    )

    expected = create_graph_diff(
        to_create=DiffContext(
            sources={manifest_s2.name: manifest_s2},
            segmentations={manifest_seg2.name: manifest_seg2},
            windows={manifest_w2.name: manifest_w2},
            validators={manifest_v2.name: manifest_v2},
            channels={manifest_ch2.name: manifest_ch2},
            notification_rules={manifest_r2.name: manifest_r2},
        ),
        to_delete=DiffContext(
            sources={server_s3.name: server_s3},
            segmentations={server_seg3.name: server_seg3},
            windows={server_w4.name: server_w4},
            validators={server_v3.name: server_v3},
            channels={server_ch4.name: server_ch4},
            notification_rules={server_r4.name: server_r4},
        ),
        to_update=create_resource_updates(
            windows={
                manifest_w3.name: ResourceUpdate(
                    manifest_w3,
                    server_w3,
                )
            },
            channels={
                manifest_ch3.name: ResourceUpdate(
                    manifest_ch3,
                    server_ch3,
                ),
            },
            notification_rules={
                manifest_r3.name: ResourceUpdate(
                    manifest_r3,
                    server_r3,
                )
            },
        ),
    )

    _add_namespace(namespace, server_ctx)
    assert expected == _diff_resource_graph(namespace, manifest_ctx, server_ctx)


def test_diff_replace_with_cascade() -> None:
    namespace = "my_namespace"
    manifest_g = ResourceGraph()
    server_g = ResourceGraph()

    manifest_c1 = DemoCredential("c1", __internal__=manifest_g)
    manifest_c2 = DemoCredential("c2", __internal__=manifest_g)

    # s1 switches from one credential to another => replace.
    manifest_s1 = DemoSource("s1", manifest_c2)
    # w1 belongs to s1, => replace.
    manifest_w1 = TumblingWindow("w1", manifest_s1, "d", 1, WindowTimeUnit.DAY)
    # seg1 belongs to s1 => replace.
    manifest_seg1 = Segmentation("seg1", manifest_s1, ["city"])
    # v1 and v2 belong to s1 => replace.
    manifest_v1 = NumericValidator(
        "v1", manifest_w1, manifest_seg1, NumericMetric.MAX, "a"
    )
    manifest_v2 = NumericValidator(
        "v2", manifest_w1, manifest_seg1, NumericMetric.MAX, "b"
    )

    manifest_ch1 = SlackChannel("ch1", "app", "web", "tz", __internal__=manifest_g)
    manifest_ch2 = SlackChannel("ch2", "app", "web", "tz", __internal__=manifest_g)
    # r1 switches from one credential to another => replace.
    manifest_r1 = NotificationRule("r1", manifest_ch2)

    server_c1 = DemoCredential("c1", __internal__=server_g)
    server_c2 = DemoCredential("c2", __internal__=server_g)
    server_s1 = DemoSource("s1", server_c1)
    server_w1 = TumblingWindow("w1", server_s1, "d", 1, WindowTimeUnit.DAY)
    server_seg1 = Segmentation("seg1", server_s1, ["city"])
    server_v1 = NumericValidator("v1", server_w1, server_seg1, NumericMetric.MAX, "a")
    server_v2 = NumericValidator("v2", server_w1, server_seg1, NumericMetric.MAX, "b")
    server_ch1 = SlackChannel("ch1", "app", "web", "tz", __internal__=server_g)
    server_ch2 = SlackChannel("ch2", "app", "web", "tz", __internal__=server_g)
    server_r1 = NotificationRule("r1", server_ch1)

    manifest_ctx = create_diff_context(
        credentials={
            manifest_c1.name: manifest_c1,
            manifest_c2.name: manifest_c2,
        },
        sources={
            manifest_s1.name: manifest_s1,
        },
        segmentations={
            manifest_seg1.name: manifest_seg1,
        },
        windows={
            manifest_w1.name: manifest_w1,
        },
        validators={
            manifest_v1.name: manifest_v1,
            manifest_v2.name: manifest_v2,
        },
        channels={
            manifest_ch1.name: manifest_ch1,
            manifest_ch2.name: manifest_ch2,
        },
        notification_rules={
            manifest_r1.name: manifest_r1,
        },
    )

    server_ctx = create_diff_context(
        credentials={
            server_c1.name: server_c1,
            server_c2.name: server_c2,
        },
        sources={
            server_s1.name: server_s1,
        },
        segmentations={
            server_seg1.name: server_seg1,
        },
        windows={
            server_w1.name: server_w1,
        },
        validators={
            server_v1.name: server_v1,
            server_v2.name: server_v2,
        },
        channels={
            server_ch1.name: server_ch1,
            server_ch2.name: server_ch2,
        },
        notification_rules={
            server_r1.name: server_r1,
        },
    )

    expected = create_graph_diff(
        to_create=DiffContext(
            sources={manifest_s1.name: manifest_s1},
            segmentations={manifest_seg1.name: manifest_seg1},
            windows={
                manifest_w1.name: manifest_w1,
            },
            validators={
                manifest_v1.name: manifest_v1,
                manifest_v2.name: manifest_v2,
            },
            notification_rules={manifest_r1.name: manifest_r1},
        ),
        to_delete=DiffContext(
            sources={server_s1.name: server_s1},
            segmentations={server_seg1.name: server_seg1},
            windows={server_w1.name: server_w1},
            validators={
                server_v1.name: server_v1,
                server_v2.name: server_v2,
            },
            notification_rules={server_r1.name: server_r1},
        ),
        replacement_ctx=ReplacementContext(
            sources={
                manifest_s1.name: ImmutableFieldReplacementReason(
                    field_name="credential_name",
                    resource_update=ResourceUpdate(
                        manifest_s1,
                        server_s1,
                        replacement_field="credential_name",
                    ),
                )
            },
            segmentations={
                manifest_seg1.name: CascadeReplacementReason(
                    parent_resource_cls=DemoSource,
                    parent_resource_name=manifest_s1.name,
                )
            },
            windows={
                manifest_w1.name: CascadeReplacementReason(
                    parent_resource_cls=DemoSource,
                    parent_resource_name=manifest_s1.name,
                )
            },
            validators={
                manifest_v1.name: CascadeReplacementReason(
                    parent_resource_cls=DemoSource,
                    parent_resource_name=manifest_s1.name,
                ),
                manifest_v2.name: CascadeReplacementReason(
                    parent_resource_cls=DemoSource,
                    parent_resource_name=manifest_s1.name,
                ),
            },
            notification_rules={
                manifest_r1.name: ImmutableFieldReplacementReason(
                    field_name="channel_name",
                    resource_update=ResourceUpdate(
                        manifest_r1,
                        server_r1,
                        replacement_field="channel_name",
                    ),
                ),
            },
        ),
    )

    _add_namespace(namespace, server_ctx)
    actual = _diff_resource_graph(namespace, manifest_ctx, server_ctx)
    _compute_replacements(
        manifest_ctx=manifest_ctx,
        server_ctx=server_ctx,
        graph_diff=actual,
    )
    assert expected == actual


def test_diff_replace_without_cascade() -> None:
    namespace = "my_namespace"
    manifest_g = ResourceGraph()
    server_g = ResourceGraph()

    manifest_c1 = DemoCredential("c1", __internal__=manifest_g)

    manifest_s1 = DemoSource("s1", manifest_c1)
    manifest_s2 = DemoSource("s2", manifest_c1)
    manifest_w1 = TumblingWindow("w1", manifest_s1, "d", 1, WindowTimeUnit.DAY)
    manifest_w2 = TumblingWindow("w2", manifest_s1, "updated", 1, WindowTimeUnit.DAY)
    manifest_seg1 = Segmentation("seg1", manifest_s1, ["city"])
    manifest_seg2 = Segmentation("seg2", manifest_s1, ["updated"])
    manifest_v1 = NumericValidator(
        "v1", manifest_w1, manifest_seg1, NumericMetric.MAX, "updated"
    )
    manifest_v2 = NumericValidator(
        "v2", manifest_w1, manifest_seg1, NumericMetric.MAX, "b"
    )
    manifest_v3 = NumericValidator(
        "v3", manifest_w1, manifest_seg1, NumericMetric.MAX, "b"
    )
    manifest_v4 = NumericValidator(
        "v4", manifest_w1, manifest_seg1, NumericMetric.MAX, "b"
    )
    # v6 switches from fixed to dynamic threshold => replace
    manifest_v6 = NumericValidator(
        "v6",
        manifest_w1,
        manifest_seg1,
        NumericMetric.MAX,
        "a",
        threshold=DynamicThreshold(3),
    )

    server_c1 = DemoCredential("c1", __internal__=server_g)
    server_s1 = DemoSource("s1", server_c1)
    server_s2 = DemoSource("s2", server_c1)
    server_w1 = TumblingWindow("w1", server_s1, "d", 1, WindowTimeUnit.DAY)
    server_w2 = TumblingWindow("w2", server_s1, "d", 1, WindowTimeUnit.DAY)
    server_seg1 = Segmentation("seg1", server_s1, ["city"])
    server_seg2 = Segmentation("seg2", server_s1, ["city"])
    server_v1 = NumericValidator("v1", server_w1, server_seg1, NumericMetric.MAX, "a")
    server_v2 = NumericValidator("v2", server_w1, server_seg1, NumericMetric.MAX, "b")
    server_v3 = NumericValidator("v3", server_w1, server_seg1, NumericMetric.MAX, "b")
    server_v5 = NumericValidator("v5", server_w1, server_seg1, NumericMetric.MAX, "b")
    server_v6 = NumericValidator(
        "v6",
        server_w1,
        server_seg1,
        NumericMetric.MAX,
        "a",
        threshold=FixedThreshold(0.1, ComparisonOperator.EQUAL),
    )

    manifest_ctx = create_diff_context(
        credentials={
            manifest_c1.name: manifest_c1,
        },
        sources={
            manifest_s1.name: manifest_s1,
            manifest_s2.name: manifest_s2,
        },
        segmentations={
            manifest_seg1.name: manifest_seg1,
            manifest_seg2.name: manifest_seg2,
        },
        windows={
            manifest_w1.name: manifest_w1,
            manifest_w2.name: manifest_w2,
        },
        validators={
            manifest_v1.name: manifest_v1,
            manifest_v2.name: manifest_v2,
            manifest_v3.name: manifest_v3,
            manifest_v4.name: manifest_v4,
            manifest_v6.name: manifest_v6,
        },
    )

    server_ctx = create_diff_context(
        credentials={
            server_c1.name: server_c1,
        },
        sources={
            server_s1.name: server_s1,
            server_s2.name: server_s2,
        },
        segmentations={
            server_seg1.name: server_seg1,
            server_seg2.name: server_seg2,
        },
        windows={
            server_w1.name: server_w1,
            server_w2.name: server_w2,
        },
        validators={
            server_v1.name: server_v1,
            server_v2.name: server_v2,
            server_v3.name: server_v3,
            server_v5.name: server_v5,
            server_v6.name: server_v6,
        },
    )

    expected = create_graph_diff(
        to_create=DiffContext(
            segmentations={
                manifest_seg2.name: manifest_seg2,
            },
            windows={
                manifest_w2.name: manifest_w2,
            },
            validators={
                manifest_v1.name: manifest_v1,
                manifest_v4.name: manifest_v4,
                manifest_v6.name: manifest_v6,
            },
        ),
        to_delete=DiffContext(
            segmentations={server_seg2.name: server_seg2},
            windows={server_w2.name: server_w2},
            validators={
                server_v1.name: server_v1,
                server_v5.name: server_v5,
                server_v6.name: server_v6,
            },
        ),
        replacement_ctx=ReplacementContext(
            segmentations={
                manifest_seg2.name: ImmutableFieldReplacementReason(
                    field_name="fields",
                    resource_update=ResourceUpdate(
                        manifest_seg2,
                        server_seg2,
                        replacement_field="fields",
                    ),
                )
            },
            windows={
                manifest_w2.name: ImmutableFieldReplacementReason(
                    field_name="data_time_field",
                    resource_update=ResourceUpdate(
                        manifest_w2,
                        server_w2,
                        replacement_field="data_time_field",
                    ),
                )
            },
            validators={
                manifest_v1.name: ImmutableFieldReplacementReason(
                    field_name="source_field",
                    resource_update=ResourceUpdate(
                        manifest_v1,
                        server_v1,
                        replacement_field="source_field",
                    ),
                ),
                manifest_v6.name: ImmutableFieldReplacementReason(
                    field_name="threshold",
                    resource_update=ResourceUpdate(
                        manifest_v6,
                        server_v6,
                        replacement_field="threshold",
                    ),
                ),
            },
        ),
    )

    _add_namespace(namespace, server_ctx)
    actual = _diff_resource_graph(namespace, manifest_ctx, server_ctx)
    _compute_replacements(
        manifest_ctx=manifest_ctx,
        server_ctx=server_ctx,
        graph_diff=actual,
    )
    assert expected == actual


def test_diff_replace_cascade_with_conflicting_ops() -> None:
    """
    Replacing a resource that already has a create/update/delete
    operation ongoing.
    """
    namespace = "my_namespace"
    manifest_g = ResourceGraph()
    server_g = ResourceGraph()

    manifest_c1 = DemoCredential("c1", __internal__=manifest_g)

    manifest_s1 = DemoSource("s1", manifest_c1)
    # Updated both mutable and immutable property => replace
    manifest_w1 = TumblingWindow("w1", manifest_s1, "updated", 2, WindowTimeUnit.DAY)
    manifest_seg1 = Segmentation("seg1", manifest_s1, ["city"])
    # Validator to create
    manifest_v1 = NumericValidator(
        "v1", manifest_w1, manifest_seg1, NumericMetric.MAX, "updated"
    )
    # Validator to update
    manifest_v2 = NumericDistributionValidator(
        name="v2",
        window=manifest_w1,
        segmentation=manifest_seg1,
        threshold=DynamicThreshold(2),
        metric=NumericDistributionMetric.MAXIMUM_RATIO,
        source_field="a",
        reference_source_field="b",
        filter=NullFilter(field="abc"),
        reference=Reference(
            manifest_s1,
            manifest_w1,
            1,
            0,
            NullFilter(field="abc"),
        ),
    )

    server_c1 = DemoCredential("c1", __internal__=server_g)
    server_s1 = DemoSource("s1", server_c1)
    server_w1 = TumblingWindow("w1", server_s1, "d", 1, WindowTimeUnit.DAY)
    server_seg1 = Segmentation("seg1", server_s1, ["city"])
    server_v2 = NumericDistributionValidator(
        name="v2",
        window=server_w1,
        segmentation=server_seg1,
        threshold=DynamicThreshold(2),
        metric=NumericDistributionMetric.MAXIMUM_RATIO,
        source_field="a",
        reference_source_field="b",
        filter=NullFilter(field="abc"),
        reference=Reference(
            server_s1,
            server_w1,
            10,
            1,
            NullFilter(field="abc"),
        ),
    )
    # Validator to delete
    server_v3 = NumericValidator("v3", server_w1, server_seg1, NumericMetric.MAX, "b")

    manifest_ctx = create_diff_context(
        credentials={
            manifest_c1.name: manifest_c1,
        },
        sources={
            manifest_s1.name: manifest_s1,
        },
        segmentations={
            manifest_seg1.name: manifest_seg1,
        },
        windows={
            manifest_w1.name: manifest_w1,
        },
        validators={
            manifest_v1.name: manifest_v1,
            manifest_v2.name: manifest_v2,
        },
    )

    server_ctx = create_diff_context(
        credentials={
            server_c1.name: server_c1,
        },
        sources={
            server_s1.name: server_s1,
        },
        segmentations={
            server_seg1.name: server_seg1,
        },
        windows={
            server_w1.name: server_w1,
        },
        validators={
            server_v2.name: server_v2,
            server_v3.name: server_v3,
        },
    )

    expected = create_graph_diff(
        to_create=DiffContext(
            windows={
                manifest_w1.name: manifest_w1,
            },
            validators={
                manifest_v1.name: manifest_v1,
                manifest_v2.name: manifest_v2,
            },
        ),
        to_delete=DiffContext(
            windows={server_w1.name: server_w1},
            validators={
                server_v2.name: server_v2,
                server_v3.name: server_v3,
            },
        ),
        replacement_ctx=ReplacementContext(
            windows={
                manifest_w1.name: ImmutableFieldReplacementReason(
                    field_name="data_time_field",
                    resource_update=ResourceUpdate(
                        manifest_w1,
                        server_w1,
                        replacement_field="data_time_field",
                    ),
                )
            },
            validators={
                manifest_v1.name: CascadeReplacementReason(
                    parent_resource_cls=TumblingWindow,
                    parent_resource_name=manifest_w1.name,
                ),
                manifest_v2.name: CascadeReplacementReason(
                    parent_resource_cls=TumblingWindow,
                    parent_resource_name=manifest_w1.name,
                ),
            },
        ),
    )

    _add_namespace(namespace, server_ctx)
    actual = _diff_resource_graph(namespace, manifest_ctx, server_ctx)
    _compute_replacements(
        manifest_ctx=manifest_ctx,
        server_ctx=server_ctx,
        graph_diff=actual,
    )
    assert expected == actual


@pytest.mark.parametrize(
    ("filter_field", "reference_filter_field", "offset", "expect_update"),
    [
        ("age", "age10", 2, False),
        ("age2", "age10", 2, True),
        ("age", "age10", 3, True),
        ("age", "age", 2, True),
    ],
)
def test_diff_should_detect_updates_on_nested_objects(
    filter_field: FieldSelector,
    reference_filter_field: FieldSelector,
    offset: int,
    expect_update: bool,
) -> None:
    namespace = "my_namespace"
    manifest_g = ResourceGraph()
    server_g = ResourceGraph()

    manifest_c1 = DemoCredential("c1", __internal__=manifest_g)
    manifest_s1 = DemoSource("s1", manifest_c1)
    manifest_seg1 = Segmentation("seg1", manifest_s1, ["city"])
    manifest_w1 = TumblingWindow("w1", manifest_s1, "d", 1, WindowTimeUnit.DAY)

    manifest_v = NumericDistributionValidator(
        name="v1",
        window=manifest_w1,
        segmentation=manifest_seg1,
        threshold=DynamicThreshold(2),
        metric=NumericDistributionMetric.MAXIMUM_RATIO,
        source_field="a",
        reference_source_field="b",
        filter=NullFilter(field=filter_field),
        reference=Reference(
            manifest_s1,
            manifest_w1,
            1,
            offset,
            NullFilter(field=reference_filter_field),
        ),
    )

    manifest_ch1 = WebhookChannel(
        name="ch1",
        application_link_url="link",
        webhook_url="url",
        auth_header="header",
        __internal__=manifest_g,
    )

    manifest_nr1 = NotificationRule(
        name="nr1",
        channel=manifest_ch1,
        conditions=Conditions(
            tag_conditions=[TagNotificationRuleCondition(tags={"label": "a"})]
        ),
    )

    manifest_nr2 = NotificationRule(
        name="nr2",
        channel=manifest_ch1,
        conditions=Conditions(
            tag_conditions=[
                TagNotificationRuleCondition(tags={"label": "a"}),
                TagNotificationRuleCondition(tags={"another_label": "a"}),
            ]
        ),
    )

    server_c1 = DemoCredential("c1", __internal__=server_g)
    server_s1 = DemoSource("s1", server_c1)
    server_seg1 = Segmentation("seg1", server_s1, ["city"])
    server_w1 = TumblingWindow("w1", server_s1, "d", 1, WindowTimeUnit.DAY)
    server_v = NumericDistributionValidator(
        name="v1",
        window=server_w1,
        segmentation=server_seg1,
        threshold=DynamicThreshold(2),
        metric=NumericDistributionMetric.MAXIMUM_RATIO,
        source_field="a",
        reference_source_field="b",
        filter=NullFilter(field="age"),
        reference=Reference(server_s1, server_w1, 1, 2, NullFilter(field="age10")),
    )

    server_ch1 = WebhookChannel(
        name="ch1",
        application_link_url="link",
        webhook_url="url",
        auth_header="header",
        __internal__=server_g,
    )

    server_nr1 = NotificationRule(
        name="nr1",
        channel=server_ch1,
        conditions=Conditions(
            tag_conditions=[TagNotificationRuleCondition(tags={"label": "b"})]
        ),
    )

    server_nr2 = NotificationRule(
        name="nr2",
        channel=server_ch1,
        conditions=Conditions(
            tag_conditions=[
                TagNotificationRuleCondition(tags={"label": "b"}),
                TagNotificationRuleCondition(tags={"another_label": "b"}),
            ]
        ),
    )

    manifest_ctx = create_diff_context(
        credentials={manifest_c1.name: manifest_c1},
        sources={manifest_s1.name: manifest_s1},
        segmentations={manifest_seg1.name: manifest_seg1},
        windows={manifest_w1.name: manifest_w1},
        validators={manifest_v.name: manifest_v},
        notification_rules={
            manifest_nr1.name: manifest_nr1,
            manifest_nr2.name: manifest_nr2,
        },
    )
    server_ctx = create_diff_context(
        credentials={server_c1.name: server_c1},
        sources={server_s1.name: server_s1},
        segmentations={server_seg1.name: server_seg1},
        windows={server_w1.name: server_w1},
        validators={server_v.name: server_v},
        notification_rules={server_nr1.name: server_nr1, server_nr2.name: server_nr2},
    )

    expected = create_graph_diff(
        to_update=create_resource_updates(
            validators=(
                {
                    manifest_v.name: ResourceUpdate(
                        manifest_v,
                        server_v,
                    ),
                }
                if expect_update
                else {}
            ),
            notification_rules=(
                {
                    manifest_nr1.name: ResourceUpdate(manifest_nr1, server_nr1),
                    manifest_nr2.name: ResourceUpdate(manifest_nr2, server_nr2),
                }
            ),
        )
    )

    _add_namespace(namespace, server_ctx)
    assert expected == _diff_resource_graph(namespace, manifest_ctx, server_ctx)


def test_diff_should_ignore_update_on_ignore_changes() -> None:
    namespace = "my_namespace"
    manifest_g = ResourceGraph()
    server_g = ResourceGraph()

    # c1 has diff, but ignored changes
    manifest_c1 = AwsCredential(
        name="c1",
        access_key="ak1",
        secret_key="sk1",
        ignore_changes=True,
        __internal__=manifest_g,
    )
    # c2 has diff, and doesn't ignore changes
    manifest_c2 = AwsCredential(
        name="c2",
        access_key="ak2",
        secret_key="sk2",
        ignore_changes=False,
        __internal__=manifest_g,
    )
    # c3 is new, and ignores changes.
    manifest_c3 = AwsCredential(
        name="c3",
        access_key="ak3",
        secret_key="sk3",
        ignore_changes=True,
        __internal__=manifest_g,
    )

    server_c1 = AwsCredential(
        name="c1",
        access_key="ak1old",
        secret_key="sk1old",
        ignore_changes=True,
        __internal__=server_g,
    )
    server_c2 = AwsCredential(
        name="c2",
        access_key="ak2old",
        secret_key="sk2old",
        ignore_changes=False,
        __internal__=server_g,
    )
    # c4 is being deleted and ignores changes.
    server_c4 = AwsCredential(
        name="c4",
        access_key="ak4",
        secret_key="sk4",
        ignore_changes=True,
        __internal__=server_g,
    )

    manifest_ctx = create_diff_context(
        credentials={
            manifest_c1.name: manifest_c1,
            manifest_c2.name: manifest_c2,
            manifest_c3.name: manifest_c3,
        },
    )
    server_ctx = create_diff_context(
        credentials={
            server_c1.name: server_c1,
            server_c2.name: server_c2,
            server_c4.name: server_c4,
        },
    )

    expected = create_graph_diff(
        to_create=DiffContext(
            credentials={manifest_c3.name: manifest_c3},
        ),
        to_delete=DiffContext(
            credentials={server_c4.name: server_c4},
        ),
        to_update=create_resource_updates(
            credentials={manifest_c2.name: ResourceUpdate(manifest_c2, server_c2)},
        ),
    )

    _add_namespace(namespace, server_ctx)
    assert expected == _diff_resource_graph(namespace, manifest_ctx, server_ctx)
