<h1 align="center">Room Statistics Visualization</h1>

---

A Python script that reads a JSON file of room data, visualizes various statistics, detects anomalies, and saves the generated plots. It also includes unit tests to verify the functionality of the implemented methods and a Jupyter notebook for interactive analysis.

## Table of Contents
- [Installation](#installation)
- [Usage](#usage)
  - [Functions](#functions)
  - [Running the Script](#running-the-script)
  - [Running Unit Tests](#running-unit-tests)
  - [Jupyter Notebook](#jupyter-notebook)
- [File Structure](#file-structure)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Alexanderms36/DokuSketch_testtask.git
   cd DokuSketch_testtask
   ```

2. Create a virtual environment (optional):
   ```bash
   python3 -m venv venv
   source venv/bin/activate   # for Windows: venv\\Scripts\\activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

   Ensure the following libraries are included in your `requirements.txt`:
   - `pandas 2.2.1`
   - `matplotlib 3.8.4`

## Usage

### Functions

The repository provides the functions in `function.py`:

1. **draw_plots(json_path)**:
   - Reads a JSON file and generates plots that are comparing floor and ceiling statistics
   - Plots are saved in a folder named `/plots/`
   - Returns a list of plot pathes

2. **generate_statistics(df)**:
   - Computes and prints mean, max, and min errors for floor and ceiling data
   - Generates bar plots for average mean errors and max/min errors per room

3. **draw_anomalies(df, anomaly_threshold)**:
   - Detects and plots rooms with anomalies based on a specified threshold for differences between floor and ceiling mean values

### Running the Script

You can generate plots and perform analysis by running the following:

```py
from function import draw_plots
json_path = "deviation.json" #put the path to your json
draw_plots(json_path)
```

This will read the JSON file provided in the `json_path` and generate plots in the `plots` directory

Make sure to have a valid JSON file with the required structure (name, gt_corners, rb_corners, mean, max, min etc.)

### Running Unit Tests

Unit tests are provided in the `test_function.py` file, which uses Python’s `unittest` framework and mocks certain functions to test the script

To run the unit tests, use:

```bash
python -m unittest discover
```

The tests verify that:
- JSON reading and plotting functions work as expected
- The statistics and anomaly detection functions execute correctly

### Jupyter Notebook

You can explore the functionality interactively using the provided Jupyter notebook (`Notebook.ipynb`). This notebook demonstrates how to load a JSON file and generate visualizations based on JSON data

To start the notebook, run:

```bash
jupyter notebook
```

Open `Notebook.ipynb` from the Jupyter interface

## File Structure

- `function.py`: Main Python script that contains the `draw_plots` function
- `test_function.py`: Unit tests to verify the functionality of the methods in `function.py`
- `Notebook.ipynb`: Jupyter notebook for interactive data analysis and visualization
- `plots/`: Directory where generated plots are saved as .png pictures
- `requirements.txt`: List of dependencies required to run the project
- `deviation.json`: JSON data using for drawing plots
