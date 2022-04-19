from configparser import ConfigParser
from typing import Any, Dict, Union
from argparse import ArgumentParser
from pathlib import Path
import os
import re

from .category import Category


class TracerParser(object):
    """Parses relevant args for Tracer

    Attributes
    ----------
    config_file : Union[Path, str]
        Path to a `.conf` file

    Methods
    -------
    obj.parse() -> Dict
        Parses args from the config file and from the
        CLI.

    Supported Operations
    --------------------
    `str(obj)`
        Returns the str representation of the parser

    Note
    ----
    The given config file has to include a `[DEFAULT]`
    header as the parser looks for values defined under
    that header.

    Author
    ------
    chr3st5an
    """

    def __init__(self, config_file: Union[Path, str]):
        """Creates a parser

        Parameters
        ----------
        config_file : Union[Path, str]
            Path to a `.conf` file

        Note
        ----
        The config file has to include a `[DEFAULT]`
        header
        """

        self.config_file = config_file

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}(config_file={self.config_file})>"

    def parse(self) -> Dict[Any, Any]:
        """Parses args from the config file and the CLI

        Returns
        -------
        Dict[str, str]
            A dict containing the given args
        """

        kwargs = self._parse_conf_file()
        kwargs.update(self._parse_console())

        return kwargs

    def _parse_conf_file(self) -> Dict[str, str]:
        """Parses args from the config file

        Returns
        -------
        Dict[str, str]
            A dict containing the given args
        """

        if not os.path.exists(self.config_file):
            return dict()

        parser = ConfigParser()
        parser.read(self.config_file)

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

    def _parse_console(self) -> Dict[str, Any]:
        """Parses provided options from the CLI

        Returns
        -------
        Dict[str, Any]
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
                Categories: {', '.join(Category.all_categories())}""",
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
