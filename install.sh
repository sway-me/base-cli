#!/bin/bash

set -e

# config env
# run base.sh && server.sh

# generate_env.py
# generate_docker_compose.py


# link config files
echo -e "\nLinking traefik config files...\n"
stow --target=$HOME traefik




