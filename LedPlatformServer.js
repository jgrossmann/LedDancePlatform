var sys = require("sys");
var net = require("net");
var url = require("url");
var fs = require("fs");
http = require("http");
//default password that will most likely change on startup
var password = "thetachi";
var users = [];
var platform = net.createConnection("/tmp/Led_Dance_Platform_Socket");
platform.on("connect", function() {
    console.log("Connected to the raspberry pi");
})
platform.on("error", function(error) {
    console.log(error);
})
platform.on("data", function(data) {
    password = data.toString();
    sys.puts("Server password is: "+password);
})

http.createServer(function(request,response){
    var parsedUrl = url.parse(request.url, parseQueryString=true);
    var authenticated = false;
    var connectAddr = request.connection.remoteAddress;
    for (var i=0; i<users.length; i++){
        if(connectAddr === users[i]){
            authenticated = true;
        };
    };
    if(authenticated == false){
        if(parsedUrl.query.password){
            if(parsedUrl.query.password == password){
                users.push(request.connection.remoteAddress);
            };
            response.writeHead(301,{Location: "http://"+request.connection.localAddress+":"+request.connection.address().port});
            response.end();
        };
        
        if(parsedUrl.query.mode){
            response.writeHead(301,{Location: "http://"+request.connection.localAddress+":"+request.connection.address().port});
            response.end();
        };         
        fs.createReadStream("ServerAuthenticate.html").pipe(response);
     
    }else{
        if(parsedUrl.query.kill){
            sys.puts("kill call from Server by addr: "+connectAddr);
            platform.write("kill");
        };
        var mode = "randsquares";
        response.writeHead(200, {"Content-Type":"text/html"});
        if(parsedUrl.query.mode){
            mode = parsedUrl.query.mode;
            if(mode == "textdisplay"){
                if(parsedUrl.query.text){
                    text = parsedUrl.query.text;
                    mode = mode+" text="+"'"+text+"'";
                };
            };
            if(mode == "solidcolor"){
                if(parsedUrl.query.r && parsedUrl.query.g && parsedUrl.query.b){
                    rgb = "'("+parsedUrl.query.r+","+parsedUrl.query.g+","+parsedUrl.query.b+")'";       
                    mode = mode+" colorrgb="+rgb;
                };
            };
            sys.puts(mode);
            platform.write(mode)
            response.writeHead(301,
                {Location: "http://"+request.connection.localAddress+":"+request.connection.address().port});
            response.end();
        };
        fs.createReadStream("ServerView.html").pipe(response);
        //response.writeHead(200, {"Content-Type":"text/plain"});
        //response.write(mode)
        //response.end();
    };
}).listen(8080, "127.0.0.1"); //run on 0.0.0.0 for real thing
sys.puts("Server Running on port: 8080");

