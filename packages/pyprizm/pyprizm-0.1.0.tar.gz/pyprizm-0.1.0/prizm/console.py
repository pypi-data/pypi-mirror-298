import time

from prizm.util.color import (
	RED, GRE, YEL, BLU, MAG, CYA,
	BRED, BGRE, BYEL, BBLU, BMAG, BCYA
)
from prizm.util.file import path_exists

class Console:

	def _write(self, *args):
		if self.path is not None:
			path = f"./log/{self.path}"
			path_exists(path)
			with open(path, "a") as f:
				f.write(" ".join(map(str, args)) + "\n")

	def __init__(self, directory="./log/", terminal=True):
		self.directory = directory
		path_exists(directory)
		self.terminal = terminal
		self._log = True
		timestamp = int(time.time() * 1000)
		self.path = self.directory + str(timestamp) + ".log"
		self.labels = []

	def label(self, label):
		self.labels.append(label)

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

	def set_log(log_gate: bool):
		self._log = log_gate

	def _color_switch(self, color, *args):
		if color is None:
			print(*args)
		elif color == "GRE":
			GRE(*args)
		elif color == "RED":
			RED(*args)
		elif color == "BLU":
			BLU(*args)
		elif color == "YEL":
			YEL(*args)
		elif color == "MAG":
			MAG(*args)
		elif color == "CYA":
			CYA(*args)
		elif color == "BGRE":
			BGRE(*args)
		elif color == "BRED":
			BRED(*args)
		elif color == "BBLU":
			BBLU(*args)
		elif color == "BYEL":
			BYEL(*args)
		elif color == "BMAG":
			BMAG(*args)
		elif color == "BYA":
			BCYA(*args)

	def log(self, *args, color=None, label=None):
		if label is not None:
			if label in self.labels:
				if self.terminal is True:
					self._color_switch(color, *args)
					if self.path is not None:
						self._write(*args)
				elif self.path is not None:
					self._write(*args)
		else:
			if self.terminal is True:
				self._color_switch(color, *args)
				if self.path is not None:
					self._write(*args)
			elif self.path is not None:
				self._write(*args)