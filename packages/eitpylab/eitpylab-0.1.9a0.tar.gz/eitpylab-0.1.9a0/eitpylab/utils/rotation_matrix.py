import numpy as np


def rotMatrix(axis="x", angle_rad=0.0):
    if axis.lower() == "x":
        R = np.array(
            [
                [1, 0, 0],
                [0, np.cos(angle_rad), -np.sin(angle_rad)],
                [0, np.sin(angle_rad), np.cos(angle_rad)],
            ]
        )
    if axis.lower() == "y":
        R = np.array(
            [
                [np.cos(angle_rad), 0, np.sin(angle_rad)],
                [0, 1, 0],
                [-np.sin(angle_rad), 0, np.cos(angle_rad)],
            ]
        )
    if axis.lower() == "z":
        R = np.array(
            [
                [np.cos(angle_rad), -np.sin(angle_rad), 0],
                [np.sin(angle_rad), np.cos(angle_rad), 0],
                [0, 0, 1],
            ]
        )
    return R
