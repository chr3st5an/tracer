from __future__ import annotations

from typing import Any, Callable, Coroutine, Dict, Optional, Union
from time import monotonic
from copy import deepcopy
import asyncio
import re

from aiohttp import ClientSession, ClientResponse, ClientTimeout
from asyncio import TimeoutError

from .category import Category
from .result import Result


__all__ = ("Website", )


class Website(object):
    """Represents a website

    Attributes
    ----------
    name : str
        The name of the website, e.g. 'example'
    domain : str
        The domain name of the website, e.g. 'example.com'
    username : str
        The username whose existence is being checked on this
        website
    url : str
        The url that represents an users page on this website,
        e.g. 'https:\/\/example.com/user/'
    true_url : str
        The url that gets used to make the HTTP request to this
        website
    category : int
        The category to which the website belongs to
    result : tracer.Result
        The result of the request, `None` if no request was
        started yet
    err_ignore_code : bool
        Indicates if the returned status code of the request
        should be ignored
    err_text_pattern : str
        Regex pattern that gets applied on the returned text.
        If it matches, the username is considered as
        'Not Found'
    err_url_pattern : str
        Regex pattern that gets applied on the returned url.
        If it matches, the username is considered as
        'Not Found'
    err_on_dot : bool
        Indicates if the website responses with an error
        if the username contains a dot. If `True`, no
        actual request is send to the website

    Methods
    -------
    obj.set_username(str) -> None
        Sets a username for the website whose existence is later being
        checked
    obj.set_result(tracer.Result) -> None
        Sets a result for the website
    obj.send_request(aiohttp.ClientSession, Optional[float], Optional[Callable]) -> None
        Sends a HTTP GET request to the website and checks if
        the username exists. Then creates a `tracer.Result` object
        and assigns it to itself by using `obj.set_result`

    Classmethods
    ------------
    cls.from_dict(dict) -> tracer.Website
        Creates a `tracer.Website` object by using the values
        of the dict

    Supported Operations
    --------------------
    `str(obj)`
        Returns the str representation of the website
    `x == obj`
        Compares if `(1):` the other object is a `tracer.Website`
        object and if `(2):` the values are the same
    `copy.copy(obj)`
        Returns a copy of the website
    `copy.deepcopy(obj)`
        Returns a deepcopy of the website

    Note
    ----
    The URL(s) passed to an object of this class should
    be structured as following `https://www.example.com/path/{}`,
    where `{}` represents the field into which the username
    is placed

    Author
    ------
    chr3st5an
    """

    @classmethod
    def from_dict(cls, data: Dict[str, str]):
        """Creates a Website by using the given data

        Parameters
        ----------
        data : Dict[str, str]
            A dict whose values are used to create the
            Website. The dict must include the following
            keys: `domain`, `url` & `category`

        Returns
        -------
        tracer.Website
            The Website that got created

        Example
        -------
        >>> data = {"domain": "example.com", "url": "https://...", "category": Category.OTHER}

        >>> site = Website.from_dict(data)
        """

        return cls(
            domain=data["domain"],
            true_url=data["url"],
            category=data["category"],
            display_url=data.get("display_url"),
            err_ignore_code=data.get("err_ignore_code", False),
            err_text_pattern=data.get("err_text_pattern"),
            err_url_pattern=data.get("err_url_pattern"),
            err_on_dot=data.get("err_on_dot", False)
        )

    def __init__(self,
        domain: str,
        true_url: str,
        category: int,
        display_url: Optional[str] = None,
        err_ignore_code: bool = False,
        err_text_pattern: Optional[str] = None,
        err_url_pattern: Optional[str] = None,
        err_on_dot: bool = False
    ) -> None:
        """Creates an instance

        Parameters
        ----------
        domain : str
            The domain name of the website, e.g. 'example.com'
        true_url : str
            The url that gets used to make the HTTP request to this
            website
        category : int
            The category to which the website belongs to
        display_url : str, optional
            The url that represents an users page on this website,
            e.g. 'https:\/\/example.com/user/'. If None, then
            `true_url` is used, by default None
        err_ignore_code : bool
            Indicates if the returned status code of the request
            should be ignored, by default False
        err_text_pattern : str
            Regex pattern that gets applied on the returned text.
            If it matches, the username is considered as
            'Not Found', by default None
        err_url_pattern : str
            Regex pattern that gets applied on the returned url.
            If it matches, the username is considered as
            'Not Found', by default None
        err_on_dot : bool
            Indicates if the website responses with an error
            if the username contains a dot. If `True`, no
            actual request is send to the website, by default
            False
        """

        self.__url      = display_url if display_url else true_url
        self.__true_url = true_url
        self.__username = None
        self.__result   = None
        self.__category = Category(self, category)
        self.__domain   = domain

        self.err_ignore_code  = err_ignore_code
        self.err_text_pattern = err_text_pattern
        self.err_url_pattern  = err_url_pattern
        self.err_on_dot       = err_on_dot

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}(name=\"{self.name}\", domain=\"{self.domain}\", " \
            f"url=\"{self.url}\", category={self.category}, result={self.result})>"

    def __eq__(self, other: Any) -> bool:
        return isinstance(other, self.__class__) and self.__dict__ == other.__dict__

    def __copy__(self):
        website = self.__class__.__new__(self.__class__)
        website.__dict__.update(self.__dict__)

        return website

    def __deepcopy__(self, memo: Dict[int, Any]):
        website = self.__class__.__new__(self.__class__)

        memo[id(self)] = website

        for k, v in self.__dict__.items():
            setattr(website, k, deepcopy(v, memo))

        return website

    @property
    def name(self) -> str:
        return self.__domain.split('.')[0]

    @property
    def domain(self) -> str:
        return self.__domain

    @property
    def username(self) -> Optional[str]:
        return self.__username

    @property
    def category(self) -> Category:
        return self.__category

    @property
    def result(self) -> Optional[Result]:
        return self.__result

    @property
    def url(self) -> str:
        return self.__url.format(self.username) if self.username else self.__url

    @property
    def true_url(self) -> str:
        return self.__true_url.format(self.username) if self.username else self.__true_url

    def set_username(self, username: Optional[str]) -> None:
        """Sets a username

        Parameters
        ----------
        username : Optional[str]
            The username to set for the website
        """

        self.__username = username

    def set_result(self, result: Optional[Result]) -> None:
        """Sets a result

        Parameters
        ----------
        result : Optional[Result]
            The result for the website
        """

        self.__result = result

    async def send_request(self,
        session: ClientSession,
        timeout: Optional[float] = None,
        callback: Optional[Callable[[Result], Union[Coroutine, Any]]] = None
    ) -> None:
        """Sends a GET requests and evaluates the response

        Parameters
        ----------
        session : ClientSession
            ClientSession to use for the GET request
        timeout : Optional[float], optional
            How many seconds the request has before a
            TimeoutError occurs, by default None
        callback : Optional[Callable[[Result], Union[Coroutine, Any]]], optional
            Any callable object that gets called when
            the result is available. It should only
            take in one parameter which is the result,
            by default None

        Raises
        ------
        TypeError
            username not set
        """

        if self.username is None:
            raise TypeError("Cannot start request without a username being set")

        if "." in self.username and self.err_on_dot:
            self.set_result(Result(self, 400, False, 0, self.domain, self.url))

            await self.__callback(callback)

            return None

        start = monotonic()

        try:
            async with session.get(self.true_url, timeout=ClientTimeout(timeout)) as r:
                if await self.__user_exists(r, await r.text()):
                    self.set_result(Result(self, r.status, True, monotonic() - start, r.host, self.url))
                else:
                    self.set_result(Result(self, r.status, False, monotonic() - start, r.host, self.url))

                r.close()
                await r.wait_for_close()
        except TimeoutError:
            self.set_result(Result(self, 400, False, monotonic() - start, self.domain, self.url, True))
        except Exception as e:
            self.set_result(Result(self, 600, False, monotonic() - start, self.domain, self.url, error=e))

        await self.__callback(callback)

    async def __user_exists(self, response: ClientResponse, html: str) -> bool:
        """Checks based on the returned response if the username is in use.

        First checks if the response status is 200 and then
        applies the given regex pattern.

        Parameters
        ----------
        response : aiohttp.ClientResponse
            A ClientResponse generated by `aiohttp`.
        html : str
            The html text returned by the response.

        Returns
        -------
        bool
            Indicator if the username exists
        """

        if not (response.status == 200 or self.err_ignore_code):
            return False

        await asyncio.sleep(0)

        if self.err_url_pattern and re.search(self.err_url_pattern, str(response.url), flags=re.I):
            return False

        await asyncio.sleep(0)

        if self.err_text_pattern and re.search(self.err_text_pattern, html, flags=re.S + re.I + re.M):
            return False

        return True

    async def __callback(self, callback: Optional[Callable[[Result], Union[Coroutine, Any]]]) -> Any:
        if (callback is None) or (not callable(callback)):
            return None

        await asyncio.sleep(0)

        if asyncio.iscoroutinefunction(callback):
            return await callback(self.result)

        return callback(self.result)
