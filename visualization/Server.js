var fs = require("fs");
var express = require("express");
var app = express();
var admin = require('firebase-admin');
var formidable = require('formidable');
const { v4: uuidv4 } = require('uuid');

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
					console.log("Request for dashboard with id", dashboard);
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
								response["dashboard"] = doc.data();
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
					console.log("Dashboard", dashboard, "NOT AUTHORIZED for user", uid);
					res.writeHead(403);
					res.write(JSON.stringify(response));
					res.end();
				}

			});
		}).catch(function(error) {});
	});
});

app.post('/newSite', function(req, res) {
	var response = {"success":false, "error":null};

	var form = new formidable.IncomingForm();
	form.parse(req);

	var formData = {};

	form.on("error", (err) => {
		res.writeHead(400);
		response["error"] = err;
		res.write(JSON.stringify(response));
		res.end();
		console.log("Error in receiving newSite form", err);
		return;
	});

	form.on('field', (fieldName, fieldValue) => {
		formData[fieldName] = fieldValue;
	});

	form.on('end', function (name, file) {
		var error = null;

		var token = formData["user-token"];
		var siteName = formData["name"];
		var streamLink = formData["stream-link"]
		var lat_vals = formData["lat_vals"];
		var lon_vals = formData["lon_vals"];
		var lonlat_origin = formData["lonlat_origin"];
		var pixelX_vals = formData["pixelX_vals"];
		var pixelY_vals = formData["pixelY_vals"];

		var docUUID = uuidv4();

		admin.auth().verifyIdToken(token).then(function(decodedToken) {
			dbDashboards.doc(docUUID).set({
				"name":siteName,
				"streamlink":streamLink,
				"calibration":{
					"lat-vals":JSON.parse(lat_vals),
					"lon-vals":JSON.parse(lon_vals),
					"lonlat_origin":JSON.parse(lonlat_origin),
					"pixelX_vals":JSON.parse(pixelX_vals),
					"pixelY_vals":JSON.parse(pixelY_vals)
				}
			})
			var userDoc = dbUsers.doc(decodedToken.uid);
			var userDocData = userDoc.get();
			userDocData.catch((err) => {
				res.writeHead(500);
				response["error"] = err;
				res.write(JSON.stringify(response));
				res.end();
				console.log("Error in reading user document", err);
				return;
			});
			userDocData.then((doc) => {
				if (doc.exists) {
					//TODO: Make functions to add environment, change value, etc
					var docData = doc.data();
					docData["accessibleEnvironments"][docUUID] = siteName;
					userDoc.set(docData);

					response["success"] = true
					res.writeHead(200);
					res.write(JSON.stringify(response));
					res.end();
					return;
				}
			});
		});
	});
});

var PORT=3000;
app.listen(PORT, function() {
	console.log("Listening on port " + PORT);
});
