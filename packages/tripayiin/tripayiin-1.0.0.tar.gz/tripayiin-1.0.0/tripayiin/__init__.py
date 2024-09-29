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

import random
from datetime import datetime
from pytz import timezone
from typing import Literal, Optional, Union
from babel.numbers import format_currency, NumberPattern

from tripayiin.api import Api
from tripayiin.method import Method


__version__ = "1.0.0"


class Tripayiin(Api, Method):
    version: str = __version__
    def __init__(
        self,
        apiKey: str,
        privateKey: str,
        sandbox: Optional[bool],
        merchantCode: Optional[str] = None
    ):
        super(Tripayiin, self).__init__(
            apiKey=apiKey,
            privateKey=privateKey,
            sandbox=sandbox
        )
        self._sandbox = sandbox if sandbox is not None else False
        self._apiKey = apiKey
        self._privateKey = privateKey
        self._merchantCode = merchantCode

    def setMerchantCode(self, merchantCode: str):
        self._merchantCode = merchantCode

    def formatCurrency(
        self,
        price: str,
        currency: str = "IDR",
        format: Optional[Union[str, NumberPattern]] = None,
        locale: Optional[str] = "id_ID",
        currency_digits: bool = True,
        format_type: Literal['name', 'standard', 'accounting'] = "standard",
        decimal_quantization: bool = True,
        group_separator: bool = True,
        *,
        numbering_system: Union[str, Literal['default']] = "latn"
    ):
        currency = format_currency(
            number=price,
            currency=currency,
            locale=locale,
            currency_digits=currency_digits,
            format=format,
            format_type=format_type,
            decimal_quantization=decimal_quantization,
            group_separator=group_separator,
            numbering_system=numbering_system
        )
        return currency

    def genUniqCode(self, name: str, length: int):
        _string = '1 2 3 4 5 6 7 8 9 0'.split()
        unikCode: str = name
        for x in range(length):
            unikCode += random.choice(_string)
        return unikCode

    def reformatDate(
        self,
        timestamp: Union[int, float],
        format: str = "%d-%m-%Y %H:%M:%S",
        zone: Optional[str] = "Asia/Jakarta"
    ):
        # Format TimeStamp To Date
        date = datetime.fromtimestamp(timestamp, tz=timezone(zone))
        return date.strftime(format)
