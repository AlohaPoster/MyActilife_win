var thrift = require('thrift');
var userService = require('../../gen-nodejs/userService.js');
var ttypes = require('../../gen-nodejs/test_types.js');
var thriftConnection = thrift.createConnection('127.0.0.1', 8000);
var thriftClient = thrift.createClient(userService,thriftConnection);

thriftConnection.on("error",function(e)
{
    console.log(e);
});

const {BrowserWindow} = require('electron').remote
const {dialog} = require('electron').remote
const ipc = require('electron').ipcRenderer

var rolename = document.querySelector("#rolename")
var tbody = document.querySelector("#accessbody")
var returnbu = document.querySelector("#return")
var finishbu = document.querySelector("#finish")
var holdinfo
ipc.on('accesswinfinish', (e, message) => {
    // console.log("事件渐入")
    // console.log(message)
    
    rolename.innerText = "修改" + message["role_name"] + "权限"
    message = JSON.stringify(message)
    thriftClient.getaccessjson(message,(error,res) =>{
        if(error){
            console.log(error)
        }else{
            res = JSON.parse(res)
            console.log(res)
            message = JSON.parse(message)
            message["role_access"] = res
            holdinfo = message
            roleacc = message["role_access"]
            console.log(roleacc)
            for (var verb in roleacc){
                for (var obj in roleacc[verb]){
                    var tr = document.createElement("tr")
                    var td = document.createElement("td")
                    td.innerHTML = verb
                    var td2 = document.createElement("td")
                    td2.innerHTML = obj
                    var td3 = document.createElement("td")
                    var checkbox = document.createElement("input")
                    checkbox.type = "checkbox"
                    checkbox.name = "checkRow"
                if(roleacc[verb][obj]){
                    checkbox.checked = true
                }
                    td3.appendChild(checkbox)
                    tr.appendChild(td)
                    tr.appendChild(td2)
                    tr.appendChild(td3)
                    tbody.appendChild(tr)
                                        }
                                   }
        }
    })

    // roleacc = message["role_access"]
    // for (var verb in roleacc){
    //     for (var obj in roleacc[verb]){
    //         var tr = document.createElement("tr")
    //         var td = document.createElement("td")
    //         td.innerHTML = verb
    //         var td2 = document.createElement("td")
    //         td2.innerHTML = obj
    //         var td3 = document.createElement("td")
    //         var checkbox = document.createElement("input")
    //         checkbox.type = "checkbox"
    //         checkbox.name = "checkRow"
    //         if(roleacc[verb][obj]){
    //             checkbox.checked = true
    //         }
    //         td3.appendChild(checkbox)
    //         tr.appendChild(td)
    //         tr.appendChild(td2)
    //         tr.appendChild(td3)
    //         tbody.appendChild(tr)
    //     }
    // }
   });

returnbu.onclick = function(){
    roleacc = holdinfo["role_access"]
    console.log(roleacc)
    var checkboxs=document.getElementsByName("checkRow");
		for(var i=0;i<checkboxs.length;i++){
   //console.log(checkboxs[i].parentNode.parentNode.firstChild.innerText)
            var verb = checkboxs[i].parentNode.parentNode.firstChild.innerText
            var obj = checkboxs[i].parentNode.parentNode.childNodes[1].innerText
            if (roleacc[verb][obj]){checkboxs[i].checked = true}
            else{checkboxs[i].checked = false}
        }
}

finishbu.onclick = function(){
    info = holdinfo["role_access"]
    var checkboxs=document.getElementsByName("checkRow");
		for(var i=0;i<checkboxs.length;i++){
            var verb = checkboxs[i].parentNode.parentNode.firstChild.innerText
            var obj = checkboxs[i].parentNode.parentNode.childNodes[1].innerText
            if(checkboxs[i].checked){info[verb][obj]=1}
            else{info[verb][obj]=0}
        }
    info = JSON.stringify({"role_id":holdinfo["role_id"],
                            "accessjson":info})
    thriftClient.rolechangeaccess(info,(error,res) => {
        if(error){

        }else{
            if(res == "success"){

            }else{
                
            }
        }
    })
}


