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

	context.beginPath();
	context.arc(x, y, radius, 0, 2 * Math.PI, false);
	context.fillStyle = 'green';
	context.fill();
	context.lineWidth = 0;
	context.strokeStyle = '#003300';
	context.stroke();
}

function drawPoints() {
	var coordinates = coordinatesObj.coordinates;
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
		coordinatesObj.coordinates = coordinates_all[camName]
		console.log(coordinatesObj.coordinates);
	};
}

