from qiskit import IBMQ, Aer
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.qasm import pi
from qiskit.extensions import U3Gate
import numpy as np
import matplotlib.pyplot as plt
import os
from rwutil import *

OUTPUT = "output"

IBMQ.load_account()
Prov = IBMQ.get_provider(group='open')

BACKENDS = {
    'qasm_simulator': (Aer.get_backend('qasm_simulator'), True),
    'ibmq_qasm_simulator': (Prov.get_backend('ibmq_qasm_simulator'), False),
    'ibmq_london': (Prov.get_backend('ibmq_qasm_simulator'), False),
    'ibmq_vigo': (Prov.get_backend('ibmq_qasm_simulator'), False)
}

SHOTS = 1000
T = np.linspace(0, 6.5, num=50)


def circuit(t):
    q = QuantumRegister(1, name="q")
    c = ClassicalRegister(1, name="c")
    circuit = QuantumCircuit(q, c)

    circuit.append(U3Gate(2 * t, -pi/2, pi/2), [0])
    circuit.measure(q, c)

    return circuit


circuits = [circuit(t) for t in T]

if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)

for (name, (backend, enabled)) in BACKENDS.items():
    if enabled:
        results = run_circuits(circuits, backend, SHOTS, 1)
        plot_circuits(T, results)
        plt.savefig(f"{OUTPUT}/continuous_1_{name}.png")
        plot_position_over_time(T, results)
        plt.savefig(f"{OUTPUT}/continuous_1_{name}_pos.png")
        plt.show()
