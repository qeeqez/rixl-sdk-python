from __future__ import annotations
from collections.abc import Callable
from kiota_abstractions.base_request_builder import BaseRequestBuilder
from kiota_abstractions.get_path_parameters import get_path_parameters
from kiota_abstractions.request_adapter import RequestAdapter
from typing import Any, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .item.with_lang_code_item_request_builder import WithLang_codeItemRequestBuilder

class LanguageRequestBuilder(BaseRequestBuilder):
    """
    Builds and executes requests for operations under /videos/{videoId}/subtitles/language
    """
    def __init__(self,request_adapter: RequestAdapter, path_parameters: Union[str, dict[str, Any]]) -> None:
        """
        Instantiates a new LanguageRequestBuilder and sets the default values.
        param path_parameters: The raw url or the url-template parameters for the request.
        param request_adapter: The request adapter to use to execute the requests.
        Returns: None
        """
        super().__init__(request_adapter, "{+baseurl}/videos/{videoId}/subtitles/language", path_parameters)
    
    def by_lang_code(self,lang_code: str) -> WithLang_codeItemRequestBuilder:
        """
        Gets an item from the rixl_sdk.videos.item.subtitles.language.item collection
        param lang_code: Language Code (BCP 47)
        Returns: WithLang_codeItemRequestBuilder
        """
        if lang_code is None:
            raise TypeError("lang_code cannot be null.")
        from .item.with_lang_code_item_request_builder import WithLang_codeItemRequestBuilder

        url_tpl_params = get_path_parameters(self.path_parameters)
        url_tpl_params["lang_code"] = lang_code
        return WithLang_codeItemRequestBuilder(self.request_adapter, url_tpl_params)
    

