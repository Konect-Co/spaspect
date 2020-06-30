var fs = require("fs");
var express = require("express");
var app = express();

app.get('/', function (req, res){
    res.sendFile(__dirname + '/index.html');
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

app.get('/test.json', function (req, res){
	fs.readFile("./test.json", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "text/json"});
		res.write(content);
		res.end();
	});
});

app.get('/video.mp4', function (req, res){
	fs.readFile("/home/ravit/Videos/TimesSquare2.mp4", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "video/mp4"});
		res.write(content);
		res.end();
	});
});

app.get('/image.jpg', function (req, res){
	fs.readFile("/home/ravit/Videos/Frame2.jpg", function (err, content) {
		if (err) { res.end(); return; }
		res.writeHeader(200, {"Content-Type": "image/jpg"});
		res.write(content);
		res.end();
	});
});

var PORT=3000;
app.listen(PORT, function() {
	console.log("Listening on port " + PORT);
});
