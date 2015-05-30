from db_controller import DBController
from web import *
import json

def main():
  db = DBController("/home/pi/pyconapac-rpi/db/pycon2015.db.nofacebook") 
  #cursor = db.conn.cursor()
  #cursor.execute("UPDATE regist SET regist_wtime=? WHERE reg_no=?", ('1', '274',))
  #cursor.execute("UPDATE regist SET scan_status=? WHERE reg_no=?", (0, '274',))
 
  #info = db.getInfoByReg('274')
  #info.scan_status = False
  #print info.scan_status
  #print info

  web = Web()
  needUpdateList = db.getNeedUpdate()
  print needUpdateList
  for info in needUpdateList:
    uid = info.uid
    reg_no = info.reg_no
    time = info.regist_wtime
    try:
      print uid, reg_no, time
      payload = {'action':'regist-update', 'reg_no':reg_no, 'uid':uid, 'regist_wtime':time}
      result = requests.post(web.url, data=payload)
      return json.loads(result.text)
    except requests.exceptions.RequestException as e:
      print e
      return self.err()
      
if __name__ == '__main__':
  main()

