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

import tripayiin
import tripayiin.exception as exception
from tripayiin.types.response import Response


class DetailPayment:
    async def detailOpenPayment(
        self: "tripayiin.Tripayiin",
        reference: str
    ) -> Response:
        """
        Get Detail Open Payment

        Args:
            reference (`str`): Transaction reference code

        Returns:
            dict: Returns a dictionary
        """
        if self._sandbox is True:
            raise exception.SandboxModeError()

        res = await self.get(
            url=f"/open-payment/{reference}/detail"
        )
        return res
