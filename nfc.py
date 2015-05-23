import subprocess


class NFC(object):
    
    def __init__(self, cmd_path):

        self.cmd_path = cmd_path

    def read(self):
        p = subprocess.Popen(self.cmd_path, shell=True, 
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

        for line in p.stdout.readlines():
            if "UID (NFCID1)" in line:
                uid_nfcid = line.split(":")
                uuid = uid_nfcid[1].strip(' \t\n\r')
                return uuid

if __name__ == "__main__":
    print NFC('/home/pi/3rd/libnfc-1.7.0-rc7/examples/nfc-poll').read()
