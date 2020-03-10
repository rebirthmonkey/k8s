//backend exposes "Hello world" to port 8889

var http = require('http');

http.createServer(function (request, response) {


    var fs = require("fs");

    var data = fs.readFileSync('input.txt');

    console.log("File Read" + data.toString());
    // Send HTTP header
    // HTTP state value: 200 : OK
    // Content type: text/plain
    response.writeHead(200, {'Content-Type': 'text/plain'});

    // Send response "Hello World"
    response.end(data.toString());
}).listen(8889);

console.log('Backend server running at port 8889');