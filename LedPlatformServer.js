var sys = require("sys");
var net = require("net");
var url = require("url");
var fs = require("fs");
//var platform = net.createConnection("/tmp/Led_Dance_Platform_Server");
http = require("http");

http.createServer(function(request,response){
    var parsedUrl = url.parse(request.url, parseQueryString=true);
    var username = "No Name Entered";
    if(parsedUrl.query.userName){
        username = parsedUrl.query.userName;
    }
    response.write("LED Dance Platform Mode Interface\n");
    response.write(username+"\n");
    var page = 
        '<!DOCTYPE html>'+
        '<form>' +
        '<input id=userName name=userName placeholder="enter name" required>'+
        '<button type=submit>Do it!</button>'+
        '</form>'; 
    response.writeHeader(200, {"Content-Type":"text/html"});
    response.end(page);
}).listen(8080, "0.0.0.0");
sys.puts("Server Running on port: 8080");

//platform.on("connect", function() {
  //  sys.puts("Connected to the raspberry pi")
//});

