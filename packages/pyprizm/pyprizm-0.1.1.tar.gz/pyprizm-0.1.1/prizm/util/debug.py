from core.util.color import RED, GRE, YEL, BLU, MAG, CYA

# 6.6.24: should write test for this eventually


class Console:

    def _write(self, *args):
        if self.path is not None:
            with open(f"./log/{self.path}", "w") as f:
                f.write(" ".join(map(str, args)))

    def __init__(self, debug=False, mode=0, write=None):
        self.debug = debug
        self.mode = mode
        self.path = write

    def warning(self, *args):
        print("\033[1;35mWARNING: \033[0m", end="")
        for arg in args:
            print(arg, end=" ")
        self._write("WARNING:", *args)

    def error(self, *args):
        print("\033[1;31mERROR: \033[0m", end="")
        for arg in args:
            print(arg, end=" ")
        self._write("ERROR:", *args)

    def red(self, *args, mode=0):
        if self.debug and mode == self.mode:
            RED(args)
        self._write(*args)

    def gre(self, *args, mode=0):
        if self.debug and mode == self.mode:
            GRE(args)
        self._write(*args)

    def yel(self, *args, mode=0):
        if self.debug and mode == self.mode:
            YEL(args)
        self._write(*args)

    def blu(self, *args, mode=0):
        if self.debug and mode == self.mode:
            BLU(args)
        self._write(*args)

    def mag(self, *args, mode=0):
        if self.debug and mode == self.mode:
            MAG(args)
        self._write(*args)

    def cya(self, *args, mode=0):
        if self.debug and mode == self.mode:
            CYA(args)
        self._write(*args)

    def log(self, *args, mode=0):
        if self.debug and mode == self.mode:
            print(*args)
        self._write(*args)
