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
N = [2, 3, 4, 5]


def add_gate():
    # 0 = cin, 1 = q, 2 = cout
    q = QuantumRegister(3)
    circuit = QuantumCircuit(q, name='add')
    circuit.ccx(0, 1, 2)
    circuit.cx(0, 1)
    return circuit.to_instruction()


def sub_gate():
    # 0 = cin, 1 = q, 2 = cout
    q = QuantumRegister(3)
    circuit = QuantumCircuit(q, name='sub')
    circuit.x(1)
    circuit.ccx(0, 1, 2)
    circuit.x(1)
    circuit.cx(0, 1)
    return circuit.to_instruction()


def shift_gate(n, add_gate, sub_gate):
    q = QuantumRegister(3 * n - 1)
    circuit = QuantumCircuit(q, name='shift')
    circuit.append(add_gate, [0, 1, 2])
    for i in range(1, n - 1):
        circuit.append(add_gate, [3 * i - 1, 3 * i + 1, 3 * i + 2])
    circuit.cx(3 * (n - 1) - 1, 3 * (n - 1) + 1)
    circuit.x(0)
    for i in range(n - 1):
        circuit.append(sub_gate, [3 * i, 3 * i + 1, 3 * i + 3])
    circuit.cx(3 * (n - 1), 3 * (n - 1) + 1)
    circuit.x(0)
    return circuit.to_instruction()


def circuit(n, t, add_gate, sub_gate):
    shift = shift_gate(n, add_gate, sub_gate)
    q = QuantumRegister(3 * n - 1, name="q")
    c = ClassicalRegister(n, name="c")
    circuit = QuantumCircuit(q, c)

    for i in range(t):
        circuit.h(0)
        circuit.append(shift, q)

    circuit.measure([2 * i + 1 for i in range(n)], c)
    return circuit


add = add_gate()
sub = sub_gate()

if not os.path.exists(OUTPUT):
    os.mkdir(OUTPUT)

for n in N:
    circuits = [circuit(n, t, add, sub) for t in T]
    for (name, (backend, enabled)) in BACKENDS.items():
        if enabled:
            results = run_circuits(circuits, backend, SHOTS, n)
            plot_circuits(T, results)
            plt.savefig(f"{OUTPUT}/discrete_n_{n}_{name}.png")
            plot_position_over_time(T, results)
            plt.savefig(f"{OUTPUT}/discrete_n_{n}_{name}_pos.png")
            # plt.show()
