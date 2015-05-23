#!/bin/bash

sudo kill -9 $(ps -ef |grep wpa| awk '{print $2}')

sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant/wpa_supplicant.conf

sudo dhclient wlan0

ifconfig  | grep 'inet addr:'| grep -v '127.0.0.1' | cut -d: -f2 | awk '{ print $1}'

