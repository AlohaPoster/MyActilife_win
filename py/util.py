import numpy as np
import json
from socket import *
#from win32com import client as wc
import os
# result
# +----------------+-------------+------+-----+---------+----------------+
# | Field          | Type        | Null | Key | Default | Extra          |
# +----------------+-------------+------+-----+---------+----------------+
# | result_id      | int(11)     | NO   | PRI | NULL    | auto_increment |
# | deviceid       | int(11)     | NO   |     | NULL    |                |
# | deviceuserid   | int(11)     | NO   |     | NULL    |                |
# | starttime      | varchar(25) | YES  |     | NULL    |                |
# | rawdatapng_url | varchar(50) | YES  |     | NULL    |                |
# | rawdatacsv_url | varchar(50) | YES  |     | NULL    |                |
# | report_url     | varchar(50) | YES  |     | NULL    |                |
# | filename       | varchar(20) | YES  |     | NULL    |                |
# +----------------+-------------+------+-----+---------+----------------+

# uploader_result
# +-----------+---------+------+-----+---------+----------------+
# | Field     | Type    | Null | Key | Default | Extra          |
# +-----------+---------+------+-----+---------+----------------+
# | id        | int(11) | NO   | PRI | NULL    | auto_increment |
# | user_id   | int(11) | NO   |     | NULL    |                |
# | result_id | int(11) | NO   |     | NULL    |                |
# +-----------+---------+------+-----+---------+----------------+

#user
# +---------------+-------------+------+-----+---------+----------------+
# | Field         | Type        | Null | Key | Default | Extra          |
# +---------------+-------------+------+-----+---------+----------------+
# | user_id       | int(11)     | NO   | PRI | NULL    | auto_increment |
# | md5_password  | varchar(12) | NO   |     | NULL    |                |
# | md5_salt      | varchar(12) | NO   |     | NULL    |                |
# | email         | varchar(40) | NO   |     | NULL    |                |
# | register_time | date        | YES  |     | NULL    |                |
# | account       | varchar(15) | YES  |     | NULL    |                |
# +---------------+-------------+------+-----+---------+----------------+

#role
# +-----------+-------------+------+-----+---------+----------------+
# | Field     | Type        | Null | Key | Default | Extra          |
# +-----------+-------------+------+-----+---------+----------------+
# | role_id   | int(11)     | NO   | PRI | NULL    | auto_increment |
# | role_name | varchar(10) | YES  |     | NULL    |                |
# +-----------+-------------+------+-----+---------+----------------+

#access
# +---------------+-------------+------+-----+---------+----------------+
# | Field         | Type        | Null | Key | Default | Extra          |
# +---------------+-------------+------+-----+---------+----------------+
# | access_id     | int(11)     | NO   | PRI | NULL    | auto_increment |
# | restfulverb   | varchar(12) | NO   |     | NULL    |                |
# | restfulobject | varchar(20) | NO   |     | NULL    |                |
# +---------------+-------------+------+-----+---------+----------------+



def tojson(data,num,namelist):
    L = []
    for row in data:
        row = list(row)
        L.append(row)
    jsont = [dict(zip(namelist, d)) for d in L]
    ids = range(1,num+1)
    jsons = {}
    for i in ids:
        jsons[str(i)] = jsont[i-1]
    for key in jsons.keys():
        for nextkey in jsons[key].keys():
            if nextkey == "date":
                jsons[key][nextkey] = jsons[key][nextkey].strftime('%Y-%m-%d')
    jsons["num"] = num
    #print(jsons)
    jsons = json.dumps(jsons)
    return jsons
