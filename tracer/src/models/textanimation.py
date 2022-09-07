from typing import Any, Callable, Coroutine, Tuple
import asyncio

from colorama import Fore


__all__ = ("AsyncTextAnimation", )


class AsyncTextAnimation(object):
    """Represents a simple text animation

    Attributes
    ----------
    message : str
        The message that gets displayed
    condition : Callable[..., bool]
        A callable object representing the loop condition. As
        soon as it returns `False`, the animation will stop
    args : Tuple[Any]
        Args that get passed to the condition when calling it
    colored : bool
        If the animation should be colored

    Example
    -------
    >>> async def foo():

    >>>     await asyncio.sleep(5)

    >>> task = asyncio.create_task(foo())

    >>> animation = AsyncTextAnimation("Waiting for foo...", lambda: not task.done())

    >>> await animation()

    Supported Operations
    --------------------
    `str(obj)`
        Returns the str representation of the text animation
    `len(obj)`
        Returns the length of the message
    `obj()`
        Returns a coroutine which starts the animation.
        Alias for `obj.start()`

    Note
    ----
    While the animation is being displayed, there shouldn't
    be any other part calling `print`

    Author
    ------
    chr3st5an
    """

    def __init__(self, message: str, condition: Callable[..., bool], *args, color: bool = True) -> None:
        """Creates an animation object

        Parameters
        ----------
        message : str
            The message that gets displayed
        condition : Callable[..., bool]
            A callable object representing the loop condition. As
            soon as it returns `False`, the animation will stop
        *args : Any
            Args that get passed to the condition when calling it
        color : bool, optional
            If the animation should be colored, by default True
        """

        self.set_message(message)
        self.set_condition(condition)

        self.__args  = args
        self.__color = bool(color)

    def __str__(self) -> str:
        return f"<{self.__class__.__qualname__}(message=\"{self.__message}\", " \
            f"condition={self.__condition}, args={self.__args}, colored={self.__color})>"

    def __len__(self) -> int:
        return len(self.__message)

    def __call__(self) -> Coroutine[Any, Any, None]:
        return self.start()

    @property
    def message(self) -> str:
        return self.__message

    @property
    def condition(self) -> Callable[..., bool]:
        return self.__condition

    @property
    def args(self) -> Tuple[Any]:
        return self.__args

    @property
    def colored(self) -> bool:
        return self.__color

    def set_message(self, message: str) -> None:
        """Assigns a new message to the animation

        Parameters
        ----------
        message : str
            The message to set for the animation object

        Raises
        ------
        TypeError
            Parameter is not type 'str'
        """

        if not isinstance(message, str):
            raise TypeError(f"Expected type 'str' instead of type '{type(message).__qualname__}'")

        self.__message = message

    def set_condition(self, condition: Callable[..., bool]) -> None:
        """Sets a new condition

        Parameters
        ----------
        condition : Callable[..., bool]
            A callable object representing the loop condition. As
            soon as it returns `False`, the animation will stop

        Raises
        ------
        TypeError
            Parameter is not callable
        """

        if not callable(condition):
            raise TypeError(f"Expected a callable object instead of '{type(condition).__qualname__}'")

        self.__condition = condition

    async def start(self) -> None:
        """Displays a loading animation as long as the condition is True

        This is done by creating and awaiting an `asyncio.Task` object.
        While the animation is displayed, there shouldn't be any other
        function using `print`.
        """

        await asyncio.create_task(self.__runner())

    async def __runner(self) -> None:
        """Main logic of the animation
        """

        animation_sequence = "|/-\\"

        while self.__condition(*self.__args):
            for char in animation_sequence:
                await asyncio.sleep(0.1)

                beginning = f"[{Fore.CYAN}{char}{Fore.RESET}]" if self.colored else f"[{char}]"

                message = f"{beginning} {self.__message}"

                print("\r" + message, end="")

        # Removes the loading message
        print("\r" + " " * (len(self) + 10), end="\r")
