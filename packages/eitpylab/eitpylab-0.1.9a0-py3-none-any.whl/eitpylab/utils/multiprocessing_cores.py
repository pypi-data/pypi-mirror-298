import os


def set_cores(limiter):
    return max(1, os.cpu_count() - limiter)
