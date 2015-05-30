from web import Web
import sys

def main(uid):
    web = Web()
    r = web.infoQuery(uid)

if __name__ == '__main__':
    main(sys.argv[1])
