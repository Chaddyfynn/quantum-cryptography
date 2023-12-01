# -*- coding: utf-8 -*-
"""
Created on Thu Oct 19 15:52:05 2023

@author: felipe
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
from scipy.optimize import fmin
import random
import matplotlib.lines as mlines

FILE_NAME = "Final data_1.csv"

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
    raw_data = np.genfromtxt(FILE_NAME, dtype='float', delimiter=',', skip_header=1)

    return raw_data

def function(angle, centre, b):
    angle = np.array(np.deg2rad(angle))
    return 10.64*np.exp(-((angle-centre)**2)/(2*b**2))

def function2(angle, c1, b1):
    y1 = np.array(function(angle, c1, b1))
    y2 = np.array(function(angle, (c1+np.pi), b1))
    y3 = np.array(function(angle, (c1-np.pi), b1))
    final_y_vals = []
    for i in angle:
        if i <= 20:
            final_y_vals.append((function(i, (c1-np.pi), b1)))
        if i>20 and i <= 200:
            final_y_vals.append((function(i, c1, b1)))
        elif i > 200:
            final_y_vals.append((function(i, (c1+np.pi), b1)))
    return final_y_vals

def chi_test(params, data):
    c1 = params[0]
    b1 = params[1]
    """
    new_data = []
    for row in data:
        if row[1] > 1:
            new_data.append(row[:4])
    new_data = np.array(new_data)
    """
    chi_sqr_y = np.sum(
        ((data[:, 1] - function2(data[:,0],c1,b1))**2) / data[:, 3]**2)
    return chi_sqr_y

def plot_data(data,params,chi):
    fig = plt.figure(figsize=(12,8))
    ax = fig.add_subplot(111)
    angles = np.linspace(0,360,500)
    ax.set_title("Intensity Pattern for Optics Setup ", fontsize=17)
    ax.set_xlabel(r'Angle of Polariser ($\degree$)', fontsize=15)
    ax.set_ylabel('Voltage (V)', fontsize=15)
    ax.errorbar(data[:, 0], data[:, 1], xerr=data[:,2], yerr=data[:, 3],
                fmt='.', color='dodgerblue', label='Data Recorded')
    c1 = params[0]
    b1 = params[1]
    final_y = function2(angles, c1, b1)
    ax.plot(angles, final_y, color='black',label='Theoretical Fit')
    ax.grid(True, color='grey', dashes=[2])
    ax.set_ylim(-0.5,11.5)
    ax.set_xlim(-10,370)
    plt.xticks(np.arange(0, 380, 20))
    plt.yticks(np.arange(0,12,1))
    c1 = np.rad2deg(c1)
    ax.plot([c1,c1], [12,-0.5], '--',c='blue',label='Peak Centers')
    ax.plot([c1+180,c1+180], [12,-0.5], '--',c='blue')
    ax.plot([-10,370],[10.64,10.64],'--',c='red',label='Peak Amplitude')
    ax.text(-4,7,(r'$\chi^2$ value: {0:.0f}'.format(chi)+'\n'+r'Peak Amplitude: {0:.4g} (V)'.format(10.64)+'\n'+r'$\theta_{{central}}$: {0:.2f}$\degree$'.format(c1) +'\n'+r'$\sigma_{{width}}$: {0:.2f}$\degree$'.format(np.rad2deg(b1))),bbox=dict(facecolor='white',alpha=0.5), fontsize=10)
    plt.legend(loc='best',framealpha=0.7)
    plt.show()
    plt.savefig('Malus_Law_graph_convolution_final_test1.png', dpi=800)


def minimisation(data):
    c1_start = 109*(np.pi/180)
    b1 = 25*(np.pi/180)
    parameters = fmin(chi_test, (c1_start, b1), full_output=True, disp=False, args=(data,))
    print(parameters)
    return parameters

def mesh_params(centre, width):
    centre_mesh = np.linspace(0.999*centre, 1.001*centre, 200)
    width_mesh = np.linspace(0.999*width, 1.001*width, 200)
    return np.meshgrid(centre_mesh, width_mesh)

def chi_function_mesh(meshes, data):

    centre_mesh = meshes[0]
    width_mesh = meshes[1]
    chi_matrix = np.empty((200, 200))
    counter1 = 0  # row index
    while counter1 < 200:
        for counter2 in range(200):  # counter2 is the column index
            chi_val = chi_test(
                [centre_mesh[counter1, counter2], width_mesh[counter1, counter2]], data)
            chi_matrix[counter1, counter2] = chi_val
        counter1 += 1
    return chi_matrix

def contour_plot_lines(mesh_arrays, data, c1, b1, chi):

    rb_mesh = mesh_arrays[0]
    sr_mesh = mesh_arrays[1]
    fig = plt.figure(figsize=(13, 11))
    ax = fig.add_subplot(111)

    ax.set_title(r'Contour Plot of Parameters and $\chi^2$', fontsize=14)
    ax.set_xlabel(r'$\theta_{{central}}$ (rad)', fontsize=14)
    ax.set_ylabel(r'$\sigma_{{width}}$ (rad)', fontsize=14)
    ax.set_ylim(0.421,0.4216)
    ax.set_xlim(1.9035,1.9045)
    ax.scatter(c1, b1, color='k')
    label = [r'$\chi^2_{{min.}}$ = {0:.0f}'.format(chi),r'$\chi^2_{{min.}}$+1.00']
    contour_line_1 = ax.contour(rb_mesh, sr_mesh, chi_function_mesh(
        mesh_arrays, data),  [chi,chi+1], linewidths=2,colors=['black','crimson'])
    h1,_ = contour_line_1.legend_elements()
    box = ax.get_position()
    ax.set_position([box.x0, box.y0, box.width * 0.8,
                     box.height])


    contour_line_2 = ax.contour(rb_mesh, sr_mesh, chi_function_mesh(
        mesh_arrays, data),  [chi+1], linewidths=2,colors=['crimson'])
    array = contour_line_2.collections[0].get_paths()[0].vertices

    rb_vals = array[:, 0]
    sr_vals = array[:, 1]

    rb_err = (np.max(rb_vals) - np.min(rb_vals))/2
    sr_err = (np.max(sr_vals) - np.min(sr_vals))/2

    line1, = plt.plot([c1+rb_err, c1+rb_err],[0.421,0.4216],'--',color='indigo',label=r'$\theta_{{central}}$ = {0:.4f} $\pm$ {1:.1g} rad'.format(c1,rb_err))
    plt.plot([c1-rb_err, c1-rb_err],[0.421,0.4216],'--',color='indigo')

    line2, = plt.plot([1.9035,1.9045],[b1+sr_err, b1+sr_err], '--',color='magenta',label=r'$\sigma_{{width}}$ = {0:.4f} $\pm$ {1:.1g} rad'.format(b1,sr_err))
    plt.plot([1.9035,1.9045],[b1-sr_err, b1-sr_err], '--',color='magenta')
    legend2 = ax.legend(handles=[line1,line2], loc='center left', bbox_to_anchor=(1, 0.5),fontsize=12)
    ax.add_artist(legend2)
    ax.legend(h1,label,loc='center left', bbox_to_anchor=(1, 0.6),fontsize=12)
    plt.show()
    plt.savefig('Contour_plot_lines_Malus_final_test1.png', dpi=800)
    return rb_err, sr_err


def main():
    data = get_data()
    params = minimisation(data)[0]
    print(np.rad2deg(params))
    chi = chi_test(params, data)
    plot_data(data, params, chi)
    centre = params[0]
    width = params[1]
    meshgrid = mesh_params(centre, width)
    uncs = contour_plot_lines(meshgrid, data, centre, width, chi)
    percent1 = 100*uncs[0]/params[0]
    percent2 = 100*uncs[1]/params[1]
    print(percent1)
    print(percent2)


main()