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
PROBS1 = [0.991714208,0.550833094,0.568813292, 0.006117577]
PROBS2 = [0.986253124,0.437515014,0.481797817,0.003161698]

UNCERTAINS1 = [0.045257911,0.031513137,0.029498697,0.022383054]
UNCERTAINS2 = [0.037687646,0.023950758,0.029166418,0.022584011]
"""
#updated
PROBS1 = [0.984194058,0.52466991, 0.460664777, 0.018405446]
PROBS2 = [0.998448226,0.511767302,0.532008489,0.000921125]

UNCERTAINS1 = [0.0019738,0.0012733,0.0012023,0.000801]
UNCERTAINS2 = [0.00203,0.0012933,0.001249,0.0008773]


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
    """
    print(new_probs)
    print(new_uncs)
    p1 = new_probs[0]
    err1 = new_uncs[0]
    p2 = new_probs[-1]
    err2 = new_uncs[-1]
    p3 = 1-p2
    p_converge = p1*p3
    p_err = np.sqrt(err1**2 + err2**2)
    print(p_converge, p_err)
    """
    return new_probs,new_uncs

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
        if ob == (0,0):
            if rando_num < new_probs[0]:
                unfilter_key.append('omit')
            else:
                unfilter_key.append(1)
        elif ob == (0,1):
            if rando_num < new_probs[1]:
                unfilter_key.append(0)
            else:
                unfilter_key.append('omit')
        elif ob == (1,0):
            if rando_num < new_probs[2]:
                unfilter_key.append('omit')
            else:
                unfilter_key.append(1)
        elif ob == (1,1):
            if rando_num < new_probs[3]:
                unfilter_key.append(0)
            else:
                unfilter_key.append('omit')
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
    plt.savefig('B92_{0}bits_{1}repeats_new_probs.png'.format(N,REPEATS), dpi=800)

def save_data(cors,bitls,incors, final_l):
    with open('B92_{0}bits_{1}repeats_new_probs.csv'.format(N,REPEATS), 'w', newline='') as new_file:
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