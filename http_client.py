from aiohttp import ClientSession
from async_lru import alru_cache

class HTTPClient:
    def __init__(self, base_url: str, headers: dict):
        self.base_url = base_url
        self.headers = headers
        self._session = None

    async def init_session(self):
        self._session = ClientSession(headers=self.headers)

    async def close(self):
        if self._session:
            await self._session.close()

class IMEIHTTPClient(HTTPClient):
    @alru_cache
    async def get_listings(self, message: str):
        if not self._session:
            await self.init_session()
        url = f'{self.base_url}/v1/checks'
        async with self._session.post(url, json={"deviceId": message, "serviceId": 12}) as resp:
            result = await resp.json()
            return result