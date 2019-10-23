getdata();
// Initiate Sunburst draw
function init() {
  getdata();
}

// Define input variables
var par, lbl, ids, val

// If window is resized, resize chart accordingly
window.onresize = function() {
  var area = d3.select('svg');

  if (!area.empty()) {
      area.remove();
          draw();
  }
};

//Pull Data for the sub-api setup
function getdata() {

  var url = `/sunburst`;
  d3.json(url).then(function(sunnyb) {

  ids = sunnyb.ids
  lbl = sunnyb.labels
  par = sunnyb.parents
  val = (sunnyb.values).map(Number)
  weat = sunnyb.weather

  draw();
})
}


//Here comes the sun doo, doo, doo
function draw() {
  
//Define sunburst data
var data = [
    {
      type: "sunburst",
      ids: ids,
      labels: lbl,
      parents: par,
      values: val,
      maxdepth: 3,
      branchvalues: 'total',
    }
  ];

  var layout = {
    width: document.getElementById("sunburst").offsetWidth,
    height: document.getElementById("sunburst").offsetWidth*.6,
    sunburstcolorway:["#866d4f","#c83803","#002244","#b0a3bc","#a71930"],
    extendsunburstcolorway: true
  };  

Plotly.newPlot("sunburst", data, layout, {responsive: true});
}