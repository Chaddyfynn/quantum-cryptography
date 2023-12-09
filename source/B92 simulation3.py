# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:33:30 2023

@author: felipe
BB92 code

"""

import numpy as np
import random
import matplotlib.pyplot as plt
import csv
"""
PROBS1 = [0.991714208,
          0.550833094,
          0.481797817,
          0.986253124] # on axis
PROBS2 = [0.99683830,
          0.56248499,
          0.43118671,
          0.99388242] # off axis

UNCERTAINS1 = [0.045257911,
               0.031513137,
               0.029166418,
               0.037687646]

UNCERTAINS2 = [0.05037069,
               0.02713008,
               0.02571711,
               0.04980150]
"""
#updated

PROBS1 = [0.984194058,0.460664777, 0.52466991, 0.981594554]

PROBS2 = [0.998448226,0.488232698,0.532008489,0.999078875]

UNCERTAINS1 = [0.0019738, 0.0012023, 0.0012733,0.00200]

UNCERTAINS2 = [0.00203,0.0012338251,0.001249,0.00203]


REPEATS = 100
N = 996 # number of bits in Alice's starting key

def weighted_probabilities():
    new_probs = []
    new_uncs = []
    for i in range(len(PROBS1)):
        val = np.array([PROBS1[i], PROBS2[i]])
        error = np.array([UNCERTAINS1[i], UNCERTAINS2[i]])
        wmtop = np.sum(val/(error**2))
        wmbot = np.sum(1/(error**2))
        weighted_mean = wmtop/wmbot
        error_in_wm = np.sqrt(1/(np.sum(1/(error**2))))
        new_probs.append(weighted_mean)
        new_uncs.append(error_in_wm)
    return PROBS2, UNCERTAINS2

def generate_bits(n):
    n = int(n)
    bits = str(bin(random.randint(0, 2**n)))[2:]
    n_bits = [int(i) for i in bits]
    if len(n_bits) < n:
        for i in range(n-len(n_bits)):
            n_bits.insert(0,0)
    return n_bits

def observations(qubits, bases, n):
    observs = []
    for k in range(n):
        observs.append((qubits[k],bases[k]))
    return observs

def results(observation, PROBS, UNCERTAINS):
    unfilter_key = []
    clean_key = []
    omitted_bits = []
    for ob in observation:
        new_probs = []
        for p in enumerate(PROBS):
            prob = p[1]
            p_index = p[0]
            uncert = UNCERTAINS[p_index]
            new_p = random.normalvariate(prob, uncert)
            if new_p > 1:
                new_p = 1
            elif new_p < 0:
                new_p = 0
            new_probs.append(new_p)
        rando_num = random.uniform(0,1)
        if ob == (0,0): # 0 deg qubit measured in + basis.
            if rando_num < new_probs[0]:
                unfilter_key.append('omit')
            else:
                unfilter_key.append(1)
        elif ob == (0,1):
            if rando_num < new_probs[1]:
                unfilter_key.append('omit')
            else:
                unfilter_key.append(0)
        elif ob == (1,0):
            if rando_num < new_probs[2]:
                unfilter_key.append('omit')
            else:
                unfilter_key.append(1)
        elif ob == (1,1):
            if rando_num < new_probs[3]:
                unfilter_key.append('omit')
            else:
                unfilter_key.append(0)
    for j in enumerate(unfilter_key):
        if j[1] == 0 or j[1] == 1:
            clean_key.append(j[1])
        else:
            omitted_bits.append(j[0])
    return clean_key, omitted_bits


def alice_key(qubits,omit):
    final_key = []
    for a in omit:
        qubits[a] = 'omit'
    for j in enumerate(qubits):
        if j[1] == 0 or j[1] == 1:
            final_key.append(j[1])
    return final_key

def check_keys(key1, key2):
    counter = 0
    for b in enumerate(key1):
        if b[1] == key2[b[0]]:
            counter += 1
    correctness = (counter/len(key1))*100
    num_incorrect = len(key1) - counter
    return correctness, num_incorrect, len(key1)

def plot_data(percs, bit_lengths, incorrects, final_l):
    #average = []
    #key_length_plot = np.arange(20,N)
    #for i in range(N):
     #   avg = np.mean(percs[:(i+1)])
      #  average.append(avg)
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.set_title("B92 Simulation updated", fontsize=17)
    ax.set_xlabel(r'Initial Key length', fontsize=15)
    ax.set_ylabel("Correctness of Bob's key (%)", fontsize=15)
    ax.set_ylim(70,100)
    #plt.yticks(np.arange(96, 98.5, 0.5), fontsize=13)
    plt.scatter(bit_lengths, percs, s=2, c='blue')
    #plt.plot(key_length_plot, average, color='dodgerblue')
    ax.grid(True, color='grey', dashes=[2])
    #ax.text(0,96.5,('Starting bits: {0}'.format(N)),bbox=dict(facecolor='dodgerblue',alpha=0.7), fontsize=12)
    plt.show()
    plt.savefig('B92_{0}bits_{1}repeats_initial_patch_final.jpeg'.format(N,REPEATS), dpi=1000)

def save_data(cors,bitls,incors, final_l):
    with open('B92_{0}bits_{1}repeats_patch_final.csv'.format(N,REPEATS), 'w', newline='') as new_file:
        counter = 0
        for c in cors:
            row = [c,bitls[counter], incors[counter], final_l[counter]]
            writer = csv.writer(new_file)
            writer.writerow(row)
            counter += 1

def main():
    percents = []
    bit_lengths = []
    incorrects = []
    final_length = []
    for i in range(REPEATS):
        for j in np.arange(32,N,4):
            bit_lengths.append(j)
    for k in bit_lengths:
        qubits = generate_bits(k)
        bob_bases = generate_bits(k)
        obs = observations(qubits, bob_bases, k)
        probs, uncerts = weighted_probabilities()
        Bob_key, omit = results(obs, probs, uncerts)
        alicekey = alice_key(qubits, omit)
        percents.append(check_keys(alicekey, Bob_key)[0])
        incorrects.append(check_keys(alicekey, Bob_key)[1])
        final_length.append(check_keys(alicekey, Bob_key)[2])
        print("Correctness is:", check_keys(alicekey, Bob_key)[0])
    plot_data(percents, bit_lengths, incorrects, final_length)
    save_data(percents, bit_lengths, incorrects, final_length)


main()
#weighted_probabilities()