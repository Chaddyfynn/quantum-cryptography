# -*- coding: utf-8 -*-
"""
|/-----------------Key_Generator------------------\|
PHYS30180 -- Assignment 1 -- QUantum Cryptography
|/------------------------------------------------\|

[CODE DESCRIPTION/USAGE/OUTLINE]


Created: Thu Sep 28 10:54:51 2023
Last Updated:

@author: Charlie Fynn Perkins, UID: 10839865 0
"""
import numpy as np
import matplotlib.pyplot as ply
import random as rand
import time as t


def generate_string(length):
    # Generates a string of 0 and 1 of length length
    return_var = []
    for i in range(0, length):
        return_var.append(rand.randint(0, 1))
    return return_var


if __name__ == "__main__":
    key_length = int(
        input("Approximately how many bits should the shared key be?"))
    # print("Key length is", key_length)
    t0 = t.time_ns()
    initial_key = generate_string(2 * key_length)
    t1 = t.time_ns()
    print("Time taken to run function twice", (t1-t0)*2, "s")
    print("The string to send is...")
    print(initial_key)
    sent_bases = generate_string(2 * key_length)
    print("The bases to send are...")
    print(sent_bases)
    print("\n")
    print("In essence...")
    for i in range(0, 2 * key_length):
        print("Send", initial_key[i], "in basis", sent_bases[i])

    print("\n")

    measured_bases = []
    for i in range(0, 2 * key_length):
        measured_bases.append(
            int(input("What bases did Bob use for " + str(i) + "?")))

    correct_bases = []
    for i in range(0, 2 * key_length):
        correct_bases.append(sent_bases[i] and measured_bases[i])

    key = []
    for i in range(0, 2 * key_length):
        if correct_bases[i]:
            key.append(initial_key[i])

    print("Key calculated...")
    print("Actual key length is", len(key))
    print("Shared key is", key)
