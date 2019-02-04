# Kbase App Catalog Static Page
KBase apps are analysis tools that you can use in KBase. Apps interoperate seamlessly to enable a range of scientific workflows (see figure below). Some of the apps were written by KBase scientists and developers; others are third-party tools that were integrated into KBase with our Software Developer Kit (SDK). The number of apps available in KBase will increase rapidly as members of the community use our SDK to integrate their analysis tools into the KBase platform.
The KBase [App Catalog](https://narrative.kbase.us/#appcatalog) lists all of the currently available apps.
This page is made so that Kbase Apps show up on web searches.

## Tech Stack
Python, Flask, Jinja

## Installation
Clone the repo on your local machine and install dependency.
```
$ pip install -r requirements.txt
```
Set the application to work with by exporting the FLASK_APP environment variable:
```
$ export FLASK_APP=index.py
```
Run the application
```
$ flask run
``` 
or 
```
$ python -m flask run
```

## Environment Variables
KBASE_ENDPOINT: https://kbase.us/services

DASHBOARD_ENDPOINT: https://narrative.kbase.us

ROOT_PREFIX: /applist

GA_TRACKING_ID: Google Analytics Tracking ID

## Docker Image build and run
- export environment variables

```
export KBASE_ENDPOINT= https://kbase.us/services
export DASHBOARD_ENDPOINT=https://narrative.kbase.us
export ROOT_PREFIX=/applist
```
- build docker image 
```
docker build . -t kbase-catalog kbase-catalog
```
- run docker image using port 5000
```
docker run -e KBASE_ENDPOINT -e DASHBOARD_ENDPOINT -e ROOT_PREFIX -p 5000:5000 kbase-catalog
```