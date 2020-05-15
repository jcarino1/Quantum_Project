from qiskit import execute
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d
from itertools import product


def plot_circuits(T, results):
    plt.clf()
    plt.cla()
    for state in results.keys():
        plt.plot(T, results[state], label=state)
    plt.legend()
    plt.ylabel('Probability')
    plt.xlabel('Time')


def plot_position_over_time(T, results):
    results = {int(key[::-1], 2): value for key, value in results.items()}
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


# Runs the circuit on the provided backend and saves output as necessary
def run_circuits(circuits, backend, shots, clbits):
    results = {state: [] for state in get_possible_states(clbits)}

    for circuit in circuits:
        counts = run(circuit, backend, shots)

        for state in counts.keys():
            counts[state] /= shots

        for state in results.keys():
            results[state].append(counts.get(state, 0))

    return results


# Runs the circuit on the provided backend and saves output as necessary
def run(circuit, backend, shots):
    job = execute(circuit, backend, shots=shots)
    while not job.done():
        pass
    result = job.result()
    return result.get_counts(circuit)


def get_possible_states(clbits):
    for bits in product([0, 1], repeat=clbits):
        yield "".join(str(bit) for bit in bits)
