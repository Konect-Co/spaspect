var camName = "Location1";
coordinatesObj = {
	coordinatesInternal: [],
	listener: function(val) {},
	set coordinates(val) {
		this.coordinatesInternal = val;
		this.listener(val);
	},
	get coordinates() {
		return this.coordinatesInternal;
	},
	registerListener: function(listener) {
		this.listener = listener;
	}
}

var canvas = document.getElementById('birds-eye');
var context = canvas.getContext('2d');

function drawPoint(x, y) {
	var radius = 5; //size of the point

	console.log("VALUES", x, y);

	context.beginPath();
	context.arc(25+x, 25+y, radius, 0, 2 * Math.PI, false);
	context.fillStyle = 'green';
	context.fill();
	context.lineWidth = 0;
	context.strokeStyle = '#003300';
	context.stroke();
}

function drawPoints() {
	console.log("drawPoints called with coordinates", coordinatesObj.coordinates);
	var coordinates = coordinatesObj.coordinates[:2]; //TODO: Check if syntax is correct
	for (i = 0; i < coordinates.length; i++) {
		drawPoint(coordinates[i][0], coordinates[i][1]);
	}
}

function clearCanvas() {
	//clearing the canvas
	context.clearRect(0, 0, canvas.width, canvas.height);
}

coordinatesObj.registerListener(function(val) {
	//when a new value of coordinates is stored, the canvas is cleared and points are redrawn
	clearCanvas();
	drawPoints(coordinatesObj.coordinates);
});

function refreshPoints() {
	let xhr = new XMLHttpRequest();
	xhr.open("GET", "/points.json", true);
	xhr.send();

	xhr.onload = function() {
		//get coordinates from correct location
		coordinates_all = JSON.parse(xhr.response);
		console.log(camName);

		var dropdown = document.getElementById("location-dropdown");
		console.log(dropdown.options[dropdown.selectedIndex].innerHTML);
		console.log(coordinates_all);
		coordinatesObj.coordinates = coordinates_all[camName][0]["coordinates"];

		var drawingScale = (coordinates_all[camName][0]["drawingScale"]);
		console.log(coordinatesObj.coordinates);
		for (let i = 0; i < coordinatesObj.coordinates.length; i++) {
			for (let j = 0; j < coordinatesObj.coordinates[i].length; j++) {			
				coordinatesObj.coordinates[i][j] *= drawingScale;
			}
		}
		console.log(coordinatesObj.coordinates);
	};
}

