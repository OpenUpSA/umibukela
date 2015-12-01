Umibukela.Site = function() {
  var self = this;

  self.init = function() {
    self.$map = $('.site-header .map');
    if (self.$map.length) {
      self.coords = [self.$map.data('lat'), self.$map.data('lng')];
      self.drawMap();
    }

    // TODO: do this better
    self.drawCharts();
  };

  self.drawMap = function() {
    // load map of a place
    self.map = new L.Map(self.$map[0], {
      scrollWheelZoom: false,
      zoomControl: false,
      dragging: true,
    });
    self.map.attributionControl.setPrefix('');
    new L.Control.Zoom({position: 'topright'}).addTo(self.map);
    new L.TileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: 'Map © <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      maxZoom: 18
    }).addTo(self.map);

    self.map.setView(self.coords, 13);
    L.marker(self.coords).addTo(self.map);
  };

  self.drawCharts = function() {
    Highcharts.setOptions({
      credits: {enabled: false},
      chart: {
        animation: false,
      },
      plotOptions: {
        series: {
          animation: false,
        },
        column: {
          tooltip: {
            pointFormat: '<b>{point.y}</b>',
          }
        },
        line: {
          tooltip: {
            pointFormat: '<b>{point.y}</b>',
          }
        },
        bar: {
          tooltip: {
            pointFormat: '<b>{point.y}</b>',
          }
        },
      },
      title: {
        text: null,
      },
      yAxis: {
        title: {
          text: null,
        },
        floor: 0,
      },
      legend: {
        enabled: false
      }
    });

    $('.chart').highcharts({
      chart: {type: 'column'},
      xAxis: {
        categories: ['Yes', 'No'],
        labels: {step: 1},
      },
      series: [{data: [152, 152]}],
    });
  };
};

$(function() {
  Umibukela.site = new Umibukela.Site();
  Umibukela.site.init();
});
