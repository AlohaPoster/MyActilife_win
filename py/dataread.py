import os

def getusb():
    var = os.popen('diskutil list')
    num = 0
    usblist = []
    mainsize = []
    for temp in var.readlines():
        if "/dev" in temp:
            usblist.append(temp)
            num = num + 1
        if "0:" in temp:
            lt = temp.split(" ")
            for i in range(0,len(lt)):
                if 'B' in lt[i]:
                    mainsize.append(lt[i-1]+lt[i])
    mainsize.append("")
    mainsize.append("")
    mainsize.append("")
    mainsize.append("")
    usblist.append("")
    usblist.append("")
    usblist.append("")
    usblist.append("")
    return num,usblist,mainsize
        

def getdevice():
    var = os.popen('ls /dev/tty*')
    num = 0
    usblist = []
    for temp in var.readlines():
        if "/tty.usb" in temp:
            usblist = []
            num = num + 1
    usblist.append("")
    usblist.append("")
    usblist.append("")
    usblist.append("")
    return num,usblist
    

if __name__ == "__main__":
    getusb()
