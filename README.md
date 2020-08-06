# Kbase App Catalog Static Page

KBase apps are analysis tools that you can use in KBase. Apps interoperate seamlessly to enable a range of scientific workflows (see figure below). Some of the apps were written by KBase scientists and developers; others are third-party tools that were integrated into KBase with our Software Developer Kit (SDK). The number of apps available in KBase will increase rapidly as members of the community use our SDK to integrate their analysis tools into the KBase platform.
The KBase [App Catalog](https://narrative.kbase.us/#appcatalog) lists all of the currently available apps.
This page is made so that Kbase Apps show up on web searches.

## Tech Stack

Python, Flask, Jinja

## Installation

Clone the repo on your local machine and install dependency.

```bash
pip install -r requirements.txt
```

## Docker Image build and run

Go to the project root folder and run

```bash
sh scripts/start_docker_server.sh
```

## `ROOT_PREFIX`

By default this app operates on the path `/applist`. This is required for the prod environment in which this app runs at `https://kbase.us/applist`. The path prefix `applist` is used in the top level proxy to route kbase.us requests to this app.

When developing locally, you can operate at root (`/`) as well. 

All local paths must be prefixed with `{{ conf.ROOT_PREFIX }}`. Relative paths won't work because of the usage of templates.

This is controlled in `conf.ini` for prod and `scripts/start_docker_server.sh` for local development.
