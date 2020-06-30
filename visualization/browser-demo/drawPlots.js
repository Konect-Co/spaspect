//TODO: Have x, y, and z be read from the json file "test.json"

//var Plotly = require('plotly.js-dist');

//setInterval( function() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		   // Typical action to be performed when the document is ready:
		   var data = JSON.parse(xhttp.responseText);
		} else {
			return;
		}

		var x_values_safe = [];
		var y_values_safe = [];
		var z_values_safe = [];
		var x_values_unsafe = [];
		var y_values_unsafe = [];
		var z_values_unsafe = [];
		for (let i = 0; i < data['3DCoordinates'].length; i++) {
			var curr_coordinate = data['3DCoordinates'][i];
			if (data['safe'][i] == 1) {
				x_values_safe.push(curr_coordinate[0]);
				y_values_safe.push(curr_coordinate[1]);
				z_values_safe.push(curr_coordinate[2]);
			} else if (data['safe'][i] == 0) {
				x_values_unsafe.push(curr_coordinate[0]);
				y_values_unsafe.push(curr_coordinate[1]);
				z_values_unsafe.push(curr_coordinate[2]);
			}
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
		var trace_safe = {
		    x: x_values_safe,
		    y: y_values_safe,
		    z: z_values_safe,
			name: 'safe',
		    mode: 'markers',
		    marker: {
		        size: 8,
		        line: {
		            color: 'rgba(217, 217, 217, 0.14)',
		            width: 0.5
		        },
		        opacity: 0.8
		    },
		    type: 'scatter3d'
		};

		var trace_unsafe = {
		    x: x_values_unsafe,
		    y: y_values_unsafe,
		    z: z_values_unsafe,
			name: 'unsafe',
		    mode: 'markers',
		    marker: {
		        size: 8,
		        line: {
		            color: 'rgba(217, 0, 0, 0.14)',
		            width: 0.5
		        },
		        opacity: 0.8
		    },
		    type: 'scatter3d'
		};

		var data1 = [trace_safe, trace_unsafe];
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
			size:8
		  },
		  text:['Person1', 'Person2']
		}]

		var layout = {
		  autosize: true,
		  hovermode:'closest',
		  mapbox: {
			bearing:110,
			center: {
			  lat:lat_values[0],
			  lon:long_values[0]
			},
			pitch:0,
			zoom:19
		  },
		}

		Plotly.setPlotConfig({
		  mapboxAccessToken: "pk.eyJ1Ijoic3Jhdml0MSIsImEiOiJja2JzY3NpcHgwMGJnMnZzYTY5ZWsyeDR6In0.CIOWohypCmf_oCzed32xRA"
		})

		Plotly.newPlot('mapDiv', data, layout);
	};
	xhttp.open("GET", "test.json", true);
	xhttp.send();
//}, 10000);
