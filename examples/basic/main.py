import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from _shared.auth import ApiKeyHeaderAuth
from _shared.env import must_env

from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from rixl_client import RixlClient


async def main() -> None:
    api_key = must_env("RIXL_API_KEY")
    base_url = os.environ.get("RIXL_BASE_URL", "http://localhost:8081")

    adapter = HttpxRequestAdapter(ApiKeyHeaderAuth(api_key))
    adapter.base_url = base_url
    client = RixlClient(adapter)

    page = await client.images.get()
    items = page.data or []
    print(f"Listed {len(items)} images")
    for img in items:
        print(f"  - {img.id}")

    image_id = os.environ.get("IMAGE_ID")
    if image_id:
        image = await client.images.by_image_id(image_id).get()
        print(f"Image {image.id}: {image.width}x{image.height}")


if __name__ == "__main__":
    asyncio.run(main())
