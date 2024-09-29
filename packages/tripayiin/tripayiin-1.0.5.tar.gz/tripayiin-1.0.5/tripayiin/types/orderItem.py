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

from typing import Optional, Union


class OrderItem:
    def __init__(
        self,
        sku: str,
        productName: str,
        price: Union[int, float],
        quantity: int,
        productUrl: Optional[str] = None,
        imageUrl: Optional[str] = None
    ):
        self.sku = sku
        self.name = productName
        self.price = price
        self.quantity = quantity
        self.productUrl = productUrl if productUrl is not None else ''
        self.imageUrl = imageUrl if imageUrl is not None else ''

    def __repr__(self):
        return f"OrderItem(sku={self.sku}, name={self.name}, price={self.price}, quantity={self.quantity}, product_url={self.productUrl}, image_url={self.imageUrl})"

    def parse(self):
        return {
            "sku": self.sku,
            "name": self.name,
            "price": self.price,
            "quantity": self.quantity,
            "product_url": self.productUrl,
            "image_url": self.imageUrl
        }
