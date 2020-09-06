var thrift = require('thrift');
var userService = require('../../gen-nodejs/userService.js');
var ttypes = require('../../gen-nodejs/test_types.js');
var thriftConnection = thrift.createConnection('127.0.0.1', 8000);
var thriftClient = thrift.createClient(userService,thriftConnection);

thriftConnection.on("error",function(e)
{
    console.log(e);
});

const {ipcRenderer} = require('electron')
const {dialog} = require('electron').remote

var access
var result_dict
var pdf_have_bind = new Set()
var csv_have_bind = new Set()
let minebutton = document.querySelector("#mine")
let search = document.querySelector("#search")
let uploader = document.querySelector("#uploader")
let startdate = document.querySelector("#startdate")
let userid = document.querySelector("#userid")
let deviceid = document.querySelector("#deviceid")
let tbody = document.querySelector("#resulttablebody")
let downpath = document.querySelector("#downpath") 
let lastpage = document.querySelector("#lastpage")
let nextpage = document.querySelector("#nextpage")
let pagestate = document.querySelector("#pagestate")
let resulttable = document.querySelector("#resulttable")
let dimg = document.querySelector("#pic")
let dtip = document.querySelector("#pictip")

var page_num = 0
var page_now = 0

function pagestatechange(){
  pagestate.innerText = page_now+"/"+page_num+"页"
}

function cleartable(){
  var len = resulttable.rows.length
  for(var i =1;i<len;i++){
      resulttable.deleteRow(1)
  }
  pdf_have_bind.clear()
  csv_have_bind.clear()
  
}
ipcRenderer.on('tell_search', (e, message) => {
  access = message
 });


  minebutton.onclick = function(){
    cleartable()
    info = {
      "account":access['account']
    }
    info = JSON.stringify(info)

    thriftClient.getmineresult(info,(error,res) => {
      if(error){
        console.error(error)
      }else{
        res = JSON.parse(res)
        for(var key in res){
          if (key=="wrong"){
            dialog.showErrorBox('error', '没有查询到结果或查询错误！');
            return 
          }
        }
        result_dict = res
        var num = res["num"]
        var endd
        if(num > 10){
          page_num = parseInt(num/10)
          endd = 10
        }else{
          endd = num
          page_num = 1
        }
        page_now = 1

        for(var i=0;i<endd;i++){
          var k = String(i+1)
          var tr = document.createElement("tr")
          tr.style.backgroundColor = "#CCE8EB"
          var td = document.createElement("td")
          td.innerHTML = res [k]["result_id"]
          var td2 = document.createElement("td")
          td2.innerHTML = access["account"]
          var td3 = document.createElement("td")
          td3.innerHTML = res[k]['deviceid']
          var td4 = document.createElement("td")
          td4.innerHTML = res[k]['userid']
          var td5 = document.createElement("td")
          td5.innerHTML = res[k]['starttime']

          var td6 = document.createElement("td")
          var download = document.createElement("button")
          download.innerText = "下载原始数据"
          download.name="buttoncsvpng";
          td6.appendChild(download)

          var td7 = document.createElement("td")
          var download = document.createElement("button")
          download.innerText = "下载分析结果"
          download.name="buttonpdf";
          td7.appendChild(download)

          tr.appendChild(td)
          tr.appendChild(td2)
          tr.appendChild(td3)
          tr.appendChild(td4)
          tr.appendChild(td5)
          tr.appendChild(td6)
          tr.appendChild(td7)
          tbody.appendChild(tr)
        }
        pagestatechange()
        var csvdown = document.getElementsByName("buttoncsvpng")
        // console.log("---------------")
        // console.log(csvdown.length)
        for (var i =0;i<csvdown.length;i++){
          if(csv_have_bind.has(i)){
            continue
          }else{
            csvdown[i].setAttribute("who",i)
            csvdown[i].addEventListener('click',function(){
              dimg.src = "../../resources/loading.gif"
              dtip.style.color = "green"
              dtip.innerHTML = "正在下载中..."
              k = this.getAttribute("who")
              var csvdown = document.getElementsByName("buttoncsvpng")
              var n = csvdown[k].parentNode.parentNode
              var p = downpath.value 
              if(p=="")
              {p == "/Users/zhangruilin/Desktop/"}
              info = {
                "result_id" : n.firstChild.innerText,
                "localpath" : p,
                "class" : "csv"
              }
              info = JSON.stringify(info)
              thriftClient.downloadresources(info,(error,res) =>{
                if(error){
                  console.error(error)
                }else{
                  res = JSON.parse(res)
                  if(res=="1")
                  {
                  dimg.src = "../../resources/fininsh.png"
                  dtip.style.color = "red"
                  dtip.innerHTML = "下载成功！"
                }
                }
              })
            })
          }
        }

        var pdfdown = document.getElementsByName("buttonpdf")
        for (var i =0;i<pdfdown.length;i++){
          if(pdf_have_bind.has(i)){
            continue
          }else{
            pdfdown[i].setAttribute("who",i)
            pdfdown[i].addEventListener('click',function(){
              dimg.src = "../../resources/loading.gif"
              dtip.style.color = "green"
              dtip.innerHTML = "正在下载中..."
              k = this.getAttribute("who")
              var pdfdown = document.getElementsByName("buttonpdf")
              var n = pdfdown[k].parentNode.parentNode
              var p = downpath.value 
              console.log(p)
              if(p.length==0)
              {p == "/Users/zhangruilin/Desktop/"}
              info = {
                "result_id" : n.firstChild.innerText,
                "localpath" : p,
                "class" : "pdf"
              }
              info = JSON.stringify(info)
              console.log(info)
              thriftClient.downloadresources(info,(error,res) =>{
                if(error){
                  console.error(error)
                }else{
                  if(res=="1")
                  {
                    dimg.src = "../../resources/fininsh.png"
                    dtip.style.color = "red"
                    dtip.innerHTML = "下载成功！"
                  }
                }
              })
            })
          }
        }




      }
    })

  }

  search.onclick = function(){
    info = {
      "uploader" : uploader.value,
      "startdate": startdate.value,
      "userid" : userid.value,
      "deviceid" : deviceid.value
    }
    info = JSON.stringify(info)
    
    thriftClient.getconditionresult(info,(error,res) =>{
      cleartable()
      if(error){
        console.error(error)
      }else{
        res = JSON.parse(res)
        for(var key in res){
          if (key=="wrong"){
            dialog.showErrorBox('error', '没有查询到结果或查询错误！');
            return 
          }
        }
        result_dict = res
        var num = res["num"]
        var endd
        if(num > 10){
          page_num = parseInt(num/10)
          endd = 10
        }else{
          endd = num
          page_num = 1
        }
        page_now = 1

        for(var i=0;i<endd;i++){
          var k = String(i+1)
          var tr = document.createElement("tr")
          tr.style.backgroundColor = "#CCE8EB"
          var td = document.createElement("td")
          td.innerHTML = res [k]["result_id"]
          var td2 = document.createElement("td")
          td2.innerHTML = res[k]['account']
          var td3 = document.createElement("td")
          td3.innerHTML = res[k]['deviceid']
          var td4 = document.createElement("td")
          td4.innerHTML = res[k]['userid']
          var td5 = document.createElement("td")
          td5.innerHTML = res[k]['starttime']

          var td6 = document.createElement("td")
          var download = document.createElement("button")
          download.innerText = "下载原始数据"
          download.name="buttoncsvpng";
          td6.appendChild(download)

          var td7 = document.createElement("td")
          var download = document.createElement("button")
          download.innerText = "下载分析结果"
          download.name="buttonpdf";
          td7.appendChild(download)

          tr.appendChild(td)
          tr.appendChild(td2)
          tr.appendChild(td3)
          tr.appendChild(td4)
          tr.appendChild(td5)
          tr.appendChild(td6)
          tr.appendChild(td7)
          tbody.appendChild(tr)
        }
        pagestatechange()
        var csvdown = document.getElementsByName("buttoncsvpng")
        for (var i =0;i<csvdown.length;i++){
          if(csv_have_bind.has(i)){
            continue
          }else{
            csvdown[i].setAttribute("who",i)
            csvdown[i].addEventListener('click',function(){
              dimg.src = "../../resources/loading.gif"
              dtip.innerHTML = "正在下载中..."
              k = this.getAttribute("who")
              var csvdown = document.getElementsByName("buttoncsvpng")
              var n = csvdown[k].parentNode.parentNode
              var p = downpath.value 
              if(p=="")
              {p == "/"}
              info = {
                "result_id" : n.firstChild.innerText,
                "localpath" : p,
                "class" : "csv"
              }
              info = JSON.stringify(info)
              thriftClient.downloadresources(info,(error,res) =>{
                if(error){
                  console.error(error)
                }else{
                  res = JSON.parse(res)
                  if(res=="1")
                  {
                    dimg.src = "../../resources/fininsh.png"
                    dtip.innerHTML = "下载成功！"
                  }
                }
              })
            })
          }
        }

        var pdfdown = document.getElementsByName("buttonpdf")
        for (var i =0;i<pdfdown.length;i++){
          if(pdf_have_bind.has(i)){
            continue
          }else{
            pdfdown[i].setAttribute("who",i)
            pdfdown[i].addEventListener('click',function(){
              dimg.src = "../../resources/loading.gif"
              dtip.innerHTML = "正在下载中..."
              k = this.getAttribute("who")
              var pdfdown = document.getElementsByName("buttonpdf")
              var n = pdfdown[k].parentNode.parentNode
              var p = downpath.value 
              if(p=="")
              {p == "/"}
              info = {
                "result_id" : n.firstChild.innerText,
                "localpath" : p,
                "class" : "pdf"
              }
              info = JSON.stringify(info)
              thriftClient.downloadresources(info,(error,res) =>{
                if(error){
                  console.error(error)
                }else{
                  res = JSON.parse(res)
                  if(res=="1")
                  {
                    dimg.src = "../../resources/fininsh.png"
                    dtip.innerHTML = "下载成功！"
                  }
                }
              })
            })
          }
        }


      }
    })
  }

//下载按钮时间群

ipcRenderer.on('tell_search', (e, message) => {
  access = message
 });

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
      table.rows[k].childNodes[1].innerText = user_dict[i]["result_id"]
      table.rows[k].childNodes[2].innerText = user_dict[i]["uploader"]
      table.rows[k].childNodes[3].innerText = user_dict[i]["deviceid"]
      table.rows[k].childNodes[4].innerText = user_dict[i]["userid"]
      table.rows[k].childNodes[5].innerText = user_dict[i]["uploadedate"]
      
      
  }
  page_now = page_now+1
  //pagestatechange()
}

lastpage.onclick = function(){
  if (page_num==0 || page_num==1 || page_now==1){
      return
  }
  var be = (page_now-2)*10+1
  var en = (page_now-1)*10
  for(var i=be,k=1;i<=en;i++,k++){
    table.rows[k].childNodes[1].innerText = user_dict[i]["result_id"]
    table.rows[k].childNodes[2].innerText = user_dict[i]["uploader"]
    table.rows[k].childNodes[3].innerText = user_dict[i]["deviceid"]
    table.rows[k].childNodes[4].innerText = user_dict[i]["userid"]
    table.rows[k].childNodes[5].innerText = user_dict[i]["uploadedate"]
      
  }
          page_now = page_now -1
          //pagestatechange()
}