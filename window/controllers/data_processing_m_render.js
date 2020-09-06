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
const {dialog} = require('electron').remote
const notification = {
    title:'可能未插入设备',
    body:'可能没有检测到是CPAT设备的存储器',
    icon: path.join(__dirname, '../icon/user.png')
}
let getinfo = document.querySelector("#getinfot")
let searchd = document.querySelector("#searchdevice")
let choosed = document.querySelector("#choosedevice")
let table = document.querySelector("#tad")

let searchd2 = document.querySelector("#searchdevice2")
let gettime = document.querySelector("#searchdevice3")
let retime = document.querySelector("#choosedevice3")
let getpower = document.querySelector("#getpower2")
let table2 = document.querySelector("#tad2")

let p1 = document.querySelector("#img1")
let p2 = document.querySelector("#img2")

var cchoosed1 = 8
var cchoosed2 = 8

changeColorWithTrs('tad',1);
changeColorWithTrs('tad2',2);

function changeColorWithTrs(tabid,name){
   var table1=document.getElementById(tabid);     
   var trs = table1.getElementsByTagName('tr');  
   for( var i=0; i<trs.length; i++ ){  
     trs[i].onmousedown = function(){  
       tronmousedown(this,tabid,name);  
     }  
   }  
}  

function tronmousedown(obj,tabid,name){

   var table1=document.getElementById(tabid);     
   var trs = table1.getElementsByTagName('tr');  
   for( var o=0; o<trs.length; o++ ){  
      if( trs[o] == obj ){  
       trs[o].style.backgroundColor = '#1e7bd9';  
        trs[o].style.border = "2px solid #1e7bd9"
        if(name == 1){
            cchoosed1 = o;
        }else{
            cchoosed2 = o;
        }  
      }else{  
    trs[o].style.border = "1px solid #cad9ea"
       trs[o].style.backgroundColor = '';  
      }  
   }  
} 



searchd.onclick = function(){
   p1.src = "../icon/u10.png"
   thriftClient.getsdreader("1",(error,res) =>{
       if(error){
           console.error(error)
       }else{
           console.log(res)
           res=JSON.parse(res)
           console.log(res['firstusb'].split("(|)"))
           ul1 = res['firstusb'].split(" ")
           ul2 = res['secondusb'].split(" ")
           ul3 = res['thirdusb'].split(" ")
           ul4 = res['fourthusb'].split(" ")
           table.rows[1].childNodes[1].innerText=ul1[0]
           table.rows[1].childNodes[2].innerText="非SD"
           table.rows[1].childNodes[3].innerText=res['firstsize']
           table.rows[2].childNodes[1].innerText=ul2[0]
           table.rows[2].childNodes[2].innerText="非SD"
           table.rows[2].childNodes[3].innerText=res['secondsize']
           table.rows[3].childNodes[1].innerText=ul3[0]
           table.rows[3].childNodes[2].innerText="SD_1"
           table.rows[3].childNodes[3].innerText=res['thirdsize']
        //    table.rows[4].childNodes[1].innerText=ul4[0]
        //    table.rows[4].childNodes[2].innerText=ul4[1]
        //    table.rows[4].childNodes[3].innerText=res['fourthsize']
       }
   })
   
}

choosed.onclick = function(){
    console.log("导入数据进入")
    console.log(cchoosed1)
    console.log(table.rows[cchoosed1].childNodes[1].innerText)
    if (cchoosed1 == 8){
        return 
    }
    var info = {
        "devicepath" : table.rows[cchoosed1].childNodes[1].innerText,
   }
   ipc.send("begin_getdataresult",info)
   /*thriftClient.getdataresult(info,(error,res) =>{
       if(error){
           console.error(error)
       }else{

       }
   })*/
   //ipc.send("over_getdataresult",(e,info) => {})
    
}

searchd2.onclick = function(){
    p2.src = "../icon/u10.png"
}


gettime.onclick = function(){

}

retime.onclick = function(){

}

getpower.onclick = function(){

}