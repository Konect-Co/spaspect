var first = true;

function renderRealtime(data) {
	//TODO: Seems like this doesn't update the video successfully
	var player = videojs('video');
	player.src(data["streamlink"]);
	player.ready(function() {
		player.play();
	});

	//TODO: Check if the data actually has an output section
	dashboard = data["realtime"];

	document.getElementById("statsTotal").innerHTML = dashboard['masked'].length;

	var x_values = dashboard['X3D_vals'];
	var y_values = dashboard['Y3D_vals'];
	var z_values = dashboard['Z3D_vals'];
	var distanced = dashboard['distanced'];
	var lat_vals = dashboard['lat_vals'];
	var lon_vals = dashboard['lon_vals'];
	var masked = dashboard['masked'];
	var tracked = dashboard['tracked'];

	var color_values = [];
	var text_values = [];

	var undistancedCount = 0;
	var unmaskedCount = 0;

	for (let i = 0; i < masked.length; i++) {
		var unmasked = masked[i] == 2 ? true : false;
		var undistanced = distanced[i] == 0 ? true : false;

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
		text: text_values
	};
	

	
	//TODO: Add a separate trace for the history of each person
	//	Fill the values of the trace with the appropriate line and
	//	color for each person by reading from the data argument.
	//  Add this trace to scatterData variable below

	var scatterData = [trace]//, mapDataTrace];
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
		lat:lat_vals,
		lon:lon_vals,
		mode:'marker',
		marker: {
			size:8
		}
	}]

	var mapLayout = {
		autosize: true,
		hovermode:'closest',
		mapbox: {
			bearing:0,
			center: {
    			lat:lat_vals[0],
    			lon:lon_vals[0]
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
	};

	Plotly.setPlotConfig({
		mapboxAccessToken: "pk.eyJ1Ijoic3Jhdml0MSIsImEiOiJja2JzY3NpcHgwMGJnMnZzYTY5ZWsyeDR6In0.CIOWohypCmf_oCzed32xRA"
	})

	if (first) {
		Plotly.newPlot('plotDiv', scatterData, scatterLayout);
		Plotly.newPlot('mapDiv', mapData, mapLayout);
		first = false;
	} else {
		Plotly.react('plotDiv', scatterData, scatterLayout);
		Plotly.react('mapDiv', mapData, mapLayout);
	}
}

/*
    var tracked = dashboard['tracked'];
    var trackedNamesLen = Object.values(tracked).length;
    
    var trackingX = [];
    var trackingY = [];
    var trackingZ = [];

    for(name = 0 ; name < trackedNamesLen ; name++){
        var history = Object.values(tracked)[name]['history'];
        var historyKeys = Object.keys(history);
        var historyTimesLen = Object.keys(history).length;
        for(time = 0 ; time < historyTimesLen ; time++){
        	var time_key = historyKeys[time];
            var X_tracing = history[time_key]['X3D'];
            var Y_tracing = history[time_key]['Y3D'];
            var Z_tracing = history[time_key]['Z3D'];
            //console.log(Array(X_tracing));
            
            var X_len = 0;
            
            if(typeof X_tracing == 'number'){
                X_len = 1;
            }
            else{
                X_len = X_tracing.length;
            }
            var actualX = 0;
            var actualY = 0;
            var actualZ = 0;
            var id = historyKeys[time];
            for(val = 0 ; val < X_len ; val++){
                var colorTracing = (parseInt((id % 1)*255), parseInt((id*100%1)*255), parseInt((id*10000%1)*255));
                console.log(colorTracing);
                if(typeof X_tracing == 'number'){
                    actualX = X_tracing;
                    actualY = Y_tracing;
                    actualZ = Z_tracing;
                    break;
                }
                else{
                    actualX = X_tracing[val];
                    actualY = Y_tracing[val];
                    actualZ = Z_tracing[val];
                }
                
                trackingX.push(actualX);
                trackingY.push(actualY);
                trackingZ.push(actualZ);
            }
        }
    }

	var mapDataTrace = {
		x: trackingX,
		y: trackingY,
		z: trackingZ,
		name: 'history',
		mode: 'lines',
		marker: {
			color: colorTracing,
			size: 8,
			line: {
				width: 0.5
			},
			opacity: 0.8
		},
		type: 'scatter3d',
		text: text_values
	};
*/

	//var name = dashboard['tracked']['name']
	//var name2 = data['currentTime']
	//console.log(name2);
	

	//var lat_tracing = dashboard['tracked']['history']['latlonX'];
    //var lon_tracing = dashboard['tracked']['history']['latlonY'];
    
    /*var mapDataTracing = {
		type:'scattermapbox',
		lat:lat_tracing,
		lon:lon_tracing,
		mode:'lines',
		line: {
			size:1
		}
	};*/