# -*- coding: utf-8 -*-
"""
|/--------------------TITLE--------------------\|
PHYS20161 -- Assignment N -- [ASSIGNMENT NAME]
|/---------------------------------------------\|

[CODE DESCRIPTION/USAGE/OUTLINE]


Created: Thu Sep 28 13:34:20 2023
Last Updated:

@author: Charlie Fynn Perkins, UID: 10839865 0
"""
import random as rand
import matplotlib.pyplot as ply
import numpy as np


def generate_string(length):
    # Generates a string of 0 and 1 of length length
    return_var = []
    for i in range(0, length):
        return_var.append(rand.randint(0, 1))
    return return_var


if __name__ == "__main__":
    key_length = int(
        input("Approximately how many bits should the shared key be?"))

    measured_bases = generate_string(2 * key_length)
    print("Use these bases to mesaure the incoming bit stream...")
    print(measured_bases)

    measured_values = []
    for i in range(0, 2 * key_length):
        measured_values.append(
            int(input("What was the value of bit " + str(i) + " ?")))

    print("Your eavesdropped values were...")
    print(measured_values)
