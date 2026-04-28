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
    from ...models.github_com_rixlhq_api_internal_errors.error_response import ErrorResponse
    from ...models.video import Video
    from .audio_tracks.audio_tracks_request_builder import AudioTracksRequestBuilder
    from .chapters.chapters_request_builder import ChaptersRequestBuilder
    from .delete.delete_request_builder import DeleteRequestBuilder
    from .subtitles.subtitles_request_builder import SubtitlesRequestBuilder
    from .thumbnail.thumbnail_request_builder import ThumbnailRequestBuilder

class WithVideoItemRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /videos/{videoId}
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new WithVideoItemRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/videos/{videoId}", path_parameters)
    
    async def get(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[Video]:
        """
        Retrieve a video by its ID for a specific project.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[Video]
        """
        request_info = self.to_get_request_information(
            request_configuration
        )
        from ...models.github_com_rixlhq_api_internal_errors.error_response import ErrorResponse

        error_mapping: dict[str, type[ParsableFactory]] = {
            "400": ErrorResponse,
            "401": ErrorResponse,
            "403": ErrorResponse,
            "404": ErrorResponse,
            "500": ErrorResponse,
        }
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ...models.video import Video

        return await self.request_adapter.send_async(request_info, Video, error_mapping)
    
    def to_get_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Retrieve a video by its ID for a specific project.
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.GET, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def with_url(self,raw_url: str) -> WithVideoItemRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: WithVideoItemRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return WithVideoItemRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def audio_tracks(self) -> AudioTracksRequestBuilder:
        """
        The audioTracks property
        """
        from .audio_tracks.audio_tracks_request_builder import AudioTracksRequestBuilder

        return AudioTracksRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def chapters(self) -> ChaptersRequestBuilder:
        """
        The chapters property
        """
        from .chapters.chapters_request_builder import ChaptersRequestBuilder

        return ChaptersRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def delete_path(self) -> DeleteRequestBuilder:
        """
        The deletePath property
        """
        from .delete.delete_request_builder import DeleteRequestBuilder

        return DeleteRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def subtitles(self) -> SubtitlesRequestBuilder:
        """
        The subtitles property
        """
        from .subtitles.subtitles_request_builder import SubtitlesRequestBuilder

        return SubtitlesRequestBuilder(self.request_adapter, self.path_parameters)
    
    @property
    def thumbnail(self) -> ThumbnailRequestBuilder:
        """
        The thumbnail property
        """
        from .thumbnail.thumbnail_request_builder import ThumbnailRequestBuilder

        return ThumbnailRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class WithVideoItemRequestBuilderGetRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

