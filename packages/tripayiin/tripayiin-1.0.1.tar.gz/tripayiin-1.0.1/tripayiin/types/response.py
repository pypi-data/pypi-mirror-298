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

from typing import Union


class Response:
    def __init__(self, **kwargs):
        self.success: bool = kwargs.get("success", False)
        self.message: str = kwargs.get("message", "")
        self.data: Union[Union[dict, list], None] = kwargs.get("data", None)

    def __repr__(self):
        return f"Response(success={self.success}, message={self.message}, data={self.data})"

    def parse(self):
        return {
            "success": self.success,
            "message": self.message,
            "data": self.data
        }
