import sys


if __name__ == "__main__":
    major, minor = sys.version_info[:2]

    if major != 3 or minor < 7:
        print("This program requires python 3.7.x or higher")
        sys.exit(0)

    import tracer

    tracer.main()
