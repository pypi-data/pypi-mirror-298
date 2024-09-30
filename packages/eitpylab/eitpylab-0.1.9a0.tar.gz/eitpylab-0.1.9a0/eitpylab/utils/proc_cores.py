import os

class CPUCores:
    def __init__(self):
        self.total_cores = os.cpu_count()

    def get_half_cores(self):
        if self.total_cores is not None:
            c = self.total_cores // 2
            return c
        else:
            return 1