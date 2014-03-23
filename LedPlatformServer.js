var sys = require("sys");
var net = require("net");
var url = require("url");
var fs = require("fs");
http = require("http");
var platform = net.createConnection("/tmp/Led_Dance_Platform_Socket");
platform.on("connect", function() {
    console.log("Connected to the raspberry pi");
})
platform.on("error", function(error) {
    console.log(error);
})

http.createServer(function(request,response){
    var parsedUrl = url.parse(request.url, parseQueryString=true);
    var mode = "randsquares";
    response.writeHead(200, {"Content-Type":"text/html"});
    if(parsedUrl.query.mode){
        mode = parsedUrl.query.mode;
        str = 
            "<!DOCTYPE html>"+
            "<html>"+
            "<h3>The mode has been changed!</h3>" +
            "</html>";
        response.write(str);
        platform.write(mode)
    };
    fs.createReadStream("ServerView.html").pipe(response)
    //response.writeHead(200, {"Content-Type":"text/plain"});
    //response.write(mode)
    //response.end();
}).listen(8080, "127.0.0.1"); //run on 0.0.0.0 for real thing
sys.puts("Server Running on port: 8080");

