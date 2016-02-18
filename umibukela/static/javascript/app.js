var Umibukela = {};

Umibukela.General = function() {
  var self = this;

  self.init = function() {
    self.initMaps();

    // function for scrolling around website (links to "#section" will scroll to that section)
    $('a[href^="#"]').on('click',function (e) {
      e.preventDefault();

      var target = this.hash;
      var $target = $(target);
      
      if ($target.length) {
        $('html, body').stop().animate({
            'scrollTop': $target.offset().top-15
        }, 300, 'swing');
      }
    });

    if ($("#about").length) {
      self.initAboutPage();
    }

    $('.btn-print').on('click', function() {
      window.print();
    });

    self.initSocial();
  };

  self.initAboutPage = function() {
    // scrollspy
    $('body').scrollspy({
      target: '.steps-sidebar',
      offset: 100
    });

    var $lastRow = $('.steps-content section').last();

    // affix
    $('.steps-sidebar').affix({
      offset: {
        top: $('.steps-sidebar').offset().top - 30,
        // stop affix 2/3 of the way down the last step row
        bottom: $('body').height() - $lastRow.offset().top - $lastRow.height() * 2 / 3,
      }
    });

    $('#subnav').affix({
      offset: {
        top: $('#subnav').offset().top - 10,
      }
    });
  };

  self.initMaps = function() {
    // load map of a place
    var $maps = $('.map');
    if ($maps.length) {
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
    }
  };

  self.initSocial = function() {
    var url = window.location.toString();

    // social buttons
    $('.fb-share').on('click', function(e) {
      e.preventDefault();

      window.open("https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(url),
                  "share", "width=600, height=400, scrollbars=no");
      ga('send', 'social', 'facebook', 'share', url);
    });

    $('.twitter-share').on('click', function(e) {
      e.preventDefault();
          var tweet = $(this).data('tweet') || '';

      window.open("https://twitter.com/intent/tweet?" +
                  "text=" + encodeURIComponent(tweet) +
                  "&url=" + encodeURIComponent(url) +
                  "share", "width=364, height=250, scrollbars=no");
      ga('send', 'social', 'twitter', 'share', url);
    });
  }
};

$(function() {
  Umibukela.general = new Umibukela.General();
  Umibukela.general.init();
});
