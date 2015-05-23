import subprocess as sub

def execute(cmd):
    p = sub.Popen(cmd, stdout=sub.PIPE, stderr=sub.PIPE)
    output, errors = p.communicate()
    return output

MACHINE_ID = execute("cat /proc/cpuinfo | grep Serial | awk ' {print $3}'")
SD_ID = execute("ls -l /dev/disk/by-uuid/ | grep mmcblk0p2 | awk '{print $9}'")
