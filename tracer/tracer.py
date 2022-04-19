"""Tracer

This script allows the user to detect on which websites a username is currently
used. Chances are that there is always the same person behind a username as
long as the username is special enough.

Arguments can be provided through the CLI or through a config (.conf) file.

This script requires aiohttp, requests, aiofiles & colorama to be installed.
"""

from typing import Dict, List, Optional, Union
from time import monotonic
from pathlib import Path
import http.cookies
import webbrowser
import asyncio
import json
import os

from aiohttp import ClientSession
from colorama import Fore
import aiohttp
import aiofiles

try:
    from src import *
except ModuleNotFoundError:
    from .src import *


CONFIG            = "./settings.conf"
REPORT_OUTPUT_DIR = f"{Path.home()}/Downloads/"
MY_IP             = "https://api.myip.com"


class Tracer(object):
    @classmethod
    def main(cls) -> None:
        """Creates a tracer instance and calls its run coro

        Parses given args and creates an asyncio event loop
        with which it applies `run_until_complete` on the
        run coro.
        """

        os.chdir(os.path.dirname(os.path.realpath(__file__)))

        # Gets the configs from the conf file and
        # updates these with the provided CLI options
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

        self.__filter_sites()

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
            print(f"{Fore.CYAN}{LOGO}{Fore.RESET}\n")

        async with ClientSession(headers=self.headers, cookie_jar=aiohttp.DummyCookieJar()) as session:
            if self.kwargs.get("ip_check"):
                await self.retrieve_ip(session, timeout=self.kwargs.get("ip_timeout"))

            self.pool.set_username(self.username)

            print(f"[{Fore.CYAN}*{Fore.RESET}] Checking {Fore.CYAN}{self.username}{Fore.RESET} on {len(self.pool)} sites:\n")

            start = monotonic()

            requests = self.pool.start_requests(session, self.kwargs.get("timeout"))

            counter = 0

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
                    webbrowser.open(response.url)

                counter += 1

        await session.close()

        print(
            f"\n[{Fore.CYAN}={Fore.RESET}] Found {Fore.CYAN}{counter}{Fore.RESET} match(es) "
            f"in {Fore.CYAN}{round(monotonic() - start, 2)}s{Fore.RESET}"
        )

        await self.write_report(REPORT_OUTPUT_DIR)

    async def write_report(self, out_dir: Union[str, Path]) -> None:
        """Creates and writes a report file which contains the results

        Parameters
        ----------
        username : str
            The username for whom the report is generated.
            The filename is also gonna be the same as the username.
        out_dir : Union[str, Path]
            Specifies the location where the file shall be created.

        Raises
        ------
        Exception
            `out_dir` doesn't exist
        """

        if not os.path.exists(out_dir):
            raise Exception("Provided path does not exist")

        name = f"{out_dir}{self.username}.txt"
        mode = "w" if os.path.exists(name) else "x"

        async with aiofiles.open(name, mode) as file:
            await file.write(f"{LOGO}\nReport for {self.username}:\n\n")

            for result in self.pool.results:
                await file.write(result.url + "\n")

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


if __name__ == "__main__":
    Tracer.main()
