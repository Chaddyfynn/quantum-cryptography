# -*- coding: utf-8 -*-
"""
|/--------------------TITLE--------------------\|
PHYS20161 -- Assignment N -- [ASSIGNMENT NAME]
|/---------------------------------------------\|

[CODE DESCRIPTION/USAGE/OUTLINE]


Created: Thu Oct 26 11:10:13 2023
Last Updated:

@author: Charlie Fynn Perkins, UID: 10839865 0
"""


import matplotlib.pyplot as plt
import numpy as np

system = ("Tx 45, Rx 45", "Tx 45, Rx 0", "Tx 90, Rx 45", "Tx 90, Rx 0",
          "Tx -45, Rx 45", "Tx -45, Rx 0", "Tx 0, Rx 45", "Tx 0, Rx 0")
probability = {
    '0 (On Axis)': (98.6, 48.2, 43.8, 0.3, 0.6, 56.9, 55.1, 99.2),
    '1 (Off Axis)': (1.4, 51.8, 56.2, 99.7, 99.4, 43.1, 44.9, 0.8),
}

errors = [3.8, 2.9, 2.4, 2.3, 2.2, 2.9, 3.1,
          4.5, 1.7, 3, 2.7, 5, 5, 2.6, 2.8, 2]

error = [r'$98.6 \pm 3.8$', r'$48.2 \pm 2.9$', r'$43.8 \pm 2.4$',
         r'$10.3 \pm 2.1$', r'$0.6 \pm 2.2$', r'$56.9 \pm 2.9$',
         r'$17.3 \pm 4.1$', r'$99.2 \pm 4.5$', r'$1,4 \pm 1.7$',
         r'$51.8 \pm 3.0$', r'$56.2 \pm 2.7$', r'$89.7 \pm 4.2$',
         r'$99.4 \pm 5.0$', r'$43.1 \pm 2.6$', r'$82.7 \pm 7.5$',
         r'$0.8 \pm 2$']


x = np.arange(len(system))  # the label locations
width = 0.25  # the width of the bars
multiplier = 0

fig, ax = plt.subplots(layout='constrained')

for attribute, measurement in probability.items():
    if attribute == "1 (Off Axis)":
        colour = "goldenrod"
    else:
        colour = "lightseagreen"
    offset = width * multiplier
    rects = ax.bar(x + offset, measurement, width,
                   label=attribute, color=colour, zorder=2)
    ax.errorbar(x + offset, measurement,
                yerr=errors[multiplier], fmt=".", color="mediumvioletred", zorder=3)
    ax.bar_label(rects, padding=3, fontsize=7, zorder=3)
    # ax.text(x + offset, measurement, error[multiplier])
    multiplier += 1

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Probability (%)')
ax.set_title('Single Photon Probabilities for All Possible BB84 Photon States')

major_ticks = np.arange(0, 120, 20)
minor_ticks = np.arange(0, 120, 5)

ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

ax.grid(which='both')

# Or if you want different settings for the grids:
ax.grid(which='minor', alpha=0.2, zorder=0)
ax.grid(which='major', alpha=0.5, zorder=0)

ax.set_xticks(x + width, system, rotation="vertical")
ax.legend(loc=(0.1, 0.8))
ax.set_ylim(0, 120)
plt.savefig("fig.png", dpi=1000)

plt.show()
