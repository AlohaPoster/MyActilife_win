var thrift = require('thrift');
var userService = require('./gen-nodejs/userService.js');
var ttypes = require('./gen-nodejs/test_types.js');
var thriftConnection = thrift.createConnection('127.0.0.1', 8000);
var thriftClient = thrift.createClient(userService,thriftConnection);

thriftConnection.on("error",function(e)
{
    console.log(e);
});

const {BrowserWindow} = require('electron').remote
const ipc = require('electron').ipcRenderer
const path = require('path')
const notification = {
    title:'账户密码错误',
    body:'忘记密码请联系安全管理员或重新申请账号',
    icon: path.join(__dirname, './resources/passwrong.png')
}

let singupwindow
let singinwindow
let name_input = document.querySelector('#nameinput')
let password_input = document.querySelector('#passwordinput')
let login_btn = document.querySelector('#login')
let register_btn = document.querySelector('#registe')

name_input.onclick = function(){
    name_input.style.border = "none"
    password_input.style.border = "none"
}

password_input.onclick = function(){
    name_input.style.border = "2px"
    password_input.style.border = "2px"
}

login_btn.onclick = function(){ 
    var info = {name: name_input.value,
                password: password_input.value
               }
    info = JSON.stringify(info)
    thriftClient.log_test(info,(error,res) =>{
        if(error){
            console.error(error)
        }else{
            console.log(res)
            res = JSON.parse(res)
            if(res["ifsuccess"] == "no"){
                console.log('unsuccess')
                const myNotification = new window.Notification(notification.title,notification)
                myNotification.onclick = () => {
                    console.log('clicked')
                }
                name_input.style.border = "2px solid #B22222"
                password_input.style.border = "2px solid #B22222"
            }
            else {
                ipc.send('login_success',res)
            }
        }
    })
   
}

register_btn.onclick = function(){
ipc.send('add_register_win')
}

