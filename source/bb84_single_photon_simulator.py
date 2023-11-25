# -*- coding: utf-8 -*-
"""
|/--------------------TITLE--------------------\|
PHYS20161 -- Assignment N -- [ASSIGNMENT NAME]
|/---------------------------------------------\|

[CODE DESCRIPTION/USAGE/OUTLINE]


Created: Thu Oct 26 14:51:07 2023
Last Updated:

@author: Charlie Fynn Perkins, UID: 10839865 0
"""

'''
Definitions:
    We can send a 0 or a 1 in an A or B basis.
    A is the 0/90 basis
    B is the -45,45 basis

    In combination, we can send data as:
        0A - 0*
        1A - 90*
        0B - 45*
        1B - -45*
    using the above angles.

    They can be measured in A or B, giving 8 possible scenarios:
        0AA - Tx 0*, Rx 0*
        0AB - Tx 0*, Rx 45*
        0BA - Tx 45*, Rx 0*
        0BB - Tx 45*, Rx 45*
        1AA - Tx 90*, Rx 0*
        1AB - Tx 90*, Rx 45*
        1BA - Tx -45*, Rx 0*
        1BB - Tx -45*, Rx 45*
    each with its own probability of measuring a 1 or 0.
    The array called PROBABILITIES is formatted ["state", p(0), dp(0)]
    Which outlines the statistics of measuring a 1 or a 0 for a given system
'''


# User Variables
import numpy as np
import matplotlib.pyplot as plt
debug = False
log = True
DESIRED_LENGTH = 1024
START = int(32/4)
END = int(996/4)
STEP = 1
REPEAT = 50
NUM = 25
FNAME = "..//data//B92_996bits_100repeats_new_probs.csv"
BINS = [0, 25, 50, 75, 100, 125, 150, 200, 250, 300, 350, 400, 450, 500]
MULTICOLOUR = True
SIMULATE = False
if SIMULATE:
    NUM_TEST = END - START
else:
    NUM_TEST = END - START + 1

# System Variables
PROBABILITIES = [
    ['0AA', '0AB', '0BA', '0BB', '1AA', '1AB', '1BA', '1BB'],
    [0.984194058, 0.460664777, 0.52466991, 0.981594554,
        0.001551774, 0.511767302, 0.467991511, 0.000921125],
    [0.0019738, 0.00120231, 0.0012733, 0.0019991,
        0.0008767, 0.0012933, 0.0011976, 0.0008773]
]


def generate_bits(length):
    return np.random.randint(2, size=length)


def comparison_var(length):
    return np.random.uniform(low=0.0, high=1.0, size=length)


def get_system_states(bit, tx, rx):
    system_states = []
    for i in range(0, len(bit)):
        inter = "ERROR"
        if not bit[i]:
            if not tx[i]:
                if not rx[i]:
                    inter = '0AA'
                else:
                    inter = '0AB'
            else:
                if not rx[i]:
                    inter = '0BA'
                else:
                    inter = '0BB'
        else:
            if not tx[i]:
                if not rx[i]:
                    inter = '1AA'
                else:
                    inter = '1AB'
            else:
                if not rx[i]:
                    inter = '1BA'
                else:
                    inter = '1BB'
        system_states.append(inter)
    return system_states


def generate_normal(means, errors):
    comparison_values = []
    for i in range(len(errors)):
        comparison_values.append(np.random.normal(means[i], errors[i]))
    return comparison_values


def run_experiment(length):
    # Generate the starting key
    initial_key = generate_bits(length * 2)

    # Generate the Tx bases
    tx_bases = generate_bits(length * 2)

    # Generate the Rx bases
    rx_bases = generate_bits(length * 2)

    # Convert from arrays to '0AA' form
    system_states = get_system_states(initial_key, tx_bases, rx_bases)

    # Generate simulated results
    means = []
    errors = []
    for i in range(length * 2):
        state = system_states[i]
        index = PROBABILITIES[0].index(state)
        means.append(PROBABILITIES[1][index])
        errors.append(PROBABILITIES[2][index])
    simulated_results = generate_normal(means, errors)

    # Generate comparison values
    comparison_values = comparison_var(length * 2)

    # Compare values and define measurements
    alice_bits = []
    bob_bits = []
    correct = 0
    total = 0
    for i in range(length * 2):
        if tx_bases[i] == rx_bases[i]:
            alice_compare = initial_key[i]
            alice_bits.append(alice_compare)
            if comparison_values[i] <= simulated_results[i]:
                bob_bits.append(0)
                bob_compare = 0
            else:
                bob_bits.append(1)
                bob_compare = 1
            if alice_compare == bob_compare:
                correct += 1
            total += 1

    # Print string
    if debug:
        print("Initial Key:")
        print(initial_key)

        print("Tx Bases:")
        print(tx_bases)

        print("Rx Bases:")
        print(rx_bases)

        print("Tx Key:")
        print(alice_bits)

        print("Rx Key:")
        print(bob_bits)

    if log:
        print("Desired key length was -", str(length) + ".")
        print("Actual length was", str(total) + ".")
        print("Which is", str(round(100 * total/length, 4)) +
              "% of what was expected.")
        print("Total correct bits were", str(correct) + ".")
        print("Transmission success of", str(
            round(100*correct/total, 5)) + "%.")
    return (100 * total/length, 100*correct/total, total - correct, total)


if __name__ == "__main__":
    key_length_0 = []
    key_length_1 = []
    key_length_2 = []
    key_length_3 = []
    key_length_4 = []
    key_length_5 = []
    key_length_other = []
    key_length_arr = [key_length_0,
                      key_length_1,
                      key_length_2,
                      key_length_3,
                      key_length_4,
                      key_length_5,
                      key_length_other]

    transmission_success_0 = []
    transmission_success_1 = []
    transmission_success_2 = []
    transmission_success_3 = []
    transmission_success_4 = []
    transmission_success_5 = []
    transmission_success_other = []
    transmission_success_arr = [transmission_success_0,
                                transmission_success_1,
                                transmission_success_2,
                                transmission_success_3,
                                transmission_success_4,
                                transmission_success_5,
                                transmission_success_other]

    key_lengths = np.arange(START, END, STEP)
    transmission_success = []
    key_success = []
    graph_keys = []

    num_success = np.zeros(NUM_TEST)
    num_total = np.zeros(NUM_TEST)
    success_ratio = []
    success_ratio_means = [0]
    success_ratio_means_x = [12]
    half_point = 0

    # j = 0
    # for i in range(len(key_lengths) * REPEAT):
    #     length = key_lengths[j]
    #     result = run_experiment(length)
    #     key_success.append(result[0])
    #     transmission_success.append(result[1])
    #     graph_keys.append(length * 2)

    #     if (i + 1) % REPEAT == 0 and i != 0:
    #         j += 1
    if SIMULATE:
        j = 0
        for i in range(len(key_lengths) * REPEAT):
            length = key_lengths[j]
            result = run_experiment(length)

            if result[2] < 6:
                arr_index = result[2]
            else:
                arr_index = 6

            if result[2] == 0:
                num_success[length - START] += 1

            num_total[length - START] += 1

            transmission_success_arr[arr_index].append(result[1])
            key_length_arr[arr_index].append(length)

            if (i + 1) % REPEAT == 0 and i != 0:
                j += 1
    else:
        data = np.genfromtxt(FNAME, dtype='float',
                             delimiter=',', skip_header=1)
        correctness = data[:, 0]

        bit_lengths = data[:, 1]
        num_incorrect = data[:, 2]
        shared_length = data[:, 3]
        for i in range(len(bit_lengths)):
            bit_lengths[i] = int(bit_lengths[i])
            num_incorrect[i] = int(num_incorrect[i])
            shared_length[i] = int(shared_length[i])

        j = 0
        for i in range(len(correctness)):
            length = bit_lengths[i] / 4
            result = (100*0.25*shared_length[i]/bit_lengths[i],
                      correctness[i], num_incorrect[i], shared_length[i])

            if result[2] < 6:
                arr_index = result[2]
            else:
                arr_index = 6

            if result[2] == 0:
                num_success[int(length) - START] += 1

            num_total[int(length) - START] += 1

            transmission_success_arr[int(arr_index)].append(result[1])
            key_length_arr[int(arr_index)].append(int(length))

            if (i + 1) % REPEAT == 0 and i != 0:
                j += 1

    for i in range(len(num_success)):
        success_ratio.append(num_success[i]*100/num_total[i])

    counter = 0
    for i in range(len(success_ratio)):
        if (i % 5 == 0) and (i != 0):
            success_ratio_means[counter] /= 5
            if abs((50 - success_ratio_means[counter])) < abs((50 - success_ratio_means[half_point])):
                half_point = counter
            counter += 1
            success_ratio_means.append(0)
            success_ratio_means_x.append(START + i)
        success_ratio_means[counter] += success_ratio[i]

    transmission_success_arr_flat = []
    for arr in transmission_success_arr:
        for elem in arr:
            transmission_success_arr_flat.append(elem)

    print("Overall mean:", np.mean(transmission_success_arr_flat))
    mean_success = np.mean(
        transmission_success_arr_flat[(int(len(transmission_success_arr_flat)/3)):])

    print("Overall std dev:", np.std(transmission_success_arr_flat))
    dev_success = np.std(
        transmission_success_arr_flat[(int(len(transmission_success_arr_flat)/3)):])

    fig, ax = plt.subplots(nrows=1, ncols=1, figsize=(9, 6))
    ax2 = ax.twinx()

    colors = ['deeppink', 'firebrick', 'darkorange', 'darkgoldenrod', 'gold', 'lawngreen',
              'seagreen']
    labels = ['= 0', '= 1', '= 2', '= 3', '= 4', '= 5', '> 5']

    ax.set(title="B92 Fidelity Simulation 8bit to 249bit Desired Length (Extra Conditions)")
    ax.set(xlabel="Desired Shared Key Length")
    ax2.set(ylabel="Success Ratio, %")
    ax.set(ylabel="Percentage Correctness (After Contraction), %")

    ax2.plot(success_ratio_means_x, success_ratio_means,
             linestyle="dotted", color="indigo", label="n = 0 Probability")

    ax2.axvline(success_ratio_means_x[half_point], color="navy",
                label="~50% Chance of Success", linestyle="dashdot")

    if (not MULTICOLOUR):
        ax.scatter(graph_keys, transmission_success, color="darkgoldenrod",
                   linestyle='None', label="Transmission Success Rate", s=0.25)

    else:
        for i in range(len(key_length_arr)):
            ax.scatter(key_length_arr[i], transmission_success_arr[i], color=colors[i],
                       linestyle='None', s=0.25)

    # ax2.plt(key_lengths, success_ratio, color="indigo",
    #        linestyle="dotted", label="Mean Success Ratio")

    # ax.scatter(key_lengths, key_success, color="teal",
    #           marker=".", linestyle='None', label="Key Length Success")

    ax.axhline(y=mean_success, color='navy',
               linestyle='-', label="Mean Correctness (convergent): " + str(round(mean_success, 3)))
    ax.axhline(y=mean_success+dev_success, color='indigo',
               linestyle='--', label="Standard Deviation (convergent): " + str(round(dev_success, 3)))
    ax.axhline(y=mean_success-dev_success, color='indigo',
               linestyle='--')
    print("Mean success after 1/3 was:", mean_success)
    print("Standard Deviation after 1/3 was:", dev_success)
    print("50% Chance Length At:", success_ratio_means_x[half_point])
    ax.legend()
    ax2.legend(loc="lower left")
    ax.grid(alpha=0.5)
    plt.tight_layout()
    plt.savefig("..//results//Fidelity_16.png", dpi=1000)
    plt.show()
    plt.clf()
