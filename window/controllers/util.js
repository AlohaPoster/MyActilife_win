
function changeColorWithTrs(tabid,choosenum){
       var table1=document.getElementById(tabid);     
       var trs = table1.getElementsByTagName('tr');  
       for( var i=0; i<trs.length; i++ ){  
         trs[i].onmousedown = function(){  
           tronmousedown(this,tabid,choosenum);  
         }  
       }  
    }  
    
    function tronmousedown(obj,tabid,chossenum){
       var table1=document.getElementById(tabid);     
       var trs = table1.getElementsByTagName('tr');  
       for( var o=0; o<trs.length; o++ ){  
          if( trs[o] == obj ){  
           trs[o].style.backgroundColor = '#00CCFF';  
           chossenum = o; 
          }else{  
           trs[o].style.backgroundColor = '';  
          }  
       }  
    } 
