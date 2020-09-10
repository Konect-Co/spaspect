var fbUtils = require("./firebaseUtils");
var args = process.argv.slice(2);
if (args.length != 4) {
	throw new Error("Usage: node " + process.argv[1] + " [read/write] <collectionName> <docName> <fileLocation>");	
}

var mode = args[0];
var collectionName = args[1];
var docName = args[2];
var fileLocation = args[3];
if (mode == "read") {
	console.log("[INFO] reading from firebase collection " + collectionName + ", document name " +
		+ docName + ", and writing output to file location " + fileLocation);
	fbUtils.readFromFirebase(collectionName, docName, fileLocation);
} else if (mode == "write") {
	console.log("[INFO] reading from file location " + fileLocation +
		", and writing output to firebase collection " + collectionName + ", document name " + docName);
	fbUtils.writeToFirebase(collectionName, docName, fileLocation);
}