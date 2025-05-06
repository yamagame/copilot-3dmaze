#!/bin/bash

OPTION=$1

if [ "$OPTION" == "REBUILD" ]; then
    docker build -t pyxapp .
fi
docker run -it --rm -v $PWD/:/app -w /app/src -p 8000:8000 pyxapp pyxel package . main.py
mv ./src/src.pyxapp ./out/copilot-3dmaze.pyxapp
