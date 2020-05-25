#!/usr/bin/env node
var fs = require('fs');

var express = require('express');
var app = express();

app.use(express.urlencoded());
app.use(express.json());

/*
Useful Links
- https://expressjs.com/en/api.html#res.render

*/


app.get('/', function (req, res){
    res.sendFile(__dirname + '/SpaSpect.html');
});

app.get('/style.css', function (req, res){
	fs.readFile("./style.css", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/css"});
		res.write(content);
		res.end();
	});
});

app.get('/drawPoints.js', function (req, res){
	fs.readFile("./drawPoints.js", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/js"});
		res.write(content);
		res.end();
	});
});

app.get('/points.json', function (req, res){
	fs.readFile("./points.json", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/json"});
		res.write(content);
		res.end();
	});
});


var PORT=8000;
app.listen(PORT, function() {
	console.log("Listening on port " + PORT);
});
