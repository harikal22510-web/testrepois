# Hyperactive CI Docker Image
# Pre-installs all dependencies to speed up CI runs
#
# Build with: docker build --build-arg PYTHON_VERSION=3.11 -t ghcr.io/simonblanke/hyperactive-ci:py3.11 .
# Push with:  docker push ghcr.io/simonblanke/hyperactive-ci:py3.11

ARG PYTHON_VERSION=3.11

FROM python:${PYTHON_VERSION}-slim

ARG PYTHON_VERSION

LABEL org.opencontainers.image.source="https://github.com/SimonBlanke/Hyperactive"
LABEL org.opencontainers.image.description="Hyperactive CI image with pre-installed dependencies (Python ${PYTHON_VERSION})"
LABEL org.opencontainers.image.licenses="MIT"

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy only dependency files first (for better layer caching)
WORKDIR /deps
COPY pyproject.toml ./
COPY docs/requirements.txt ./docs-requirements.txt

# Install all dependencies without the package itself
# We install extras separately to handle optional dependencies gracefully
RUN pip install --no-cache-dir \
    # Core test dependencies
    pytest==9.0.1 \
    flake8 \
    pytest-cov \
    pathos \
    # Build dependencies
    setuptools \
    build \
    wheel \
    # Docs dependencies
    sphinx>=7.0.0 \
    sphinx-autobuild \
    sphinx-copybutton \
    sphinx-design \
    sphinx-issues \
    myst-parser \
    numpydoc \
    pydata-sphinx-theme \
    # Core package dependencies
    "numpy>=1.18.1,<3.0.0" \
    "tqdm>=4.48.0,<5.0.0" \
    "pandas<3.0.0" \
    "gradient-free-optimizers>=1.2.4,<2.0.0" \
    "scikit-base<1.0.0" \
    "scikit-learn<1.8.0" \
    # all_extras dependencies
    "optuna<5" \
    cmaes \
    # test_parallel_backends (skip ray for now - complex deps)
    dask \
    joblib \
    # Pre-commit for code quality
    pre-commit

# Install torch CPU-only (much smaller than full torch)
# Skip for Python 3.14 as torch may not be available
RUN if [ "${PYTHON_VERSION}" != "3.14" ]; then \
    pip install --no-cache-dir torch --index-url https://download.pytorch.org/whl/cpu; \
    fi

# Install lightning (depends on torch)
RUN if [ "${PYTHON_VERSION}" != "3.14" ]; then \
    pip install --no-cache-dir lightning; \
    fi

# Install tf_keras
RUN pip install --no-cache-dir tf_keras || true

# Install sktime/skpro (skip for Python 3.14)
RUN if [ "${PYTHON_VERSION}" != "3.14" ]; then \
    pip install --no-cache-dir sktime skpro || true; \
    fi

# Clean up
RUN rm -rf /deps

# Set working directory for CI
WORKDIR /workspace

# Default command
CMD ["python", "--version"]
