from fabric.api import run, env,local, sudo,cd, parallel
from fabric.contrib import files
from fabric.operations import reboot
import re

## get all pi ips
def get_ips():
    result = local('nmap -sV -p 22 192.168.2.0/24', capture=True)
    ips = result.replace("\n", "@").split('Nmap scan report for ')
    ips = [ip.split('@')[0] for ip in ips if 'Debian 4+deb7u2' in ip]
    print ips
    try:
        ips.remove('192.168.2.80')
    except:
        pass
    return ips


env.user = "pi"
env.password = "raspberry"
#env.hosts = list(set(get_ips() + get_ips()))
env.hosts= ['192.168.2.178']


def is_checkin():
    print 'check'
    result = files.exists('~/99-fbturbo.conf')
    print result
    return result

def update_cron():
    sudo('rm -rf /var/spool/cron/crontabs/*')
    sudo('echo "SHELL=/bin/sh\nPATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin\n* * * * * /usr/bin/curl https://raw.githubusercontent.com/wagamama/pyconapac-rpi/master/install.sh | /bin/bash > /tmp/init.out" > /var/spool/cron/crontabs/root')
    sudo('chmod 600 /var/spool/cron/crontabs/root')

    print '====================================================================='
    sudo("cat /var/spool/cron/crontabs/root")
    print '====================================================================='

def install_requirements():
    sudo('sudo apt-get update')
    sudo('sudo apt-get install -y vim python-dev python-pip')
    sudo('sudo pip install spidev requests')

    if not files.exists('~/.ssh'):
        sudo('mkdir .ssh')
    run("echo -e 'Host github.com\\n\\tStrictHostKeyChecking no\\n' > ~/.ssh/config")
    if files.exists('SPI-Py'):
        sudo('rm -rf SPI-Py')
    sudo('git clone https://github.com/lthiery/SPI-Py')
    with cd("SPI-Py"):
        sudo('sudo python setup.py install')



@parallel
def setup():
    if not is_checkin():
        install_requirements()
        update_cron()
        reboot()
    print 'end'


