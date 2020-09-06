import json
import pymysql
import datetime
import cloudclient
import traceback
def rolemakejson(role_id,cursor,json):
    sql = 'select b.restfulverb,b.restfulobject from role_access a join access b on a.access_id=b.access_id where a.role_id="%d";' % int(role_id)
    num = cursor.execute(sql)
    data = cursor.fetchall()
    for i in range(0,num):
        json[data[i][0]][data[i][1]] = 1
    return json

def rootmakejson(root_id,cursor):
    sql = 'select b.restfulverb,b.restfulobject from role_access a join access b on a.access_id=b.access_id where a.role_id="%d";' % int(root_id) 
    num = cursor.execute(sql)
    data = cursor.fetchall()
    json = {
        'GET':{},
        'PUT':{},
        'POST':{},
        'DELETE':{}
    }
    for i in range(0,num):
        json[data[i][0]][data[i][1]] = 0
    return json

def getusrroles(user_class,cursor):
    try :
        sql = 'select b.role_id from user a join user_role b on a.user_id=b.user_id where a.user_id="%d";' % user_class
        num = cursor.execute(sql)
        data = cursor.fetchall()
        return num,data
    except:
        return -1,{}

#加载用户的权限散列
def accessjson(user_class):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try : 
        cursor = db.cursor()
        #以超级用户为基础查询所有权限
        json = rootmakejson(1,cursor)
        #用户对应的所有角色
        num,data = getusrroles(user_class,cursor)
        if num == -1 :
            raise Exception("ddd")
        #用每个角色的权限去填充权限散列表
        for i in range(0,num):
            json = rolemakejson(data[i][0],cursor,json)
        db.close()
        return json
    except :
        traceback.print_exc()
        db.close()
        return -1

#加载某一角色的权限散列
def accessjson_role(role_id):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        cursor = db.cursor()
        json = rootmakejson(1,cursor)
        json = rolemakejson(role_id,cursor,json)
        db.close()
        return json
    except :
        db.close()
        return -1

#加载角色列表
def roledict():
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        cursor = db.cursor()
        sql = 'select * from role' 
        num = cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        return num,data
    except :
        db.close()
        return -1,{}

#加载用户列表
def userdict():
    try :
        db = pymysql.connect("47.96.227.243","root","root","cpat")
        cursor = db.cursor()
        sql = 'select a.user_id,a.account,a.register_time,a.email,group_concat(b.role_id) from user a right join user_role b on a.user_id=b.user_id group by a.user_id;' 
        num = cursor.execute(sql)
        data = cursor.fetchall()
        db.close()
        return num,data
    except :
        db.close()
        return -1,{}

#删除角色
def killrole(role_id):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        role_id = int(role_id)
        cursor = db.cursor()
        sql = 'delete from role where role_id="%d";' % role_id
        cursor.execute(sql)
        sql = 'delete from role_access where role_id="%d"' % role_id
        cursor.execute(sql)
        db.commit()
        db.close()
        return 0
    except :
        db.close()
        return -1

#新增角色
def makerole(role_name,access_json):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try:
        rolename = role_name
        acc = access_json
        cursor = db.cursor()
        sql = 'select * from role where role_name="%s";' % rolename
        num = cursor.execute(sql)
        if num != 0:
            return 2
        sql = 'select max(role_id) from role'
        cursor.execute(sql)
        max_id = cursor.fetchone()
        max_id = int(max_id[0])
        sql = 'insert into role(role_id,role_name) values("%d","%s");' % (int(max_id+1),rolename)
        cursor.execute(sql)
        for verb in acc.keys():
            for obj in acc[verb].keys():
                if acc[verb][obj] == 1:
                    sql = 'select access_id from access where restfulverb = "%s" and restfulobject = "%s"' % (verb,obj)
                    num = cursor.execute(sql)
                    accid = cursor.fetchone()
                    accid = int(accid[0])
                    sql = 'insert into role_access(role_id,access_id) values("%d","%d");' % (int(max_id+1),int(accid))
                    cursor.execute(sql)
        db.commit()
        db.close()
        return 1
    except:
        db.close()
        return -1
    

#删除用户
def killuser(user_id):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        user_id = int(user_id)
        cursor = db.cursor()
        sql = 'delete from user where user_id="%d";' % user_id
        cursor.execute(sql)
        sql = 'delete from user_role where user_id="%d"' % user_id
        cursor.execute(sql)
        db.commit()
        db.close()
        return 0
    except :
        db.close()
        return -1

#新增用户
def makeuser(user_info_dict):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        role_list = user_info_dict["rolelist"].split(",")
        cursor = db.cursor()
        sql = 'select * from user where account="%s";' % user_info_dict["account"]
        num = cursor.execute(sql)
        if num != 0:
            return 2
        sql = 'select max(user_id) from user'
        cursor.execute(sql)
        max_id = cursor.fetchone()
        max_id = max_id[0]

        date = datetime.datetime.now().strftime("%Y-%m-%d")
        sql = 'insert into user(user_id,md5_password,md5_salt,email,account,register_time) values("%d","%s","%s","%s","%s","%s");' % (max_id+1,user_info_dict["password"],user_info_dict["salt"],user_info_dict["email"],user_info_dict["account"],date)
        cursor.execute(sql)
        for role_id in role_list:
            sql = 'insert into user_role(user_id,role_id) values("%d","%d");' % (max_id+1,int(role_id))
            cursor.execute(sql)
        db.commit()
        db.close()
        return 1
    except :
        return -1

#修改用户角色关系
def remake_user_role(user_id,role_id_list):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try:
        # user_id = info['userid']
        # role_id_list = []
        # for keys in info.keys():
        #     if keys != "userid" and info[keys] == 1:
        #         role_id_list.append(int(keys))
        cursor = db.cursor()
        #DELETE
        sql = 'delete from user_role where user_id="%d";' % int(user_id)
        cursor.execute(sql)
        #INSERT
        for i in range(0,len(role_id_list)):
            sql = 'insert into user_role(user_id,role_id) values("%d","%d");' % (int(user_id),role_id_list[i])
            cursor.execute(sql)
        db.commit()  
        db.close()
        return 0
    except :
        db.close()
        return -1

#修改角色权限关系
def remake_role_access(data):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        role_id = int(data['role_id'])
        role_access_json = data['access_json']
        cursor = db.cursor()
        #DELETE
        sql = 'delete from role_access where role_id="%d";' % role_id
        cursor.execute(sql)
        #INSERT
        for firstkey in role_access_json.keys():
            for secondkey in role_access_json[firstkey].keys():
                if int(role_access_json[firstkey][secondkey]) == 1 :
                    sql = 'select access_id from access where restfulverb="%s" and restfulobject="%s";' % (firstkey,secondkey)
                    cursor.execute(sql)
                    access_id = cursor.fetchone()
                    access_id = int(access_id[0])
                    sql = 'insert into role_access(role_id,access_id) values("%d","%d");' % (role_id,access_id)
                    cursor.execute(sql)
        db.commit()
        db.close()
        return 0
    except :
        db.close()
        return -1

#上传一份新的数据
def uploaddata(info):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        cursor = db.cursor()
        # #查找用户
        sql = 'select user_id from user where account="%s";' % info["account"]
        cursor.execute(sql)
        user_id = cursor.fetchone()[0]
        print(user_id)
        #插入结果
        sql = 'select result_id from uploader_result'
        num = cursor.execute(sql)
        ids = cursor.fetchall()
        idss = []
        for x in ids:
            idss.append(x[0])
        print(max(idss))
        if num == 0:
            sql = 'insert into uploader_result(user_id,result_id) values(%d,1)' % user_id
            cursor.execute(sql)
            db.commit()
            result_id = 1
        else:
            result_id = int(max(idss))+1
            sql = 'insert into uploader_result(user_id,result_id) values(%d,%d)' % (user_id,result_id)
            cursor.execute(sql)
            db.commit()
        print("结果编号为：%d" % result_id)
        #INSERT
        url = "./cpat/c"+str(result_id)+"/"
        sql = 'insert into result(result_id,deviceid,deviceuserid,starttime,rawdatapng_url,rawdatacsv_url,report_url,filename) values(%d,%d,%d,"%s","%s","%s","%s","%s")' % (result_id, int(info["deviceid"]), int(info["userid"]), info["date"], url, url, url, info["csvfilename"])
        cursor.execute(sql)
        db.commit()    
        db.close()
    except :
        db.close()
        return -2
    try :
        print("开始传输文件了")
        cloudclient.sendsm(str(result_id),info["csvpath"],"./cpat/c"+str(result_id)+"/",info["csvfilename"]+".csv")
        cloudclient.sendsm(str(result_id),info["csvpath"],"./cpat/c"+str(result_id)+"/",info["csvfilename"]+".pdf")
        cloudclient.sendsm(str(result_id),info["csvpath"],"./cpat/c"+str(result_id)+"/",info["csvfilename"]+"_"+"X-axis.png")
        cloudclient.sendsm(str(result_id),info["csvpath"],"./cpat/c"+str(result_id)+"/",info["csvfilename"]+"_"+"Y-axis.png")
        cloudclient.sendsm(str(result_id),info["csvpath"],"./cpat/c"+str(result_id)+"/",info["csvfilename"]+"_"+"Z-axis.png")
        cloudclient.sendsm(str(result_id),info["csvpath"],"./cpat/c"+str(result_id)+"/",info["csvfilename"]+"_"+"combined.png")
        return 0
    except :
        return -1

# 下载文件
def downloadsm(info):
    #result_id  localpath  class(csv,pdf)
    
    if info["class"] == "csv":
        db = pymysql.connect("47.96.227.243","root","root","cpat")
        try :
            cursor = db.cursor()
            sql = 'select rawdatacsv_url,rawdatapng_url,filename from result where result_id=%d;' % info["result_id"]
            cursor.execute(sql)
            t = list(cursor.fetchone())
            csv_url = t[0]
            png_url = t[1]
            fileanme = t[2]
            db.close()
        except:
            db.close()
            return -2
        try :
            cloudclient.getsm(str(info["result_id"]),info["localpath"],csv_url,fileanme+".csv")
            cloudclient.getsm(str(info["result_id"]),info["localpath"],png_url,fileanme+"_"+"X-axis.png")
            cloudclient.getsm(str(info["result_id"]),info["localpath"],png_url,fileanme+"_"+"Y-axis.png")
            cloudclient.getsm(str(info["result_id"]),info["localpath"],png_url,fileanme+"_"+"Z-axis.png")
            return 0
        except:
            return -1

    if info["class"] == "pdf":
        db = pymysql.connect("47.96.227.243","root","root","cpat")
        try :
            cursor = db.cursor()
            sql = 'select report_url,filename from result where result_id=%d;' % info["result_id"]
            cursor.execute(sql)
            t = list(cursor.fetchone())
            rep_url = t[0]
            fileanme = t[1]
            db.close()
        except :
            db.close()
            return -2
        try :
            cloudclient.getsm(str(info["result_id"]),info["localpath"],rep_url,fileanme+".pdf")
            return 0
        except :
            return -2
    

#删除一份数据
def deletedata(result_id):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        cursor = db.cursor()
        sql = 'delete from uploader_result where result_id=%d;' % result_id
        cursor.execute(sql)
        db.commit()
        sql = 'select rawdatapng_url,rawdatacsv_url,report_url,filename from result where result_id=%d' % result_id
        cursor.execute(sql)
        res = cursor.fetchone()
        cloudclient.deletesm(res)
        #通知server删除数据
        sql = 'delete from result where result_id=%s;' % result_id
        cursor.execute(sql)
        db.commit()
        db.close()
        return 0
    except:
        db.close()
        return -1

#查询我的数据
def minedata(user_account):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    cursor = db.cursor()
    try :
        sql = 'select user_id from user where account="%s";' % user_account
        num = cursor.execute(sql)
        if (not num):
            raise Exception("wrong")
        user_id = cursor.fetchone()[0]
        sql = 'select result_id from uploader_result where user_id= %d;' % user_id
        num = cursor.execute(sql)
        resultlist = cursor.fetchall()
        rlist = str(tuple([x[0] for x in resultlist])) if len(resultlist)!=1 else '(' + str(resultlist[0][0]) + ')'
        sql = 'select result_id,deviceid,deviceuserid,starttime from result where result_id in %s;' % rlist
        num = cursor.execute(sql)
        data = cursor.fetchall()
    except :
        db.close()
        return -1,{}
    else :
        db.close()
        return num,data

#按条件查询数据
def conditiondata(info):
    uploader = info["uploader"].split(",")
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    cursor = db.cursor()
    try : 
        if len(uploader) == 1 and uploader[0]=="":
            sql = 'select user_id from user;'
        else :
            ss = str(tuple(uploader)) if len(uploader)!=1 else '('+ '\'' + uploader[0] +'\'' + ')'
            sql = 'select user_id from user where account in %s;' % ss
        num = cursor.execute(sql)
        if(not num):
            raise Exception("NO RESULT!")
        user_id = cursor.fetchall()
        user_id = str(tuple([i[0] for i in user_id ])) if len(user_id)!=1 else '(' + str(user_id[0][0]) + ')'
        sql = 'select result_id from uploader_result where user_id in %s;' % user_id
        num = cursor.execute(sql)
        if(not num):
            raise Exception("NO RESULT!")
        resultlist = cursor.fetchall()
        rlist = str(tuple([x[0] for x in resultlist])) if len(resultlist)!=1 else '(' + str(resultlist[0][0]) + ')'
        sql = 'select a.result_id,c.account,a.deviceid,a.deviceuserid,a.starttime from result a,uploader_result b,user c where c.user_id=b.user_id and b.result_id=a.result_id and a.result_id in %s;' % rlist
        num = cursor.execute(sql)
        print(num)
        if(not num):
            raise Exception("NO RESULT!")
        data = cursor.fetchall()
        startdate = info["startdate"].split(",")
        
        if(not(len(startdate) == 1 and startdate[0]=="")):
            data = tuple([x for x in data if x[4] in startdate])
            print(data)
        if (not len(data)) :
            raise Exception("NO RESULT!")
        userid = info["userid"].split(",")
        if(not(len(userid) == 1 and userid[0]=="")):
            data = tuple([x for x in data if str(x[3]) in userid])
            print(data)
        if (not len(data)) :
            raise Exception("NO RESULT!")
        deviceid = info["deviceid"].split(",")
        if(not(len(deviceid) == 1 and deviceid[0]=="")):
            data = tuple([x for x in data if str(x[2]) in deviceid])
            print(data)
        if (not len(data)) :
            raise Exception("NO RESULT!")
    except :
        db.close()
        return -1,{}
    else :
        print(data)
        db.close()
        num = len(data)
        return num,data

def login_test(info):
    db = pymysql.connect("47.96.227.243","root","root","cpat")
    try :
        cursor = db.cursor()
        sql = 'select account,user_id,email from user where user.account="%s" and user.md5_password="%s";' % (info["name"],info["password"])
        ifsuccess = cursor.execute(sql)
        if ifsuccess == 0 :
            return -1
        else :
            tell = cursor.fetchone()
            print(tell)
            return tell
    except :
        return -2
    finally :
        db.close()



if __name__ == "__main__":
    print("Test")
#     info = {
#         "result_id":1,
#         "class":"pdf",
#         "localpath":"/Users/zhangruilin/Desktop/"
#     }
#     # downloadsm(info)
# #     info = {
# #         'csvfilename': 'datatest2',
# #         'account' : 'zhangrl',
# #         'csvpath': '/Users/zhangruilin/Desktop/test/',
# #         'username': 'Hong',
# #         'userid': '002',
# #         'deviceid': '112',
# #         'ospassword': '102495',
# #         'ifupload': 'on',
# #         'date': '2020/3/31'
# # }
# info2 = {
#     'uploader' : "",
#     'startdate' : "",
#     'userid' : "",
#     'deviceid' : "106"
# }
# print(accessjson(1))

#    num,data = minedata(info["account"])
#    import util
#    asss = util.tojson(data,num,['result_id','deviceid','userid','starttime'])
#    print(asss)

    #insert into result(resultid,deviceid,deviceuserid,starttime,rawdatapng_url,rawdatacsv_url,report_url,filename) values(1,18,24,"2020-03-17","./cpat/c1","./cpat/c1","./cpat/c1","hahahahh")

    