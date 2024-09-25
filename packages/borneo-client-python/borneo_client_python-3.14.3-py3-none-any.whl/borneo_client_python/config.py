# Code generated by smithy-python-codegen DO NOT EDIT.

from dataclasses import dataclass
from typing import Any, Callable, TypeAlias, Union

from smithy_core.aio.interfaces.identity import IdentityResolver
from smithy_core.interceptors import Interceptor
from smithy_core.interfaces import URI
from smithy_core.interfaces.identity import IdentityProperties
from smithy_core.interfaces.retries import RetryStrategy
from smithy_core.retries import SimpleRetryStrategy
from smithy_http.aio.aiohttp import AIOHTTPClient
from smithy_http.aio.auth.apikey import ApiKeyAuthScheme
from smithy_http.aio.endpoints import StaticEndpointResolver
from smithy_http.aio.identity.apikey import ApiKeyIdentity
from smithy_http.aio.interfaces import EndpointResolver, HTTPClient
from smithy_http.aio.interfaces.auth import HTTPAuthScheme
from smithy_http.interfaces import HTTPRequestConfiguration

from .auth import HTTPAuthSchemeResolver
from .models import (
    AddDiscoveredRecipientAsRecipientsInput,
    AddDiscoveredRecipientAsRecipientsOutput,
    ArchiveDiscoveredRecipientInput,
    ArchiveDiscoveredRecipientOutput,
    CreateAndSendDashboardReportInput,
    CreateAndSendDashboardReportOutput,
    CreateAssetInput,
    CreateAssetOutput,
    CreateCategoryInput,
    CreateCategoryOutput,
    CreateDashboardReportInput,
    CreateDashboardReportOutput,
    CreateDepartmentInput,
    CreateDepartmentOutput,
    CreateDomainInput,
    CreateDomainOutput,
    CreateDpiaInput,
    CreateDpiaOutput,
    CreateEmployeeInput,
    CreateEmployeeOutput,
    CreateHeadquarterInput,
    CreateHeadquarterOutput,
    CreateProcessingActivityInput,
    CreateProcessingActivityOutput,
    CreateRecipientInput,
    CreateRecipientOutput,
    CreateScanInput,
    CreateScanOutput,
    CreateThresholdInput,
    CreateThresholdOutput,
    DescribeAccountInput,
    DescribeAccountOutput,
    DescribeAssetInput,
    DescribeAssetOutput,
    DescribeCatalogResourceInput,
    DescribeCatalogResourceOutput,
    DescribeCategoryInput,
    DescribeCategoryOutput,
    DescribeCloudAccountInput,
    DescribeCloudAccountOutput,
    DescribeConnectorInput,
    DescribeConnectorOutput,
    DescribeDashboardReportEditionInput,
    DescribeDashboardReportEditionOutput,
    DescribeDashboardReportInput,
    DescribeDashboardReportOutput,
    DescribeDepartmentInput,
    DescribeDepartmentOutput,
    DescribeDiscoveredRecipientInput,
    DescribeDiscoveredRecipientOutput,
    DescribeDomainInput,
    DescribeDomainOutput,
    DescribeDpiaInput,
    DescribeDpiaOutput,
    DescribeEmployeeInput,
    DescribeEmployeeOutput,
    DescribeErrorInput,
    DescribeErrorOutput,
    DescribeHeadquarterInput,
    DescribeHeadquarterOutput,
    DescribeInspectionResultInput,
    DescribeInspectionResultOutput,
    DescribeInventoryResourceInput,
    DescribeInventoryResourceOutput,
    DescribeIssueInput,
    DescribeIssueOutput,
    DescribeProcessingActivityInput,
    DescribeProcessingActivityOutput,
    DescribeRecipientInput,
    DescribeRecipientOutput,
    DescribeResourceLineageInput,
    DescribeResourceLineageOutput,
    DescribeScanInput,
    DescribeScanIterationInput,
    DescribeScanIterationOutput,
    DescribeScanOutput,
    DescribeThresholdInput,
    DescribeThresholdOutput,
    DescribeTomInput,
    DescribeTomOutput,
    DescribeUserProfileInput,
    DescribeUserProfileOutput,
    DownloadDashboardReportEditionInput,
    DownloadDashboardReportEditionOutput,
    DownloadDashboardReportInput,
    DownloadDashboardReportOutput,
    ListAccessLogsInput,
    ListAccessLogsOutput,
    ListAccountsInput,
    ListAccountsOutput,
    ListAssetsInput,
    ListAssetsOutput,
    ListAuditLogsInput,
    ListAuditLogsOutput,
    ListCatalogLeafResourcesExportInput,
    ListCatalogLeafResourcesExportOutput,
    ListCatalogLeafResourcesInput,
    ListCatalogLeafResourcesOutput,
    ListConnectorsInput,
    ListConnectorsOutput,
    ListDepartmentsForFilterInput,
    ListDepartmentsForFilterOutput,
    ListDepartmentsInput,
    ListDepartmentsOutput,
    ListDiscoveredRecipientsInput,
    ListDiscoveredRecipientsOutput,
    ListDiscoveredRecipientsUsersInput,
    ListDiscoveredRecipientsUsersOutput,
    ListDomainsInput,
    ListDomainsOutput,
    ListEmployeesForFilterInput,
    ListEmployeesForFilterOutput,
    ListEmployeesInput,
    ListEmployeesOutput,
    ListErrorsInput,
    ListErrorsOutput,
    ListEventsInput,
    ListEventsOutput,
    ListHeadquartersInput,
    ListHeadquartersOutput,
    ListInfotypeCategoriesInput,
    ListInfotypeCategoriesOutput,
    ListInsightsFilterInput,
    ListInsightsFilterOutput,
    ListInspectionResultsInput,
    ListInspectionResultsOutput,
    ListInventoryResourcesExportInput,
    ListInventoryResourcesExportOutput,
    ListInventoryResourcesInput,
    ListInventoryResourcesOutput,
    ListIssuesInput,
    ListIssuesOutput,
    ListProcessingActivitiesExportInput,
    ListProcessingActivitiesExportOutput,
    ListProcessingActivitiesInput,
    ListProcessingActivitiesOfRecipientInput,
    ListProcessingActivitiesOfRecipientOutput,
    ListProcessingActivitiesOutput,
    ListProcessingActivityFilterInput,
    ListProcessingActivityFilterOutput,
    ListRecipientFilterInput,
    ListRecipientFilterOutput,
    ListRecipientsExportInput,
    ListRecipientsExportOutput,
    ListRecipientsForFilterInput,
    ListRecipientsForFilterOutput,
    ListRecipientsInput,
    ListRecipientsOutput,
    ListReportSchedulesInput,
    ListReportSchedulesOutput,
    ListReportsEditionInput,
    ListReportsEditionOutput,
    ListScanIterationsInput,
    ListScanIterationsOutput,
    ListScansInput,
    ListScansOutput,
    ListTomsInput,
    ListTomsOutput,
    ListUserProfilesInput,
    ListUserProfilesOutput,
    PageInsightsExportInput,
    PageInsightsExportOutput,
    PauseScanInput,
    PauseScanOutput,
    PollDomainInput,
    PollDomainOutput,
    PrepareDetailedInspectionResultInput,
    PrepareDetailedInspectionResultOutput,
    RemoveAssetInput,
    RemoveAssetOutput,
    RemoveCategoryInput,
    RemoveCategoryOutput,
    RemoveDashboardReportInput,
    RemoveDashboardReportOutput,
    RemoveDepartmentInput,
    RemoveDepartmentOutput,
    RemoveDomainInput,
    RemoveDomainOutput,
    RemoveDpiaInput,
    RemoveDpiaOutput,
    RemoveEmployeeInput,
    RemoveEmployeeOutput,
    RemoveHeadquarterInput,
    RemoveHeadquarterOutput,
    RemoveProcessingActivityInput,
    RemoveProcessingActivityOutput,
    RemoveRecipientInput,
    RemoveRecipientOutput,
    RemoveThresholdInput,
    RemoveThresholdOutput,
    ResumeScanInput,
    ResumeScanOutput,
    StopScanInput,
    StopScanOutput,
    SummarizeClassificationStatsInput,
    SummarizeClassificationStatsOutput,
    SummarizeResourceStatsInput,
    SummarizeResourceStatsOutput,
    UntagResourcesInput,
    UntagResourcesOutput,
    UpdateAssetInput,
    UpdateAssetOutput,
    UpdateCategoryInput,
    UpdateCategoryOutput,
    UpdateDashboardReportInput,
    UpdateDashboardReportOutput,
    UpdateDepartmentInput,
    UpdateDepartmentOutput,
    UpdateDomainInput,
    UpdateDomainOutput,
    UpdateDpiaInput,
    UpdateDpiaOutput,
    UpdateEmployeeInput,
    UpdateEmployeeOutput,
    UpdateHeadquarterInput,
    UpdateHeadquarterOutput,
    UpdateProcessingActivityInput,
    UpdateProcessingActivityOutput,
    UpdateRecipientInput,
    UpdateRecipientOutput,
    UpdateThresholdInput,
    UpdateThresholdOutput,
    UpdateTomInput,
    UpdateTomOutput,
)


_ServiceInterceptor = Union[
    Interceptor[
        AddDiscoveredRecipientAsRecipientsInput,
        AddDiscoveredRecipientAsRecipientsOutput,
        Any,
        Any,
    ],
    Interceptor[
        ArchiveDiscoveredRecipientInput, ArchiveDiscoveredRecipientOutput, Any, Any
    ],
    Interceptor[
        CreateAndSendDashboardReportInput, CreateAndSendDashboardReportOutput, Any, Any
    ],
    Interceptor[CreateAssetInput, CreateAssetOutput, Any, Any],
    Interceptor[CreateCategoryInput, CreateCategoryOutput, Any, Any],
    Interceptor[CreateDashboardReportInput, CreateDashboardReportOutput, Any, Any],
    Interceptor[CreateDepartmentInput, CreateDepartmentOutput, Any, Any],
    Interceptor[CreateDomainInput, CreateDomainOutput, Any, Any],
    Interceptor[CreateDpiaInput, CreateDpiaOutput, Any, Any],
    Interceptor[CreateEmployeeInput, CreateEmployeeOutput, Any, Any],
    Interceptor[CreateHeadquarterInput, CreateHeadquarterOutput, Any, Any],
    Interceptor[
        CreateProcessingActivityInput, CreateProcessingActivityOutput, Any, Any
    ],
    Interceptor[CreateRecipientInput, CreateRecipientOutput, Any, Any],
    Interceptor[CreateScanInput, CreateScanOutput, Any, Any],
    Interceptor[CreateThresholdInput, CreateThresholdOutput, Any, Any],
    Interceptor[DescribeAccountInput, DescribeAccountOutput, Any, Any],
    Interceptor[DescribeAssetInput, DescribeAssetOutput, Any, Any],
    Interceptor[DescribeCatalogResourceInput, DescribeCatalogResourceOutput, Any, Any],
    Interceptor[DescribeCategoryInput, DescribeCategoryOutput, Any, Any],
    Interceptor[DescribeCloudAccountInput, DescribeCloudAccountOutput, Any, Any],
    Interceptor[DescribeConnectorInput, DescribeConnectorOutput, Any, Any],
    Interceptor[DescribeDashboardReportInput, DescribeDashboardReportOutput, Any, Any],
    Interceptor[
        DescribeDashboardReportEditionInput,
        DescribeDashboardReportEditionOutput,
        Any,
        Any,
    ],
    Interceptor[DescribeDepartmentInput, DescribeDepartmentOutput, Any, Any],
    Interceptor[
        DescribeDiscoveredRecipientInput, DescribeDiscoveredRecipientOutput, Any, Any
    ],
    Interceptor[DescribeDomainInput, DescribeDomainOutput, Any, Any],
    Interceptor[DescribeDpiaInput, DescribeDpiaOutput, Any, Any],
    Interceptor[DescribeEmployeeInput, DescribeEmployeeOutput, Any, Any],
    Interceptor[DescribeErrorInput, DescribeErrorOutput, Any, Any],
    Interceptor[DescribeHeadquarterInput, DescribeHeadquarterOutput, Any, Any],
    Interceptor[
        DescribeInspectionResultInput, DescribeInspectionResultOutput, Any, Any
    ],
    Interceptor[
        DescribeInventoryResourceInput, DescribeInventoryResourceOutput, Any, Any
    ],
    Interceptor[DescribeIssueInput, DescribeIssueOutput, Any, Any],
    Interceptor[
        DescribeProcessingActivityInput, DescribeProcessingActivityOutput, Any, Any
    ],
    Interceptor[DescribeRecipientInput, DescribeRecipientOutput, Any, Any],
    Interceptor[DescribeResourceLineageInput, DescribeResourceLineageOutput, Any, Any],
    Interceptor[DescribeScanInput, DescribeScanOutput, Any, Any],
    Interceptor[DescribeScanIterationInput, DescribeScanIterationOutput, Any, Any],
    Interceptor[DescribeThresholdInput, DescribeThresholdOutput, Any, Any],
    Interceptor[DescribeTomInput, DescribeTomOutput, Any, Any],
    Interceptor[DescribeUserProfileInput, DescribeUserProfileOutput, Any, Any],
    Interceptor[DownloadDashboardReportInput, DownloadDashboardReportOutput, Any, Any],
    Interceptor[
        DownloadDashboardReportEditionInput,
        DownloadDashboardReportEditionOutput,
        Any,
        Any,
    ],
    Interceptor[ListAccessLogsInput, ListAccessLogsOutput, Any, Any],
    Interceptor[ListAccountsInput, ListAccountsOutput, Any, Any],
    Interceptor[ListAssetsInput, ListAssetsOutput, Any, Any],
    Interceptor[ListAuditLogsInput, ListAuditLogsOutput, Any, Any],
    Interceptor[
        ListCatalogLeafResourcesInput, ListCatalogLeafResourcesOutput, Any, Any
    ],
    Interceptor[
        ListCatalogLeafResourcesExportInput,
        ListCatalogLeafResourcesExportOutput,
        Any,
        Any,
    ],
    Interceptor[ListConnectorsInput, ListConnectorsOutput, Any, Any],
    Interceptor[ListDepartmentsInput, ListDepartmentsOutput, Any, Any],
    Interceptor[
        ListDepartmentsForFilterInput, ListDepartmentsForFilterOutput, Any, Any
    ],
    Interceptor[
        ListDiscoveredRecipientsInput, ListDiscoveredRecipientsOutput, Any, Any
    ],
    Interceptor[
        ListDiscoveredRecipientsUsersInput,
        ListDiscoveredRecipientsUsersOutput,
        Any,
        Any,
    ],
    Interceptor[ListDomainsInput, ListDomainsOutput, Any, Any],
    Interceptor[ListEmployeesInput, ListEmployeesOutput, Any, Any],
    Interceptor[ListEmployeesForFilterInput, ListEmployeesForFilterOutput, Any, Any],
    Interceptor[ListErrorsInput, ListErrorsOutput, Any, Any],
    Interceptor[ListEventsInput, ListEventsOutput, Any, Any],
    Interceptor[ListHeadquartersInput, ListHeadquartersOutput, Any, Any],
    Interceptor[ListInfotypeCategoriesInput, ListInfotypeCategoriesOutput, Any, Any],
    Interceptor[ListInsightsFilterInput, ListInsightsFilterOutput, Any, Any],
    Interceptor[ListInspectionResultsInput, ListInspectionResultsOutput, Any, Any],
    Interceptor[ListInventoryResourcesInput, ListInventoryResourcesOutput, Any, Any],
    Interceptor[
        ListInventoryResourcesExportInput, ListInventoryResourcesExportOutput, Any, Any
    ],
    Interceptor[ListIssuesInput, ListIssuesOutput, Any, Any],
    Interceptor[
        ListProcessingActivitiesInput, ListProcessingActivitiesOutput, Any, Any
    ],
    Interceptor[
        ListProcessingActivitiesExportInput,
        ListProcessingActivitiesExportOutput,
        Any,
        Any,
    ],
    Interceptor[
        ListProcessingActivitiesOfRecipientInput,
        ListProcessingActivitiesOfRecipientOutput,
        Any,
        Any,
    ],
    Interceptor[
        ListProcessingActivityFilterInput, ListProcessingActivityFilterOutput, Any, Any
    ],
    Interceptor[ListRecipientFilterInput, ListRecipientFilterOutput, Any, Any],
    Interceptor[ListRecipientsInput, ListRecipientsOutput, Any, Any],
    Interceptor[ListRecipientsExportInput, ListRecipientsExportOutput, Any, Any],
    Interceptor[ListRecipientsForFilterInput, ListRecipientsForFilterOutput, Any, Any],
    Interceptor[ListReportSchedulesInput, ListReportSchedulesOutput, Any, Any],
    Interceptor[ListReportsEditionInput, ListReportsEditionOutput, Any, Any],
    Interceptor[ListScanIterationsInput, ListScanIterationsOutput, Any, Any],
    Interceptor[ListScansInput, ListScansOutput, Any, Any],
    Interceptor[ListTomsInput, ListTomsOutput, Any, Any],
    Interceptor[ListUserProfilesInput, ListUserProfilesOutput, Any, Any],
    Interceptor[PageInsightsExportInput, PageInsightsExportOutput, Any, Any],
    Interceptor[PauseScanInput, PauseScanOutput, Any, Any],
    Interceptor[PollDomainInput, PollDomainOutput, Any, Any],
    Interceptor[
        PrepareDetailedInspectionResultInput,
        PrepareDetailedInspectionResultOutput,
        Any,
        Any,
    ],
    Interceptor[RemoveAssetInput, RemoveAssetOutput, Any, Any],
    Interceptor[RemoveCategoryInput, RemoveCategoryOutput, Any, Any],
    Interceptor[RemoveDashboardReportInput, RemoveDashboardReportOutput, Any, Any],
    Interceptor[RemoveDepartmentInput, RemoveDepartmentOutput, Any, Any],
    Interceptor[RemoveDomainInput, RemoveDomainOutput, Any, Any],
    Interceptor[RemoveDpiaInput, RemoveDpiaOutput, Any, Any],
    Interceptor[RemoveEmployeeInput, RemoveEmployeeOutput, Any, Any],
    Interceptor[RemoveHeadquarterInput, RemoveHeadquarterOutput, Any, Any],
    Interceptor[
        RemoveProcessingActivityInput, RemoveProcessingActivityOutput, Any, Any
    ],
    Interceptor[RemoveRecipientInput, RemoveRecipientOutput, Any, Any],
    Interceptor[RemoveThresholdInput, RemoveThresholdOutput, Any, Any],
    Interceptor[ResumeScanInput, ResumeScanOutput, Any, Any],
    Interceptor[StopScanInput, StopScanOutput, Any, Any],
    Interceptor[
        SummarizeClassificationStatsInput, SummarizeClassificationStatsOutput, Any, Any
    ],
    Interceptor[SummarizeResourceStatsInput, SummarizeResourceStatsOutput, Any, Any],
    Interceptor[UntagResourcesInput, UntagResourcesOutput, Any, Any],
    Interceptor[UpdateAssetInput, UpdateAssetOutput, Any, Any],
    Interceptor[UpdateCategoryInput, UpdateCategoryOutput, Any, Any],
    Interceptor[UpdateDashboardReportInput, UpdateDashboardReportOutput, Any, Any],
    Interceptor[UpdateDepartmentInput, UpdateDepartmentOutput, Any, Any],
    Interceptor[UpdateDomainInput, UpdateDomainOutput, Any, Any],
    Interceptor[UpdateDpiaInput, UpdateDpiaOutput, Any, Any],
    Interceptor[UpdateEmployeeInput, UpdateEmployeeOutput, Any, Any],
    Interceptor[UpdateHeadquarterInput, UpdateHeadquarterOutput, Any, Any],
    Interceptor[
        UpdateProcessingActivityInput, UpdateProcessingActivityOutput, Any, Any
    ],
    Interceptor[UpdateRecipientInput, UpdateRecipientOutput, Any, Any],
    Interceptor[UpdateThresholdInput, UpdateThresholdOutput, Any, Any],
    Interceptor[UpdateTomInput, UpdateTomOutput, Any, Any],
]


@dataclass(init=False)
class Config:
    """Configuration for Borneo."""

    interceptors: list[_ServiceInterceptor]
    retry_strategy: RetryStrategy
    http_client: HTTPClient
    http_request_config: HTTPRequestConfiguration | None
    endpoint_resolver: EndpointResolver[Any]
    endpoint_uri: str | URI | None
    http_auth_schemes: dict[str, HTTPAuthScheme[Any, Any, Any, Any]]
    http_auth_scheme_resolver: HTTPAuthSchemeResolver
    api_key_identity_resolver: (
        IdentityResolver[ApiKeyIdentity, IdentityProperties] | None
    )

    def __init__(
        self,
        *,
        interceptors: list[_ServiceInterceptor] | None = None,
        retry_strategy: RetryStrategy | None = None,
        http_client: HTTPClient | None = None,
        http_request_config: HTTPRequestConfiguration | None = None,
        endpoint_resolver: EndpointResolver[Any] | None = None,
        endpoint_uri: str | URI | None = None,
        http_auth_schemes: dict[str, HTTPAuthScheme[Any, Any, Any, Any]] | None = None,
        http_auth_scheme_resolver: HTTPAuthSchemeResolver | None = None,
        api_key_identity_resolver: (
            IdentityResolver[ApiKeyIdentity, IdentityProperties] | None
        ) = None,
    ):
        """Constructor.

        :param interceptors: The list of interceptors, which are hooks that are called
        during the execution of a request.

        :param retry_strategy: The retry strategy for issuing retry tokens and computing
        retry delays.

        :param http_client: The HTTP client used to make requests.

        :param http_request_config: Configuration for individual HTTP requests.

        :param endpoint_resolver: The endpoint resolver used to resolve the final
        endpoint per-operation based on the configuration.

        :param endpoint_uri: A static URI to route requests to.

        :param http_auth_schemes: A map of http auth scheme ids to http auth schemes.

        :param http_auth_scheme_resolver: An http auth scheme resolver that determines
        the auth scheme for each operation.

        :param api_key_identity_resolver: Resolves the API key. Required for operations
        that use API key auth.
        """
        self.interceptors = interceptors or []
        self.retry_strategy = retry_strategy or SimpleRetryStrategy()
        self.http_client = http_client or AIOHTTPClient()
        self.http_request_config = http_request_config
        self.endpoint_resolver = endpoint_resolver or StaticEndpointResolver()
        self.endpoint_uri = endpoint_uri
        self.http_auth_schemes = http_auth_schemes or {
            "smithy.api#httpApiKeyAuth": ApiKeyAuthScheme(),
        }

        self.http_auth_scheme_resolver = (
            http_auth_scheme_resolver or HTTPAuthSchemeResolver()
        )
        self.api_key_identity_resolver = api_key_identity_resolver

    def set_http_auth_scheme(self, scheme: HTTPAuthScheme[Any, Any, Any, Any]) -> None:
        """Sets the implementation of an auth scheme.

        Using this method ensures the correct key is used.

        :param scheme: The auth scheme to add.
        """
        self.http_auth_schemes[scheme.scheme_id] = scheme


# A callable that allows customizing the config object on each request.
Plugin: TypeAlias = Callable[[Config], None]
