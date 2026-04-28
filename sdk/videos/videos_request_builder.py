from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from ..models.github_com_rixlhq_api_internal_errors.error_response import ErrorResponse
    from ..models.pagination.paginated_response_video import PaginatedResponseVideo
    from .item.with_video_item_request_builder import WithVideoItemRequestBuilder
    from .languages.languages_request_builder import LanguagesRequestBuilder
    from .upload.upload_request_builder import UploadRequestBuilder

class VideosRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /videos
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new VideosRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/videos{?limit*,offset*,order*,sort*}", path_parameters)
    
    def by_video_id(self,video_id: str) -> WithVideoItemRequestBuilder:
        """
        Gets an item from the rixl_sdk.videos.item collection
        param video_id: Video ID
        Returns: WithVideoItemRequestBuilder
        """
        if video_id is None:
            raise TypeError("video_id cannot be null.")
        from .item.with_video_item_request_builder import WithVideoItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["videoId"] = video_id
        return WithVideoItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[VideosRequestBuilderGetQueryParameters]] = None) -> Optional[PaginatedResponseVideo]:
        """
        Retrieve all videos for a specific project, with pagination and sorting.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[PaginatedResponseVideo]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ..models.github_com_rixlhq_api_internal_errors.error_response import ErrorResponse

        error_mapping: dict[str, type[ParsableFactory]] = {
            "400": ErrorResponse,
            "401": ErrorResponse,
            "403": ErrorResponse,
            "500": ErrorResponse,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ..models.pagination.paginated_response_video import PaginatedResponseVideo

        return await self.request_adapter.send_async(request_info, PaginatedResponseVideo, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[VideosRequestBuilderGetQueryParameters]] = None) -> RequestInformation:
        """
        Retrieve all videos for a specific project, with pagination and sorting.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> VideosRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: VideosRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return VideosRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def languages(self) -> LanguagesRequestBuilder:
        """
        The languages property
        """
        from .languages.languages_request_builder import LanguagesRequestBuilder

        return LanguagesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def upload(self) -> UploadRequestBuilder:
        """
        The upload property
        """
        from .upload.upload_request_builder import UploadRequestBuilder

        return UploadRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class VideosRequestBuilderGetQueryParameters():
        """
        Retrieve all videos for a specific project, with pagination and sorting.
        """
        # Maximum number of items to return in a single request. <br> **Default:** `25`
        limit: Optional[int] = None

        # Starting point of the result set. <br>To get page 2 with a limit of 25, set `offset` to `25`. <br> **Default:** `0`
        offset: Optional[int] = None

        # Sort order (asc, desc)
        order: Optional[str] = None

        # Field to sort by (created_at, name, size, updated_at, duration)
        sort: Optional[str] = None

    
    @dataclass
    class VideosRequestBuilderGetRequestConfiguration(RequestConfiguration[VideosRequestBuilderGetQueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

