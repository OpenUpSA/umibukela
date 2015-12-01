$(function() {
  var $map = $('.site-header .map');

  if ($map.length) {
    // load map of a place
    var map = new L.Map($map[0], {
      scrollWheelZoom: false,
      zoomControl: false,
      dragging: true,
    });
    map.attributionControl.setPrefix('');
    new L.Control.Zoom({position: 'topright'}).addTo(map);
    new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18
    }).addTo(map);

    var coords = [$map.data('lat'), $map.data('lng')];
    map.setView(coords, 13);
    L.marker(coords).addTo(map);
  }
});
