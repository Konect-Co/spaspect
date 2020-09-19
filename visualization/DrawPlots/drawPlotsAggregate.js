var first = true;

function renderAgg(data){
	//data for current hour, all locations separately
	var dashboardNames = [];
	var averageDistances = [];
	var visitorCount = [];
	var unmaskedCount = [];
	var undistancedCount = [];
	var violationsCount = [];

	// data for all hours separately, all locations combined
	var totalVisitorCount = {};
	var totalUnmaskedCount = {};
	var totalUndistancedCount = {};
	var totalViolationsCount = {};

	//Use data variable to draw stuff on aggregate dashboard
	var availableDashboards = data["availableDashboards"];

	Object.keys(availableDashboards).forEach(dashboardID => {
		var dashboardName = availableDashboards[dashboardID];

		var aggData = data[dashboardID];
		var hours = Object.keys(aggData).sort().reverse();
		var currHour = hours[0];

		hours.forEach(hour => {
			var hourData = aggData[hour];

			var visitors = hourData["visitorCount"];
			var unmasked = hourData["unmaskedCount"];
			var undistanced = hourData["undistancedCount"];
			var violations = hourData["violationsCount"];

			//If this is the current hour, then we add the relevant data
			if (hour == currHour) {
				dashboardNames.push(dashboardName);
				averageDistances.push(hourData["averageDistance"]);
				visitorCount.push(visitors);
				unmaskedCount.push(unmasked);
				undistancedCount.push(undistanced);
				violationsCount.push(violations);
			}

			//Initialize the total counts if not done so already
			if (!Object.keys(totalVisitorCount).includes(hour)) {
				totalVisitorCount[hour] = 0;
				totalUnmaskedCount[hour] = 0;
				totalUndistancedCount[hour] = 0;
				totalViolationsCount[hour] = 0;
			}

			//Add counts to the data structure
			totalVisitorCount[hour] += visitors;
			totalUnmaskedCount[hour] += unmasked;
			totalUndistancedCount[hour] += undistanced;
			totalViolationsCount[hour] += violations;
		});
	});

	//=========================
	//PEOPLE VS TIME LINE GRAPH
	//=========================
	time = [1, 2, 3, 4, 5];
	visitorCount = [10, 15, 13, 17];

	var ppl_time = {
  		x: Object.keys(totalVisitorCount),
  		y: Object.values(totalVisitorCount),
  		type: "line"
	};

	Plotly.newPlot('ppl_time', [ppl_time]);


	//=========================
	//DISTANCE DISTRIBUTION
	//=========================
	var distance = {
  	x: dashboardNames,
  	y: visitorCount,
  	type: "scatter"
	};

	//TODO: Find a better usage than having a variable store this information
	//var graphOptionsLine = {filename: "basic-line", fileopt: "overwrite"};

	//Plotly.newPlot('x_loc', [distance]);

		//=========================
	//DISTANCE DISTRIBUTION
	//=========================
	
}