var fs = require("fs");
var express = require("express");
var app = express();
var admin = require('firebase-admin');

admin.initializeApp({
	credential: admin.credential.applicationDefault(),
	databaseURL: 'https://spaspect-dashboard.firebaseio.com'
});
const db = admin.firestore();
const dbUsers = db.collection('users');
const dbDashboards = db.collection('dashboards');

//TODO: Clean up Express app considering Reg Ex rules for routing

app.get('/', function (req, res){
    res.sendFile(__dirname + '/index.html');
});

app.get('/Pictures/Logo.png', function (req, res){
	res.sendFile(__dirname + '/Pictures/Logo.png');
});

app.get('/index.js', function(req, res){
	res.sendFile(__dirname + '/index.js');
});

app.get('/drawPlots.js', function (req, res){
	res.sendFile(__dirname + '/drawPlots.js');
});

app.get('/styles.css', function (req, res){
	res.sendFile(__dirname + '/styles.css');
});

app.post('/dashboards', function(req, res) {
	var body = "";
	req.on('data', function (chunk) {
		body += chunk;
	});
	req.on('end', function () {
		bodyJSON = JSON.parse(body);
		var idToken = bodyJSON["idtoken"];

		admin.auth().verifyIdToken(idToken).then(function(decodedToken) {
			let uid = decodedToken.uid;

			dbUsers.doc(uid).get().then((doc) => {
				if (doc.exists) {
					var userData = doc.data();
					var accessibleEnvironments = userData["accessibleEnvironments"];

					res.writeHead(200);
					res.write(JSON.stringify(accessibleEnvironments));
					res.end();	
				} else {
					fs.readFile("./demoEnvs.json", function(err, content) {
						if (err) { res.end(); return; }
						console.log("Initializing account of id", uid);
						var userData = JSON.parse(content);
						dbUsers.doc(uid).set(userData);

						res.writeHead(200);
						res.write(JSON.stringify(userData["accessibleEnvironments"]));
						res.end();
					});
				}
			});
		});
	});
});

app.post('/environment', function(req, res) {
	var body = "";
	req.on('data', function (chunk) {
		body += chunk;
	});
	req.on('end', function () {
		bodyJSON = JSON.parse(body);
		var idToken = bodyJSON["idtoken"];
		var dashboard = bodyJSON["dashboard"];
		var lastUpdate = bodyJSON["lastUpdate"];

		admin.auth().verifyIdToken(idToken).then(function(decodedToken) {
			let uid = decodedToken.uid;
			var response = {"authorized":false, "toDate":false, "currentTime":null, "dashboard":null};
			var docPromise = dbUsers.doc(uid).get()
			docPromise.then ((doc) => {
				var userData;
				if (doc.exists) {
					userData = doc.data();
				} else {
					console.log("Initializing account of id", uid);
					dbUsers.doc(uid).set(userData);
					userData = JSON.parse(fs.readFileSync("./demoEnvs.json"));
				}
				var accessibleEnvironments = userData["accessibleEnvironments"];

				var authorized = false;
				Object.keys(accessibleEnvironments).forEach(function (key) {
					if (dashboard == key) {
						authorized = true;
						//TODO: How can we break out of this?
					}
				});
				if (authorized) {
					response["authorized"] = true;
					var dashboardPromise = dbDashboards.doc(dashboard).get();
					dashboardPromise.catch (()=> {
						console.log("Error in obtaining dashboard doc");
					});
					dashboardPromise.then ((doc) => {
						if (doc.exists) {
							var docTime = doc._updateTime._seconds + doc._updateTime._nanoseconds*1e-9;
							response["currentTime"] = docTime;

							if (docTime > lastUpdate) {
								response["toDate"] = false;
								response["dashboard"] = doc.data()["output"];
								console.log("Request for dashboard with id", dashboard);
							} else {
								response["toDate"] = true;
								console.log("Request unupdated for dashboard with id", dashboard);
							}
							res.write(JSON.stringify(response));
							res.end();
						} else {
							response["authorized"] = false;
							res.writeHead(404);
							res.write(JSON.stringify(response));
							res.end();
						}
					});
				} else {
					response["authorized"] = false;
					console.log("Dashboard", dashboard,"NOT AUTHORIZED for user", uid);
					res.writeHead(403);
					res.write(JSON.stringify(response));
					res.end();
				}

			});
		}).catch(function(error) {});
	});
})

var PORT=3000;
app.listen(PORT, function() {
	console.log("Listening on port " + PORT);
});
