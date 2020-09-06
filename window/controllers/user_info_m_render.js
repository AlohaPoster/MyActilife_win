const {
    ipcRenderer,
    remote
  } = require('electron')
const {session} = require('electron').remote.session

var kind = {
    1:"安全管理员",
    2:"高级科研人员",
    3:"普通科研人员",
    4:"普通用户"
}
let name=document.querySelector("#one")
let mail=document.querySelector("#two")
let userclass=document.querySelector("#three")

ipcRenderer.on('tell_user', (e, message) => {
   console.log(message)
   console.log(message['account'])
   name.textContent = "账号名称：" + message["account"]
   mail.textContent = "邮箱：" + message["email"]
   userclass.textContent = "用户类别：" + kind[message["user_id"]]
  });