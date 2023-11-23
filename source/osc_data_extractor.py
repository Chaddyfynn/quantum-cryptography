# -*- coding: utf-8 -*-
"""
|/----------------Data_Extractor----------------\|
PHYS30180 ------- Week 4 ------- Week 4 Analysis
|/---------------------------------------------\|

[CODE DESCRIPTION/USAGE/OUTLINE]


Created: Thu Oct 19 09:30:41 2023
Last Updated:

@author: Charlie Fynn Perkins, UID: 10839865 0
"""

from os.path import isfile, join
from os import listdir
import numpy as np

PATH = "C:\\Users\\chadd\\OneDrive\\Documents\\Undergrad Degree\\Semester 5 (2023)\\Labs\\Week 3\\Optics Tests and Setup (Exp 2)\\New folder\\"

NUM_COLS = 2  # How many columns per group
NUM_GROUPS = 2  # Number of groups
IGNORE_COLS = 3  # Number of redundant columns at the start


def extract(filename):
    master_arr = []
    for i in range(0, NUM_COLS * NUM_GROUPS):
        master_arr.append([])

    with open(PATH + filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            line_split = line.split(",")

            group = 0
            additional = 0

            for index, column in enumerate(master_arr):
                if group != 0:
                    additional = 4
                extracted_val = float(line_split[index+3+additional])
                master_arr[index].append(extracted_val)

                if (index + 1) % NUM_COLS == 0:
                    group += 1
    new_arr = []
    for i in range(0, len(master_arr[0])):
        intermediate_arr = []
        for j in range(0, len(master_arr)):
            intermediate_arr.append(master_arr[j][i])
        new_arr.append(intermediate_arr)

    np.savetxt(PATH + filename[0:-4] +
               "_extracted.csv", new_arr, delimiter=',')


def main():
    files = [f for f in listdir(PATH) if isfile(join(PATH, f))]
    for file in files:
        print("extracting", file)
        if ((".csv" in file) or (".CSV" in file)):
            extract(file)


if __name__ == "__main__":
    main()
