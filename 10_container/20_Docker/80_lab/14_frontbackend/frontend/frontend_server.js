var http = require('http');
var vm1_port = 8888
var vm2_ip = 'backend'
var vm2_port = 8889

// Request options
var options = {
   host: vm2_ip, //The address of VM2
   port: vm2_port.toString(), // The port of VM2
   path: ''
};

var body_data;

// Callback function
var callback = function(response){
   var body = '';
   response.on('data', function(data) {
      body += data;
   });

   response.on('end', function() {
    console.log(body);
    body_data = body;
   });
}
// Send Request

var http = require('http');

http.createServer(function (request, response) {
    var req = http.request(options, callback);
    req.end();
    response.writeHead(200, {'Content-Type': 'text/plain'});
    response.end(body_data);
}).listen(vm1_port);

console.log('Frontend Server running ' + vm1_port.toString());
