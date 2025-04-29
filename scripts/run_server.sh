#!/bin/sh

eval $(pdm venv activate)
fastapi run src/zimit_manager/main.py
