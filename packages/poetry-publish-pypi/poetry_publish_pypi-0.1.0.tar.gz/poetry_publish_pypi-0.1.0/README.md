# Pypi

## pip config

Poetry stores your API token in a plaintext file when you add it as your credentials.

    $HOME/.config/pip/pip.conf
    $HOME/.pip/pip.conf

## Simple text file

### 1. Configure token to repositories

    poetry config pypi-token.pypi <your-api-token>

### 2. Build and pulish it

    poetry publish --build

## Using keyring

### 1. Install Keyring

Ensure you have the keyring package installed:

    pip install keyring

### 2. Check Available Backends

List available backends to see which ones are installed:

    python -m keyring --list-backends

## 3. Using env

    export PYPI_USERNAME=__token__
    export PYPI_PASSWORD=<token-from-pypi>


poetry run pytest --cov=src tests/
