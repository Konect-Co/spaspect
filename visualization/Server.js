var fs = require("fs");
var path = require("path");

var express = require("express");
var app = express();
var admin = require('firebase-admin');
var formidable = require('formidable');
//var refreshToken;
const { v4: uuidv4 } = require('uuid');

admin.initializeApp({
    databaseURL: 'https://spaspect-dashboard.firebaseio.com',
    credential: admin.credential.cert({
        project_id: 'spaspect-dashboard',
		private_key: "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/Iumm0cHkDSFP\nmHl6oJGwITuja2d++M8ATsUD8Byj0+8flP2Up6LItTy+u+pI9q1meXufg3WQmPzC\ndvkLYklQmOA86ItCcLXGtQCVuSTNC75scMuAFW2PJQBibhYfC5tZ3zc5Aa/23fn1\n4YbtAqZ7IZrmIcTLCohqZq1vGMPanEP/b4uaU2rFPNZ134PUhk94tPcrYpqeaZJG\neSEhnFN9IrJrzRea0DRnSs0nhojw+L4+6NtN3DJCjSsuTWAnrlJHCPucpBdh3uMO\nuM0tVZPpx1OF6LRPUMG8nPAiovr7Bpv/zOOb2Et9ZY2+6sM9Q82MrMXDjCthtiTR\nuoqIQjArAgMBAAECggEABnYgLvcFVnfJKf8uECKweiNNeFNPrt+rY8fF6kGqPjGS\ncl9fiTB3lNBnqs0AeRH5v66YqsZPaaF6XfqWpbdfYh2g6v4zgv37bym8SNN29oWQ\nnOrdPkm7J+0oy6sMDWWfjVS58a/oanCLnC/RF18RELWMnn4CwJhtDyfEci6EpHW3\n8AU/u62aN7lNShcod+hzwKwZPxrEBVbKQRBOW6QdYWuwT4LOMkjslpL1VUmwl4n7\nj8ZawmsS/WKxidPhVH/6E1rB2RB0TqG2rxPhDHeq7yMW8pc4hAgk6R9+In6SlYce\nyfqV+NX2DCRvND2jFEnvIeh5sGK5DU1XlucjYIr3sQKBgQDnkai2qtz+i3IQvqYv\nXhNyPKgIpxDJQv7Jk0l01LMpLMOYnLQIMqbzmYpxChz9GAQqCG4k95r0uP7fJanU\nSAZKNoi6u4U/+yfKc0zCoOuNT07ho4jWjUVnxwsS4Tbmhr1V8iouGIHS8vQO5Bgv\npLdY1cMgjenJrMNXnbJ2xdOPkQKBgQDTTTpaHVrRhmYvVyaL3G4qdw5FGQfLOIsC\n9C0GQwjSx/UOsXIuxKUFeB+y7AMgIP3tRZF4t66tKa+zGfsOkvQrf/fEG0PGO3CE\nRABkZ+7rTGn9yz6/vmLUPNE2onW4Hln94ZFh3T44DVzyCZSprKcZZA0bmyeeFB2g\nDYb52wEd+wKBgB2jYviePdLGfj7uZ87AN7TzVn5lA5z+2iVqmIg/gP7QH+i0hcZW\n1U9wY2u8Y6FxJXdLxO0uU8LmuphM9cOZxFRTToS344Ig3yLmRvjSJ9PaRrpSd/0d\n77gsnZo5ARHYRPtvFz73HAan2dzeDMpsRps0INlV0Ipjdk0Mff79qupBAoGAYiFn\njBo95zinlCzBNgr1Druj4Osy92oXBRQpJNNU8a7zXBOEl7uzd8rFze5VtUIdK2g3\nmvyTHtBRTLgwJCCTTPBtPKH8478PDh4WoIq0JoqiXr9ZMOtWMoLcFqd0TEGsQX/U\naMK69oUeOTnB1Nrd76jLfZqc14k4CPC/UqIm7qkCgYBMcLiFFgKTmFqr1I7D78jh\nd6dbfVDYwsD1uMXtHJuf/Vb1F/5ZBsh6EJzd0+R6BvqEZ812/lUQcH60WjW8ANy8\nskKFVyrWCwSesUUfGV4391pFgT3DrHkgLstBg+Py/gWwZTLEjwcEL+J+0A1nybF3\nHCuJyDNXFafsCO9cdPehIg==\n-----END PRIVATE KEY-----\n",
        client_email: "firebase-adminsdk-bip9h@spaspect-dashboard.iam.gserviceaccount.com"
    })
});
const db = admin.firestore();
const dbUsers = db.collection('users');
const dbDashboards = db.collection('dashboards');
const dbAggregate = db.collection('aggregate');
const dbRealtime = db.collection('realtime');

const firebaseFilesDir = path.join(path.dirname(__dirname), "firebaseFiles");

// Utils Functions

/*
Checks whether specified dashboard is demo dashboard, and calls callback if so.
*/
function isDemoDashboard(dashboard, callback) {
    //reading demoEnvs.json to see whether provided dashboard is a demo dashboard or not
    fs.readFile("./demoEnvs.json", function(err, content) {
        if (err) { return; }
        var authorized = false;
        var userData = JSON.parse(content);
        Object.keys(userData["accessibleEnvironments"]).forEach(function(key) {
            if (dashboard == key) {
                authorized = true;
                //TODO: How can we break out of this?
            }
        });
        if (authorized)
            callback();
    });
}

//TODO: Clean up Express app considering Reg Ex rules for routing
// Express Functions
app.get('/', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.get('/index.html', function(req, res) {
    res.sendFile(__dirname + '/index.html');
});

app.get('/contactus.html', function(req, res) {
    res.sendFile(__dirname + '/contactus.html');
});

app.get('/signup.html', function(req, res) {
    res.sendFile(__dirname + '/signup.html');
});

app.get('/Pictures/Logo.png', function(req, res) {
    res.sendFile(__dirname + '/Pictures/Logo.png');
});

app.get('/index.js', function(req, res) {
    res.sendFile(__dirname + '/index.js');
});

app.get('/drawPlotsRealtime.js', function(req, res) {
    res.sendFile(__dirname + '/DrawPlots/drawPlotsRealtime.js');
});

app.get('/drawPlotsAggregate.js', function(req, res) {
    res.sendFile(__dirname + '/DrawPlots/drawPlotsAggregate.js');
});

app.get('/css/styles.css', function(req, res) {
    res.sendFile(__dirname + '/css/styles.css');
});

app.use('/node_modules', express.static(__dirname + '/node_modules'));

//POST request to get list of dashboards corresponding to the current user
app.post('/dashboards', function(req, res) {
    //Taking in the body of the request
    var body = "";
    req.on('data', function(chunk) {
        body += chunk;
    });
    req.on('end', function() {
        //Taking arguments from /dashboards POST request
        bodyJSON = JSON.parse(body);
        if (!("idtoken" in bodyJSON))
            res.end();
        var idToken = bodyJSON["idtoken"];

        //If user id is not specified (i.e. logged out), return values in demoEnvs.json
        if (idToken == null) {
            fs.readFile("./demoEnvs.json", function(err, content) {
                if (err) { res.end(); return; }
                var userData = JSON.parse(content);

                res.writeHead(200);
                res.write(JSON.stringify(userData["accessibleEnvironments"]));
                res.end();
            });
            return;
        }

        //verfiying given idToken first
        admin.auth().verifyIdToken(idToken).then(function(decodedToken) {
            //reading uid of current user
            let uid = decodedToken.uid;
            var fileName = path.join(firebaseFilesDir, "users", uid) + ".json";

            //reading user doc from Firebase
            //dbUsers.doc(uid).get().then((doc) => {
            fs.readFile(fileName, 'utf8', (err, data) => {
                //if doc exists, return the accessible environments
                if (!err) {
                    //var userData = doc.data();
                    var userData = JSON.parse(data);
                    var accessibleEnvironments = userData["accessibleEnvironments"];

                    res.writeHead(200);
                    res.write(JSON.stringify(accessibleEnvironments));
                    res.end();
                }
                //otherwise, read from demoEnvs.json and return demo dashboards
                else {
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

app.post('/realtimeData', function(req, res) {
    // Use dbRealtime to get the appropriate dashboard and return the result
    var body = "";
    req.on('data', function(chunk) {
        body += chunk;
    });
    req.on('end', function() {
        //Taking arguments from /dashboards POST request
        bodyJSON = JSON.parse(body);
        if (!("idtoken" in bodyJSON && "dashboardId" in bodyJSON))
            res.end();
        var idToken = bodyJSON["idtoken"];
        var dashboardId = bodyJSON["dashboardId"];

        if (!idToken) {
            res.writeHead(400);
            res.end();
            return;
        }

        //verfiying given idToken first
        admin.auth().verifyIdToken(idToken).then(function(decodedToken) {
            //reading uid of current user
            let uid = decodedToken.uid;

            //TODO: Check whether specified user is allowed to access

            var fileName = path.join(firebaseFilesDir, "realtime", dashboardId) + ".json";

            //reading user doc from Firebase
            fs.readFile(fileName, 'utf8', (err, data) => {
                //if doc exists, return the accessible environments
                if (!err) {
                    var userData = JSON.parse(data);

                    res.writeHead(200);
                    res.write(JSON.stringify(userData));
                    res.end();
                }
                //otherwise, read from demoEnvs.json and return demo dashboards
                else {
                    res.writeHead(400);
                    res.end();
                }
            });
        });
    });
});

app.post('/aggregateData', function(req, res) {
    // Use dbAggregate to get the appropriate dashboard and return the result
    var body = "";
    req.on('data', function(chunk) {
        body += chunk;
    });
    req.on('end', function() {
        //Taking arguments from /dashboards POST request
        bodyJSON = JSON.parse(body);
        if (!("idtoken" in bodyJSON))
            res.end();
        var idToken = bodyJSON["idtoken"];

        //verfiying given idToken first
        admin.auth().verifyIdToken(idToken).then(function(decodedToken) {
            //reading uid of current user
            let uid = decodedToken.uid;

            var fileName = path.join(firebaseFilesDir, "users", uid) + ".json";

            //reading user doc from Firebase
            fs.readFile(fileName, 'utf8', (err, data) => {
                //if doc exists, return the accessible environments
                if (!err) {
                    var userData = JSON.parse(data);
                    var accessibleEnvironments = Object.keys(userData["accessibleEnvironments"]);

                    var aggData = {"availableDashboards":userData["accessibleEnvironments"]};

                    var callbackComplete = {};
                    for (var i = 0; i < accessibleEnvironments.length; i++) {
                        callbackComplete[accessibleEnvironments[i]] = false;
                    }

                    accessibleEnvironments.forEach(ID => {
                        var aggFileName = path.join(firebaseFilesDir, "aggregate", ID) + ".json";
                        fs.readFile(aggFileName, 'utf8', (err, aggFileData) => {
                            if(!err){
                                var aggDocData = JSON.parse(aggFileData);
                                aggData[ID] = aggDocData;
                            }
                            callbackComplete[ID] = true;

                            //wait for callback to be complete
                            //TODO: If taking too long, just return error code in header
                            var complete = true;
                            
                            accessibleEnvironments.forEach(ID => {
                                complete &= callbackComplete[ID];
                                //TODO: Break if complete is false
                                //  Problem is idk how to break out of foreach
                            });
                            
                            if (complete) {
                                res.writeHead(200);
                                res.write(JSON.stringify(aggData));
                                res.end();
                            }
                        });
                    });
                }
                //otherwise, read from demoEnvs.json and return demo dashboards
                else {
                    console.log("user doesn't exist");
                    res.writeHead(400);
                    res.end();
                }
            });
        });
    });
});

/*//POST request to add a new site
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
});*/

var PORT = 3000;
app.listen(PORT, function() {
    console.log("Listening on port " + PORT);
});