def clr():
    print("\033[0m", end="\n")


def color(s, args):
    print(f"\033[{s}", end="")
    for arg in args:
        print(arg, end=" ")
    clr()


def BRED(*args):
    color("1;31m", args)


def BYEL(*args):
    color("1;33m", args)


def BMAG(*args):
    color("1;35m", args)


def BGRE(*args):
    color("1;32m", args)


def BCYA(*args):
    color("1;36m", args)


def BBLU(*args):
    color("1;34m", args)


def RED(*args):
    color("0;31m", args)


def YEL(*args):
    color("0;33m", args)


def MAG(*args):
    color("0;35m", args)


def GRE(*args):
    color("0;32m", args)


def CYA(*args):
    color("0;36m", args)


def BLU(*args):
    color("0;34m", args)
