# Jupyter quickstart

These steps walk through creating an isolated Python environment, installing notebook tooling, and starting Jupyter Lab with a dedicated kernel for this repository.

## 1. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

## 2. Install core notebook dependencies

Install Jupyter Lab along with a few common scientific packages used throughout the bootcamp materials.

```bash
pip install --upgrade pip
pip install jupyterlab ipykernel numpy pandas matplotlib seaborn
```

Feel free to add any additional packages needed for your specific analyses.

## 3. Register a named kernel

With the virtual environment activated, register a kernel so notebooks can target this environment explicitly.

```bash
python -m ipykernel install --user --name bootcamp-env --display-name "Python (bootcamp)"
```

You can later remove the kernel with `jupyter kernelspec uninstall bootcamp-env` if needed.

## 4. Launch Jupyter Lab

Start Jupyter Lab from the repository root so relative file paths inside notebooks resolve correctly.

```bash
jupyter lab
```

After the server starts, open the provided URL in your browser. When creating or opening notebooks, select the `Python (bootcamp)` kernel to ensure the correct environment is used.
