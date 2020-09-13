var fbUtils = require("./firebaseUtils");
var fs = require("fs");
var walk = require("walk");
var path = require('path');

var main = async function() {
	var topDirPath = "../../firebaseFiles";

	walker = walk.walk(topDirPath);

	walker.on("file", function(root, fileStats, next) {
		var docName = fileStats.name.split(".")[0];
		var fileLocation = path.join(root, fileStats.name);

		var collectionName = root.split("/")
		collectionName = collectionName[collectionName.length-1];
		console.log("Arrived at file:", fileLocation, "of collection", collectionName, "and name", docName);

		//Pushing to Firebase
		fbUtils.writeToFirebase(collectionName, docName, fileLocation);

		next();
	});
}

main();