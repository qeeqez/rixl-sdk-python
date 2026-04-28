# RIXL Python SDK

The official Python client for the [RIXL](https://rixl.com) API.

[![PyPI](https://img.shields.io/pypi/v/rixl-sdk-python.svg)](https://pypi.org/project/rixl-sdk-python/)
[![Python](https://img.shields.io/pypi/pyversions/rixl-sdk-python.svg)](https://pypi.org/project/rixl-sdk-python/)

[Installation](#installation) • [Quick start](#quick-start) • [Authentication](#authentication) • [Resources](#resources) • [Pagination](#pagination) • [Errors](#errors)

## Features

- Typed fluent API generated from the RIXL OpenAPI spec
- Async-first — every call is awaitable
- Pre-mapped error responses for 400, 401, 403, 404, and 500
- Pluggable `RequestAdapter` and authentication providers
- Support for JSON, form, multipart, and plain-text payloads

## Requirements

- Python 3.10+
- A RIXL API key

## Installation

```bash
pip install rixl-sdk-python
```

`microsoft-kiota-bundle` is pulled in as a dependency and provides the HTTP transport, serializers, and `RequestAdapter` implementation.

## Quick start

```python
import asyncio

from kiota_abstractions.authentication.api_key_authentication_provider import (
    ApiKeyAuthenticationProvider, KeyLocation,
)
from kiota_http.httpx_request_adapter import HttpxRequestAdapter

from rixl_client import RixlClient


async def main() -> None:
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

Base URL defaults to `https://api.rixl.com`. Override with `adapter.base_url = "..."`.

## Authentication

```python
from kiota_abstractions.authentication.api_key_authentication_provider import (
    ApiKeyAuthenticationProvider, KeyLocation,
)

# API key in a header
auth = ApiKeyAuthenticationProvider(
    "YOUR_RIXL_API_KEY", "X-API-Key", KeyLocation.Header,
)

# Bearer token
# Implement AccessTokenProvider, then wrap with
# BaseBearerTokenAuthenticationProvider from
# kiota_abstractions.authentication.base_bearer_token_authentication_provider
```

## Resources

### Feeds

```python
posts = await client.feeds.by_feed_id("FD4y3QB38S").get()
for post in posts.data:
    print(post.id)
```

### Images

```python
# List
page = await client.images.get()

# Get
image = await client.images.by_image_id("PS5IMKoFLm").get()

# Delete
await client.images.by_image_id("PS5IMKoFLm").delete()

# Upload (init → PUT bytes to presigned URL → complete)
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

### Videos

```python
# List
videos = await client.videos.get()

# Get
video = await client.videos.by_video_id("VI9VXQxWXQ").get()

# Subtitle tracks
tracks = await client.videos.by_video_id("VI9VXQxWXQ").subtitles.get()

# Upload (init returns presigned URLs for both the video and a poster image)
from models.video_upload_init_request import VideoUploadInitRequest
from models.github_com_qeeqez_api_internal_videos_handler_upload.complete_request \
    import CompleteRequest as VideoCompleteRequest

init_req = VideoUploadInitRequest()
init_req.file_name = "clip.mp4"
init_req.image_format = "jpeg"
init_res = await client.videos.upload.init.post(init_req)

# PUT video bytes to init_res.video_presigned_url
# PUT poster bytes to init_res.poster_presigned_url

complete_req = VideoCompleteRequest()
complete_req.video_id = init_res.video_id
video = await client.videos.upload.complete.post(complete_req)
```

## Pagination

List endpoints accept `limit`, `offset`, `sort`, and `order`:

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
    for img in page.data:
        ...
    if offset + len(page.data) >= page.pagination.total:
        break
    offset += limit
```

## Errors

API errors (400, 401, 403, 404, 500) are raised as `ErrorResponse`:

```python
from rixl_sdk.models.github_com_qeeqez_api_internal_errors.error_response import ErrorResponse

try:
    image = await client.images.by_image_id("PS5IMKoFLm").get()
except ErrorResponse as err:
    print(f"HTTP {err.code}: {err.error}")
```

Transport failures (timeouts, connection errors) surface as `httpx` exceptions.

## Models

Generated types live under `rixl_sdk.models.*`:

| Module | Contents |
|--------|----------|
| `rixl_sdk.models` | `Image`, `Video`, `Post`, `File` |
| `rixl_sdk.models.pagination` | `PaginatedResponseImage`, `PaginatedResponseVideo`, `PaginatedResponsePost` |
| `rixl_sdk.models.internal_images_handler` | Upload request and response payloads for images |
| `models.github_com_qeeqez_api_internal_videos_handler_upload` | Upload request and response payloads for videos |
| `models.internal_videos_handler_subtitles` | Subtitle PUT payloads |
| `rixl_sdk.models.github_com_qeeqez_api_internal_errors` | `ErrorResponse` |

Fields are optional — check for `None` before dereferencing.

## Async

Every method is `async def`. Use inside an `asyncio` event loop:

```python
await client.images.by_image_id("PS5IMKoFLm").get()
```

The SDK does not ship a synchronous wrapper.

## Examples

Self-contained demos live in [`examples/`](./examples). Each file imports the SDK and runs one task — copy any of them into your own project as a starting point.

| Path | What it shows |
|---|---|
| `auth/` | both auth flows in one file — picks API key or client JWT from env |
| `basic/images/` | list images, fetch one by `IMAGE_ID` |
| `basic/videos/` | list videos, fetch one by `VIDEO_ID` |
| `basic/feeds/` | read a feed — needs `RIXL_FEED_ID` |
| `basic/posts/` | read one post — needs `RIXL_FEED_ID` and `RIXL_POST_ID` |
| `advanced/images/` | full image upload (init → PUT → complete) |
| `advanced/videos/` | full video upload (video + poster) |

Credentials come from the RIXL dashboard (API key, or Client Auth → Create credential).

```bash
cd examples
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export RIXL_API_KEY=<copied from the dashboard>
export RIXL_BASE_URL=http://localhost:8081   # optional

python basic/images/main.py
python advanced/videos/main.py
python auth/main.py                          # works with either credential type
```

## Support

Open an issue at [github.com/qeeqez/rixl-sdk-python](https://github.com/qeeqez/rixl-sdk-python/issues).
