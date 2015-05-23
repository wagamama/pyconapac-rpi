import requests
import json

class web():
    #url = "http://www.raspberrypi.com.tw/pycon_tw/2015/server.php"
    #url = "http://www.raspberrypi.com.tw/pycon_tw/2015/code/srv.php"
    url = "http://www.raspberrypi.com.tw/pycon_tw/2015/code/server.php"
    #url = "http://www.raspberrypi.com.tw/pycon_tw/2015/code/json.php"
    headers = {'content-type': 'application/json'}
    payload = None

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

