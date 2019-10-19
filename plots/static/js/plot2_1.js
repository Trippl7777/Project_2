function buildLines(sample) {
  // Use `d3.json` to fetch the data for a sample
  d3.json(`/samples/${sample}`).then(function(d) {

    var cities = ["atlanta", "boston", "chicago", "denver", "los_angeles"];
    var cityName = ["Atlanta", "Boston", "Chicago", "Denver", "Los Angeles"]
    var cityColors = ["rgb(167,25,48)", "rgb(176,163,188)", "rgb(200,56,3)", "rgb(0,34,68)", "rgb(134,109,79)"]
    var dChart = [];
    
    for(var i=0; i<cities.length;i++) {
        var cityPlot = {
            x: d[cities[i]].xAxis,
            y: d[cities[i]].yAxis,
            type: "scatter",
            name: cityName[i],
            //mode: "lines",
            line: {color: cityColors[i], width: 2}  
            };
        dChart.push(cityPlot);
        };

    console.log(dChart);
    
    // Define our plot layout
    var layout = {
      title: {text: "Percentage of Crimes by " + sample, font: {family: 'Arial', size: 20, color: 'black'}},
      xaxis: {type: 'category', title: {text: sample, font: {family: 'Arial', size: 12, color: 'black'}}},
      yaxis: {title: {text: "Percentage", font: {family: 'Arial', size: 12, color: 'black'}}}

    };
 
    Plotly.newPlot("xplot", dChart, layout);
  });
};

function init() {
  // Grab a reference to the dropdown select element
  var selector = d3.select("#selDataset");

  // Use the list of sample names to populate the select options
  d3.json("/names").then((sampleNames) => {
    sampleNames.forEach((sample) => {
      selector
        .append("option")
        .text(sample)
        .property("value", sample);
    });

  // Use the first sample from the list to build the initial plots
  const firstSample = sampleNames[0];
  buildLines(firstSample);
  });
};

function optionChanged(newSample) {
  buildLines(newSample);
};

// Initialize the dashboard
init();
