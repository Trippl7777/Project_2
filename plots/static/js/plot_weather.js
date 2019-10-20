var chart = "Year";
var crime = "All";
var city = "All";
var measure = "Percentage";

function buildLines(sample) {
  // Use `d3.json` to fetch the data for a sample
  d3.json(`/samples/${sample}`).then(function(d) {

    var weather = ["base", "Clear", "Mostly Cloudy", "Overcast", "Partly Cloudy", "Rain", "Snow"];
    var cityName = ["Legend", "Clear", "Mostly Cloudy", "Overcast", "Partly Cloudy", "Rain", "Snow"]
    var cityColors = ["rgb(0,0,0)", "rgb(167,25,48)", "rgb(176,163,188)", "rgb(200,56,3)", "rgb(0,34,68)", "rgb(134,109,79)"]
    var dChart = [];
    
    for(var i=0; i<weather.length;i++) {
      if (d[weather[i]].xAxis.length > 0) {
        if (weather[i] == "base") {var wid = 0; var opa = 0;}
        else {var wid = 2; var opa = 1};
        var cityPlot = {
            x: d[weather[i]].xAxis,
            y: d[weather[i]].yAxis,
            type: "scatter",
            name: cityName[i],
            opacity: opa,
            //mode: "lines",
            line: {color: cityColors[i], width: wid}  
            };
        dChart.push(cityPlot);
      };
    };

    if (measure == "Per Capita") { var yLabel = "Per Capita (1,000 Population)";}
    else { var yLabel = measure;};

    // Define our plot layout
    var layout = {
      title: {text: 'Crimes (' + crime + ') - Weather (' + weather + ')', font: {family: 'Arial', size: 20, color: 'black'}},
      xaxis: {type: 'category', title: {text: chart, font: {family: 'Arial', size: 14, color: 'black'}}},
      yaxis: {title: {text: yLabel, font: {family: 'Arial', size: 14, color: 'black'}}}
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
  var citySelector = d3.select("#citySelector");
    d3.json("/cityroute").then((sampleNames) => {
        sampleNames.forEach((sample) => {
          citySelector
            .append("option")
            .text(sample)
            .property("value", sample);
        });
        });

  var measureSelector = d3.select("#measureSelector");
    d3.json("/measureroute").then((sampleNames) => {
        sampleNames.forEach((sample) => {
            measureSelector
             .append("option")
             .text(sample)
             .property("value", sample);
        });
        });

    const firstSample = chart + "1" + crime + "1" + city + "1" + measure;
    buildLines(firstSample); 
};

function optionChanged1(newSample) {
  chart = newSample
  var Sample = chart + "1" + crime + "1" + city + "1" + measure; 
  buildLines(Sample);
};

function optionChanged2(newSample) {
  crime = newSample
  var Sample = chart + "1" + crime + "1" + city + "1" + measure; 
  buildLines(Sample);
};

function optionChanged3(newSample) {
  city = newSample
  var Sample = chart + "1" + crime + "1" + city + "1" + measure; 
  buildLines(Sample);
  };

function optionChanged4(newSample) {
  measure = newSample
  var Sample = chart + "1" + crime + "1" + city + "1" + measure; 
  buildLines(Sample);
  };

// Initialize the dashboard
init();
