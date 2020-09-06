var thrift = require('thrift');
var userService = require('../../gen-nodejs/userService.js');
var ttypes = require('../../gen-nodejs/test_types.js');
var thriftConnection = thrift.createConnection('127.0.0.1', 8000);
var thriftClient = thrift.createClient(userService,thriftConnection);


thriftConnection.on("error",function(e)
{
    console.log(e);
});

const ipc = require('electron').ipcRenderer
const path = require('path')
const notification = {
    title:'可能未插入设备',
    body:'可能没有检测到是CPAT设备的存储器',
    icon: path.join(__dirname, '../icon/user.png')
}

let imgwait = document.querySelector("#waitimage")
let pdf = document.querySelector("#pdff")
let tip = document.querySelector("#tips")

let messagetemp

ipc.on('getdatafinsh', (e,message) => {
    messagetemp = message
    message = JSON.stringify(message)

    thriftClient.getdataresult(message,(error,res) =>{
        if(error){
            console.error(error)
        }else{
            
            if(res == "1"){
                console.log(res)
                imgwait.src = "../../resources/fininsh.png"
                tip.innerHTML = "导出数据完成，下方展示数据报告"
                pdf.src = "../../pdfjs/web/viewer.html?file="+messagetemp["csvpath"] + messagetemp["csvfilename"] + ".pdf"
            }else{
                return
            }
        }
    })
    if (message["ifupload"]=="on" && message["ifcanupload"]==1){
    //上传数据

    }


})