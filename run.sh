#!/bin/bash

docker build -t campaign-app .

open index.html

docker run -p 5000:5000 --rm campaign-app
