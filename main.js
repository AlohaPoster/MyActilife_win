/*
主进程: main.js中运行的进程是主进程
渲染进程：通过主，渲染创建的所有BrowserWindow运行的进程
ipcRenderer  &&  ipcMain  &&  remote  进行进程间通信
*/
const {app, BrowserWindow,BrowserView} = require('electron')
const ipc = require('electron').ipcMain
const {dialog} = require('electron')
const path = require('path')
const url = require('url')
var access
var devicepath

  let log_win 
  let register_win
  let main_win
  let main_view
  let getinfo_win
  let report_view
  let access_win
  function createWindow () {

    log_win = new BrowserWindow({
      width: 1200, 
      height: 822, 
      resizable: false,
      //frame: false,
      webPreferences:{
        nodeIntegration:true
      }
      
    })
    log_win.loadFile('index_log.html')

    //log_win.webContents.openDevTools()

    log_win.on('closed', () => {
    log_win = null
    })
  }

  app.on('ready', createWindow)

  app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
  })

  app.on('activate', () => {
    if (win === null) {
      createWindow()
    }
  })

  ipc.on('login_success', (event, message) => {
    main_win = new BrowserWindow({
      width:1200,
      height:800,
      resizable: false,
      webPreferences:{
        nodeIntegration:true,
        webviewTag:true
      }
    })
    access = message
    main_win.loadFile('./window/views/main_window.html')
    main_win.webContents.on('did-finish-load',function(){
      main_win.webContents.send('tell_main',access)
  })
    //main_win.webContents.openDevTools()
    
    main_win.on('closed', () =>{main_win = null})
   
    main_view = new BrowserView({
      webPreferences:{
        nodeIntegration:true
      }
    })
    main_win.setBrowserView(main_view)
    main_view.setBounds({x:180, y:0, width:1020, height:800})
    main_view.webContents.loadFile("./window/views/user_info_m.html")
    //main_view.webContents.openDevTools()
    main_view.webContents.on('did-finish-load',function(){
      main_view.webContents.send('tell_user',access)
  })
  log_win.close()
  })
  
  ipc.on('change_access',(e,info) =>{
    console.log(info)
    access_win = new BrowserWindow({
      width:400,
      height:600,
      resizable: false,
      parent: main_win,
      webPreferences:{
        nodeIntegration:true,
        webviewTag:true
      }
    })
    access_win.webContents.loadFile("./window/views/access_change.html")
    access_win.webContents.openDevTools()
    access_win.webContents.on('did-finish-load',function(){
      access_win.webContents.send('accesswinfinish',info)
  })
    access_win.on('closed', () =>{access_win = null})

  })

  ipc.on('begin_getdataresult',(e,info) => {
    console.log(info)
    devicepath = info["devicepath"]
    getinfo_win = new BrowserWindow({
      width:400,
      height:600,
      resizable: false,
      parent: main_win,
      webPreferences:{
        nodeIntegration:true,
        webviewTag:true
      }
    })
    getinfo_win.webContents.loadFile("./window/views/get_data_info.html")
    getinfo_win.on('closed', () =>{getinfo_win = null})
    //getinfo_win.webContents.openDevTools()
  })

  ipc.on('getdataprocessinfo' ,(e,info) => {
    console.log(info)
    getinfo_win.close()
    info ["ifcanupload"] = 1
    info ["account"] = access["account"]
    info ["devicepath"] = devicepath
    main_view.webContents.loadFile("./window/views/processing_result_m.html")
    main_view.webContents.on('did-finish-load',function(){
      main_view.webContents.send('getdatafinsh',info)
  })
  // main_view.webContents.openDevTools()
  })
  ipc.on('user_info', () => {
    main_view.webContents.loadFile("./window/views/user_info_m.html")
  })

  ipc.on('data_processing', () => {
    main_view.webContents.loadFile("./window/views/data_processing_m.html")
    // main_view.webContents.openDevTools()
  })

  ipc.on('data_search', () => {
    main_view.webContents.loadFile("./window/views/data_search_m.html")
    main_view.webContents.openDevTools()
    main_view.webContents.on('did-finish-load',function(){
      main_view.webContents.send('tell_search',access)
  })
  })

  ipc.on('access_control', () => {
    main_view.webContents.loadFile("./window/views/access_control_m.html")
    main_view.webContents.openDevTools()
  })

  ipc.on('device_help', () => {
    main_view.webContents.loadFile("./window/views/device_help_m.html")
    main_view.webContents.on('did-finish-load',function(){
      main_view.webContents.send('tell_help',access)
  })
  // main_view.webContents.openDevTools()
  })

  ipc.on('about_item', () => {
    main_view.webContents.loadFile("./window/views/about_item_m.html")
  })

  ipc.on('access_right', () => {
    main_view.webContents.loadFile("./window/views/access_control_next_m.html")
    main_view.webContents.openDevTools()
  })

  ipc.on('access_left', () => {
    main_view.webContents.loadFile("./window/views/access_control_m.html")
  })
  
  ipc.on('open_Directory', function(event){
    console.log("打开对话框了")
    filePath = dialog.showOpenDialog({
      properties:['openDirectory']
    },selectedFiles => console.log(selectedFiles),
    // function(files){
    //   dialog.showMessageBox("SDfsdf","dfsd")
    //   if(files){
    //     console.log(files)
    //   event.sender.send('selectDirectory',files)
    //   }
    //   else{
    //     console.log("sddddddd")
    //   }
    // }
    )
    //console.log(filePath[0])
  })

  ipc.on('add_register_win', () => {
    register_win = new BrowserWindow({
      //parent:log_win,
      //modal:true,
      width:600,
      height:772,
      resizable: false,
      parent:log_win,
      webPreferences:{nodeIntegration:true}
    })
    register_win.loadFile('./window/views/register_window.html')

    register_win.webContents.openDevTools()

    register_win.on('closed', () =>{register_win = null})

  })

//promit electron to use python 
let pyProc = null
let pyPort = null


const createPyProc = () => {
  let script = path.join(__dirname, 'py', 'thrift_server.py')
  pyProc = require('child_process').spawn('python', [script])
  if (pyProc != null) {
    console.log('child process success')
  }
}


const exitPyProc = () => {
  pyProc.kill()
  pyProc = null
  pyPort = null
}

app.on('ready', createPyProc)
app.on('will-quit', exitPyProc)