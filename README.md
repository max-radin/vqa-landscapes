# Visualization of Variational Quantum Algorithm cost-function landscapes

This project uses [orqviz](https://github.com/zapatacomputing/orqviz) to extract a two-dimensional energy landscape from a Variational Quantum Eigensolver (VQE) problem, and then render a surface plot using [PyQtGraph](https://www.pyqtgraph.org/).

This example considers using VQE for a four-qubit molecular hydrogen Hamiltonian.
First, an optimization is performed using a four-parameter ansatz.


## Installation
First install [z-quantum-core](https://github.com/zapatacomputing/z-quantum-core) and [qe-qiskit](https://github.com/zapatacomputing/qe-qiskit) following the instructions in those repos.
Then install the remaining required packages with `python -m pip install -r requirements.txt`.
If you plan to export a video, you will also need `make` and `ffmpeg`.

## Usage

### Viewing the landscape

To view the landscape, run
```bash
python main.py
```

### Generating the video
To generate a video, first begin generating images with
```bash
python main.py --save-images
```
Images will accumulate in the `img` subdirectory.
Once you feel you've collected enough images, close the application window.
The images can then be combined into a video by running `make`.
