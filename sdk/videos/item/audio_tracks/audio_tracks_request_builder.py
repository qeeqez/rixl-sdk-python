from __future__ import annotations
from collections.abc import Callable
from dataclasses import dataclass, field
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.base_request_configuration import RequestConfiguration
from kiota_abstractions.default_query_parameters import QueryParameters
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.method import Method
from kiota_abstractions.multipart_body import MultipartBody
from kiota_abstractions.request_adapter import RequestAdapter
from kiota_abstractions.request_information import RequestInformation
from kiota_abstractions.request_option import RequestOption
from kiota_abstractions.serialization import Parsable, ParsableFactory
from typing import Any, Optional, TYPE_CHECKING, Union
from warnings import warn

if TYPE_CHECKING:
    from ....models.audio_track import AudioTrack
    from ....models.audio_track_delete import AudioTrackDelete
    from .item.with_track_item_request_builder import WithTrackItemRequestBuilder
    from .language.language_request_builder import LanguageRequestBuilder

class AudioTracksRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /videos/{videoId}/audio-tracks
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new AudioTracksRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/videos/{videoId}/audio-tracks", path_parameters)
    
    def by_track_id(self,track_id: str) -> WithTrackItemRequestBuilder:
        """
        Gets an item from the rixl_sdk.videos.item.audioTracks.item collection
        param track_id: Audio Track ID
        Returns: WithTrackItemRequestBuilder
        """
        if track_id is None:
            raise TypeError("track_id cannot be null.")
        from .item.with_track_item_request_builder import WithTrackItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["trackId"] = track_id
        return WithTrackItemRequestBuilder(self.request_adapter, url_tpl_params)
    
    async def delete(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[AudioTrackDelete]:
        """
        Remove all additional audio tracks from a video using API key authentication
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[AudioTrackDelete]
        """
        request_info = self.to_delete_request_information(
            request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.audio_track_delete import AudioTrackDelete

        return await self.request_adapter.send_async(request_info, AudioTrackDelete, None)
    
    async def post(self,body: MultipartBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> Optional[list[AudioTrack]]:
        """
        Replace all audio tracks with the provided ones using API key authentication
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: Optional[list[AudioTrack]]
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = self.to_post_request_information(
            body, request_configuration
        )
        if not self.request_adapter:
            raise Exception("Http core is null") 
        from ....models.audio_track import AudioTrack

        return await self.request_adapter.send_collection_async(request_info, AudioTrack, None)
    
    def to_delete_request_information(self,request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Remove all additional audio tracks from a video using API key authentication
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        request_info = RequestInformation(Method.DELETE, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        return request_info
    
    def to_post_request_information(self,body: MultipartBody, request_configuration: Optional[RequestConfiguration[QueryParameters]] = None) -> RequestInformation:
        """
        Replace all audio tracks with the provided ones using API key authentication
        param body: The request body
        param request_configuration: Configuration for the request such as headers, query parameters, and middleware options.
        Returns: RequestInformation
        """
        if body is None:
            raise TypeError("body cannot be null.")
        request_info = RequestInformation(Method.POST, self.url_template, self.path_parameters)
        request_info.configure(request_configuration)
        request_info.headers.try_add("Accept", "application/json")
        request_info.set_content_from_parsable(self.request_adapter, "multipart/form-data", body)
        return request_info
    
    def with_url(self,raw_url: str) -> AudioTracksRequestBuilder:
        """
        Returns a request builder with the provided arbitrary URL. Using this method means any other path or query parameters are ignored.
        param raw_url: The raw URL to use for the request builder.
        Returns: AudioTracksRequestBuilder
        """
        if raw_url is None:
            raise TypeError("raw_url cannot be null.")
        return AudioTracksRequestBuilder(self.request_adapter, raw_url)
    
    @property
    def language(self) -> LanguageRequestBuilder:
        """
        The language property
        """
        from .language.language_request_builder import LanguageRequestBuilder

        return LanguageRequestBuilder(self.request_adapter, self.path_parameters)
    
    @dataclass
    class AudioTracksRequestBuilderDeleteRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    
    @dataclass
    class AudioTracksRequestBuilderPostRequestConfiguration(RequestConfiguration[QueryParameters]):
        """
        Configuration for the request such as headers, query parameters, and middleware options.
        """
        warn("This class is deprecated. Please use the generic RequestConfiguration class generated by the generator.", DeprecationWarning)
    

