import numpy as np
from pyqtgraph.opengl.GLGraphicsItem import GLOptions
from gradient_descent_optimizer import gradient_descent_optimizer
from orqviz.pca import (
    get_pca,
    perform_2D_pca_scan,
)
from qeqiskit.simulator import QiskitSimulator
from openfermion.utils import load_operator
from zquantum.core.circuits import Circuit, RY, CNOT, X
from zquantum.core.estimation import calculate_exact_expectation_values, EstimationTask
from orqviz.gradients import calculate_full_gradient
from typing import Tuple


def get_circuit(parameters, n_entangling_layers=0):
    number_of_qubits = 2
    parameter_index = 0
    circuit = Circuit()

    circuit += X(0)
    for ii in range(number_of_qubits):
        circuit += RY(parameters[parameter_index])(ii)
        parameter_index += 1

    for _ in range(n_entangling_layers):
        circuit += CNOT(0, 1)
        for ii in range(number_of_qubits):
            circuit += RY(parameters[parameter_index])(ii)
            parameter_index += 1

    return circuit


H = load_operator("h2_ham_2q.data", "./data")

backend = QiskitSimulator("statevector_simulator")


def calculate_energy(parameters, n_entangling_layers):
    """
    Function that receives parameters for a quantum circuit, as well as specifications for the circuit depth,
    and returns the energy over a previously defined Hamiltonian H.
    """
    circuit = get_circuit(parameters, n_entangling_layers)
    task = EstimationTask(H, circuit, number_of_shots=None)
    return np.sum(calculate_exact_expectation_values(backend, [task])[0].values)


n_entangling_layers = 1
initial_parameters = np.array([1.12840278, -1.85964912, -1.1847599, 1.27278466])
calculate_energy_wrapper = lambda params: calculate_energy(params, n_entangling_layers)


def gradient_function(parameters):
    return calculate_full_gradient(
        parameters, calculate_energy_wrapper, stochastic=False, eps=1e-3
    )


def compute_landscape(n_iters: int = 50, n_steps: int = 100) -> Tuple:
    print("Performing optimization...")
    parameter_trajectory, losses = gradient_descent_optimizer(
        initial_parameters,
        calculate_energy_wrapper,
        n_iters,
        learning_rate=0.2,
        full_gradient_function=gradient_function,
    )

    print("Computing PCA...")
    pca = get_pca(parameter_trajectory)

    
    print("Performing 2D scan (this may take a few minutes)...")
    scan_pca_result = perform_2D_pca_scan(
        pca, calculate_energy_wrapper, n_steps_x=n_steps, offset=10
    )
    print("Done")

    return parameter_trajectory, losses, pca, scan_pca_result
