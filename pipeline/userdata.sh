#!/bin/bash

sudo yum update -y
sudo yum install git python36 docker -y
sudo service docker start

git clone --recurse-submodules https://github.com/tjduigna/greatery.git

