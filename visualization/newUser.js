var admin = require('firebase-admin');
var fs = require("fs");

admin.initializeApp({
	credential: admin.credential.applicationDefault(),
	databaseURL: 'https://spaspect-dashboard.firebaseio.com'
});

const db = admin.firestore();
const dbUsers = db.collection('users');
const dbDashboards = db.collection('dashboards');

var emails = ["ravit@konect-co.com"];

emails.forEach(function (email, index) {
	var pw = "random123";
	admin.auth().createUser({
		email: email,
		password: pw
	})
	.then(function(userRecord) {
		// See the UserRecord reference doc for the contents of userRecord.
		console.log('Successfully created new user:', userRecord.uid);
		const uid = userRecord.uid;
		fs.readFile("./demoEnvs.json", function(err, content) {
			if (err) { res.end(); return; }
			console.log("Initializing account of id", uid);
			var userData = JSON.parse(content);
			dbUsers.doc(uid).set(userData);
		});
		return;
	})
	.catch(function(error) {
		console.log('Error creating new user:', error);
	});
	return;
});