//TODO: Have x, y, and z be read from the json file "test.json"

var trace1 = {
    x: [50, 100],
    y: [100, 150],
    z: [0, 0],
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

var data = [trace1];
var layout = {
    margin: {
        l: 0,
        r: 0,
        b: 0,
        t: 0
    }
};
Plotly.newPlot('3DPlot', data, layout);
