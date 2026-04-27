import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx

from _shared.auth import ApiKeyHeaderAuth
from _shared.env import must_env

from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from models.github_com_qeeqez_api_internal_videos_handler_upload.complete_request import (
    CompleteRequest as VideoCompleteRequest,
)
from models.internal_images_handler.complete_request import (
    CompleteRequest as ImageCompleteRequest,
)
from models.internal_images_handler.upload_init_request import UploadInitRequest
from models.video_upload_init_request import VideoUploadInitRequest
from rixl_client import RixlClient

SAMPLE_IMAGE = "https://picsum.photos/seed/rixl/800/600.jpg"
SAMPLE_VIDEO = "https://download.samplelib.com/mp4/sample-5s.mp4"


async def fetch(url: str) -> bytes:
    async with httpx.AsyncClient(timeout=60.0) as c:
        resp = await c.get(url)
        resp.raise_for_status()
        return resp.content


async def put_bytes(url: str, body: bytes, content_type: str) -> None:
    async with httpx.AsyncClient(timeout=300.0) as c:
        resp = await c.put(url, content=body, headers={"Content-Type": content_type})
        resp.raise_for_status()


async def upload_image(client: RixlClient) -> None:
    print("== Image upload ==")
    body = await fetch(SAMPLE_IMAGE)
    print(f"downloaded {len(body)} bytes")

    init_req = UploadInitRequest()
    init_req.name = "sample.jpg"
    init_req.format = "jpeg"
    init_res = await client.images.upload.init.post(init_req)
    print(f"init: image_id={init_res.image_id}")

    await put_bytes(init_res.presigned_url, body, "image/jpeg")
    print("uploaded bytes")

    complete_req = ImageCompleteRequest()
    complete_req.image_id = init_res.image_id
    complete_req.attached_to_video = False
    image = await client.images.upload.complete.post(complete_req)
    print(f"complete: id={image.id} {image.width}x{image.height}\n")


async def upload_video(client: RixlClient) -> None:
    print("== Video upload ==")
    video, poster = await asyncio.gather(fetch(SAMPLE_VIDEO), fetch(SAMPLE_IMAGE))
    print(f"downloaded video={len(video)} bytes poster={len(poster)} bytes")

    init_req = VideoUploadInitRequest()
    init_req.file_name = "sample.mp4"
    init_req.image_format = "jpeg"
    init_res = await client.videos.upload.init.post(init_req)
    print(f"init: video_id={init_res.video_id} poster_id={init_res.poster_id}")

    await asyncio.gather(
        put_bytes(init_res.video_presigned_url, video, "video/mp4"),
        put_bytes(init_res.poster_presigned_url, poster, "image/jpeg"),
    )
    print("uploaded video and poster")

    complete_req = VideoCompleteRequest()
    complete_req.video_id = init_res.video_id
    finished = await client.videos.upload.complete.post(complete_req)
    print(f"complete: id={finished.id}")


async def main() -> None:
    api_key = must_env("RIXL_API_KEY")
    base_url = os.environ.get("RIXL_BASE_URL", "http://localhost:8081")

    adapter = HttpxRequestAdapter(ApiKeyHeaderAuth(api_key))
    adapter.base_url = base_url
    client = RixlClient(adapter)

    await upload_image(client)
    await upload_video(client)


if __name__ == "__main__":
    asyncio.run(main())
