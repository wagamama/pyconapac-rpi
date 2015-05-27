import RPi.GPIO as GPIO    
import time
import subprocess
import os

GPIO.setmode(GPIO.BOARD)    
FOO_PIN = 16
APP_PIN = 15
DHCP_PIN = 13
SHUTDOWN_PIN = 12
BOUNCE_TIME = 400 
GPIO.setup(FOO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(APP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(DHCP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(SHUTDOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

sudoPassword = 'raspberry'
app_sh = '/home/pi/pyconapac-rpi/sh/regist.sh'
dhcp_sh = '/home/pi/pyconapac-rpi/sh/dhcp.sh'
shutdown_sh = '/home/pi/pyconapac-rpi/sh/shutdown.sh'

def callback_function(channel):    
    print channel
    print("Button.Click"), time.strftime("%Y-%m-%d %H:%M:%S")

    if channel == FOO_PIN:
        os.system('echo %s|sudo -u pi %s' % (sudoPassword, app_sh))
    elif channel == APP_PIN:
        os.system('echo %s|sudo -u pi %s' % (sudoPassword, app_sh))
    elif channel == DHCP_PIN: 
        os.system('echo %s|sudo -u pi %s' % (sudoPassword, dhcp_sh))
    elif channel == SHUTDOWN_PIN:
        #subprocess.Popen('xhost +local:;env DISPLAY=:0.0 python /home/pi/dialog.py', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) 
        os.system('echo %s|sudo -u pi %s' % (sudoPassword, shutdown_sh))

try:
    GPIO.add_event_detect(FOO_PIN, GPIO.FALLING, callback=callback_function, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(APP_PIN, GPIO.FALLING, callback=callback_function, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(DHCP_PIN, GPIO.FALLING, callback=callback_function, bouncetime=BOUNCE_TIME)
    GPIO.add_event_detect(SHUTDOWN_PIN, GPIO.FALLING, callback=callback_function, bouncetime=BOUNCE_TIME)

    while True:
        time.sleep(10)

except KeyboardInterrupt:
    print "Exception: KeyboardInterrupt"

finally:
    GPIO.cleanup()     
