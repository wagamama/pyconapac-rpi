from web import Web

web = Web()
cmd = {'action':'query-all'}
r = web.post(cmd)
print r.status_code
print r.text

