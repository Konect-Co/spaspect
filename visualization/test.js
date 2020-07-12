var fs = require("fs");
var admin = require('firebase-admin');

admin.initializeApp({
credential: admin.credential.applicationDefault(),
databaseURL: 'https://spaspect-dashboard.firebaseio.com'
});
const db = admin.firestore();
const dbUsers = db.collection('users');
const dbDashboards = db.collection('dashboards');

id = "86176f90-d02c-4a5b-94f7-c6baf24d2f7f"
var content = fs.readFileSync("./VeniceBeach.json");
dbDashboards.doc(id).set(JSON.parse(content));