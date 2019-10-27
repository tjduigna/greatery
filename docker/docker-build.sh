#!/bin/bash

# assumes already logged in to docker hub
sudo docker build -t greatery-base:latest -f Dockerfile.base .
sudo docker build -t greatery:latest -f Dockerfile.greatery .
