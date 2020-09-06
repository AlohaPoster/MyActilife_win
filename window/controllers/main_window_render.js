const {
    ipcRenderer,
    remote
  } = require('electron')
var access
//const {session} = require('electron').remote.session
let oneb = document.querySelector("#one")
let twob = document.querySelector("#two")
let threeb = document.querySelector("#three")
let fourb = document.querySelector("#four")
let fiveb = document.querySelector("#five")
let sixb = document.querySelector("#six")


 oneb.onclick = function(){
   ipcRenderer.send('user_info',{})
 }
 twob.onclick =function(){
   ipcRenderer.send('data_processing',{})
 }
 threeb.onclick = function(){
  ipcRenderer.send('data_search',{})
}
fourb.onclick =function(){
  if (access['GET']['userrole'] == 0 || access['GET']['roleaccess'] == 0){
    dialog.showMessageBox({
      type: "info",
      title: "提示",
      message: "您没有操作权限"})
      return
  }
  ipcRenderer.send('access_control',{})
}
fiveb.onclick = function(){
  ipcRenderer.send('device_help',{})
}
sixb.onclick =function(){
  ipcRenderer.send('about_item',{})
}

ipcRenderer.on('tell_main', (e, message) => {
  access = message
 });