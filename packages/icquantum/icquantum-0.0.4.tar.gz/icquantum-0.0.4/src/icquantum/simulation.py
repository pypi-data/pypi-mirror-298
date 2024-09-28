import time
from pathlib import Path
import os

from iccore.serialization import Serializable, write_json


class QuantumSimulationBackend(Serializable):
    def __init__(self) -> None:
        self.num_cores: int = 1
        self.num_parallel_exp: int = 0
        self.parallel_threshold: int = 14
        self.library: str = ""
        self.library_version: str = ""
        self.use_gpu: bool = False
        self.library_backend: str = ""
        self.seed_simulator = None

    def serialize(self):
        return {
            "num_cores": self.num_cores,
            "num_parallel_exp": self.num_parallel_exp,
            "parallel_threshold": self.parallel_threshold,
            "library": self.library,
            "library_version": self.library_version,
            "use_gpu": self.use_gpu,
            "library_backend": self.library_backend,
            "seed_simulator": self.seed_simulator,
        }


class QuantumSimulation(Serializable):
    def __init__(self) -> None:
        self.results: dict = {}
        self.state = "created"
        self.start_time: float = 0
        self.end_time: float = 0
        self.circuit_label: str = "sample"
        self.num_circuits: int = 1
        self.num_qubits: int = 1
        self.num_iters: int = 1
        self.backend: QuantumSimulationBackend = QuantumSimulationBackend()

    def on_started(self):
        self.start_time = time.time()
        self.state = "started"

    def on_finished(self):
        self.end_time = time.time()
        self.state = "finished"

    def serialize_results(self) -> list[dict]:
        all_results = []
        if self.results:
            for result in self.results["results"]:
                counts = result["data"]["counts"]
                seed = result["seed_simulator"]
                circuit_time = result["time_taken"]
                circuit_results = {
                    "counts": counts,
                    "seed": seed,
                    "circuit_simulation_time": circuit_time,
                }
                all_results.append(circuit_results)
        return all_results

    def serialize(self):
        return {
            "results": self.serialize_results(),
            "state": self.state,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "circuit_label": self.circuit_label,
            "num_circuits": self.num_circuits,
            "num_iters": self.num_iters,
            "num_qubits": self.num_qubits,
            "backend": self.backend.serialize(),
        }

    def write(self, directory: Path, filename: str = "quantum_simulation.json"):
        os.makedirs(directory, exist_ok=True)
        write_json(self.serialize(), directory / filename)
