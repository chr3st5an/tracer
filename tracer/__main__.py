import sys


if __name__ == "__main__":
    major, minor = sys.version_info[:2]

    if (major != 3) or not (6 < minor):
        print("This program requires python 3.6 < 3.x")
        sys.exit(0)

    from tracer import Tracer

    Tracer.main()
