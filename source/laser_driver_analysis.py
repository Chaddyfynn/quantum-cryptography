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
from scipy import stats

PATH = "C:\\Users\\chadd\\OneDrive\\Documents\\Undergrad Degree\\Semester 5 (2023)\\Labs\\Week 3\\Laser Driver Comparison (Exp 3)\\"
LASER = "Laser Intensity.csv"
DRIVER = "Driver Signal.csv"

if __name__ == "__main__":
    laser = []
    driver = []
    times = []

    with open(PATH + LASER, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_split = line.split(",")
            for count, element in enumerate(line_split):
                times.append(float(line_split[0]))
                laser.append((float(line_split[1])))

    with open(PATH + DRIVER, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_split = line.split(",")
            for count, element in enumerate(line_split):
                driver.append((float(line_split[1])))

    laser_max = max(laser)
    driver_max = max(laser)

    mean_grad = 0

    for i in range(0, len(laser) - 1):
        change = abs(laser[i] - laser[i+1])
        grad = change / 0.000002
        mean_grad += grad

    mean_grad / (len(laser) - 1)
    print(mean_grad)

    laser_peak_index = 1043
    for i in range(1, len(laser)):
        if ((laser[i] - laser[i - 1])/0.000002 > 100000):
            laser_peak_index = i
            break

    driver_max_index = driver.index(max(driver))

    for index, element in enumerate(laser):
        laser[index] /= laser_max

    for index, element in enumerate(driver):
        driver[index] /= driver_max

    print(driver_max_index)
    print(laser_peak_index)

    index_diff = abs(laser_peak_index - driver_max_index)
    # index_diff = 280

    res = stats.spearmanr(laser, driver)

    fig, (ax, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(5, 5))
    ax.set(title="Laser Signal Investigation")
    ax.set(xlabel="Time, s")
    ax.set(ylabel="Relative Intensity, Dimensionless")
    ax.plot(times[:-index_diff], laser[:-index_diff], color="darkgoldenrod",
            marker=".", linestyle='None', label="Laser Signal")

    ax.errorbar(times[:-index_diff], driver[index_diff:], color="teal",
                marker=".", linestyle='None', label="Driver Signal")

    ax2.set(title="Laser Driver vs Laser Signal (Intensity)")
    ax2.set(xlabel="Signal Intensity, Dimensionless")
    ax2.set(ylabel="Driver Intensity, Dimensionless")
    ax2.plot(laser, driver, color="teal", marker=".", linestyle='None',
             label="Spearman's Correlation:" + str(round(res[0], 3)))

    ax.legend()
    ax.grid()
    ax2.grid()
    ax2.legend()
    plt.tight_layout()
    plt.savefig("Laser Comparison.png", dpi=1000)
    plt.show()
    plt.clf()
