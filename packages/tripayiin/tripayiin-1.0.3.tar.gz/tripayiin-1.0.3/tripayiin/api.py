#  TriPayiin - Payment Gateaway Client For Python (Unofficial)
#  Copyright (C) 2024-present AyiinXd <https://github.com/AyiinXd>
#
#  This file is part of TriPayiin.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with TriPayiin.  If not, see <http://www.gnu.org/licenses/>.


from aiohttp import ClientSession
import hmac
import hashlib

from typing import Optional
from tripayiin.types.response import Response


class Api:
    sandboxUrl: str = "https://tripay.co.id/api-sandbox"
    productionUrl: str = "https://tripay.co.id/api"
    def __init__(self, apiKey: str, privateKey: str, sandbox: Optional[bool]):
        self._apiKey = apiKey
        self._privateKey = privateKey
        self.baseUrl = self.sandboxUrl if sandbox is True else self.productionUrl

    async def get(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        async with ClientSession(
            headers={
                "Authorization": f"Bearer {self._apiKey}",
                "Content-Type": "application/json"
            }
        ) as response:
            
            res = await response.get(
                url=f"{self.baseUrl}{url}",
                json=data,
                headers=headers
            )
            json = await res.json()
            return Response(**json)

    async def post(self, url: str, data: Optional[dict] = None, headers: Optional[dict] = None) -> Response:
        async with ClientSession(
            headers={
                "Authorization": f"Bearer {self._apiKey}",
                "Content-Type": "application/json"
            }
        ) as response:
            res = await response.post(
                url=f"{self.baseUrl}{url}",
                json=data,
                headers=headers
            )
            json = await res.json()
            return Response(**json)

    async def createSignature(
        self,
        merchantCode: str,
        merchantRef: Optional[str] = None,
        amount: Optional[str] = None,
        channel: Optional[str] = None
    ):
        signStr = f"{merchantCode}{merchantRef if merchantRef is not None else channel}{amount if amount is not None else merchantRef}"
        signature = hmac.new(bytes(self._privateKey,'latin-1'), bytes(signStr,'latin-1'), hashlib.sha256).hexdigest()
        return signature
