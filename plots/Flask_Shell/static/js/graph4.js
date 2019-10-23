var URL = `/heatmap`;

var map = L.map('map').setView([38, -89], 4);

var baseLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
}).addTo(map);

getdata();




function getdata() {

  d3.json(URL).then(function(heat) {

    lat = parseFloat(heat.lat)
    lng = parseFloat(heat.lng)
    count = heat.Count



    console.log(lng)

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

    console.log("test");

    L.geoJson(geoJson).addTo(map);

    // Add Heat Map

    var coords = [];

    for (var i = 0; i < heat.lng.length; i++) {
      var location = coords.push([heat.lng[i],heat.lat[i],1])};

    console.log(coords);
    return coords;





    // var heatArray = [];
    //
    // for (var i = 0; i < geoJson.length; i++) {
    //   var location = geoJson[i].location;
    //
    //   if (location) {
    //     lat.push([location.coordinates[1]]);
    //     lng.push([location.coordinates[0]]);
    //
    //     console.log(heatArray);
    //   }
    // }

    var heatMapTest = new L.heatLayer(coords, {
      radius: 25,
      blur: 35
    }).addTo(map);

    // new points

    // var pointStyle = {
    //   radius: 2,
    //   fillColor: "#000000",
    //   color: "#000000",
    //   weight: 1,
    //   fillOpacity: 1
    // };
    //
    // var points = new L.GeoJSON.AJAX(coords, {pointToLayer: function (feature, coords) {
    //     return L.circleMarker(coords, pointStyle);
    //   }}).addTo(map);

    // console.log(geoJson)



  });



  };