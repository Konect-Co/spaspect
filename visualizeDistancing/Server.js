var express = require("express");
var app = express();

app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.get('/index.js', function(req, res) {
    res.sendFile(__dirname + '/index.js');
});

app.get('/styles.css', function(req, res) {
    res.sendFile(__dirname + '/styles.css');
});

app.use('/csvFiles', express.static(__dirname + '/csvFiles'));

var PORT = 3000;
app.listen(PORT, function() {
    console.log("Listening on port " + PORT);
});