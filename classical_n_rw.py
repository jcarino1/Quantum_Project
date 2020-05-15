import matplotlib.pyplot as plt
from rwutil import plot_circuits
from random import *
import os

OUTPUT = "output"

SHOTS = 1000
T = [*range(0, 5)]
N = [1, 2, 3]


def classical_rw(states, t):
    num_dimensions = 1
    init_location = 0
    end_locations = [init_location for i in range(num_dimensions)]
    # print("Initial locations: ", end_locations)

    # Iterate through the number of steps
    for i in range(t):
        # For ever step, iterate through each dimension
        for j in range(num_dimensions):

            r = randint(0, 1)
            if (r == 0):
                end_locations[j] -= 1
            elif (r == 1):
                end_locations[j] += 1

            # Constrain the number of bits
            end_locations[j] %= states

            # print("step(i) =",i , " \tdimension(j) =", j, " \tr =", r, " \tlocation =", end_locations[j], " \tall locations =", end_locations)

    # print("Steps taken: ", t, "\nEnd locations: ", end_locations)

    return end_locations[-1]


def repeated_rw(states, t, shots):
    results = {}
    for i in range(shots):
        state = str(classical_rw(states, t))

        if state not in results.keys():
            results[state] = 1
        else:
            results[state] += 1
    return results


def repeated_rw_over_time(states, T, shots):
    results = {str(state): [] for state in range(states)}

    for t in T:
        counts = repeated_rw(states, t, shots)

        for state in counts.keys():
            counts[state] /= shots

        for state in results.keys():
            results[state].append(counts.get(state, 0))

    return results


def plot_position_over_time(T, results):
    X = []
    Y = []
    Z = []

    for (state, probs) in results.items():
        for (t, prob) in zip(T, probs):
            X.append(t)
            Y.append(state)
            Z.append(prob)

    plt.clf()
    plt.cla()
    ax = plt.axes(projection='3d', label='position_over_time')
    ax.plot_trisurf(X, Y, Z, cmap='winter')
    ax.set_zlabel('Probability')
    ax.set_ylabel('Position')
    ax.set_xlabel('Time')


if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)

for n in N:
    results = repeated_rw_over_time(2 ** n, T, SHOTS)
    plot_circuits(T, results)
    plt.savefig(f"{OUTPUT}/classical_n_{n}.png")
    plot_position_over_time(T, results)
    plt.savefig(f"{OUTPUT}/classical_n_{n}_pos.png")
    # plt.show()
