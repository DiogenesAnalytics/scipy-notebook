# ------------------------------------------------------------------------------
# Reproducible Jupyter scientific image
# ------------------------------------------------------------------------------

FROM quay.io/jupyter/minimal-notebook:python-3.11

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# ------------------------------------------------------------------------------
# Root system dependencies
# ------------------------------------------------------------------------------

USER root

RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    # for cython: https://cython.readthedocs.io/en/latest/src/quickstart/install.html
    build-essential \
    # for latex labels
    cm-super \
    dvipng \
    # for matplotlib anim
    ffmpeg && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# More info: https://github.com/jupyter/docker-stacks/issues/2296
RUN rm -rf "/home/${NB_USER}/.cache/"

# ------------------------------------------------------------------------------
# Switch back to Jupyter user
# ------------------------------------------------------------------------------

USER ${NB_UID}

# ------------------------------------------------------------------------------
# Copy environment first for Docker layer caching
# ------------------------------------------------------------------------------

COPY --chown=${NB_UID}:${NB_GID} environment.yml /tmp/environment.yml

# ------------------------------------------------------------------------------
# Rebuild the scientific Python stack reproducibly
# ------------------------------------------------------------------------------

RUN mamba env update -n base -f /tmp/environment.yml && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Import matplotlib the first time to build the font cache
RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions "/home/${NB_USER}"

# More info: https://github.com/jupyter/docker-stacks/issues/2296
RUN rm -rf "/home/${NB_USER}/.cache/"

# ------------------------------------------------------------------------------
# Runtime context (Jupyter user)
# ------------------------------------------------------------------------------

USER ${NB_UID}
WORKDIR "${HOME}"
