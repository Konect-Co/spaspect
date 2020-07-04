var first = true;

function update() {
	var xhttp = new XMLHttpRequest();
	xhttp.onreadystatechange = function() {
		if (this.readyState == 4 && this.status == 200) {
		// Typical action to be performed when the document is ready:
		var data = JSON.parse(xhttp.responseText);
		} else {
			return;
		}

		document.getElementById("statsTotal").innerHTML = data['3DCoordinates'].length;
		
		//Safety classification rules are in this exact order:
		//    if unmasked individual (regardless of distance), dark red individual
		//    else if individual is masked but distance is critical, bright red individual
		//    else if unsure about mask, orange individual
		//    otherwise, mark cyan for safe individual
		var safe_values = [[],[],[]];
		var undistanced_values = [[],[],[]];
		var unmasked_values = [[],[],[]];
		var undistanced_unmasked_values = [[],[],[]];

		for (let i = 0; i < data['3DCoordinates'].length; i++) {
			var curr_coordinate = data['3DCoordinates'][i];

			var unmasked = data['masked'][i] == 2 ? true : false;
			var undistanced = data['distanced'][i] == 0 ? true : false;
			
			if (unmasked && undistanced) {
				undistanced_unmasked_values[0].push(curr_coordinate[0]);
				undistanced_unmasked_values[1].push(curr_coordinate[1]);
				undistanced_unmasked_values[2].push(curr_coordinate[2]);
			} else if (unmasked) {
				unmasked_values[0].push(curr_coordinate[0]);
				unmasked_values[1].push(curr_coordinate[1]);
				unmasked_values[2].push(curr_coordinate[2]);
			} else if (undistanced) {
				undistanced_values[0].push(curr_coordinate[0]);
				undistanced_values[1].push(curr_coordinate[1]);
				undistanced_values[2].push(curr_coordinate[2]);
			} else {
				safe_values[0].push(curr_coordinate[0]);
				safe_values[1].push(curr_coordinate[1]);
				safe_values[2].push(curr_coordinate[2]);
			}
		}

		document.getElementById("statsUndistanced").innerHTML = undistanced_values[0].length + undistanced_unmasked_values[0].length;
		document.getElementById("statsUnmasked").innerHTML = unmasked_values[0].length + undistanced_unmasked_values[0].length;

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
			x: safe_values[0],
			y: safe_values[1],
			z: safe_values[2],
			name: 'safe',
			mode: 'markers',
			marker: {
				color: 'rgba(0, 100, 0, 0.5)',
				size: 8,
				line: {
					width: 0.5
				},
				opacity: 0.8
			},
			type: 'scatter3d'
		};

		var trace_undistanced = {
			x: undistanced_values[0],
			y: undistanced_values[1],
			z: undistanced_values[2],
			name: 'undistanced',
			mode: 'markers',
			marker: {
				color: 'rgba(255, 150, 0, 0.5)',
				size: 8,
				line: {
					width: 0.5
				},
				opacity: 0.8
			},
			type: 'scatter3d'
		};

		var trace_unmasked = {
			x: unmasked_values[0],
			y: unmasked_values[1],
			z: unmasked_values[2],
			name: 'unmasked',
			mode: 'markers',
			marker: {
				color: 'rgba(255, 255, 0, 0.5)',
				size: 8,
				line: {
					width: 0.5
				},
				opacity: 0.8
			},
			type: 'scatter3d'
		};

		var trace_mask_undistanced_unmasked = {
			x: undistanced_unmasked_values[0],
			y: undistanced_unmasked_values[1],
			z: undistanced_unmasked_values[2],
			name: 'undistanced_unmasked',
			mode: 'markers',
			marker: {
				color: 'rgba(255, 0, 0, 0.5)',
				size: 8,
				line: {
					width: 0.5
				},
				opacity: 0.8
			},
			type: 'scatter3d'
		};

		var scatterData = [trace_safe, trace_undistanced, trace_unmasked, trace_mask_undistanced_unmasked];
		var scatterLayout = {
			margin: {
				l: 0,
				r: 0,
				b: 0,
				t: 0
			}
		};
		

		//==========================
		var mapData = [{
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
		margin: {
			l: 0,
			r: 0,
			b: 0,
			t: 0
		}
		}

		Plotly.setPlotConfig({
		mapboxAccessToken: "pk.eyJ1Ijoic3Jhdml0MSIsImEiOiJja2JzY3NpcHgwMGJnMnZzYTY5ZWsyeDR6In0.CIOWohypCmf_oCzed32xRA"
		})

		if (first) {
			Plotly.newPlot('plotDiv', scatterData, scatterLayout);
			Plotly.newPlot('mapDiv', mapData, layout);
			first = false;
		} else {
			Plotly.react('plotDiv', scatterData, scatterLayout);
			Plotly.react('mapDiv', mapData, layout);
		}

	};
	xhttp.open("GET", "output.json", true);
	xhttp.send();
}

setInterval(update(), 1000);