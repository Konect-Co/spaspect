var first = true;

avg_dist = [];
unmasked = [];
violationsCount = [];
visitorCount = [];


function renderAgg(data){
	//Use data variable to draw stuff on aggregate dashboard
	//console.log("Data in drawPlotsAggregate", data);
	var aggData = data["aggregateData"];
    var hourData = aggData["1"];
    var distance = hourData["averageDistance"];
    if (data["authorized"] && !data["toDate"]) {
        lastUpdate = data["currentTime"];
		var dashboard = data["dashboard"];
		JSON.data.array.forEach(element => {
			avg_dist.push(element.averageDistance);
			unmasked.push(element.unmaskedCount);
			violationsCount.push(element.violationsCount);
			visitorCount.push(element.visitorCount);
			console.log("This unmasked: ", unmasked);
		});
			
	};
        //following function is in drawPlotsAggregate.js
        //renderAgg(dashboard);
    

	//=========================
	//PEOPLE VS TIME LINE GRAPH
	//=========================
	time = [1, 2, 3, 4, 5];
	visitorCount = [5, 6, 7, 3, 9];

	var ppl_time = {
  	x: time,
  	y: visitorCount,
  	type: "scatter"
	};

	//TODO: Find a better usage than having a variable store this information
	var graphOptionsLine = {filename: "basic-line", fileopt: "overwrite"};
	Plotly.newPlot('ppl_time', ppl_time, graphOptionsLine);


	//=========================
	//DISTANCE DISTRIBUTION
	//=========================
	time = [1, 2, 3, 4, 5]; 
	
	var distance = {
  	x: time,
  	y: averageDistance,
  	type: "scatter"
	};

	//TODO: Find a better usage than having a variable store this information
	Plotly.newPlot('distance', distance);
	
}