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


__version__ = "1.0.5"


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

    def setSandbox(self, sandbox: bool):
        """
        Set Sandbox Mode

        Args:
            sandbox (bool): Sandbox Mode For This Transaction
        """
        self._sandbox = sandbox

    def setApiKey(self, apiKey: str):
        """
        Set Api Key

        Args:
            apiKey (str): Api Key For This Transaction
        """
        self._apiKey = apiKey

    def setPrivateKey(self, privateKey: str):
        """
        Set Private Key

        Args:
            privateKey (str): Private Key For This Transaction
        """
        self._privateKey = privateKey

    def setMerchantCode(self, merchantCode: str):
        """
        Set Merchant Code

        Args:
            merchantCode (str): Merchant Code For This Transaction
        """
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
        """
        Format Currency

        Args:
            price (`str`): Price To Format
            currency (`str`, optional): the currency code. Defaults to "IDR".
            format (`str` | `NumberPattern`, optional): the format string to use. Defaults to None.
            locale (`str`, optional): the Locale object or locale identifier. Defaults to "id_ID".
            currency_digits (`bool`, optional): use the currency's natural number of decimal digits. Defaults to True.
            format_type (`Literal['name', 'standard', 'accounting']`, optional): the currency format type to use. Defaults to "standard".
            decimal_quantization (`bool`, optional): Truncate and round high-precision numbers to the format pattern. Defaults to True.. Defaults to True.
            group_separator (`bool`, optional): Boolean to switch group separator on/off in a locale's number format.. Defaults to True.
            numbering_system (`str` | `Literal['default']`, optional): The numbering system used for formatting number symbols. Defaults to "latn". The special value "default" will use the default numbering system of the locale.. Defaults to "latn".

        Returns:
            str: return formatted currency
        """
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
        """
        Generate Unique Code based on name

        Args:
            name (str): Name For Unique Code
            length (int): Length of Unique Code ID

        Returns:
            str: return unique code in string
        """
        _string = '1 2 3 4 5 6 7 8 9 0'.split()
        unikCode: str = name
        for x in range(length):
            unikCode += random.choice(_string)
        return unikCode

    def formatDate(
        self,
        timestamp: Union[int, float],
        format: str = "%d-%m-%Y %H:%M:%S",
        zone: Optional[str] = "Asia/Jakarta"
    ):
        """
        Format Date

        Args:
            timestamp (`int` | `float`): Timestamp in seconds
            format (`str`, optional): Format Date. Defaults to "%d-%m-%Y %H:%M:%S".
            zone (`str`, optional): TimeZone. Defaults to "Asia/Jakarta".

        Returns:
            str: return formatted date in string
        """
        date = datetime.fromtimestamp(timestamp, tz=timezone(zone))
        return date.strftime(format)
