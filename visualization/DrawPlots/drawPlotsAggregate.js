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
	var ppl_time_trace = {
  		x: Object.keys(totalVisitorCount),
  		y: Object.values(totalVisitorCount),
  		type: "line",
  		name: "people"
	};

	var undistanced_time_trace = {
		x: Object.keys(totalUndistancedCount),
		y: Object.values(totalUndistancedCount),
		type: "line",
		name: "undistanced"
	};

	var unmasked_time_trace = {
		x: Object.keys(totalUnmaskedCount),
		y: Object.values(totalUnmaskedCount),
		type: "line",
		name: "unmasked"
	};

	var violations_time_trace = {
		x: Object.keys(totalViolationsCount),
		y: Object.values(totalViolationsCount),
		type: "line",
		name: "violations"
	};

	var linegraph_data = [ppl_time_trace, undistanced_time_trace, unmasked_time_trace, violations_time_trace];

	var ppl_time_layout = { 
		title: '<b>Analytics vs time</b>',
		font: {size: 12},
		plot_bgcolor:"#FDFDFD",
		paper_bgcolor:"#F0F0F0",
		xaxis: {
			title: {text: 'time (hour)'}
		},
		yaxis: {
			title: {text: 'analytics'}
		}
	};
	Plotly.newPlot('ppl_time', linegraph_data, ppl_time_layout, {responsive: true});


	//=========================
	//CROSS LOCATION (X-LOC) DISTRIBUTION
	//=========================
	var x_loc_trace = {
		x: dashboardNames,
		y: visitorCount,
		type: "bar"
	};
	var x_loc_layout = {
		title: '<b>Cross Location Visitation</b>',
		font: {size: 12},
		plot_bgcolor:"#FDFDFD",
		paper_bgcolor:"#F0F0F0",
		xaxis: {
			title: {text: 'location'}
		},
		yaxis: {
			title: {text: '# people'}
		}
	};
	Plotly.newPlot('x_loc', [x_loc_trace], x_loc_layout, {responsive: true});

	
	
}