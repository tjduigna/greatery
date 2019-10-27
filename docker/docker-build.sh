#!/bin/bash

# assumes already logged in to docker hub
#sudo docker build -t greatery:base-latest -f Dockerfile.base .
sudo docker build -t 597104984438.dkr.ecr.us-east-1.amazonaws.com/greatery:latest -f Dockerfile.greatery .

# sudo docker image inspect greatery:latest > manifest.json

# assumes aws configure already done
aws ecr get-login
sudo docker `aws ecr get-login` # but remove the -e none ? unset param..
