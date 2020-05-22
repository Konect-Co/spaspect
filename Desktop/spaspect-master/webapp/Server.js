var express = require('express');
var app = express();

app.use(express.urlencoded());
app.use(express.json());

/*
Useful Links
- https://expressjs.com/en/api.html#res.render

*/
var server = function(req, res, next) {

}

app.use(server);

var PORT=8000;
app.listen(PORT, function() {
	console.log("Listening on port " + PORT);
});
