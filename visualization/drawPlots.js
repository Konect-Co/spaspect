var first = true;

function update(data) {
	console.log("setting video link to", data["streamlink"])
	//document.getElementById("video-src").setAttribute("src", data["streamlink"]);
	//TODO: Seems like this doesn't update the video successfully
	var player = videojs('video');
	player.src(data["streamlink"]);
	player.ready(function() {
		player.play();
	});

	//TODO: Check if the data actually has an output section
	dashboard = data["output"];
	document.getElementById("statsTotal").innerHTML = dashboard['masked'].length;

	var x_values = dashboard['X3D_vals'];
	var y_values = dashboard['Y3D_vals'];
	var z_values = dashboard['Z3D_vals'];

	var color_values = [];
	var text_values = [];

	var undistancedCount = 0;
	var unmaskedCount = 0;

	for (let i = 0; i < dashboard['masked'].length; i++) {
		var unmasked = dashboard['masked'][i] == 2 ? true : false;
		var undistanced = dashboard['distanced'][i] == 0 ? true : false;

		var color = unmasked || undistanced ? 'rgba(255, 0, 0, 1)' : 'rgba(0, 255, 0, 1)';
		color_values.push(color);

		var distanced_txt = undistanced ? "undistanced" : "distanced";
		var unmasked_txt = unmasked ? "unmasked" : "not unmasked";

		var full_txt = distanced_txt + " and " + unmasked_txt;
		text_values.push(full_txt);

		if (undistanced)
			undistancedCount++;
		if (unmasked)
			unmaskedCount++;
	}

	document.getElementById("statsUndistanced").innerHTML = undistancedCount;
	document.getElementById("statsUnmasked").innerHTML = unmaskedCount;

	var lat_values = dashboard['lat_vals'];
	var long_values = dashboard['lon_vals'];

	//==========================
	var trace = {
		x: x_values,
		y: y_values,
		z: z_values,
		name: 'people',
		mode: 'markers',
		marker: {
			color: color_values,
			size: 8,
			line: {
				width: 0.5
			},
			opacity: 0.8
		},
		type: 'scatter3d',
		text:text_values
	};

	var scatterData = [trace]//, trace_undistanced, trace_unmasked, trace_mask_undistanced_unmasked];
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
		}
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
}
