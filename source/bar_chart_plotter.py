# -*- coding: utf-8 -*-
"""
|/------------------MAX_FINDER-----------------\|
PHYS30180 ------- Week 4 ------- Week 4 Analysis
|/---------------------------------------------\|

[CODE DESCRIPTION/USAGE/OUTLINE]


Created: Thu Oct 19 12:00:41 2023
Last Updated:

@author: Charlie Fynn Perkins, UID: 10839865 0
"""

from os.path import isfile, join
from os import listdir
import numpy as np
import matplotlib.pyplot as plt

PATH = "C:\\Users\\chadd\\OneDrive\\Documents\\Undergrad Degree\\Semester 5 (2023)\\Labs\\Week 3 Datasets Extracted\\Optics Tests and Setup (Exp 2) EXTRACTED\\"
FILENAME = "Max_Vals.csv"


if __name__ == "__main__":
    det_1 = []
    det_2 = []
    y_err = 0.3

    with open(PATH + FILENAME, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_split = line.split(",")
            for count, element in enumerate(line_split):
                if (count % 2) == 0:
                    det_1.append(float(element))
                else:
                    det_2.append(float(element))

    x_vals = np.linspace(1, len(det_1), len(det_1))

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(5, 5))
    ax.set(title="Optics Adjustment")
    ax.set(xlabel="Test #")
    ax.set(ylabel="Absolute Intensity, V")
    ax.errorbar(x_vals, det_1, y_err, color="darkgoldenrod",
                marker=".", linestyle='None', label="On Axis Detector")

    ax.errorbar(x_vals, det_2, y_err, color="teal",
                marker=".", linestyle='None', label="Off Axis Detector")

    ax.legend()
    ax.grid()
    plt.tight_layout()
    plt.savefig("Optics Tests.png", dpi=800)
    plt.show()
    plt.clf()
