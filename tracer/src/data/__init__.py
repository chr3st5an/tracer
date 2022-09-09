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
from secrets import choice
import json
import os


__all__ = ("LOGO", "USER_AGENT", "POOL")


POOL: List[Dict[str, str]]
LOGO: str
USER_AGENT: str


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
    USER_AGENT = _path + "user_agents.json"
    POOL       = _path + "pool.json"


try:
    with open(FileLocation.LOGO) as f:
        LOGO = f.read()
except FileNotFoundError:
    LOGO = ""
    print(f"[WARNING] File '{FileLocation.LOGO}' not found! Using no logo.")

# UserAgents taken from here: https://gist.github.com/pzb/b4b6f57144aea7827ae4#file-user-agents-txt
try:
    with open(FileLocation.USER_AGENT) as f:
        USER_AGENT = choice(json.load(f))
except FileNotFoundError:
    USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"
    print(f"[WARNING] File '{FileLocation.USER_AGENT}' not found! Using the default UserAgent.")

try:
    with open(FileLocation.POOL) as f:
        POOL = json.load(f)
except FileNotFoundError:
    print(f"[ERROR] Required file '{FileLocation.POOL}' not found! Quitting program.")
    exit(0)
