# rixl

Python client for the [RIXL](https://rixl.com) API.

[![PyPI](https://img.shields.io/pypi/v/rixl.svg)](https://pypi.org/project/rixl/)

## Install

```bash
pip install rixl
```

Requires Python 3.10+. `microsoft-kiota-bundle` is pulled in transitively (HTTP transport, serializers, request adapter).

## Quick start

```python
import asyncio
from kiota_abstractions.authentication.api_key_authentication_provider import (
    ApiKeyAuthenticationProvider, KeyLocation,
)
from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from rixl_client import RixlClient


async def main():
    auth = ApiKeyAuthenticationProvider(
        api_key="YOUR_RIXL_API_KEY",
        parameter_name="X-API-Key",
        key_location=KeyLocation.Header,
    )
    adapter = HttpxRequestAdapter(auth)
    client = RixlClient(adapter)

    image = await client.images.by_image_id("PS5IMKoFLm").get()
    print(image.id, image.width, image.height)


asyncio.run(main())
```

Default base URL: `https://api.rixl.com`. Override with `adapter.base_url = "..."`.

## Authentication

API key:

```python
from kiota_abstractions.authentication.api_key_authentication_provider import (
    ApiKeyAuthenticationProvider, KeyLocation,
)

auth = ApiKeyAuthenticationProvider(
    "YOUR_RIXL_API_KEY", "X-API-Key", KeyLocation.Header,
)
```

Bearer token: implement `AccessTokenProvider`, then wrap with `BaseBearerTokenAuthenticationProvider` from `kiota_abstractions.authentication.base_bearer_token_authentication_provider`.

## Feeds

```python
posts = await client.feeds.by_feed_id("FD4y3QB38S").get()
for post in posts.data:
    print(post.id)
```

## Images

```python
page = await client.images.get()
image = await client.images.by_image_id("PS5IMKoFLm").get()
await client.images.by_image_id("PS5IMKoFLm").delete()
```

Upload (init → PUT bytes → complete):

```python
import httpx
from models.internal_images_handler.upload_init_request import UploadInitRequest
from models.internal_images_handler.complete_request import CompleteRequest

init_req = UploadInitRequest()
init_req.name = "photo.jpg"
init_req.format = "jpeg"
init_res = await client.images.upload.init.post(init_req)

async with httpx.AsyncClient() as c:
    await c.put(init_res.presigned_url, content=image_bytes,
                headers={"Content-Type": "image/jpeg"})

complete_req = CompleteRequest()
complete_req.image_id = init_res.image_id
complete_req.attached_to_video = False
image = await client.images.upload.complete.post(complete_req)
```

## Videos

```python
videos = await client.videos.get()
video = await client.videos.by_video_id("VI9VXQxWXQ").get()
tracks = await client.videos.by_video_id("VI9VXQxWXQ").subtitles.get()
```

Upload returns presigned URLs for both the video and a poster image:

```python
from models.video_upload_init_request import VideoUploadInitRequest
from models.github_com_rixlhq_api_internal_videos_handler_upload.complete_request \
    import CompleteRequest as VideoCompleteRequest

init_req = VideoUploadInitRequest()
init_req.file_name = "clip.mp4"
init_req.image_format = "jpeg"
init_res = await client.videos.upload.init.post(init_req)
# PUT bytes to init_res.video_presigned_url and init_res.poster_presigned_url

complete_req = VideoCompleteRequest()
complete_req.video_id = init_res.video_id
video = await client.videos.upload.complete.post(complete_req)
```

## Pagination

List endpoints take `limit`, `offset`, `sort`, `order`:

```python
from kiota_abstractions.base_request_configuration import RequestConfiguration
from rixl_sdk.images.images_request_builder import ImagesRequestBuilder

limit, offset = 50, 0
while True:
    params = ImagesRequestBuilder.ImagesRequestBuilderGetQueryParameters(
        limit=limit, offset=offset,
    )
    page = await client.images.get(
        request_configuration=RequestConfiguration(query_parameters=params),
    )
    if offset + len(page.data) >= page.pagination.total:
        break
    offset += limit
```

## Errors

```python
from rixl_sdk.models.github_com_rixlhq_api_internal_errors.error_response import ErrorResponse

try:
    image = await client.images.by_image_id("PS5IMKoFLm").get()
except ErrorResponse as e:
    print(f"HTTP {e.code}: {e.error}")
```

Network failures raise `httpx` exceptions.

## Examples

Runnable demos in [examples/](./examples):

```bash
cd examples
pip install -r requirements.txt
export RIXL_API_KEY=<key>
python basic/images/main.py
python advanced/videos/main.py
```

## Issues

[github.com/rixlhq/rixl-python/issues](https://github.com/rixlhq/rixl-python/issues)
