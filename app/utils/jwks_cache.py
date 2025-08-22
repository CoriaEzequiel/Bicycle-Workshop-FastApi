import time
from typing import Any
import httpx


class JWKSCache:
    def __init__(self, url: str, ttl_seconds: int = 600):
     self.url = url
     self.ttl = ttl_seconds
     self._cached: dict[str, Any] | None = None
     self._exp: float = 0


async def get(self) -> dict[str, Any]:
    now = time.time()
    if self._cached and now < self._exp:
        return self._cached
    async with httpx.AsyncClient() as client:
        resp = await client.get(self.url, timeout=10.0)
        resp.raise_for_status()
        self._cached = resp.json()
        self._exp = now + self.ttl
        return self._cached