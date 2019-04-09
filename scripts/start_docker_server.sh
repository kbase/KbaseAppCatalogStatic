#!/bin/sh
set -e

# Build docker image 'kbase-catalog'
docker build . -t kbase-catalog

# Export environment variables
export ROOT_PREFIX=/applist
export KBASE_ENDPOINT=https://kbase.us/services
export DASHBOARD_ENDPOINT=https://narrative.kbase.us
export GA_TRACKING_ID=UA-137652528-1
export AW_TRACKING_ID=AW-753507180
export DEVELOPMENT=1

# Create/start a new docker container and run it on port 5000. 
docker run -i -t -v $(pwd):/app -e DEVELOPMENT -e ROOT_PREFIX -e KBASE_ENDPOINT -e DASHBOARD_ENDPOINT -e GA_TRACKING_ID -e AW_TRACKING_ID -p 5000:5000 kbase-catalog