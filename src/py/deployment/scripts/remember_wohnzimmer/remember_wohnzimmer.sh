#!/bin/bash
source /home/pi/Git/homebridge_automations/.venv/bin/activate

cd /home/pi/Git/homebridge_automations

PYTHONPATH=. python3 src/py/deployment/scripts/remember_wohnzimmer/remember_wohnzimmer.py