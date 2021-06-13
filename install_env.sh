#!/bin/bash

# prepare venv
ENV="env"
ENV_PY="$ENV/bin/python3"

if [! -d $ENV]; then
    python3 -m venv $ENV
fi

# install dependencies
$ENV_PY -m pip install "requirements.txt"
$ENV_PY -m pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.0.0/en_core_web_sm-3.0.0.tar.gz"

# download necessery files for hotspot
# wget . .
# unzip . .