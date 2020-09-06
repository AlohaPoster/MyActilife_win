import serial
import time
def getpower(devStr):
    ser = serial.Serial(devStr, 115200, timeout = 1)
    ser.write("3: Get Service Power".encode())
    recvStr = ser.read(64)
    return recvStr

def gettime(devStr):
    ser = serial.Serial(devStr, 115200, timeout=1)
    ser.write("2: Get RTC time now".encode())
    recvStr = ser.read(64)
    return recvStr

def getcurrtime(devStr):
    ser = serial.Serial(devStr, 115200, timeout=1)
    ctime = "1: "+ time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
    ser.write(ctime.encode())
    recvStr = ser.read(64)
    return recvStr
