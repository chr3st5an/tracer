import sys


if __name__ == "__main__":
    major, minor = sys.version_info[:2]

    if (major != 3) or not (6 < minor < 10):
        #> This program works with Python 3.10 in theory
        #> but when I tested it, I noticed heavy lags and
        #> other things that aren't supposed to happen.
        #> I assume that either Python 3.10 or asyncio
        #> are causing these issues.
        print("This program requires python 3.6 < 3.x < 3.10")
        sys.exit(0)

    from tracer import Tracer

    Tracer.main()
