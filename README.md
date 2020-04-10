# Overview

A simple example of how to use dsdk.

# Quickstart


## Building a model
1. Bring up jupyter to build a model `docker-compose up jupyter`
2. Navigate to `http://127.0.0.1:8889/` to connect to jupyter
3. Find an example of building a model at `dsdkexample.ipynb`
4. Run the code to create and save the model in `dsdk` compatable format

## Update your local
Modify the `model` parameter of `local/config.yaml` to point to your model in the `model` directory

## Update your secrets
See `secrets/example_config.yaml`
1. Create `secrets/config.yaml`

## Run the pipeline
1. Bring up the pipeline `docker-compose up`
2. `\o/`