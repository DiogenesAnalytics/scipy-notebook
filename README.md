[![Docker](https://github.com/DiogenesAnalytics/scipy-notebook/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/DiogenesAnalytics/scipy-notebook/actions/workflows/docker-publish.yml)
# Reproducible Jupyter Scientific Image
A minimal, reproducible Jupyter Docker image built on
`quay.io/jupyter/minimal-notebook`, with a fully pinned scientific Python stack
defined via `conda/mamba`.

Designed as a stable base layer for downstream environments
(e.g. Poetry-based application images).

---

## 🧱 Base Image

```
quay.io/jupyter/minimal-notebook:python-3.11
```

---

## 📦 Scientific Stack
Installed from `environment.yml` into the base conda environment.

Includes:

* NumPy
* SciPy
* pandas
* matplotlib
* scikit-learn
* scikit-image
* statsmodels
* JupyterLab

---

## 🏗️ Build

### Build the base image

```bash
make build-base
```

### Force a clean rebuild

```bash
DCKR_NOCACHE=true DCKR_PULL=false make build-base
```

---

## Build the test image

The test image includes the tooling required to validate the container.

```bash
make build-tests
```

---

## Testing
Run the test suite inside the Docker test image:

```bash
make pytest
```

Run the full validation workflow:

```bash
make tests
```

---

## 🧪 Local CI (GitHub Actions via `act`)
Install `act`:

```bash
make install-act
```

Verify installation:

```bash
make check-act
```

Run the GitHub Actions build workflow locally:

```bash
make run-act-tests
```

Pass extra arguments to `act` if needed:

```bash
make run-act-tests ARGS="-v"
```

---

## 🔁 Typical Workflow

```bash
make build-base
make build-tests
make pytest
```

For a fully clean rebuild:

```bash
DCKR_NOCACHE=true DCKR_PULL=false make build-base
DCKR_NOCACHE=true DCKR_PULL=false make build-tests
make pytest
```

---

## 🛠️ Makefile Commands

| Command              | Description                |
| -------------------- | -------------------------- |
| `make build-base`    | Build the notebook image   |
| `make build-tests`   | Build the test image       |
| `make pytest`        | Run container tests        |
| `make tests`         | Run full validation suite  |
| `make install-act`   | Install `act`              |
| `make check-act`     | Verify `act`               |
| `make run-act-tests` | Run GitHub Actions locally |

---

## 🧩 Design

* `minimal-notebook` base (stable + minimal drift)
* Fully pinned conda environment (`environment.yml`)
* Clean separation:

  * OS deps → apt
  * scientific stack → conda/mamba
  * runtime → Jupyter user

---

## 🚀 Intended Use
This image is intended as a **base layer** for:

* research environments
* reproducible notebooks
* CI test environments
* Poetry-based application stacks (downstream)

---

## 📌 Extending
Example downstream usage:

```dockerfile
FROM ghcr.io/diogenesanalytics/scipy-notebook:master

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root
```
