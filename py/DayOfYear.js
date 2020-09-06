// author : Wang rui



function DayOfYear(d){
    var months = new Array(31,28,31,30,31,30,31,31,30,31)
    if (!IsLeapYear(d.getYear())){
        months[1] = 29
    }
    var sum = 0
    for (var i = 1;i <= d.getMonth()-1;i++){
        sum += months[i-1]
    }
    return sum + d.getDate()
}

function IsLeapYear(y){
    if((y % 4 ==0 ) && (y % 100 != 0) || (y % 400 == 0) ) {
        return true
    } else {
        return false;
    }
}


// SuperClass
function SClass(){
    this.property1 = "2"
    this.property2 = 1
}

// Child Class
function CClass(){
    SClass.call(this)
}

function inherit(){
    CClass.prototype = Object.create(SClass.prototype)
    CClass.prototype.constructor = CClass
    return new CClass()
}

// Test 
var Do = document.querySelector("#Do")
Do.onclick = function(){
    var day = new Date(2000,2,8)
    console.log("We Use Date(2000.2.8)")
    console.log(DayOfYear(day))
}
var In = document.querySelector("#Class")
In.onclick = function(){
    var test = inherit()
    console.log(test instanceof CClass)
    console.log(test instanceof SClass)
}