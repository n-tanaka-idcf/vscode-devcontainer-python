#!/bin/bash

# Install misc commands
aqua install --config .devcontainer/${DEVCONTAINER_NAME}/aqua.yaml

# Setup starship config
mkdir -p ${HOME}/.config
cp .devcontainer/${DEVCONTAINER_NAME}/starship.toml ${HOME}/.config/starship.toml

# Install python and its packages
cd /workspace/${DEVCONTAINER_NAME}
# uv sync
uv python install --default --preview-features python-install-default
# uv sync --frozen
