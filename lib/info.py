import re, os
import logging

re_machine = re.compile(r'Serial[\s]+:[\s]+([a-f\d]+)')
def machine_id():
    try:
        return re_machine.findall(open('/proc/cpuinfo').read())[0]
    except Exception as e:
        logging.exception(e)

MACHINE_ID = machine_id()

re_sd = re.compile(r'([\da-f]{8}\-[\da-f\-]+)')
def sd_id():
    try:
        os.system("ls -l /dev/disk/by-uuid/ > disks.tmp")
        with open('disks.tmp') as ifile:
            for iline in ifile:
                if 'mmcblk0p2' in iline:
                    return re_sd.findall(iline)[0]
    except Exception as e:
        logging.exception(e)

SD_ID = sd_id()
