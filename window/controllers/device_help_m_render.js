

const {ipcRenderer,} = require('electron')
const {dialog}=require('electron').remote

var thrift = require('thrift');
var userService = require('../../gen-nodejs/userService.js');
var ttypes = require('../../gen-nodejs/test_types.js');
var thriftConnection = thrift.createConnection('127.0.0.1', 8000);
var thriftClient = thrift.createClient(userService,thriftConnection);


thriftConnection.on("error",function(e)
{
    console.log(e);
});


   ipcRenderer.on('tell_help', (e, message) => {
    access = message
   });
