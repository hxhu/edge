import sys
import getopt
import time
from mqttPublisher import sender

def main(argv=None):   
    # get picture

    # detect
    data = {"device":1234567890,"message":"test","model":"yolov3-2020-12-3"}
    
    # mqtt sender
    sender(data)
    

if __name__ == "__main__":
    sys.exit(main())