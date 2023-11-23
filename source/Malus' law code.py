# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:52:05 2023

@author: felipe
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.optimize import fmin

FILE_NAME = "../data/Final data.csv"


def get_data():
    """
    try:
        with open(FILE_NAME, 'r', encoding='utf-8') as input_file:
            raw_data = np.empty((0, 3))
            for line in input_file:
                split_line = line.split(',')
                if line[0] != '%':
                    try:
                        row = np.array([])
                        clean_row = np.array([])
                        for index in enumerate(split_line):
                            val = float(split_line[index[0]])
                            row = np.append(row, val)
                        for value in row:
                            if np.isnan(value) == False and np.isinf(value) == False:
                                clean_row = np.append(clean_row, value)
                        if len(clean_row) == 3:
                            raw_data = np.vstack((raw_data, clean_row))
                    except ValueError:
                        print()
    except FileNotFoundError:
        print('\nThe file you have requested has not been found.')
    """
    raw_data = np.genfromtxt(FILE_NAME, dtype='float',
                             delimiter=',', skip_header=1)
    data = raw_data[:19]  # ?
    return data


def function(vals, n):
    c_angle = vals
    if n == 19:
        angle = np.arange(0, 190, 10)
    else:
        angle = np.linspace(0, 180, 50)
    centre = np.linspace(c_angle, c_angle, n)
    return (np.cos(angle*(np.pi/180) - centre)**2)*10.65


def inv_function(vals, n):
    c_angle = vals
    if n == 19:
        V = np.linspace(0, 10.65, 19)
    else:
        V = np.linspace(0, 10.65, 50)
    A_0 = np.linspace(10.65, 10.65, n)
    return (np.arccos(np.sqrt(V/A_0)) + c_angle)*(180/np.pi)


def chi_test(paras, data):
    chi_sqr_y = np.sum(
        (data[:, 1] - function(paras, 19)**2 / data[:, 3]**2))

    chi_sqr_x = np.sum(
        (data[:, 0] - inv_function(paras, 19)**2 / data[:, 2]**2))
    chi_sqr = np.sqrt(chi_sqr_x**2 + chi_sqr_y**2)
    return chi_sqr


def plot_data(data, params, chi):
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111)
    angles = np.linspace(0, 180, 50)
    ax.set_title("Malus' Law", fontsize=17)
    ax.set_xlabel(r'Angle ($\degree$)', fontsize=15)
    ax.set_ylabel('Voltage (V)', fontsize=15)
    ax.errorbar(data[:, 0], data[:, 1], xerr=data[:, 2], yerr=data[:, 3],
                fmt='x', color='dodgerblue', label='Data recorded')
    ax.plot(angles, function(params, 50),
            color='black', label=r'$Cos^2(\theta)$ fit')
    ax.grid(True, color='grey', dashes=[2])
    centre = params*(180/np.pi)
    # ax.set_ylim(6,14)
    #ax.text(50,4.5,(r'$\chi^2$ value: {0:.3f}'.format(chi)+'\n'+r'Peak amplitude: {0:.3f} (V)'.format(params[0])+'\n'+r'$\theta_{{central}}$: {0:.3f}$\degree$'.format(centre)),bbox=dict(facecolor='dodgerblue',alpha=0.7), fontsize=12)
    #plt.legend(loc='lower left')
    plt.show()
    plt.savefig('Malus_Law_graph_1.png', dpi=800)


def minimisation(data):
    centre_start = 100*(np.pi/180)
    parameters = fmin(chi_test, (centre_start),
                      full_output=True, disp=False, args=(data,))
    print(parameters)
    return parameters


def main():
    data = get_data()
    params = minimisation(data)[0]
    plot_data(data, params, chi_test(params, data))


main()
