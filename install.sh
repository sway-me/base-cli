#!/bin/bash

set -e
sudo apt install python3-pip
sudo -H pip3 install regex PyInquirer PyNamecheap pyyaml

# config env
# run base.sh && server.sh
mkdir -p Backups Books Code Docs Downloads/books Feeds Film Music Office Public Series


# generate_env.py
# generate_docker_compose.py


# link config files
echo -e "\nLinking traefik config files...\n"
stow --target=$HOME traefik




