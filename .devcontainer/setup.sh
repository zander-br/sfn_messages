#!/bin/bash

set -xe

# Config uv
pipx install uv==0.9.10
[ -e .venv ] || (uv venv --python /usr/local/bin/python .venv && uv sync)

# Completion
pipx install argcomplete
mkdir -p ~/.local/share/bash-completion/completions
echo 'eval "$(pip completion --bash)"' > ~/.local/share/bash-completion/completions/pip
echo 'eval "$(register-python-argcomplete pipx)"' > ~/.local/share/bash-completion/completions/pipx
