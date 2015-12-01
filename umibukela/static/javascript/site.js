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
      chart: {animation: false},
      colors: ['#f6921d', '#000'],
      title: {text: null},
      xAxis: {
        lineWidth: 0,
        tickWidth: 0,
      },
      yAxis: {visible: false},
      legend: {enabled: false},
      tooltip: {enabled: false},
      plotOptions: {
        series: {
          animation: false,
          pointPadding: 0.05,
          groupPadding: 0,
        },
        column: {
          dataLabels: {
            enabled: true,
            format: '{y}%',
          },
        },
      },
    });

    var data = {
      chart1: {
        labels: ['Yes', 'No'],
        values: [88, 109],
      },
      chart2: {
        labels: ['Yes', 'No'],
        values: [64, 43],
      },
      chart3: {
        labels: ['Positive', 'Neutral', 'Negative'],
        values: [65, 36, 96],
      },
      chart4: {
        labels: ['Positive', 'Neutral', 'Negative'],
        values: [46, 28, 33],
      },
      chart5: {
        labels: ['More than 4 hours', '1 - 2 hours', '3 - 4 hours', '2 - 3 hours', 'Less than 1 hour'],
        values: [1, 84, 4, 22, 86],
      },
      chart6: {
        labels: ['More than 4 hours', '1 - 2 hours', '3 - 4 hours', '2 - 3 hours', 'Less than 1 hour'],
        values: [1, 84, 4, 22, 86],
      },
    };

    $('.chart').each(function(i) {
      var d = data[$(this).data('indicator')];
      var total = _.reduce(d.values, function(s, v){ return s + v; }, 0);
      var values = _.map(d.values, function(v) { return Math.round(v / total * 100); });

      $(this).highcharts({
        chart: {type: 'column'},
        xAxis: {
          categories: d.labels,
          labels: {step: 1},
        },
        series: [{data: values}],
      });
    });
  };
};

$(function() {
  Umibukela.site = new Umibukela.Site();
  Umibukela.site.init();
});
