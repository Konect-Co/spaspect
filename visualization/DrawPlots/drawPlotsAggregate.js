var first = true;

avg_dist = [];
unmasked = [];
violationsCount = [];
visitorCount = [];
undistancedTot = [];


function renderAgg(data){
	//Use data variable to draw stuff on aggregate dashboard
	console.log("Data in drawPlotsAggregate", data);
	var calib = data["calibration"];

	Object.keys(calib).forEach(dashboardID => {
    	//access data["calibration"][dashboardID][aggregateData][1][disance...]
    	//console.log("Dashboards from renderAgg: ", calib[dashboardID]);
    	var aggData = data[calib[dashboardID]]["aggregateData"];
    	//console.log("aggData: ",aggData);
    	var hourData = aggData[1];
    	var averageDistance = hourData["averageDistance"];
    	var undistanced = hourData["undistancedCount"];
    	var violations = hourData["violationsCount"];
    	var visitors = hourData["visitorCount"];

    	//console.log("Undistanced: ",undistanced);

    	avg_dist.push(averageDistance);
		undistancedTot.push(undistanced);
		violationsCount.push(violations);
		visitorCount.push(visitors);
	})

    //lastUpdate = data["currentTime"];
	//var dashboard = data["dashboard"];
	// JSON.data.array.forEach(element => {
	// 	avg_dist.push(element.averageDistance);
	// 	unmasked.push(element.unmaskedCount);
	// 	violationsCount.push(element.violationsCount);
	// 	visitorCount.push(element.visitorCount);
	// 	//console.log("This unmasked: ", unmasked);
	// });
			

        //following function is in drawPlotsAggregate.js
        //renderAgg(dashboard);
    

	//=========================
	//PEOPLE VS TIME LINE GRAPH
	//=========================
	time = [1, 2, 3, 4, 5];
	visitorCount = [10, 15, 13, 17];

	var ppl_time = {
  		x: time,
  		y: visitorCount,
  		type: "scatter"
	};

	var data1 = [ppl_time];

	//TODO: Find a better usage than having a variable store this information
	//var graphOptionsLine = {filename: "basic-line", fileopt: "overwrite"};
	
	Plotly.newPlot('ppl_time', data1);


	//=========================
	//DISTANCE DISTRIBUTION
	//=========================
	time = [1, 2, 3, 4, 5]; 
	
	var distance = {
  	x: time,
  	y: avg_dist,
  	type: "scatter"
	};

	//TODO: Find a better usage than having a variable store this information
	//Plotly.newPlot('distance', distance);
	
}