/**
 * Name: bootstrap-web-setup.js
 * Purpose: Initialize the Bootstrap-Budget DB and Configurations over Web
 * Author: Blake Phillips (forgineer)
 */
var http = require('http');
var fs = require('fs');
const path = require('path');

http.createServer(function (req, res) {
    // Read the requested file content from file system
    fs.readFile(path.join(__dirname, "/bootstrap-web-setup.html"), function (err, data) {
        if(err) {
            console.log(err);
            // HTTP Status: 404 : NOT FOUND
            // Content Type: text/plain
            res.writeHead(404, {'Content-Type': 'text/html'});
        } else {	
            // Page found	  
            // HTTP Status: 200 : OK
            // Content Type: text/plain
            res.writeHead(200, {'Content-Type': 'text/html'});	

            // Write the content of the file to response body
            res.write(data);		
        }

        // Send the response body 
        res.end();
    });
}).listen(8080);

// Console will print the message
console.log('Navigate to http://localhost:8080/bootstrap-web-setup.html to complete Bootstrap install');