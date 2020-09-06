let inputcsvfilename = document.querySelector("#csvfilename")
let inputcsvpath = document.querySelector("#csvpath")
let inputusername = document.querySelector("#username")
let inputuserid = document.querySelector("#userid")
let inputdeviceid = document.querySelector("#deviceid")
let inputpassword = document.querySelector("#password")
let ifupload = document.querySelector("#ifupload")

let yesbutton = document.querySelector("#yes")
const ipc = require('electron').ipcRenderer

yesbutton.onclick = function(){
    var myDate = new Date()
    mydate = myDate.toLocaleDateString()
    console.log(mydate)
    info = {
        "csvfilename" : inputcsvfilename.value,
        "csvpath" : inputcsvpath.value,
        "username" : inputusername.value,
        "userid" : inputuserid.value,
        "deviceid" : inputdeviceid.value,
        "ospassword" : inputpassword.value,
        "ifupload" : ifupload.value,
        "date" : mydate
    }
    ipc.send("getdataprocessinfo",info)
}