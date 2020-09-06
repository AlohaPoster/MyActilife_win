var thrift = require('thrift');
var userService = require('../../gen-nodejs/userService.js');
var ttypes = require('../../gen-nodejs/test_types.js');
var thriftConnection = thrift.createConnection('127.0.0.1', 8000);
var thriftClient = thrift.createClient(userService,thriftConnection);

thriftConnection.on("error",function(e)
{
    console.log(e);
});
var kind = {
    1:"安全管理员",
    2:"高级科研人员",
    3:"普通科研人员",
    4:"普通用户"
}
const {BrowserWindow} = require('electron').remote
const {dialog} = require('electron').remote
const ipc = require('electron').ipcRenderer

var have_bind = new Set()
var role_dict
var access_dict

let rolesearch = document.querySelector("#search")
let newrole = document.querySelector("#new")
let deleterole = document.querySelector("#delete")
let changerole = document.querySelector("#change")

let tbody = document.querySelector("#usertablebody")
let right = document.querySelector("#right")
let lastpage = document.querySelector("#lastpage")
let nextpage = document.querySelector("#nextpage")
let pagestate = document.querySelector("#pagestate")
let usertable = document.querySelector("#usertable")

var page_num = 0
var page_now = 0

function pagestatechange(){
    pagestate.innerText = page_now+"/"+page_num+"页"
}

function cleartable(){
    var len = usertable.rows.length
    for(var i =1;i<len;i++){
        usertable.deleteRow(1)
    }
   have_bind.clear()
}

rolesearch.onclick =function(){
    cleartable()
    info = {}
    info = JSON.stringify(info)

    thriftClient.getroles(info,(error,res) =>{
        if(error){
            console.error(error)
        }else{
            res = JSON.parse(res)
            console.log(res)
            role_dict = res
            var num = res["num"]
            var endd
            if (num>10){
                page_num = parseInt(num/10)
                endd = 10;
            }else{
                endd = num;
                page_num = 1
            }
            page_now = 1
            
            for(var i=0;i<num;i++)
            {   
                var k = String(i+1)
                var tr = document.createElement("tr")
                var td = document.createElement("td")
                td.innerHTML = res[k]["roleid"]
                var td2 = document.createElement("td")
                td2.innerHTML = kind[res[k]["roleid"]] + "/" +res[k]["rolename"]
                var td3 = document.createElement("td")
                var bu = document.createElement("button")
                bu.innerText = "查看与修改权限"
                bu.name = "access_look"
                td3.appendChild(bu)
                
                tr.appendChild(td)
                tr.appendChild(td2)
                tr.appendChild(td3)
                tbody.appendChild(tr)
            }
            pagestatechange()
            var accesslook = document.getElementsByName("access_look")
            for(var i =0;i<accesslook.length;i++){
                if(have_bind.has(i)){
                    continue
                }else{
                    accesslook[i].setAttribute("who",i)
                    accesslook[i].addEventListener('click',function(){
                        k = this.getAttribute("who")
                        var accesslook = document.getElementsByName("access_look")
                        var n = accesslook[k].parentNode.parentNode.firstChild.innerText
                        info = {
                            "role_id": n,
                            "role_name": kind[n]
                        }
                        ipc.send('change_access',info)
                        
                    })


                }
            }
            



    }
})
}

deleterole.onclick = function (){
    var checkboxs=document.getElementsByName("checkRow");
		for(var i=0;i<checkboxs.length;i++){
			if(checkboxs[i].checked){
                var n=checkboxs[i].parentNode.parentNode;
                console.log(n.firstChild)
			}
		}
}

right.onclick = function(){
    info = {}
    ipc.send("access_left"),(e,info) => {

    }
}

// 换页有待完善
lastpage.onclick = function(){
    if (page_num==0 || page_num==1 || page_now==1){
        return
    }
    var be = (page_now-2)*10+1
    var en = (page_now-1)*10
    for(var i=be,k=1;i<=en;i++,k++){
        table.rows[k].childNodes[1].innerText = role_dict[i]["role_id"]
        table.rows[k].childNodes[2].innerText = role_dict[i]["account"]
        table.rows[k].childNodes[3].innerText = role_dict[i]["date"]
        
    }
            page_now = page_now -1
            pagestatechange()
}


nextpage.onclick = function(){
    if (page_num==0 || page_num==1 || page_now==page_num){
        return
    }
    var be = page_now*10+1
    var en = (page_now+1)*10
    if (user_dict["num"]<en){
        en = user_dict["num"]
    }
    for(var i=be,k=1;i<=en;i++,k++){
        table.rows[k].childNodes[1].innerText = user_dict[i]["user_id"]
        table.rows[k].childNodes[2].innerText = user_dict[i]["account"]
        table.rows[k].childNodes[3].innerText = user_dict[i]["date"]
        table.rows[k].childNodes[4].innerText = user_dict[i]["email"]
        var list = user_dict[i]['roles'].split(',')
        for (var m=0;m<list.length;m++)
            {table.rows[k].childNodes[5].innerText = table.rows[k].childNodes[5].innerText +"  "+ kind[list[m]]}
        
    }
    page_now = page_now+1
    pagestatechange()
}