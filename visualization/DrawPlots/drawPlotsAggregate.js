var first = true;

function renderAgg(data){
	//Use data variable to draw stuff on aggregate dashboard
    var hourData = data["1"];
    var distance = hourData["averageDistance"];
    if (data["authorized"] && !data["toDate"]) {
        lastUpdate = data["currentTime"];
        var dashboard = data["dashboard"];
        //following function is in drawPlotsAggregate.js
        renderAgg(dashboard);
    }

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
	
	//TODO: Find a better usage than having a variable store this information
	if(first){
		Plotly.newPlot('plotAggregate', lineData, graphOptionsLine);
		first = false;
	}
	else{
		Plotly.react('plotAggregate', lineData, graphOptionsLine);
	}
	
}