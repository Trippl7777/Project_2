var chart = "Year";
var crime = "All";
var weather = "All";

function buildLines(sample) {
  // Use `d3.json` to fetch the data for a sample
  d3.json(`/samples/${sample}`).then(function(d) {

    var cities = ["base", "atlanta", "boston", "chicago", "denver", "los_angeles"];
    var cityName = ["Legend", "Atlanta", "Boston", "Chicago", "Denver", "Los Angeles"]
    var cityColors = ["rgb(0,0,0)", "rgb(167,25,48)", "rgb(176,163,188)", "rgb(200,56,3)", "rgb(0,34,68)", "rgb(134,109,79)"]
    var dChart = [];
    
    for(var i=0; i<cities.length;i++) {
      if (d[cities[i]].xAxis.length > 0) {
        if (cities[i] == "base") {var wid = 0; var opa = 0;}
        else {var wid = 2; var opa = 1};
        var cityPlot = {
            x: d[cities[i]].xAxis,
            y: d[cities[i]].yAxis,
            type: "scatter",
            name: cityName[i],
            opacity: opa,
            //mode: "lines",
            line: {color: cityColors[i], width: wid}  
            };
        dChart.push(cityPlot);
      };
    };

    // Define our plot layout
    var layout = {
      title: {text: "Percentage of Crimes by " + chart, font: {family: 'Arial', size: 20, color: 'black'}},
      xaxis: {type: 'category', title: {text: chart, font: {family: 'Arial', size: 12, color: 'black'}}},
      yaxis: {title: {text: "Percentage", font: {family: 'Arial', size: 12, color: 'black'}}}
    };
 
    Plotly.newPlot("xplot", dChart, layout);
  });
};

function init() {
  
  // Grab a reference to the Chart dropdown select element
  var chartSelector = d3.select("#chartType");
  d3.json("/chartroute").then((sampleNames) => {
    //console.log(sampleNames);
    sampleNames.forEach((sample) => {
      chartSelector
        .append("option")
        .text(sample)
        .property("value", sample);
    });
    });
 
  // Grab a reference to the Crime dropdown select element
  var crimeSelector = d3.select("#crimeSelector");
    d3.json("/crimeroute").then((sampleNames) => {
      sampleNames.forEach((sample) => {
        crimeSelector
          .append("option")
          .text(sample)
          .property("value", sample);
      });
      });

  // Grab a reference to the Weather dropdown select element   
  var weatherSelector = d3.select("#weatherSelector");
    d3.json("/weatherroute").then((sampleNames) => {
        sampleNames.forEach((sample) => {
          weatherSelector
            .append("option")
            .text(sample)
            .property("value", sample);
        });
        });

    const firstSample = chart + "1" + crime + "1" + weather;
    buildLines(firstSample); 
};

function optionChanged1(newSample) {
  chart = newSample
  var Sample = chart + "1" + crime + "1" + weather; 
  buildLines(Sample);
};

function optionChanged2(newSample) {
  crime = newSample
  var Sample = chart + "1" + crime + "1" + weather; 
  buildLines(Sample);
};

function optionChanged3(newSample) {
  weather = newSample
  var Sample = chart + "1" + crime + "1" + weather; 
  buildLines(Sample);
  };
// Initialize the dashboard
init();
