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


var user_dict
var havechanged = 0

const {BrowserWindow} = require('electron').remote
const {dialog} = require('electron').remote
const ipc = require('electron').ipcRenderer

let usersearch = document.querySelector("#search")
let newuser = document.querySelector("#new")
let deleteuser = document.querySelector("#delete")
let changeuser = document.querySelector("#change")
let usertable = document.querySelector("#usertable")
let tbody = document.querySelector("#usertablebody")
let right = document.querySelector("#right")
let lastpage = document.querySelector("#lastpage")
let nextpage = document.querySelector("#nextpage")
let pagestate = document.querySelector("#pagestate")


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
        // var checks = document.getElementsByName("checkRow")
        // console.log(checks.length)
        // len = checks.length
        // for (var j=0;j<len;j++){
        //     checks[i].parentElement.removeChild(checks[i])
        // }
        // var checks = document.getElementsByName("checkRow")
        // console.log(checks.length)
    }
usersearch.onclick =function(){
    cleartable()
    info = {}
    info = JSON.stringify(info)

    thriftClient.getuser(info,(error,res) =>{
        if(error){
            console.error(error)
        }else{
            res = JSON.parse(res)
            user_dict = res
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

            for(var i=0;i<endd;i++)
            {   
                var k = String(i+1)
                var tr = document.createElement("tr")
                tr.style.backgroundColor = "#CCE8EB"
                var td = document.createElement("td")
                td.innerHTML = res [k]["userid"]
                var td2 = document.createElement("td")
                td2.innerHTML = res[k]['account']
                var td3 = document.createElement("td")
                td3.innerHTML = res[k]['date']
                var td4 = document.createElement("td")
                td4.innerHTML = res[k]['email']
                var td5 = document.createElement("td")
                var list = res[k]['roles'].split(',')
                //console.log(list)
                for (var m=0;m<list.length;m++)
                {td5.innerHTML = td5.innerHTML +"  "+ kind[list[m]]}
                //td5.innerHTML = res[k]['roles']
                var td0 = document.createElement("td")
                var checkbox=document.createElement("input");
	            checkbox.type="checkbox";
                checkbox.name="checkRow";
                td0.appendChild(checkbox)

                tr.appendChild(td)
                tr.appendChild(td2)
                tr.appendChild(td3)
                tr.appendChild(td4)
                tr.appendChild(td5)
                tr.appendChild(td0)
                tbody.appendChild(tr)
            }
            console.log(page_num)
            console.log(page_now)
            pagestatechange()
    }
})

}

deleteuser.onclick = function (){
    info = {
        "userid":""
    }
    var checkboxs=document.getElementsByName("checkRow");
		for(var i=0;i<checkboxs.length;i++){
			if(checkboxs[i].checked){
                var n=checkboxs[i].parentNode.parentNode;
                console.log(n.firstChild)
                info["userid"] = info["userid"] + n.firstChild.innerText + ","
			}
        }
    //console.log(info)
}


lastpage.onclick = function(){
    if (page_num==0 || page_num==1 || page_now==1){
        return
    }
    var be = (page_now-2)*10+1
    var en = (page_now-1)*10
    for(var i=be,k=1;i<=en;i++,k++){
        table.rows[k].childNodes[1].innerText = user_dict[i]["user_id"]
        table.rows[k].childNodes[2].innerText = user_dict[i]["account"]
        table.rows[k].childNodes[3].innerText = user_dict[i]["date"]
        table.rows[k].childNodes[4].innerText = user_dict[i]["email"]
        var list = user_dict[i]['roles'].split(',')
        for (var m=0;m<list.length;m++)
            {table.rows[k].childNodes[5].innerText = table.rows[k].childNodes[5].innerText +"  "+ kind[list[m]]}
        
    }
            page_now = page_now -1
            pagestatechange()
}


nextpage.onclick = function(){
    console.log(page_now)
    console.log(page_num)
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


changeuser.onclick = function(){
    info = {}
    info = JSON.stringify(info)
    thriftClient.getroles(info,(error,res) =>{
        if(error){
            console.error(error)
        }else{
            res = JSON.parse(res)
            var num = res["num"]
            if (havechanged!=0){
                info = {
                    "userid":"",
                    "roleid":""
                }
        var checkboxsroles = document.getElementsByName("checklist");
        var checkboxsuser  = document.getElementsByName("checkRow")

        for(var i=0;i<checkboxsuser.length;i++){
			if(checkboxsuser[i].checked){
                var n=checkboxsuser[i].parentNode.parentNode;
                info["userid"] = info["userid"]+n.firstChild.innerText+","

			}
        }
		for(var i=0;i<checkboxsroles.length;i++){
			if(checkboxsroles[i].checked){
                //console.log(kind(res[String(i+1)]["roleid"]))
                info["roleid"] = info["roleid"]+res[String(i+1)]["roleid"]+","
			}
        }
        console.log(info)
    // right.style.display="none"
    // right.style.visibility = "hidden"

            }else{
                
            var div = document.createElement("div");
            div.id = "changee"
            //div.style.display = "inline"
            div.style.wdith = "50px"
            div.style.height = "50px"
            div.style.position = "absolute"
            div.style.top = "170px"
            div.style.right = "50px"
            for (var i=1;i<=num;i++){            
                var checkbox=document.createElement("input");
	            checkbox.type="checkbox";
                checkbox.name="checklist";
                var name = document.createElement("p")
                var roleid = res[String(i)]["roleid"]
                console.log(roleid)
                name.innerText = kind[roleid]
                div.appendChild(checkbox)
                div.appendChild(name)
            }
            div.style.textAlign="left";
            //console.log(div.innerHTML)
            document.body.appendChild(div)
            havechanged = 1 
            }
        }
    })

}


right.onclick = function(){
    info = {}
    ipc.send("access_right"),(e,info) => {

    }
}