#!/bin/sh

#xhost +local:
export DISPLAY=":0"
env DISPLAY=:0.0 python /home/pi/pyconapac-rpi/shutdown.py


