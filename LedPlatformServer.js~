var sys = require("sys");
var net = require("net");
var url = require("url");
var fs = require("fs");
//var platform = net.createConnection("/tmp/Led_Dance_Platform_Server");
http = require("http");

http.createServer(function(request,response){
    var parsedUrl = url.parse(request.url, parseQueryString=true);
    var mode = "randsquares";
    if(parsedUrl.query.mode){
        mode = parsedUrl.query.mode;
        response.end(mode)
    }
    response.writeHead(200, {"Content-Type":"text/html"});
    fs.createReadStream("ServerView.html").pipe(response)
    response.writeHead(200, {"Content-Type":"text/plain"});
    response.write(mode)
    //response.end();
}).listen(8080, "0.0.0.0");
sys.puts("Server Running on port: 8080");

//platform.on("connect", function() {
  //  sys.puts("Connected to the raspberry pi")
//});

