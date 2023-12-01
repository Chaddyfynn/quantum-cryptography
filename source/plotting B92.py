# -*- coding: utf-8 -*-
"""
Created on Thu Nov 16 10:57:37 2023

@author: felipe
"""

import numpy as np
import random
import matplotlib.pyplot as plt
import csv

REPEATS = 50
N = 500 # number of bits in Alice's starting key

colours = ['r','g',]

def plot_data(percs, bit_lengths, num_incorrect):

    incorrect_0 = []
    incorrect_1 = []
    incorrect_2 = []
    incorrect_3 = []
    incorrect_4 = []
    incorrect_5 = []
    incorrect_other = []
    #for i in :


    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    ax.set_title("B92 Simulation", fontsize=17)
    ax.set_xlabel(r'Initial Key length', fontsize=15)
    ax.set_ylabel("Correctness of Bob's key (%)", fontsize=15)
    ax.set_ylim(70,100)
    plt.scatter(bit_lengths, percs, s=2, c='blue')
    #plt.plot(key_length_plot, average, color='dodgerblue')
    ax.grid(True, color='grey', dashes=[2])
    #ax.text(0,96.5,('Starting bits: {0}'.format(N)),bbox=dict(facecolor='dodgerblue',alpha=0.7), fontsize=12)
    plt.show()
    plt.savefig('B92_{0}bits_{1}repeats_type2.png'.format(N,REPEATS), dpi=800)

def read_data():
    data = np.genfromtxt('B92_{0}bits_{1}repeats_type2.csv'.format(N,REPEATS), dtype='float', delimiter=',', skip_header=1)
    corects = data[:,0]
    bit_lengths = data[:,1]
    incors = data[:,2]
    return corects, bit_lengths, incors

def main():
    percents, lengths, incorrects = read_data()
    plot_data(percents, lengths, incorrects)

main()