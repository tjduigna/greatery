#!/bin/bash

source activate greatery

cd js
node server.js &
cd ..

python greatery/api/server.py

