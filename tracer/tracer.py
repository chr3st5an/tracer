"""Tracer

This script allows the user to detect on which websites a username is currently
used. Chances are that there is always the same person behind a username as
long as the username is special enough.

Arguments can be provided through the CLI or through a config (.conf) file.

This script requires aiohttp, requests, aiofiles & colorama to be installed.
"""
import asyncio
import aiohttp
import aiofiles
import webbrowser
import http.cookies
import json
import re
import os

from aiohttp import ClientSession
from asyncio import Queue
from argparse import ArgumentParser
from configparser import ConfigParser
from colorama import Fore
from time import monotonic
from collections import namedtuple

from typing import Any, Optional, Union, AsyncGenerator, Callable, NamedTuple, List, Dict
from pathlib import Path

try:
    from src import *
except ModuleNotFoundError:
    from .src import *


__version__ = "1.0.0"
__author__  = "chr3st5an"


CONFIG            = "./settings.conf"
REPORT_OUTPUT_DIR = f"{Path.home()}/Downloads/"
MY_IP             = "https://api.myip.com"


def main() -> None:
    """Wrapper for `tracer.run`

    Parses the configs for `run` and takes care of the event
    loop.
    """

    # Gets the configs from the conf file and
    # updates these with the provided CLI options
    kwargs = get_conf(CONFIG)
    kwargs.update(get_args())

    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(run(kwargs.pop("username"), **kwargs))
    except KeyboardInterrupt:
        print("👋 Bye")
    finally:
        loop.stop()


async def run(username: str, **kwargs) -> None:
    """Runs the program

    Parameters
    ----------
    username : str
        The username that gets checked
    """

    start = monotonic()

    if kwargs.get("print_logo", True):
        print(f"{Fore.CYAN}{LOGO}{Fore.RESET}")

    # When sending a request to TikTok, an annoying message
    # is printed by aiohttp. This turns the message off.
    http.cookies._is_legal_key = lambda _: True

    sites = filter_sites(POOL, kwargs.get("exclude"), kwargs.get("exclude_category"), action="exclude")
    sites = filter_sites(sites, kwargs.get("only"), kwargs.get("only_category"), action="only")

    # Generator used to write the results to the report file
    writer = file_writer(username, REPORT_OUTPUT_DIR)

    counter = 0

    async with ClientSession(headers=HTTPHeader, cookie_jar=aiohttp.DummyCookieJar()) as session:
        if kwargs.get("ip_check"):
            await retrieve_ip(session, timeout=kwargs.get("ip_timeout"))

        # Creates the report file and writes the logo to it
        await writer.__anext__()

        print(f"[{Fore.CYAN}*{Fore.RESET}] Checking {Fore.CYAN}{username}{Fore.RESET} on {len(sites)} sites:\n")

        requests = start_requests(session, sites, username, kwargs.get("timeout"))

        async for response in requests:
            if not response.successfully:
                if kwargs.get("all"):
                    if response.timeout:
                        print(f"{Fore.RED}[Timeout]{Fore.RESET} {response.url}")
                    else:
                        print(f"{Fore.RED}[-]{Fore.RESET} {response.url} {verbose(response, kwargs.get('verbose'))}")

                continue

            print(f"{Fore.GREEN}[+]{Fore.RESET} {response.url} {verbose(response, kwargs.get('verbose'))}")

            if kwargs.get("browse"):
                webbrowser.open(response.url)

            # Writes the url to the file
            await writer.asend(response.url)

            counter += 1

    await writer.aclose()

    print(
        f"\n[{Fore.CYAN}={Fore.RESET}] Found {Fore.CYAN}{counter}{Fore.RESET} match(es) "
        f"in {Fore.CYAN}{round(monotonic() - start, 2)}s{Fore.RESET}"
    )

    # In some cases timeouts cause the program not to be
    # finished at this points
    if len(asyncio.all_tasks()) > 1:
        await shutdown_animation()


async def retrieve_ip(session: aiohttp.ClientSession, timeout: Optional[Union[int, float]] = None) -> None:
    """Retrieves the IP address and prints it

    Sleeps for 3 seconds after the IP got printed.

    Parameters
    ----------
    session : aiohttp.ClientSession
        Session used to sent a request
    timeout : Union[int, float], optional
        Sets a timeout for the request. Defaults to None.
    """

    async def send_request():
        try:
            async with session.get(MY_IP, timeout=aiohttp.ClientTimeout(timeout)) as r:
                return json.loads(await r.text())
        except asyncio.TimeoutError:
            return {"ip": "0.0.0.0 (Timeout)"}

    response = asyncio.create_task(send_request())

    await loading_animation("Retrieving IP...", lambda: not response.done())

    print(f"Your IP address is {Fore.CYAN}{response.result()['ip']}{Fore.RESET}\n")

    await asyncio.sleep(3)


async def start_requests(session: ClientSession, site_data: dict, username: str, timeout: Optional[Union[int, float]] = None) -> AsyncGenerator[NamedTuple, None]:
    """Prepares and handles all requests

    Prepares all requests that are going to be made and
    handles the results of those.

    Parameters
    ----------
    session : ClientSession
        A session object which gets used to make the
        requests.
    site_data : dict
        A dict which contains data about the websites
        to which a request is send. It should be
        structured like `src/pool.py`
    username : str
        A username whose existence is checked.
    timeout : Union[int, float], optional
        Represents the time each request has before a
        TimeoutError occurs.

    Returns
    -------
    AsyncGenerator[NamedTuple, None]
        On each iterations a result of a request is yielded

    Yields
    ------
    NamedTuple
        A simplified representation of the results of a request:
        NamedTuple(`successfully: bool`, `delay: float`, `host: str`, `url: str`, `timeout: bool`)

    Example
    -------
    results = start_requests(...)

    async for result in results:
        print(result.url)
    """

    # A queue in which each request will put their result in
    results = Queue()

    coroutines = [make_request(session, site, results, username, timeout) for site in site_data]
    requests   = asyncio.gather(*coroutines)

    while not (requests.done() and results.empty()):
        try:
            yield await asyncio.wait_for(results.get(), timeout=1)
        except Exception:
            # Force recheck of the loop condition
            continue


async def make_request(session: ClientSession, site: dict, queue: Queue, username: str, timeout: Optional[Union[int, float]] = None) -> None:
    """Makes a request and evaluates if the username exists

    Parameters
    ----------
    session : ClientSession
        A session object which gets used to make the request
    site : dict
        A dict containing data about the website. This has to
        include the url to which a request is send.
    queue : Queue
        A queue in which the result of the request is put in.
    username : str
        A username whose existence is checked.
    timeout : Optional[Union[int, float]], optional
        Sets a timeout for the request, by default None
    """
    # Checks if the username contains a dot, and if the
    # site would respond with a false result if the
    # username contains a dot.
    if "." in username and site.get("err_dot"):
        return None

    url: str = site["url"].format(user=username)

    scrn_url: str = site.get("screen_url", url).format(user=username)

    # Namedtuple used to store the result
    Response = namedtuple("Response", ["successfully", "delay", "host", "url", "timeout"], defaults=[scrn_url, False])

    start = monotonic()

    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(timeout)) as r:
            delay = monotonic() - start

            # Starting the coroutine in a new thread since this coroutine
            # depends on time consuming regex
            if user_exist(r, await r.text(), site.get("err_pattern"), site.get("err_url")):
                await queue.put(Response(True,  delay, r.host))
            else:
                await queue.put(Response(False, delay, r.host))

            return r.close()
    except asyncio.TimeoutError:
        await queue.put(Response(False, -1, site.get("domain", ""), scrn_url, True))
    except Exception:
        return None


async def file_writer(username: str, out_dir: Union[str, Path]) -> AsyncGenerator[None, str]:
    """Creates and writes a report file which contains the results

    Parameters
    ----------
    username : str
        The username for whom the report is generated.
        The filename is also gonna be the same as the username.
    out_dir : Union[str, Path]
        Specifies the location where the file shall be created.

    Returns
    -------
    AsyncGenerator[None, str]
        An AsyncGenerator to which str's can be send which
        will then be written to the file.

    Raises
    ------
    Exception
        `out_dir` doesn't exist
    """

    if not os.path.exists(out_dir):
        raise Exception("Provided path does not exist")

    name = f"{out_dir}{username}.txt"
    mode = "w" if os.path.exists(name) else "x"

    async with aiofiles.open(name, mode) as file:
        await file.write(f"{LOGO}\nReport for {username}:\n\n")

        while True:
            url = yield None

            await file.write(url + "\n")


async def shutdown_animation() -> None:
    """Alias for loading_animation"""

    await loading_animation("Safely shutting down...", lambda: len(asyncio.all_tasks()) > 1)


async def loading_animation(msg: str, condition: Callable[..., bool], *args: Any) -> None:
    """Displays a loading animation as long as the given condition is True

    Parameters
    ----------
    msg : str
        The message that will appear besides the loading animation.
    condition : Callable[..., bool]
        A callable object that returns a bool which represents the
        main condition for the animation loop. Once the callable
        returns `False`, the loading animation will end and the
        message will get removed.
    *args : Any
        Arguments that directly get passed to `condition` when
        calling it.
    """

    animation = "|/-\\"

    while condition(*args):
        for cha in animation:
            await asyncio.sleep(0.1)

            message = f"[{Fore.CYAN}{cha}{Fore.RESET}] {msg}"

            print("\r" + message, end="")

    # Removes the loading message
    print("\r" + " " * (len(msg) + 10), end="\r")


def get_conf(file: Union[Path, str]) -> Dict[str, str]:
    """Parses settings from a conf file and converts it into a dict

    Parameters
    ----------
    file : Union[Path, str]
        Path to a conf file

    Returns
    -------
    dict[str, str]
        A dict containing the settings

    Note
    ----
    The conf file must contain a `[DEFAULT]` header
    """

    if not os.path.exists(file):
        return dict()

    parser = ConfigParser()
    parser.read(file)

    settings = dict(parser["DEFAULT"])

    # Converts the options from the conf file into
    # corresponding datatypes
    for setting, value in settings.items():
        if value.lower() == "off":
            settings[setting] = False
        elif value.lower() == "on":
            settings[setting] = True
        elif value.lower() == "none":
            settings[setting] = None
        elif value == "":
            settings[setting] = list()
        elif value.isdigit():
            settings[setting] = float(value)
        else:
            settings[setting] = re.findall(r"[a-zA-Z0-9\.]+", value)

    return settings


def get_args() -> Dict[str, Any]:
    """Parses provided options from the CLI

    Returns
    -------
    dict
        A dict containing the provided options
    """

    parser = ArgumentParser(
        prog="tracer",
        usage="%(prog)s [options] username",
        description="Check on which website the specified username is in use",
        epilog="A tool created by @chr3st5an",
    )

    parser.add_argument(
        "username",
        metavar="username",
        type=str,
        help="The username to check"
    )
    parser.add_argument(
        "-t",
        "--timeout",
        metavar="seconds",
        type=int,
        help="set a timeout for each request",
    )
    parser.add_argument(
        "-e",
        "--exclude",
        metavar="domainName",
        type=str,
        default=list(),
        action="append",
        help="exclude a website, e.g. instagram.com. Can be used multiple times",
    )
    parser.add_argument(
        "-o",
        "--only",
        metavar="domainName",
        type=str,
        default=list(),
        action="append",
        help="sent a request only to the given site. Can be used multiple times",
    )
    parser.add_argument(
        "-E",
        "--exclude-category",
        metavar="category",
        type=str,
        default=list(),
        action="append",
        help=f"""exclude every website which belongs to the given category.
            Categories: {', '.join(Category.to_list())}""",
    )
    parser.add_argument(
        "-O",
        "--only-category",
        metavar="category",
        type=str,
        default=list(),
        action="append",
        help="""sent requests only to the sites belonging to the given category.
            See a list of all categories under -E""",
    )
    parser.add_argument(
        "-b",
        "--browse",
        default=False,
        action="store_true",
        help="open successfull results in browser",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        default=False,
        action="store_true",
        help="show additional information",
    )
    parser.add_argument(
        "-a",
        "--all",
        default=False,
        action="store_true",
        help="show all results"
    )
    parser.add_argument(
        "--ip-check",
        default=False,
        action="store_true",
        help="retrieve and print your IP on program startup and then wait 3s before continuing",
    )

    args: Dict[str, Any] = {}

    # Parses the args and filters options out that didn't were provided
    for key, value in dict(parser.parse_args()._get_kwargs()).items():
        if not (value == parser.get_default(key)):
            args[key] = value

    return args


def filter_sites(sites: List[Dict[str, Any]], domain_list: Optional[List[str]] = None, categories_list: Optional[List[int]] = None,
                 *, action: str = "exclude") -> List[Dict[str, Any]]:
    """Filters sites based on the parameters

    Parameters
    ----------
    sites : list[dict[str, Any]]
        A list with dict's in it on which the filters get applied
    sites_list : list[str]
        A list containing domain names which will be considered
        while filtering
    categories_list : list[int]
        A list containing the number of each category that will
        be considered while filtering
    action : str
        Two possible actions:
            `exclude`:
                removes every site from `site` that is in
                `sites_list` and `categories_list`
            `only`:
                removes every site from `site` that is not
                in `sites_list` and `categories_list`

    Returns
    -------
    list[dict[str, Any]]
        A new list containing the results of the filter process
    """

    if not (domain_list or categories_list):
        return sites

    filtered = []

    if domain_list is None:
        domain_list = []
    elif categories_list is None:
        categories_list = []

    categories_list = list(map(Category.resolve, categories_list))

    for site in sites:
        if (site.get("domain") in domain_list) or (site.get("category") in categories_list):
            if action.lower() == "exclude":
                continue
        else:
            if action.lower() == "only":
                continue

        filtered.append(site)

    return filtered


def user_exist(response: aiohttp.ClientResponse, html: str, err_pattern: Optional[str] = None, err_url: Optional[str] = None) -> bool:
    """Checks based on the returned response if the username is in use.

    First checks if the response status is 200 and then
    applies the given regex pattern.

    Parameters
    ----------
    response : aiohttp.ClientResponse
        A ClientResponse generated by `aiohttp`.
    html : str
        The html text returned by the response.
    err_pattern : str, optional
        A regex pattern which gets applied on `html`.
        If it matches, `False` is returned.
    err_url : str, optional
        A regex pattern which gets applied on the
        `response.url`. If it matches, `False` is returned.

    Returns
    -------
    bool
        Indicator if the username exists
    """

    if not (response.status == 200):
        return False
    elif err_url and re.search(err_url, str(response.url), flags=re.I):
        return False
    elif err_pattern and re.search(err_pattern, html, flags=re.S + re.I + re.M):
        return False

    return True


def verbose(response: NamedTuple, verbose: bool = True) -> str:
    """Creates a string with information about the response

    Parameters
    ----------
    response : NamedTuple
        A NamedTuple representing a response returned by
        `tracer.start_requests`
    verbose : bool, optional
        Decides if a verbose-string shall be returned or
        if an empty string is returned, by default True

    Returns
    -------
    str
        Either an empty string or a verbose string
    """

    if not verbose:
        return ""

    return f"{Fore.CYAN}{round(response.delay, 3)}s <=> {response.host}{Fore.RESET}"


if __name__ == "__main__":
    main()
