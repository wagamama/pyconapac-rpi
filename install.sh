cd /home/pi
rm -f /home/pi/master.zip
wget https://github.com/wagamama/pyconapac-rpi/archive/master.zip
rm -rf /home/pi/pyconapac-rpi
unzip master.zip
mv /home/pi/pyconapac-rpi-master /home/pi/pyconapac-rpi
touch /tmp/network