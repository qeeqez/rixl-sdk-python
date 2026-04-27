import asyncio
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import httpx

from _shared.auth import BearerAuth
from _shared.env import must_env

from kiota_http.httpx_request_adapter import HttpxRequestAdapter
from rixl_client import RixlClient


async def mint_token(base_url: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=30.0) as c:
        resp = await c.post(f"{base_url}/clientauth/token", json=payload)
        resp.raise_for_status()
        return resp.json()


async def main() -> None:
    base_url = os.environ.get("RIXL_BASE_URL", "http://localhost:8081")
    payload = {
        "client_id": must_env("RIXL_CLIENT_ID"),
        "client_secret": must_env("RIXL_CLIENT_SECRET"),
        "subject": must_env("RIXL_SUBJECT"),
        "project_id": must_env("RIXL_PROJECT_ID"),
    }

    tok = await mint_token(base_url, payload)
    print(f"minted token (expires_in={tok['expires_in']}s, type={tok['token_type']})")

    adapter = HttpxRequestAdapter(BearerAuth(tok["access_token"]))
    adapter.base_url = base_url
    client = RixlClient(adapter)

    page = await client.images.get()
    print(f"Listed {len(page.data or [])} images")


if __name__ == "__main__":
    asyncio.run(main())
