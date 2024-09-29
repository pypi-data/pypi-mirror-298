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

from typing import Dict, Optional

import tripayiin

import tripayiin.exception as exception
from tripayiin.types.code import Code


class CreatePayment:
    async def createOpenPayment(
        self: "tripayiin.Tripayiin",
        method: Code,
        merchantRef: str,
        customerName: Optional[str] = None,
        merchantCode: Optional[str] = None
    ) -> Dict:
        """
        Create Open Payment

        Args:
            method (`Code`): Payment channel code, see [Payment Channel Code](https://tripay.co.id/developer?tab=channels)
            merchantRef (`str`, optional): Merchant reference. Defaults to None.
            customerName (`str`, optional): Customer name. Defaults to None.
            merchantCode (`str`, optional): Merchant code. Defaults to None.

        Returns:
            Dict: Returns a dictionary
        """
        if self._sandbox is True:
            raise exception.SandboxModeError()
        data = {
            "method": method
        }
        if merchantRef is not None:
            data["merchant_ref"] = merchantRef
        if customerName is not None:
            data["customer_name"] = customerName
        
        if self._merchantCode is None and merchantCode is None:
            raise exception.MerchantCodeError("You must set Merchant Code with `setMerchantCode` method or with this parameter `merchantCode`")
        signature = await self.createSignature(
            merchant_code=self._merchantCode if self._merchantCode is not None else merchantCode,
            channel=method,
            merchantRef=merchantRef
        )
        data["signature"] = signature
        res = await self.post(
            url="/open-payment/create",
            data=data
        )
        if res.data:
            return res.data
        else:
            return res