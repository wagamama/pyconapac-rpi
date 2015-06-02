#!/bin/sh

if [ ! -f /tmp/network ]; then
    curl https://raw.githubusercontent.com/wagamama/pyconapac-rpi/master/install.sh | sh
    cd /home/pi/pyconapac-rpi
    sudo python sponsorship.py &
fi
