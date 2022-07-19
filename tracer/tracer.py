"""Tracer

This script allows the user to detect on which websites a username is currently
used. Chances are that there is always the same person behind a username as
long as the username is special enough.

Arguments can be provided through the CLI or through a config (.conf) file.

This script requires aiohttp, requests, aiofiles & colorama to be installed.
"""

from typing import Dict, List, Optional, Union
from threading import Thread
from time import monotonic
from pathlib import Path
import http.cookies
import webbrowser
import asyncio
import json
import os

from pyvis.network import Network
from aiohttp import ClientSession
from colorama import Fore
import aiohttp
import aiofiles

try:
    from src import *
except ModuleNotFoundError:
    from .src import *


CONFIG = "./settings.conf"
MY_IP  = "https://api.myip.com"


class Tracer(object):
    """Implements the main logic behind Tracer

    Author
    ------
    chr3st5an
    """

    @classmethod
    def main(cls) -> None:
        """Creates a tracer instance and calls its run coro

        Parses given args and creates an asyncio event loop
        with which it applies `run_until_complete` on the
        run coro.
        """

        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        #> Gets the configs from the conf file and
        #> updates these with the provided CLI options
        kwargs = TracerParser(CONFIG).parse()

        try:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(cls(kwargs.pop("username"), **kwargs).run())
        except KeyboardInterrupt:
            print("👋 Bye")
        finally:
            loop.stop()

    def __init__(self,
        username: str,
        data: List[Dict[str, str]] = POOL,
        headers: Dict[str, str] = HTTPHEADER,
        **kwargs
    ) -> None:

        self.username = username
        self.kwargs   = dict(kwargs)
        self.headers  = headers
        self.pool     = WebsitePool(*map(Website.from_dict, data), name="TracerPool")
        self.verbose  = kwargs.get("verbose", False)

        self.pool.set_username(self.username)

        self._out_dir = None
        self.__filter_sites()

        if kwargs.get("create_file_output"):
            self._create_output_dir()

        #> When sending a request to TikTok, an annoying message
        #> is printed by aiohttp. This turns the message off.
        http.cookies._is_legal_key = lambda _: True

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}(username=\"{self.username}\", kwargs={self.kwargs}, " \
            f"headers={self.headers}, pool={self.pool})>"

    def __filter_sites(self) -> None:
        include: List[str] = self.kwargs.get('only', []) + self.kwargs.get('only_category', [])
        exclude: List[str] = self.kwargs.get('exclude', []) + self.kwargs.get('exclude_category', [])

        if not (include or exclude):
            return None

        include = [string.lower() for string in include]
        exclude = [string.lower() for string in exclude]

        if exclude:
            self.pool.remove(lambda w: (w.domain in exclude) or (w.category.as_str in exclude))

        if include:
            self.pool.remove(lambda w: not ((w.domain in include) or (w.category.as_str in include)))

    async def run(self) -> None:
        """Runs the program
        """

        if self.kwargs.get("print_logo", True):
            print(f"\n{Fore.CYAN}{LOGO}{Fore.RESET}\n")

        async with ClientSession(headers=self.headers, cookie_jar=aiohttp.DummyCookieJar()) as session:
            if self.kwargs.get("ip_check"):
                await self.retrieve_ip(session, timeout=self.kwargs.get("ip_timeout"))

            print(f"[{Fore.CYAN}*{Fore.RESET}] Checking {Fore.CYAN}{self.username}{Fore.RESET} on {len(self.pool)} sites:\n")

            start    = monotonic()
            counter  = 0
            requests = self.pool.start_requests(session, self.kwargs.get("timeout"))

            async for response in requests:
                message = f"{response.url} {response.verbose() if self.kwargs.get('verbose') else ''}"

                if not response.successfully:
                    if self.kwargs.get("all"):
                        if response.timeout:
                            print(f"{Fore.RED}[Timeout]{Fore.RESET} {message}")
                        else:
                            print(f"{Fore.RED}[-]{Fore.RESET} {message}")

                    continue

                print(f"{Fore.GREEN}[+]{Fore.RESET} {message}")

                if self.kwargs.get("browse"):
                    Thread(target=webbrowser.open, args=(response.url, )).start()

                counter += 1

        await session.close()

        print(
            f"\n[{Fore.CYAN}={Fore.RESET}] Found {Fore.CYAN}{counter}{Fore.RESET} match(es) "
            f"in {Fore.CYAN}{round(monotonic() - start, 2)}s{Fore.RESET}"
        )

        await asyncio.gather(
            self.write_report(self._out_dir),
            self.draw_graph(self._out_dir)
        )

    async def write_report(self, out_dir: Union[str, Path]) -> None:
        """Creates and writes a report file which contains the results

        Parameters
        ----------
        out_dir : Union[str, Path]
            In which directory to save the report file. If `None`
            is given, then no report file is created
        """

        if self._out_dir is None:
            return None

        name = f"{out_dir}result.txt"
        mode = "w" if os.path.exists(name) else "x"

        async with aiofiles.open(name, mode) as file:
            await file.write(f"{LOGO}\nReport for {self.username}:\n\n")

            for result in self.pool.results:
                await file.write(result.url + "\n")

    async def draw_graph(self, out_dir: Optional[Union[str, Path]]) -> None:
        """Visualizes the results

        Creates a HTML file containing a graph and opens it
        in the default webbrowser

        Parameters
        ----------
        out_dir : Union[str, Path]
            In which directory to save the HTML file. If `None`
            is given, then no graph is created
        """

        if self._out_dir is None:
            return None

        net = Network(
            height="100%",
            width="100%",
            bgcolor="#282a36",
            font_color="#f8f8f2",
        )

        net.add_node(self.username, color="#ff79c6", title="Username", shape="circle")

        for category in Category.all_categories():
            net.add_node(
                n_id=category.title(),
                color="#bd93f9",
                shape="circle",
                title=category.title(),
                labelHighlightBold=True
            )
            net.add_edge(self.username, category.title())

            await asyncio.sleep(0.00075)

        for site in self.pool:
            if site.result.user_exists:
                net.add_node(
                    n_id=site.name,
                    color="#ff5555",
                    shape="circle",
                    title=site.url,
                    labelHighlightBold=True
                )
                net.add_edge(site.category.as_str.title(), site.name)

            await asyncio.sleep(0.00075)

        #> Settings for the graph
        net.toggle_physics(True)
        net.set_edge_smooth("dynamic")

        #> Saves the graph in a html file and opens it
        #> in the default browser
        net.show(f"{out_dir}graph.html")

    async def retrieve_ip(self, session: ClientSession, timeout: Optional[float] = None) -> str:
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
                return {"ip": "0.0.0.0 [TIMEOUT]"}

        response = asyncio.create_task(send_request())

        await AsyncTextAnimation("Retrieving IP...", lambda: not response.done()).start()

        print(f"Your IP address is {Fore.CYAN}{response.result()['ip']}{Fore.RESET}\n")

        await asyncio.sleep(3)

    def _create_output_dir(self) -> str:
        folder_name = "./results/"

        if not os.path.exists(folder_name):
            os.mkdir(folder_name)

        if not os.path.exists(f"{folder_name}{self.username}"):
            os.mkdir(f"{folder_name}{self.username}/")

        self._out_dir = f"{folder_name}{self.username}/"


if __name__ == "__main__":
    Tracer.main()
