var Umibukela = {};

Umibukela.General = function() {
  var self = this;

  self.init = function() {
    self.initMaps();
  };

  self.initMaps = function() {
    // load map of a place
    L.Icon.Default.imagePath = '/static/bower_components/leaflet/dist/images';

    $('.map').each(function(i, e) {
      var $map = $(e),
          coords = [$map.data('lat'), $map.data('lng')];

      var map = new L.Map(e, {
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

      map.setView(coords, 13);
      L.marker(coords).addTo(map);
    });
  };
};

$(function() {
  Umibukela.general = new Umibukela.General();
  Umibukela.general.init();
});

// function for scrolling around website (links to "#section" will scroll to that section)
$('a[href^="#"]').on('click',function (e) {
  e.preventDefault();

  var target = this.hash;
  var $target = $(target);

  $('html, body').stop().animate({
      'scrollTop': $target.offset().top-15
  }, 900, 'swing');
});

// scrollspy
$('body').scrollspy({
  target: '.steps-sidebar',
  offset: 100
});

/*
// affix
$('.nav#sidebar').affix({
      offset: {
        top: $('.nav#sidebar').height()
      }
}); 
*/