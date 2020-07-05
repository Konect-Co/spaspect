var fs = require("fs");
var express = require("express");
var app = express();

//TODO: Clean up Express app considering Reg Ex rules for routing

app.get('/', function (req, res){
    res.sendFile(__dirname + '/index.html');
});

app.get('/index.js', function(req, res){
	fs.readFile("./index.js", function(err, content) {
		if (err) { res.end(); return;}
		res.writeHeader(200, {"Content-Type": "text/js"});
		res.write(content);
		res.end();
	});
});

app.get('/drawPlots.js', function (req, res){
	fs.readFile("./drawPlots.js", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/js"});
		res.write(content);
		res.end();
	});
});

app.get('/styles.css', function (req, res){
	fs.readFile("./styles.css", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/css"});
		res.write(content);
		res.end();
	});
});

app.get('/config/*', function(req, res) {
	var outputFile = req["params"]["0"];
	fs.readFile("./config/" + outputFile, function(err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/json"});
		res.write(content);
		res.end();
	});
});

app.get('/output/*', function(req, res) {
	var outputFile = req["params"]["0"];
	fs.readFile("./output/" + outputFile, function(err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/json"});
		res.write(content);
		res.end();
	});
});

app.get('/video/*', function(req, res) {
	var videoFile = req["params"]["0"];
	fs.readFile("./video/" + videoFile, function(err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "video/mp4"});
		res.write(content);
		res.end();
	});
});

var PORT=3000;
app.listen(PORT, function() {
	console.log("Listening on port " + PORT);
});
