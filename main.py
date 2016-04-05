import sys

#if sys.version_info < (3, 0):
#    sys.stdout.write("This program is intended to be used with Python3\n")
#    sys.exit(1)

from Code.Engine import engine

if __name__ == "__main__":
    engine.start()

