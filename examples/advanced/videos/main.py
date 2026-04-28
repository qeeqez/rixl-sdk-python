"""Upload a video end-to-end. Same shape as the image flow, but Init returns
two presigned URLs (one for the video, one for the poster thumbnail) and
we PUT to both.
"""
import asyncio
import os
import sys

import httpx
from kiota_abstractions.authentication.authentication_provider import (
    AuthenticationProvider,
)
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

from models.github_com_rixlhq_api_internal_videos_handler_upload.complete_request import (
    CompleteRequest,
)
from models.video_upload_init_request import VideoUploadInitRequest
from rixl_client import RixlClient

SAMPLE_VIDEO = "https://download.samplelib.com/mp4/sample-5s.mp4"
SAMPLE_POSTER = "https://picsum.photos/seed/rixl/800/600.jpg"


class ApiKeyAuth(AuthenticationProvider):
    def __init__(self, key: str) -> None:
        self.key = key

    async def authenticate_request(self, request, additional_authentication_context=None):
        request.headers.add("X-API-Key", self.key)


async def main() -> None:
    api_key = os.environ.get("RIXL_API_KEY") or sys.exit("missing RIXL_API_KEY")
    base_url = os.environ.get("RIXL_BASE_URL", "http://localhost:8081")

    adapter = HttpxRequestAdapter(ApiKeyAuth(api_key))
    adapter.base_url = base_url
    client = RixlClient(adapter)

    async with httpx.AsyncClient(timeout=300.0) as http:
        video, poster = await asyncio.gather(http.get(SAMPLE_VIDEO), http.get(SAMPLE_POSTER))
        print(f"downloaded video={len(video.content)} poster={len(poster.content)}")

        init_req = VideoUploadInitRequest()
        init_req.file_name = "sample.mp4"
        init_req.image_format = "jpeg"
        init = await client.videos.upload.init.post(init_req)
        print(f"init: video_id={init.video_id} poster_id={init.poster_id}")

        await asyncio.gather(
            http.put(init.video_presigned_url, content=video.content, headers={"Content-Type": "video/mp4"}),
            http.put(init.poster_presigned_url, content=poster.content, headers={"Content-Type": "image/jpeg"}),
        )

    complete = CompleteRequest()
    complete.video_id = init.video_id
    v = await client.videos.upload.complete.post(complete)
    print(f"complete: id={v.id}")


if __name__ == "__main__":
    asyncio.run(main())
