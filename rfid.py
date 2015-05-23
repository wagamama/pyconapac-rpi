import subprocess
import inspect

def read():
	print inspect.stack()[0][3]
	p = subprocess.Popen('/home/pi/3rd/libnfc-1.7.0-rc7/examples/nfc-poll', shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
	for line in p.stdout.readlines():
		if "UID (NFCID1)" in line:
			uid_nfcid = line.split(":")
			uid = uid_nfcid[1].strip(' \t\n\r')
			return uid	
	return None
	


