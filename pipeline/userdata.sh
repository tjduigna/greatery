#!/bin/bash

sudo yum update -y
sudo yum install git python36 docker -y
sudo service docker start

git clone https://github.com/tjduigna/sprout.git
git clone https://github.com/tjduigna/onion.git
git clone https://github.com/tjduigna/greatery.git

