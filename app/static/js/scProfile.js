//var baseURL = "http://192.168.0.193:5000/smartCard/profile/"
var XMLHttpRequest = require("xmlhttprequest").XMLHttpRequest;
//document.addEventListener( "DOMContentLoaded", get_json_data, false ); // get_json_data is the function name that will fire on page load
var userName="User's Name";

function getPhoto(url) {
    sString = url.substring(url.lastIndexOf('/')+1);

    photoURL = baseURL + "photo/" + sString;
    window.location = photoURL;
    return sString;
}

function getName(){
    //sString = url.substring(url.lastIndexOf('/')+1);
    baseURL = "http://192.168.0.193:5000/smartCard/profile/"
    sString = "131088"
    profileURL = baseURL + sString;
    var json_obj = JSON.parse(getJsonResponse(profileURL));

/*     var table = document.getElementById("ProfileTable").createCaption();
    table.innerHTML = "<b>" + json_obj.Name + "</b>";  */
    console.log(json_obj);
}
    
function callBackFunc(){
    console.log("User Name frm cbF: " + userName );
}

function test(){
    
    var url = "http://192.168.0.193:5000/smartCard/profile/131088"

    const https = require('http');

    https.get( url, (resp) => {
    let data = '';

    // A chunk of data has been recieved.
    resp.on('data', (chunk) => {
        data += chunk;
    });

    // The whole response has been received. Print out the result.
    resp.on('end', () => {
        jsonData = JSON.parse(data)
        userName = jsonData.Name;
        callBackFunc();
        //document.getElementById("test").innerHTML = "New text!";
    });
    
    }).on("error", (err) => {
    console.log("Error: " + err.message);
    });
}

function getUserName(){
    return userName;
}
function test1(){
    document.getElementById("test").innerHTML = userName;
}

test();
console.log(getUserName());
