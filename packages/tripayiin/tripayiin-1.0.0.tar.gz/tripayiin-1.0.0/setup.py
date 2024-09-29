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

import os
import re
import shutil
import sys
from setuptools import setup, find_packages

def clearFolder(folder):
    try:
        # Remove Directory
        if os.path.exists(folder):
            shutil.rmtree(folder)
    except Exception as e:
        print(e)


with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

with open("tripayiin/__init__.py", encoding="utf-8") as f:
    version = re.findall(r"__version__ = \"(.+)\"", f.read())[0]

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

if sys.argv[-1] == "publish":
    clearFolder("build")
    clearFolder("dist")
    clearFolder("tripayiin.egg-info")
    os.system("pip install twine setuptools")
    os.system("python setup.py sdist")
    os.system("twine upload dist/*")
    sys.exit()

setup(
    name="tripayiin",
    version=version,
    description="TriPay Payment Gateaway Client For Python (Unofficial)",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/AyiinXd",
    download_url="https://github.com/AyiinXd/tripayiin/releases/latest",
    author="AyiinXd",
    author_email="ayiincorporation@gmail.com",
    license="LGPLv3",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Utilities"
    ],
    keywords="tripay payment gateway",
    project_urls={
        "Tracker": "https://github.com/AyiinXd/tripayiin/issues",
        "Community": "https://t.me/AyiinChats",
        "Source": "https://github.com/AyiinXd/tripayiin",
    },
    python_requires="~=3.8",
    package_data={
        "tripayiin": ["py.typed"],
    },
    packages=find_packages(exclude=["tests*"]),
    zip_safe=False,
    install_requires=requires,
)