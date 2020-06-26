//TODO: Have x, y, and z be read from the json file "test.json"

var Plotly = require('plotly.js-dist');

Plotly.d3.json('test.json', function(figure) {
    let data = figure.data;

    var trace1 = {
        x: data['3DCoordinates'][0][0],
        y: data['3DCoordinates'][0][1],
        z: data['3DCoordinates'][0][2],
        mode: 'markers',
        marker: {
            size: 12,
            line: {
                color: 'rgba(217, 217, 217, 0.14)',
                width: 0.5
            },
            opacity: 0.8
        },
        type: 'scatter3d'
    };

    var trace2 = {
        x: data['3DCoordinates'][1][0],
        y: data['3DCoordinates'][1][1],
        z: data['3DCoordinates'][1][2],
        mode: 'markers',
        marker: {
            color: 'rgb(127, 127, 127)',
            size: 12,
            symbol: 'circle',
            line: {
                color: 'rgb(204, 204, 204)',
                width: 1
            },
            opacity: 0.8
        },
        type: 'scatter3d'
    };

    var data1 = [trace1, trace2];
    var layout = {
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0
        }
    };
    Plotly.newPlot('plotDiv', data1, layout);
    //Plotly.plot(document.getElementById('myDiv'), data, layout);
});
