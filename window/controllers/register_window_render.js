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
 
const path = require('path')
const notification = {
    title:'错误',
    body:'两次密码不一致且不能小于5位',
    icon: path.join(__dirname, '../../resources/passwrong.png')
}
const notification2 = {
    title:'错误',
    body:'用户名长度不小于5位',
    icon: path.join(__dirname, '../../resources/passwrong.png')
}

let name_input = document.querySelector('#nameinput')
let password_first = document.querySelector('#passwordfirst')
let password_second = document.querySelector('#passwordsecond')
let people_choose = document.querySelector('#identity')
let register_btn = document.querySelector('#register')
let help_btn = document.querySelector('#helphere')

help_btn.onclick = function(){
    dialog.showMessageBox({
        type: "info",
        title: "帮助",
        message: "申请“用户”账号直接通过，其余角色请联系安全管理员"
    })
   // dialog.loadURL('www.baidu.com')
}

register_btn.onclick = function(){ 
    console.log(people_choose.value)
    var info = {
                name: name_input.value,
                password1: password_first.value,
                password2: password_second.value,
                role : people_choose.value,
                email : "testmail@qq.com"
               }
    if (info.name.length < 5 || info.name.length >= 15 ){
        const myNotification = new window.Notification(notification2.title,notification2)
        myNotification.onclick = () => {
            console.log('clicked')
        }
        return 
    }
    if (info.password1 != info.password2 || info.password2.length < 5 || info.password2.length >= 12){
        const myNotification = new window.Notification(notification.title,notification)
        myNotification.onclick = () => {
            console.log('clicked')
        }
        return
    }
    
    info = JSON.stringify(info)
   thriftClient.registe(info,(error,res) =>{
        if(error){
            console.error(error)
        }else{
            if(res == '2'){
                dialog.showMessageBox({
                    type: "info",
                    title: "注册失败",
                    message: "用户名重复!"})
            }
            if(res == '1'){    
                dialog.showMessageBox({
                type: "info",
                title: "提示",
                message: "注册成功!"})
            }
            if(res == '-2'){
                dialog.showMessageBox({
                    type: "info",
                    title: "注册失败",
                    message: "特殊角色注册请联系安全管理员!"})
            }
            if(res == '-1'){
                dialog.showMessageBox({
                    type :"info",
                    title: "注册失败",
                    message: "服务器忙或检查您的网络!"})
            }
        }

    })
        
    }



