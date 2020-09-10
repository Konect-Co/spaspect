var first = true;

function renderAgg(data){

	//=========================
	//PEOPLE VS TIME LINE GRAPH
	//=========================

	var line1 = {
  	x: [1, 2, 3, 4],
  	y: [10, 15, 13, 17],
  	type: "scatter"
	};

	var line2 = {
  	x: [1, 2, 3, 4],
  	y: [16, 5, 11, 9],
  	type: "scatter"
	};
	var lineData = [line1, line2];
	var graphOptionsLine = {filename: "basic-line", fileopt: "overwrite"};
	
	if(first){
		Plotly.newPlot('plotAggregate', lineData, graphOptionsLine);
		first = false;
	}
	else{
		Plotly.react('plotAggregate', lineData, graphOptionsLine);
	}
	
}

//TODO: PLACE CORRECTLY
updateAgg();