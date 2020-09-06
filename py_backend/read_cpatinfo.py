import time
import serial

class getUSBinfo:
    def getpower(self, devStr):
        ser = serial.Serial(devStr, 115200, timeout = 1)
        ser.wirte("Get Service Power")
        recvStr = ser.read(64)
        print(recvStr)

    def gettime(self, devStr):
        ser = serial.Serial(devStr, 115200, timeout=1)
        ser.wirte("Get RTC time now")
        recvStr = ser.read(64)
        print(recvStr)

    def getcurrtime(self, devStr):
        ser = serial.Serial(devStr, 115200, timeout=1)
        ser.wirte(time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
        recvStr = ser.read(64)
        print(recvStr)