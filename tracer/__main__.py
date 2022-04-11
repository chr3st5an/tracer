import sys
import os


if __name__ == "__main__":
    major, minor = sys.version_info[:2]

    if major != 3 or minor < 9:
        print("This program requires python 3.9.x or higher")
        sys.exit(0)

    # Changes the working directory to the directory containing this file
    os.chdir(os.path.dirname(__file__))

    import tracer

    tracer.main()
