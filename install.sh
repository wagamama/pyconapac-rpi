#!/bin/sh

if [ ! -f /tmp/network ]; then
    i="0"
    while [ $i -lt 4 ] 
    do  
        cd /home/pi
        rm -f /home/pi/master.zip 
        wget https://github.com/wagamama/pyconapac-rpi/archive/master.zip 
        size=`ls -al master.zip | awk '{print $5}'`
        if [ "$size" -gt 10000 ]; then
            rm -rf /home/pi/pyconapac-rpi
            unzip master.zip
            mv /home/pi/pyconapac-rpi-master /home/pi/pyconapac-rpi
            chown -R pi:pi pyconapac-rpi
            touch /tmp/network
            cd /home/pi/pyconapac-rpi
            # put check bee here
    
            sudo python /home/pi/pyconapac-rpi/sponsorship.py &
            break
        fi  
        i=$[$i+1]
    done
fi


