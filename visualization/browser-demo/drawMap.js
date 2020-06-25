//TODO: Have latitude and longitude coordinates be read from test.json

var data = [{
  type:'scattermapbox',
  lat:['40.759203', '40.759186'],
  lon:['-73.985068', '-73.985114'],
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
	  lat:40.759203,
	  lon:-73.985068
	},
	pitch:0,
	zoom:18
  },
}

Plotly.setPlotConfig({
  mapboxAccessToken: "INSERT TOKEN HERE"
})

Plotly.newPlot('overheadMap', data, layout)
