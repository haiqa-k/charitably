/*** 
* Creates a new marker and adds it to a group
* @param {H.map.Group} group       The group holding the new marker
* @param {H.geo.Point} coordinate  The location of the marker
* @param {String} html             Data associated with the marker
*/
if (eventList === undefined || eventList.length == 0){ //handling border case of in case the requested zipcode has no events 
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
    center: {lat: 39.958359, lng: -75.195393},
    zoom: 1,
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
}
else{

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
      var obj = [name, parseFloat(latitude), parseFloat(longitude), url, description, start_date]
      list[i] = obj


    }
      
      for (var i = 0; i < list.length; i++){
        console.log(list[i])
      }
      shift = []

      console.log("lame nnnwww")
      var inc = 0.001
      list.forEach((el)=> {
        lat_ = parseFloat(el[1])
        long_ = parseFloat(el[2])
        addMarkerToGroup(group, {lat: lat_+inc, lng: long_+inc},'<div><a href="'+el[3]+'">'+el[0]+'</a></div>'+'<div>'+el[4]+'<br /><strong>Date:</strong> '+el[5]+'</div>');
        map.addObject(group);
        inc = inc + 0.001;

      });

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
    zoom: 15,
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
}