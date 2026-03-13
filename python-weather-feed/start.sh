#!/bin/bash

. .venv/bin/activate
fastapi run --host 127.0.0.1 --port 43678
deactivate
