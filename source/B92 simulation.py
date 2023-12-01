# -*- coding: utf-8 -*-
"""
Created on Thu Oct 26 12:33:30 2023

@author: felipe
BB92 code

"""

import numpy as np
import random
import matplotlib.pyplot as plt

PROBS1 = [0.991714208,0.550833094,0.568813292, 0.006117577]
PROBS2 = [0.986253124,0.437515014,0.481797817,0.003161698]

UNCERTAINS1 = [0.045257911,0.031513137,0.029498697,0.022383054]
UNCERTAINS2 = [0.037687646,0.023950758,0.029166418,0.022584011]

RUNS = 1000
N = 4096 # number of bits in Alice's starting key

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
    return new_probs,new_uncs

def generate_bits(n):
    bits = str(bin(random.randint(0,2**n)))[2:]
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
    return correctness

def plot_data(percs, runs):
    average = []
    run_plot = np.linspace(1,runs,runs)
    for i in range(runs):
        avg = np.mean(percs[:(i+1)])
        average.append(avg)
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.set_title("B92 Simulation", fontsize=17)
    ax.set_xlabel(r'Number of runs', fontsize=15)
    ax.set_ylabel("Average correctness of Bob's key (%)", fontsize=15)
    ax.set_ylim(94,98.5)
    plt.yticks(np.arange(94, 98.5, 0.5), fontsize=13)
    plt.scatter(run_plot, average, s=1, c='blue')
    plt.plot(run_plot, average, color='dodgerblue')
    ax.grid(True, color='grey', dashes=[2])
    ax.text(0,94.5,('Starting bits: {0}'.format(N)),bbox=dict(facecolor='dodgerblue',alpha=0.7), fontsize=12)
    plt.show()
    plt.savefig('B92_{0}bits_{1}runs.png'.format(N,RUNS), dpi=800)

def main():
    percents = []
    for i in range(RUNS):
        qubits = generate_bits(N)
        bob_bases = generate_bits(N)
        obs = observations(qubits, bob_bases, N)
        probs, uncerts = weighted_probabilities()
        Bob_key, omit = results(obs, probs, uncerts)
        alicekey = alice_key(qubits, omit)
        percents.append(check_keys(alicekey, Bob_key))
    plot_data(percents, RUNS)


main()