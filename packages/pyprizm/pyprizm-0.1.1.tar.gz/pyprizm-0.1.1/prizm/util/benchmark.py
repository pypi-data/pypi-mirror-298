import time
import matplotlib.pyplot as plt

timestamp = str(time.time())

class Benchmark:
    """
    Might create a benchmark tool to track the overheard and performance in each node to identify bottlenecks.
    """

    def __init__(self):
        self.points = {}
        self.categories = {}

    def start(self):
        self.points["start"] = time.time()

    def stop(self):
        self.points["end"] = time.time()

    def mark(self, label: str, category: str = None):
        self.points["label"] = time.time()

    def plot(self):
        pass

    def overall(self):
        pass
