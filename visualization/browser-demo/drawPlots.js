var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = function() {
	if (this.readyState == 4 && this.status == 200) {
	   // Typical action to be performed when the document is ready:
	   var data = JSON.parse(xhttp.responseText);
	} else {
		return;
	}
	
	//Safety classification rules are in this exact order:
	//    if unmasked individual (regardless of distance), dark red individual
	//    else if individual is masked but distance is critical, bright red individual
	//    else if unsure about mask, orange individual
	//    otherwise, mark cyan for safe individual
	var x_values_safe = [];
	var y_values_safe = [];
	var z_values_safe = [];
	var x_values_unsafe = [];
	var y_values_unsafe = [];
	var z_values_unsafe = [];
	var x_values_mask_unsure = [];
	var y_values_mask_unsure = [];
	var z_values_mask_unsure = [];
	var x_values_unmasked = [];
	var y_values_unmasked = [];
	var z_values_unmasked = [];

	for (let i = 0; i < data['3DCoordinates'].length; i++) {
		var curr_coordinate = data['3DCoordinates'][i];
		if (data['wearingMasks'][i] == 2) {
			x_values_unmasked.push(curr_coordinate[0]);
			y_values_unmasked.push(curr_coordinate[1]);
			z_values_unmasked.push(curr_coordinate[2]);
		}else if (data['safe'][i] == 0) {
			x_values_unsafe.push(curr_coordinate[0]);
			y_values_unsafe.push(curr_coordinate[1]);
			z_values_unsafe.push(curr_coordinate[2]);
		}else if (data['wearingMasks'][i] == 0) {
			x_values_mask_unsure.push(curr_coordinate[0]);
			y_values_mask_unsure.push(curr_coordinate[1]);
			z_values_mask_unsure.push(curr_coordinate[2]);
		} else if (data['wearingMasks'][i] == 1) {
			x_values_safe.push(curr_coordinate[0]);
			y_values_safe.push(curr_coordinate[1]);
			z_values_safe.push(curr_coordinate[2]);
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
	            color: 'rgba(0, 139, 139, 0.14)',
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
	            color: 'rgba(139, 0, 0, 0.14)',
	            width: 0.5
	        },
	        opacity: 0.8
	    },
	    type: 'scatter3d'
	};

	var trace_unmasked = {
	    x: x_values_unmasked,
	    y: y_values_unmasked,
	    z: z_values_unmasked,
		name: 'maskViolation',
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

	var trace_mask_unverified = {
	    x: x_values_mask_unsure,
	    y: y_values_mask_unsure,
	    z: z_values_mask_unsure,
		name: 'unverifiedMask',
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

	var data1 = [trace_safe, trace_unsafe, trace_unmasked, trace_mask_unverified];
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
xhttp.open("GET", "output.json", true);
xhttp.send();
