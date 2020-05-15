from qiskit import IBMQ, Aer
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
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
T = [*range(0, 5)]


def shift_gate():
    q = QuantumRegister(3)
    circuit = QuantumCircuit(q, name='shift')

    circuit.ccx(0, 1, 2)
    circuit.cx(0, 1)
    circuit.x(0)
    circuit.x(1)
    circuit.ccx(0, 1, 2)
    circuit.x(1)
    circuit.cx(0, 1)

    return circuit.to_instruction()


def circuit(t, shift):
    q = QuantumRegister(3, name="q")
    c = ClassicalRegister(2, name="c")
    circuit = QuantumCircuit(q, c)

    for i in range(t):
        circuit.h(0)
        circuit.append(shift, q)
    circuit.measure([1, 2], c)

    return circuit


shift = shift_gate()
circuits = [circuit(t, shift) for t in T]

if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)

for (name, (backend, enabled)) in BACKENDS.items():
    if enabled:
        results = run_circuits(circuits, backend, SHOTS, 2)
        plot_circuits(T, results)
        plt.savefig(f"{OUTPUT}/discrete_2_{name}.png")
        plot_position_over_time(T, results)
        plt.savefig(f"{OUTPUT}/discrete_2_{name}_pos.png")
        # plt.show()
