import json
#import docx
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from gen_py.test import userService
import myinteract
import dataread
import access
import os
import util
import predict
import time

class Test:
    
    #登录申请
    def log_test(self, info):
        info = json.loads(info)
        answer = access.login_test(info)
        if answer== -1:
            info = {
                "ifsuccess":"no"
            }
        else:
            info = access.accessjson(int(answer[1]))
            info['ifsuccess'] = 'yes'
            info['user_id'] = answer[1]
            info['account'] = answer[0]
            info['email'] = answer[2]
        info = json.dumps(info)
        return info

    #申请账户
    def registe(self, info):
        info = json.loads(info)
        if int(info["role"]) == 4:
            infoget = {"rolelist": "4",
                        "account": info['name'],
                        "email": info['email'],
                        "password": info['password1'],
                        "salt": 0}
            answer = access.makeuser(infoget)
            #chongfu 
            if answer == 2:
                return "2"
            #失败
            if answer == -1:
                return "-1"
            if answer == 1:
                return "1"
        else :
            #角色需要申请
            return "-2"
    
    def getsdreader(self,info):
        try :
            num,usblist,sizelist = dataread.getusb()
            ret = {
                'num':num,
                'firstusb':usblist[0],
                'secondusb':usblist[1],
                'thirdusb':usblist[2],
                'fourthusb':usblist[3],
                'firstsize':sizelist[0],
                'secondsize':sizelist[1],
                'thirdsize':sizelist[2],
                'fourthsize':sizelist[3]
            }
            ret = json.dumps(ret)
            print(ret)
            return ret
        except :
            return "-1"
        
    def getdevice(self,info):
        try :
            num,usblist = dataread.getdevice()
            ret = {
                'num':num,
                'firstusb':usblist[0],
                'secondusb':usblist[1],
                'thirdusb':usblist[2],
                'fourthusb':usblist[3]
            }
            ret = json.dumps(ret)
            print(ret)
            return ret
        except :
            return "-1"

    def gettime(self, info):
        info = json.loads(info)
        path = info['path']
        t = myinteract.gettime(path)
        return t

    def retime(self, info):
        info = json.loads(info)
        path = info['path']
        t = myinteract.getcurrtime(path)
        return t

    def getpower(self, info):
        num,data = access.userdict()
        namelist = ['userid','account','date','email','roles']
        data = util.tojson(data,num,namelist)
        print(data)
        return data

    def getdataresult(self, info):
        info = json.loads(info)
        try :
            password = info['ospassword']
            dir_path = os.path.dirname(os.path.abspath(__file__))
            cmd = "python3 " + dir_path + "/read.py -p " + info['devicepath'] + " -u "+info['userid']+" -d " +info['deviceid'] +" -n "+info['csvfilename']+" -c "+info["csvpath"]
            os.system("echo %s|sudo -S %s" % (password,cmd))
            time.sleep(8)
            cmd = "python3 " + dir_path + "/getpdf.py -f " + info["csvfilename"] + " -p "+info['csvpath'] + " -n "+info['username'] + " -i "+info['userid'] + " -d "+info['deviceid'] + " -t "+info['date'] + " -o "+info['ifupload']
            os.system("echo %s|sudo -S %s" % (password,cmd))
            time.sleep(8)
            if info["ifupload"] == "on":
                access.uploaddata(info)
            time.sleep(5)
            return "1"
        except :
            return "-1"

    def getuser(self,info):
        num,data = access.userdict()
        if num == -1:
            return "-1"
        namelist = ['userid','account','date','email','roles']
        data = util.tojson(data,num,namelist)
        print(data)
        return data

    def getroles(self,info):
        num,data = access.roledict()
        if num == -1:
            return "-1"
        namelist = ['roleid','rolename']
        data = util.tojson(data,num,namelist)
        print(data)
        return data

    def getaccessjson(self,info):
        info = json.loads(info)
        data = access.accessjson_role(int(info["role_id"]))
        if data == -1 :
            return "-1"
        data = json.dumps(data)
        return data

    def deleteuser(self,info):
        info = json.loads(info)
        userlist = info["userid"].split(",")
        userlist = userlist[0:len(userlist):2]
        for user in userlist:
            access.killuser(user)
        return "1"
    
    def deleterole(self,info):
        info = json.loads(info)
        if access.killrole(info['roleid'])==0:
            return '1'
        else :
            return "-1"

    def userchangerole(self,info):
        info = json.loads(info)
        userlist = info["userid"].split(",")
        userlist = userlist[0:len(userlist):2]
        rolelist = info["roleid"].split(",")
        rolelist = rolelist[0:len(rolelist):2]
        for user in userlist:
            if access.remake_user_role(user,rolelist)==-1:
                return "-1"
        return "1"

    def rolechangeaccess(self,info):
        try :
            info = json.loads(info)
            if access.remake_role_access(info)==0:
                return "1"
            else :
                return "-1"
        except :
            return "-1"

    def downloadresources(self,info):
        info = json.loads(info)
        info["result_id"] = int(info["result_id"])
        answer = access.downloadsm(info)
        return str(answer)

    def dowloadinstruction(self,info):
        info = json.loads(info)
        info["result_id"] = int(info["result_id"])
        answer = access.downloadsm(info)
        return str(answer)
    
    def getmineresult(self,info):
        info = json.loads(info)
        num,data = access.minedata(info["account"])
        if num == -1:
            return json.dumps({"wrong":"wrong"})
        datajson = util.tojson(data,num,['result_id','deviceid','userid','starttime'])
        print(datajson)
        return datajson

    def getconditionresult(self,info):
        try:
            info = json.loads(info)
            print(info)
            num,data = access.conditiondata(info)
            if num == -1 :
                raise Exception("something wrong")
            datajson = util.tojson(data,num,['result_id','account','deviceid','userid','starttime'])
            print("successs")
            return datajson
        except :
            print("nnnnnnnn")
            return json.dumps({"wrong":"wrong"})
        

    def newuser(self,info):
        info = json.loads(info)
        answer = access.makeuser(info)
        return str(answer)
    
    def newrole(self,info):
        info = json.loads(info)
        answer = access.makerole(info['role_name'],info['access_json'])
        return str(answer)

if __name__ == "__main__":
    
    port = 8000
    ip = "127.0.0.1"
    # 创建服务端
    handler = Test()  
    processor = userService.Processor(handler)  
    # 监听端口
    transport = TSocket.TServerSocket(ip, port)  
    # 选择传输层
    tfactory = TTransport.TBufferedTransportFactory()
    # 选择传输协议
    pfactory = TBinaryProtocol.TBinaryProtocolFactory()
    server = TServer.TThreadedServer(processor, transport, tfactory, pfactory)
    print("start server in python")
    server.serve()
    print("Done") 