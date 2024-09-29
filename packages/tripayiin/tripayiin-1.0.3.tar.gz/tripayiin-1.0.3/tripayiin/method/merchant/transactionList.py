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

from typing import Dict, List, Optional

import tripayiin
from tripayiin.types.code import Code


class TransactionList:
    async def transactionList(
        self: "tripayiin.Tripayiin",
        page: Optional[int] = None,
        perPage: Optional[int] = None,
        sort: Optional[str] = None,
        references: Optional[str] = None,
        merchantRef: Optional[str] = None,
        method: Optional[Code] = None,
        status: Optional[str] = None
    ) -> List[Dict]:
        """
        Get Cost Calculator

        Args:
            amount (`int`): Transaction nominal
            method (`str`, optional): Payment channel code. If this parameter is empty then the result is a list of all available payment channels. Defaults to None.
            

        Returns:
            Dict[str, Any]: Returns a dictionaries
        """
        data = {}
        if method is not None:
            data["method"] = method
        if status is not None:
            data["status"] = status
        if page is not None:
            data["page"] = page
        if perPage is not None:
            data["per_page"] = perPage
        if sort is not None:
            data["sort"] = sort
        if references is not None:
            data["references"] = references
        if merchantRef is not None:
            data["merchant_ref"] = merchantRef

        res = await self.get(
            url="/merchant/transactions",
            data=data
        )
        return {
            "data": res['data'],
            "pagination": res['pagination']
        }
