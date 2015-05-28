from web import Web

web = Web()
cmd = {'action':'restore'}
r = web.post(cmd)
print r.status_code
print r.text

