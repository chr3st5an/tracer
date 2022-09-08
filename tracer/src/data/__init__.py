"""
MIT License

Copyright (c) 2022 chr3st5an

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from typing import List, Dict
import json
import os


__all__ = ("LOGO", "HTTPHEADER", "POOL")


POOL: List[Dict[str, str]]
LOGO: str
HTTPHEADER: Dict[str, str]


class FileLocation(object):
    """Represents the location of common files to load on startup

    Modify the attributes of this class in order to change
    the location where the program loads its data from.
    The value of each attribute should be either a relative
    or absolute path pointing to a file.
    """

    # Absolute path pointing to the directory of this file
    _path = os.path.dirname(os.path.realpath(__file__)) + "/"

    # COMMON FILES
    LOGO       = _path + "logo.txt"
    HTTPHEADER = _path + "httpheader.json"
    POOL       = _path + "pool.json"


try:
    with open(FileLocation.LOGO) as f:
        LOGO = f.read()
except FileNotFoundError:
    LOGO = ""
    print(f"[WARNING] File '{FileLocation.LOGO}' not found! Using no logo.")

try:
    with open(FileLocation.HTTPHEADER) as f:
        HTTPHEADER = json.load(f)
except FileNotFoundError:
    HTTPHEADER = {}
    print(f"[WARNING] File '{FileLocation.HTTPHEADER}' not found! Using default header.")

try:
    with open(FileLocation.POOL) as f:
        POOL = json.load(f)
except FileNotFoundError:
    print(f"[ERROR] Required file '{FileLocation.POOL}' not found! Quitting program.")
    exit(0)
