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
from tripayiin.types.code import Code


class Intruction:
    async def intructionPayment(
        self: "tripayiin.Tripayiin",
        code: Code,
        payCode: Optional[str] = None,
        amount: Optional[int] = None,
        allowHtml: Optional[int] = None
    ) -> Union[List[Dict], None]:
        """
        Get Payment Instruction

        Args:
            code (`Code`): Payment Channel Code, see [Payment Channel Code](https://tripay.co.id/developer?tab=channels)
            payCode (`str`, optional): To enter the payment code/VA number into the instruction response. Defaults to None.
            amount (`int`, optional): To enter a nominal value into the instruction response. Defaults to None.
            allowHtml (`int`, optional): To allow html tags on the instruction
            0 = Not allowed
            1 = Allowed.
            Defaults to 1.

        Returns:
            Union[List[Dict], None]: Returns a list of dictionaries if successful, otherwise None
        """
        data = {
            "code": code
        }
        if payCode is not None:
            data["pay_code"] = payCode
        if amount is not None:
            data["amount"] = amount
        if allowHtml is not None:
            data["allow_html"] = allowHtml
        res = await self.get(
            url="/payment/instruction",
            data=data
        )
        if res.data is None:
            return None
        return res.data
