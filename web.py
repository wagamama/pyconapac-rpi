import requests
import json
from json import JSONEncoder, JSONDecoder

class web():
    #url = "http://www.raspberrypi.com.tw/pycon_tw/2015/server.php"
    #url = "http://www.raspberrypi.com.tw/pycon_tw/2015/code/srv.php"
    url = "http://www.raspberrypi.com.tw/pycon_tw/2015/code/server.php"
    #url = "http://www.raspberrypi.com.tw/pycon_tw/2015/code/json.php"
    headers = {'content-type': 'application/json'}
    payload = None

    def __init__(self):
        self.encoder = JSONEncoder()
        self.decoder = JSONDecoder()

    class err():
        status_code = 999
        text = "exception"

    # payload : {"json":"http://playground.imagga.com/static/img/example_photo.jpg"}
    def get(self, payload):
        try:
            return requests.request("GET", self.url, headers=self.headers, params=payload)
        except requests.exceptions.RequestException as e:
            print e
            return self.err()

    def post(self, payload):
        try:
            #payload = json.dumps(payload)
            return requests.post(self.url, data=payload)
            #response = requests.post(url,params=data,headers=headers)
        except requests.exceptions.RequestException as e:
            print e
            return self.err()

    def register(self, dataList):
        # dataList = [(reg_no, uid, regist_wtime), ...]
        # return: True/False

        # test data
        # reg_no:
        # uid:
        # regist_wtime:
        payloadPy = {"action": "register",
            "data": []}
        for data in dataList:
            payloadPy['data'].append({
                "reg_no": data[0],
                "uid": data[1],
                "regist_wtime": data[2]
                })
        payloadJson = self.encoder.encode(payloadPy)
        req = self.post(payloadJson)
        # need to continue

    def tshirtQuery(self, uid):
        # uid = uid
        # return: (tshirt, tshirt_wtime)

        # test data
        # uid: 1b b6 d5 09
        payloadPy = {"action": "tshirt-register",
            "data": uid}
        payloadJson = self.encoder.encode(payloadPy)
        req = self.post(payloadJson)
        if req.status_code != 200:
            return None
        # need to continue

    def tshirtUpdate(self, data):
        # data = (uid, tshirt_wtime)
        # return: True/False
        pass

    def infoQuery(self, dataList):
        # dataList = [uid, ...]
        # return: [(reg_no, uid), ...]
        pass

def main():
    w = web()
    w.tshirtQuery('1b b6 d5 09')

if __name__ == '__main__':
    main()
