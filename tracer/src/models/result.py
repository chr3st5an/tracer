from typing import Optional, Dict, Any
from copy import deepcopy

from colorama import Fore


class Result(object):
    """Represents the result of a HTTP request

    Objects of this class are mainly intended for
    view-only use and hence don't offer big
    functionalities. Objects of this class are
    in a close relationship with `tracer.Website`
    instances as the main aim of this class is
    to represent the results of the requests performed
    by those instances.

    Attributes
    ----------
    website : tracer.Website
        The website that is associated with the result.
    status_code : int
        The returned status code of the HTTP request
    successfully : bool
        If the request was successfully in the sense of
        that the username exists.
    user_exists : bool
        Alias for `obj.successfully`.
    delay : float
        The amount of seconds it took for a response.
    ms : float
        Alias for `obj.delay`.
    host : str
        The domain name of the website.
    url : str
        The request URL.
    timeout : bool
        If a TimeoutError occurred while performing
        the request.
    error : Exception, optional
        Any other excpetion that might have occurred while
        performing the request. None if none occurred.

    Methods
    -------
    obj.verbose(Optional[bool]) -> str
        Returns a string containing the key information of the
        result.

    Supported Operations
    --------------------
    `str(obj)`
        Returns the str representation of the result
    `bool(obj)`
        Alias for `obj.successfully`
    `copy.copy(obj)`
        Returns a copy of the result
    `copy.deepcopy(obj)`
        Returns a deepcopy of the result

    Author
    ------
    chr3st5an
    """

    def __init__(self,
        website,
        status_code: int,
        successfully: bool,
        delay: float,
        host: str,
        url: str,
        timeout: bool = False,
        error: Optional[Exception] = None
    ) -> None:
        """Represents the result of a request

        Parameters
        ----------
        website : tracer.Website
            The website to which the result belongs to
        status_code : int
            The returned status code of the request
        successfully : bool
            If the request was successfully, alias if the
            username exists
        delay : float
            How many seconds it took for a response
        host : str
            The host of the website to which a requests got
            send (alias the domain)
        url : str
            The request url
        timeout : bool, optional
            If the request timed out, by default False
        error : Exception, optional
            Any exception that might have occurred, by default None
        """

        self.__website      = website
        self.__status_code  = status_code
        self.__successfully = successfully
        self.__delay        = round(delay, 3)
        self.__host         = host
        self.__url          = url
        self.__timeout      = timeout
        self.__error        = error

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}(user_exists={self.user_exists}, delay={self.delay}, " \
            f"timeout={self.timeout}, error={bool(self.error)}>"

    def __bool__(self) -> bool:
        return self.__successfully

    def __copy__(self):
        result = self.__class__.__new__(self.__class__)
        result.__dict__.update(self.__dict__)

        return result

    def __deepcopy__(self, memo: Dict[int, Any]):
        result = self.__class__.__new__(self.__class__)

        memo[id(self)] = result

        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))

        return result

    @property
    def website(self):
        return self.__website

    @property
    def status_code(self) -> int:
        return self.__status_code

    @property
    def successfully(self) -> bool:
        return self.__successfully

    @property
    def user_exists(self) -> bool:
        """Alias for `result.successfully`
        """
        return self.successfully

    @property
    def delay(self) -> float:
        return self.__delay

    @property
    def ms(self) -> float:
        """Alias for `result.delay`
        """
        return self.delay

    @property
    def host(self) -> str:
        return self.__host

    @property
    def url(self) -> str:
        return self.__url

    @property
    def timeout(self) -> bool:
        return self.__timeout

    @property
    def error(self) -> Optional[Exception]:
        return self.__error

    def verbose(self, colored: bool = True) -> str:
        """Creates a verbose string

        The string returned by this method is mainly
        intended for logging purposes. It contains
        the delay, host and status code of the request.

        Parameters
        ----------
        colored : bool, optional
            If the string should be colored, by default True

        Returns
        -------
        str
            Verbose string
        """

        message = f"{self.ms}s <=> {self.host} <=> {self.status_code}"

        return f"{Fore.CYAN}{message}{Fore.RESET}" if colored else message
