/**
 * Creates a new marker and adds it to a group
 * @param {H.map.Group} group       The group holding the new marker
 * @param {H.geo.Point} coordinate  The location of the marker
 * @param {String} html             Data associated with the marker
 */
 function addMarkerToGroup(group, coordinate, html) {
  var marker = new H.map.Marker(coordinate);
  // add custom data to the marker
  marker.setData(html);
  group.addObject(marker);
}

function getLat(){
  var json = eventList;
  var obj = JSON.parse(json[0]);
  return parseFloat(obj["latitude"])
}
function getLong(){
  var json = eventList;
  var obj = JSON.parse(json[0]);
  return parseFloat(obj["longitude"])
}


/**
 * Add markers
 * Clicking on a marker opens an infobubble which holds HTML content related to the marker.
 * @param {H.Map} map A HERE Map instance within the application
 */

function addInfoBubble(map) {
  var group = new H.map.Group();
//*********
  map.addObject(group)
  // console.log(eventList)
  
  var json = eventList;
  console.log("this is json: ",json)
  console.log("this is json: ",json.length)

  list = []
  for(var i = 0; i < json.length; i++) {
    var result = json[i];
    var obj = JSON.parse(result);
    var name = obj["name"];
    var url = "https://www.google.com/search?q="+name.replace(" ", "");
    var description = obj["description"];
    var latitude = obj["latitude"]
    latitude_constant = obj["latitude"]
    var longitude = obj["longitude"];
    long_constant = obj["longitude"];
    var start_date = obj["start_date"];
    // var obj = [name, url, description, latitude, longitude, start_date]
    var obj = [name, parseFloat(latitude), parseFloat(longitude), url]
    list[i] = obj


  }
   console.log("type of list: ", typeof list)
    //const coords = [["The Inaugural Scholarship Sneaker Ball Fundraiser", 35.22337329999999, -80.8482202], ["Big South Tourney Takeover: SkoolDAZE", 35.22764529999998, -80.8391473]];
    // const coords = [
    //     [48.8,2.35, "hi"],
    //     [41.9,12.5, "hi"],
    //     [52.5,13.38, "hi"]
    // ];
    list.forEach((el)=> {
        lat_ = parseFloat(el[1])
        long_ = parseFloat(el[2])
          addMarkerToGroup(group, {lat: lat_, lng: long_},
    '<div><a href="'+el[3]+'">'+el[0]+'</a></div>');
    map.addObject(group);
    });
    console.log("type of coords: ", typeof coords)
    // const coords = [
    // ["The Inaugural Scholarship Sneaker Ball Fundraiser", 35.22337329999999, -80.8482202], 
    // ["Big South Tourney Takeover: SkoolDAZE", 35.22764529999998, -80.8391473]
    // ];
    // 

    // coords.forEach((el)=> {
    //     lat_ = parseFloat(el[1])
    //     long_ = parseFloat(el[2])
    //       addMarkerToGroup(group, {lat: lat_, lng: long_},
    // '<div><a>'+el[0]+'</a></div>');
    // map.addObject(group);
    // });

    group.addEventListener('tap', function (evt) { 
    // event target is the marker itself, group is a parent event target
    // for all objects that it contains
    var bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
      // read custom data
      content: evt.target.getData()
    });
    // show info bubble
    ui.addBubble(bubble);
    }, false);
    



  // var name1 = "Atco Battles Alzheimer's 8";
  // var url1 = "https://www.google.com/search?q="+name1.replace(" ", "");
  // var description1 = "Atco Battles Alzheimer's is a one-day celebration of music to help raise money to combat Alzheimer's and dementia.";
  // var latitude1 = 39.9350814;
  // var longitude1 = -74.80801389999999;
  // var start_date1 = "2022-05-01";

  // var name2 = "Foundation Ball 2022";
  // var url2 = "https://www.google.com/search?q="+name2.replace(" ", "");
  // var description2 = "Please join the Rotaract Club of Birmingham as we celebrate Foundation Ball 2022 at Regions Field!";
  // var latitude2 = 35.146976;
  // var longitude2 = -90.05171159999999;
  // var start_date2 = "2022-03-12";


  // map.addObject(group);

  // add 'tap' event listener, that opens info bubble, to the group
  // group.addEventListener('tap', function (evt) {
  //   // event target is the marker itself, group is a parent event target
  //   // for all objects that it contains
  //   var bubble = new H.ui.InfoBubble(evt.target.getGeometry(), {
  //     // read custom data
  //     content: evt.target.getData()
  //   });
  //   // show info bubble
  //   ui.addBubble(bubble);
  // }, false);
  // addMarkerToGroup(group, {lat: latitude1, lng: longitude1},
  //   '<div><a href="'+url1+'">'+name1+'</a></div>' +
  //   '<div>'+description1+'<br /><strong>Date:</strong> '+start_date1+'</div>');

  // addMarkerToGroup(group, {lat: latitude2, lng: longitude2},
  //   '<div><a href="'+url2+'">'+name2+'</a></div>' +
  //   '<div>'+description2+'<br /><strong>Date:</strong> '+start_date2+'</div>');
}

/**
 * Boilerplate map initialization code starts below:
 */

// initialize communication with the platform
var platform = new H.service.Platform({
  'apikey': 'vl0jQDK2bea-wWkxBm4N8yhrEjvU-rfochR2QMvGb1U'
});
var defaultLayers = platform.createDefaultLayers();


// initialize a map - this map is centered over 2930 Chestnut Street, Philadelphia
var map = new H.Map(document.getElementById('map'),
  defaultLayers.vector.normal.map, {
  center: {lat: getLat(), lng: getLong()},
  zoom: 8,
  pixelRatio: window.devicePixelRatio || 1
});

// add a resize listener to make sure that the map occupies the whole container
window.addEventListener('resize', () => map.getViewPort().resize());

// MapEvents enables the event system
// Behavior implements default interactions for pan/zoom (also on mobile touch environments)
var behavior = new H.mapevents.Behavior(new H.mapevents.MapEvents(map));

// create default UI with layers provided by the platform
var ui = H.ui.UI.createDefault(map, defaultLayers);

// Now use the map as required...
addInfoBubble(map);