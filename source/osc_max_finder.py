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

PATH = "C:\\Users\\chadd\\OneDrive\\Documents\\Undergrad Degree\\Semester 5 (2023)\\Labs\\Week 3 Datasets Extracted\\Dataset 1 EXTRACTED\\"

NUM_CHANNELS = 2


def get_max(filename):
    times = []
    voltages = []
    for i in range(0, NUM_CHANNELS):
        times.append([])
        voltages.append([])

    with open(PATH + filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_split = line.split(",")
            channel = 0
            for index, element in enumerate(line_split):
                if index % 2 == 0:
                    times[channel].append(float(element))
                else:
                    voltages[channel].append(float(element))
                    channel += 1

        max_vals = []
        for i in range(0, NUM_CHANNELS):
            max_vals.append(max(voltages[i]))
        return max_vals


if __name__ == "__main__":
    max_vals = []
    files = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    for file in files:
        if ((".csv" in file) or (".CSV" in file)):
            max_vals.append(get_max(file))
    np.savetxt(PATH + "Max_Vals.csv", max_vals, delimiter=',')
