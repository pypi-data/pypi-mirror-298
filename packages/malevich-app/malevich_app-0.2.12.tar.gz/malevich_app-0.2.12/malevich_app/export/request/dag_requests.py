import aiohttp
from typing import Optional, Dict, Any, Union, List
import malevich_app.export.secondary.const as C


async def send_post_dag(values: Union[str, bytes], operation: str, *, raw_res: bool = False, headers: Dict[str, str] = None) -> Optional[Union[Dict[str, Any], List[str], bytes]]:
    async with aiohttp.ClientSession(timeout=C.AIOHTTP_TIMEOUT) as session:
        if headers is None:
            headers = C.DEFAULT_HEADERS
        async with session.post(operation, data=values, headers=headers) as response:
            response.raise_for_status()
            if response.status == 204:
                return None
            if raw_res:
                return await response.read()
            return await response.json()


async def send_delete_dag(values: str, operation: str):
    async with aiohttp.ClientSession(timeout=C.AIOHTTP_TIMEOUT) as session:
        async with session.delete(operation, data=values, headers=C.DEFAULT_HEADERS) as response:
            response.raise_for_status()
