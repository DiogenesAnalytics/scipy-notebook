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

Installed via `environment.yml` into the base conda environment using `mamba`.

Includes a pinned scientific Python ecosystem (NumPy/SciPy/Pandas,
JupyterLab, visualization, ML tooling, etc.).

---

## 🏗️ Build

### Build image

```bash
make build
```

### Force clean rebuild

```bash
DCKR_NOCACHE=true make build
```

---

## 🐳 Docker Build Behavior

* Always pulls latest base image (`--pull`)
* Uses optional cache control via `DCKR_NOCACHE`
* Outputs image:

```
ghcr.io/diogenesanalytics/<repo-name>:base
```

---

## 🧪 Local CI (GitHub Actions via `act`)

### Install `act`

```bash
make install-act
```

### Check install

```bash
make check-act
```

### Run tests locally

```bash
make run-act-tests
```

With arguments:

```bash
make run-act-tests ARGS="-v"
```

---

## 🔁 Typical Workflow

```bash
make build
make run-act-tests
```

or:

```bash
DCKR_NOCACHE=true make build
make run-act-tests
```

---

## 🛠️ Makefile Commands

| Command              | Description                           |
| -------------------- | ------------------------------------- |
| `make build`         | Build Docker image                    |
| `make install-act`   | Install GitHub Actions runner (`act`) |
| `make check-act`     | Verify `act` installation             |
| `make run-act-tests` | Run GitHub Actions locally            |

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
FROM ghcr.io/diogenesanalytics/<repo-name>:master


COPY pyproject.toml poetry.lock .
RUN poetry install --no-root
```

---

## 🧠 Principle

> Conda defines the scientific world.
> Poetry defines the application world.
> Docker defines the boundary.
