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

from enum import Enum


class Code(str, Enum):
    MYBVA = "MYBVA"
    QRIS_SHOPEEPAY = "QRIS_SHOPEEPAY"
    SHOPEEPAY = "SHOPEEPAY"
    DANA = "DANA"
    QRIS2 = "QRIS2"
    QRISC = "QRISC"
    QRIS = "QRIS"
    OVO = "OVO"
    ALFAMIDI = "ALFAMIDI"
    INDOMARET = "INDOMARET"
    ALFAMART = "ALFAMART"
    OTHERBANKVA = "OTHERBANKVA"
    DANAMONVA = "DANAMONVA"
    OCBCVA = "OCBCVA"
    BSIVA = "BSIVA"
    CIMBVA = "CIMBVA"
    MUAMALATVA = "MUAMALATVA"
    BCAVA = "BCAVA"
    MANDIRIVA = "MANDIRIVA"
    BRIVA = "BRIVA"
    BNIVA = "BNIVA"
    PERMATAVA = "PERMATAVA"
