//TODO: Have x, y, and z be read from the json file "test.json"

//var Plotly = require('plotly.js-dist');

var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
       // Typical action to be performed when the document is ready:
       var data = JSON.parse(xhttp.responseText);
    } else {
		return;
	}

	var x_values = [];
	var y_values = [];
	var z_values = [];
	for (let i = 0; i < data['3DCoordinates'].length; i++) {
		var curr_coordinate = data['3DCoordinates'][i];
		
		x_values.push(curr_coordinate[0]);
		y_values.push(curr_coordinate[1]);
		z_values.push(curr_coordinate[2]);
	}

	var lat_values = [];
	var long_values = [];

	//assert length of data['lat-long'][0] == data['lat-long'][1]
	for (let i = 0; i < data['lat-long'][0].length; i++) {
		var curr_geolocation = data['lat-long'];

		lat_values.push(curr_geolocation[0][i]);
		long_values.push(curr_geolocation[1][i]);
	}

	//==========================
    var trace = {
        x: x_values,
        y: y_values,
        z: z_values,
        mode: 'markers',
        marker: {
            size: 12,
            line: {
                color: 'rgba(217, 217, 217, 0.14)',
                width: 0.5
            },
            opacity: 0.8
        },
        type: 'scatter3d'
    };

    var data1 = [trace];
    var layout = {
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0
        }
    };
    Plotly.newPlot('plotDiv', data1, layout);

	//==========================
	var data = [{
	  type:'scattermapbox',
	  lat:lat_values,
	  lon:long_values,
	  mode:'markers',
	  marker: {
		size:14
	  },
	  text:['Person1', 'Person2']
	}]

	var layout = {
	  autosize: true,
	  hovermode:'closest',
	  mapbox: {
		bearing:0,
		center: {
		  lat:lat_values[0],
		  lon:long_values[0]
		},
		pitch:0,
		zoom:18
	  },
	}

	Plotly.setPlotConfig({
	  mapboxAccessToken: "pk.eyJ1Ijoic3Jhdml0MSIsImEiOiJja2JzY3NpcHgwMGJnMnZzYTY5ZWsyeDR6In0.CIOWohypCmf_oCzed32xRA"
	})

	Plotly.newPlot('mapDiv', data, layout);

};
xhttp.open("GET", "test.json", true);
xhttp.send();
