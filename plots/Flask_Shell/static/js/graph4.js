var URL = `/heatmap`;

getdata();


var map = L.map('map').setView([38, -89], 4);

var baseLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

function getdata() {

  d3.json(URL).then(function(heat) {

    lat = parseFloat(heat.lat)
    lng = parseFloat(heat.lng)

    // console.log(lat);
// new code for GeoJson

    var jsonFeatures = [];

    var feature = {type: 'Feature',
      properties: heat,
      geometry: {
        type: 'Point',
        coordinates: [lng,lat]
      }
    };

    jsonFeatures.push(feature);

    var geoJson = { type: 'FeatureCollection', features: jsonFeatures };

    console.log(geoJson);

    L.geoJson(geoJson).addTo(map);

    // Add Heat Map

    var heatArray = [];

    for (var i = 0; i < geoJson.length; i++) {
      var location = geoJson[i].location;

      if (location) {
        heatArray.push([location.coordinates[1], location.coordinates[0]]);
      }
    }

    var heat = L.heatLayer(heatArray, {
      radius: 20,
      blur: 35
    }).addTo(myMap);

  });



  };