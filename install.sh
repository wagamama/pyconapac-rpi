#!/bin/bash

if [ ! -f /tmp/network ]; then
    cd /home/pi
    rm -f /home/pi/master.zip
    wget https://github.com/wagamama/pyconapac-rpi/archive/master.zip
    size=`ls -al master.zip | awk '{print $5}'`
    if [ "$size" -gt 10000 ]; then
        rm -rf /home/pi/pyconapac-rpi
        unzip master.zip
        mv /home/pi/pyconapac-rpi-master /home/pi/pyconapac-rpi
        chown -R pi:pi pyconapac-rpi
        cd /home/pi/pyconapac-rpi
        i="0"
        while [ $i -lt 4 ]
        do
            sudo python /home/pi/pyconapac-rpi/lib/buzzer.py
            let i=$i+1
        done
        sudo dpkg --configure -a
        sudo apt-get install python-pip
        sudo pip install -r /home/pi/pyconapac-rpi/requirements.txt
        sudo kill -9 $(ps -ef | grep sponsorship.py | awk '{print $2}')
        sudo python /home/pi/pyconapac-rpi/sponsorship.py &
        sudo python /home/pi/pyconapac-rpi/health_check.py &
        touch /tmp/network
    fi
fi
