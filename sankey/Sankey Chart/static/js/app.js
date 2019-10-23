// Get the data for the sankey
getdata();

function init() {
  getdata();
}

// USED FOR DROPDOWN
// Get the data for the sankey, and make drop down for values. Default being whatever city/value is in dropdown upon load
function getdata() {
  var drop = d3.select("#citychange");

  d3.json("/sancity").then((city) => {
    // console.log(city);
    city.forEach((name) => {
      drop
        .append("option")
        .text(name)
        .property("value", name);
    });

  var dflt = city[0];
  citychange(dflt);
})}

//Use input to render city data, special case for All, render all cities' data.

function citychange(city) {

  var allc = ['Atlanta', 'Boston', 'Chicago', 'Denver', 'Los Angeles']
  var data = []

  var url = `/sankey`;
  d3.json(url).then(function(sandyc) {

  var city_data = sandyc

  // console.log('Working city', city_data)
    
  if (city == 'All') {
    for(i = 0; i < allc.length; i++) {
        console.log(allc[i])
      for(j = 0; j < city_data[allc[i]]['start'].length; j++) {
        data.push([city_data[allc[i]]['start'][j], city_data[allc[i]]['end'][j], parseInt(city_data[allc[i]]['values'][j])])
      };    
  }
  console.log(data)
  }
  else {
    for(i = 0; i < city_data[city]['start'].length; i++) {
        data.push([city_data[city]['start'][i], city_data[city]['end'][i], parseInt(city_data[city]['values'][i])])
  };
  }
  // console.log("xxx", data);
  draw(data);
})
}

//Draw the sankey chart
function draw(data) {

  google.charts.load('current', {
    packages:['sankey']
  });
  google.charts.setOnLoadCallback(brush);

  //sub-function paint does not pull data, use callback to call function brush to push data to paint
  function brush() {
    paint(data)
  }
  
  function paint(data) {
    // console.log('pain', data)

    var san = new google.visualization.DataTable();
    san.addColumn('string', 'From');
    san.addColumn('string', 'To');
    san.addColumn('number', 'Weight');
    san.addRows(data)

    var crayon = ['#1D32FF','#D33AFF','#FF579A','#FFAA75','#F1FF92','#AFFFAF','#CCFFFF'];

    var layout = {
      width: document.getElementById('sankey').offsetWidth,
      height: document.getElementById('sankey').offsetWidth*.57,
      sankey: {
          node: {
            interactivity: true,
            label: { 
              fontSize: 12,
              color: 'black',
              bold: true,
                   },
          colors: crayon
                },
          link: {
            colorMode: 'gradient',
            colors: crayon,
                }
              }
            };

      var key = new google.visualization.Sankey(document.getElementById("sankey"));
      key.draw(san, layout);
  }
}

