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