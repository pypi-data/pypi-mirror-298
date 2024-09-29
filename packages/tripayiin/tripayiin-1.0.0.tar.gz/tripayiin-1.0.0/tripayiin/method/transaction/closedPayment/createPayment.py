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

from typing import Dict, List, Optional, Union

import tripayiin

import tripayiin.exception
from tripayiin.types.code import Code
from tripayiin.types.orderItem import OrderItem


class CreatePayment:
    async def createClosedPayment(
        self: "tripayiin.Tripayiin",
        method: Code,
        merchant_ref: str,
        amount: int,
        customerName: str,
        customerEmail: str,
        orderItems: List[OrderItem],
        merchantCode: Optional[str] = None,
        customerPhone: Optional[str] = None,
        callbackUrl: Optional[str] = None,
        returnUrl: Optional[str] = None,
        expiredTime: Optional[int] = None
    ) -> Dict:
        """
        Create Closed Payment

        Args:
            method (`Code`): Payment channel code, see [Payment Channel Code](https://tripay.co.id/developer?tab=channels)
            merchant_ref (`str`): Merchant reference
            amount (`int`): Transaction nominal
            customerName (`str`): Customer name
            customerEmail (`str`): Customer email
            orderItems (`List[OrderItem]`): List of order items
            merchantCode (`str`, optional): Merchant code. Defaults to None.
            customerPhone (`str`, optional): Customer phone number. Defaults to None.
            callbackUrl (`str`, optional): Callback URL. Defaults to None.
            returnUrl (`str`, optional): Return URL. Defaults to None.
            expiredTime (`int`, optional): Expired time in timestamp. Defaults to None.

        Returns:
            Dict: Returns a dictionary
        """
        data = {
            "method": method,
            "merchant_ref": merchant_ref,
            "amount": amount,
            "customer_name": customerName,
            "customer_email": customerEmail,
            "order_items": orderItems,
        }
        if customerPhone is not None:
            data["customer_phone"] = customerPhone
        if callbackUrl is not None:
            data["callback_url"] = callbackUrl
        if returnUrl is not None:
            data["return_url"] = returnUrl
        if expiredTime is not None:
            data["expired_time"] = expiredTime
        
        if self._merchantCode is None and merchantCode is None:
            raise tripayiin.exception.MerchantCodeError("You must set Merchant Code with `setMerchantCode` method or with this parameter `merchantCode`")
        signature = await self.createSignature(
            merchantCode=self._merchantCode if self._merchantCode is not None else merchantCode,
            merchantRef=merchant_ref,
            amount=str(amount)
        )
        data["signature"] = signature
        res = await self.post(
            url="/transaction/create",
            data=data
        )
        if res.data:
            return res.data
        return res
