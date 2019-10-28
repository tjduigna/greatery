#!/bin/bash

# log in to ECR docker registry
$(aws ecr get-login --no-include-email --region us-east-1)

# add step for updating base image
# read somewhere ECR doesn't cache
# correctly so do this on-demand

#sudo docker build -t greatery-base -f Dockerfile.base .
#sudo docker tag greatery-base:latest 597104984438.dkr.ecr.us-east-1.amazonaws.com/greatery-base:latest
#sudo docker push 597104984438.dkr.ecr.us-east-1.amazonaws.com/greatery-base:latest

# build new image and push to ECR
sudo docker build -t greatery -f Dockerfile.greatery .
sudo docker tag greatery:latest 597104984438.dkr.ecr.us-east-1.amazonaws.com/greatery:latest
sudo docker push 597104984438.dkr.ecr.us-east-1.amazonaws.com/greatery:latest
