var admin = require('firebase-admin');

admin.initializeApp({
    databaseURL: 'https://spaspect-dashboard.firebaseio.com',
    credential: admin.credential.cert({
        project_id: 'spaspect-dashboard',
		private_key: "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC/Iumm0cHkDSFP\nmHl6oJGwITuja2d++M8ATsUD8Byj0+8flP2Up6LItTy+u+pI9q1meXufg3WQmPzC\ndvkLYklQmOA86ItCcLXGtQCVuSTNC75scMuAFW2PJQBibhYfC5tZ3zc5Aa/23fn1\n4YbtAqZ7IZrmIcTLCohqZq1vGMPanEP/b4uaU2rFPNZ134PUhk94tPcrYpqeaZJG\neSEhnFN9IrJrzRea0DRnSs0nhojw+L4+6NtN3DJCjSsuTWAnrlJHCPucpBdh3uMO\nuM0tVZPpx1OF6LRPUMG8nPAiovr7Bpv/zOOb2Et9ZY2+6sM9Q82MrMXDjCthtiTR\nuoqIQjArAgMBAAECggEABnYgLvcFVnfJKf8uECKweiNNeFNPrt+rY8fF6kGqPjGS\ncl9fiTB3lNBnqs0AeRH5v66YqsZPaaF6XfqWpbdfYh2g6v4zgv37bym8SNN29oWQ\nnOrdPkm7J+0oy6sMDWWfjVS58a/oanCLnC/RF18RELWMnn4CwJhtDyfEci6EpHW3\n8AU/u62aN7lNShcod+hzwKwZPxrEBVbKQRBOW6QdYWuwT4LOMkjslpL1VUmwl4n7\nj8ZawmsS/WKxidPhVH/6E1rB2RB0TqG2rxPhDHeq7yMW8pc4hAgk6R9+In6SlYce\nyfqV+NX2DCRvND2jFEnvIeh5sGK5DU1XlucjYIr3sQKBgQDnkai2qtz+i3IQvqYv\nXhNyPKgIpxDJQv7Jk0l01LMpLMOYnLQIMqbzmYpxChz9GAQqCG4k95r0uP7fJanU\nSAZKNoi6u4U/+yfKc0zCoOuNT07ho4jWjUVnxwsS4Tbmhr1V8iouGIHS8vQO5Bgv\npLdY1cMgjenJrMNXnbJ2xdOPkQKBgQDTTTpaHVrRhmYvVyaL3G4qdw5FGQfLOIsC\n9C0GQwjSx/UOsXIuxKUFeB+y7AMgIP3tRZF4t66tKa+zGfsOkvQrf/fEG0PGO3CE\nRABkZ+7rTGn9yz6/vmLUPNE2onW4Hln94ZFh3T44DVzyCZSprKcZZA0bmyeeFB2g\nDYb52wEd+wKBgB2jYviePdLGfj7uZ87AN7TzVn5lA5z+2iVqmIg/gP7QH+i0hcZW\n1U9wY2u8Y6FxJXdLxO0uU8LmuphM9cOZxFRTToS344Ig3yLmRvjSJ9PaRrpSd/0d\n77gsnZo5ARHYRPtvFz73HAan2dzeDMpsRps0INlV0Ipjdk0Mff79qupBAoGAYiFn\njBo95zinlCzBNgr1Druj4Osy92oXBRQpJNNU8a7zXBOEl7uzd8rFze5VtUIdK2g3\nmvyTHtBRTLgwJCCTTPBtPKH8478PDh4WoIq0JoqiXr9ZMOtWMoLcFqd0TEGsQX/U\naMK69oUeOTnB1Nrd76jLfZqc14k4CPC/UqIm7qkCgYBMcLiFFgKTmFqr1I7D78jh\nd6dbfVDYwsD1uMXtHJuf/Vb1F/5ZBsh6EJzd0+R6BvqEZ812/lUQcH60WjW8ANy8\nskKFVyrWCwSesUUfGV4391pFgT3DrHkgLstBg+Py/gWwZTLEjwcEL+J+0A1nybF3\nHCuJyDNXFafsCO9cdPehIg==\n-----END PRIVATE KEY-----\n",
        client_email: "firebase-adminsdk-bip9h@spaspect-dashboard.iam.gserviceaccount.com"
    })
});
const db = admin.firestore();

var fs = require("fs");

var path = require('path');

var main = async function() {
	var collections = ["users", "aggregate", "calibrations", "realtime"]
	var topDirPath = "../../firebaseFiles/";

	for (var i = 0; i < collections.length; i++) {
		var collection = collections[i];
		var querySnapshot = await db.collection(collection).get();
		var dirPath = path.join(topDirPath, collection);
		querySnapshot.forEach(function(doc) {
			var docName = doc.id;
			var docData = doc.data();
			var fileLocation = path.join(dirPath, docName) + ".json";

			console.log(fileLocation);
			fs.writeFile(fileLocation, JSON.stringify(docData, null, 4), { flag: 'w+' }, (err) => {
				if (err)
					throw err;
			});
		});
	}
}

main();