var fs = require("fs");
var admin = require('firebase-admin');

admin.initializeApp({
	credential: admin.credential.applicationDefault(),
	databaseURL: 'https://spaspect-dashboard.firebaseio.com'
});
const db = admin.firestore();
const dbUsers = db.collection('users');
const dbDashboards = db.collection('dashboards');

id = "0443639c-bfc1-11ea-b3de-0242ac130004"
/*dbDashboards.doc(id).get().then((doc) => {
	if (doc.exists) {
		var dashboardData = doc.data();

		console.log(dashboardData);	
	}
});*/

var content = fs.readFileSync("/home/ravit/Konect-Code/spaspect-project/spaspect/visualization/output/" + id + ".json");
dbDashboards.doc(id).set(JSON.parse(content));