Umibukela.Site = function() {
  var self = this;

  self.init = function() {
    self.$map = $('.place-header .map');
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
      colors: ['#f6921d', '#ccc'],
      title: {text: null},
      xAxis: {
        lineWidth: 0,
        tickWidth: 0,
      },
      yAxis: {visible: false},
      legend: {enabled: false},
      tooltip: {
        formatter: function() {
          return '<b>' + this.x + ': ' + this.y + '%</b><br>' + this.series.name;
        }
      },
      plotOptions: {
        series: {
          animation: false,
          pointPadding: 0.0,
          groupPadding: 0.07,
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
        values: {
          current: [88, 109],
          historical: [132, 83],
        },
      },
      chart2: {
        labels: ['Yes', 'No'],
        values: {
          current: [64, 43],
          historical: [53, 41],
        },
      },
      chart3: {
        labels: ['Positive', 'Neutral', 'Negative'],
        values: {
          current: [65, 36, 96],
          historical: [34, 27, 152],
        }
      },
      chart4: {
        labels: ['Positive', 'Neutral', 'Negative'],
        values: {
          current: [46, 28, 33],
          historical: [14, 9, 72],
        },
      },
      chart5: {
        labels: ['More than 4 hours', '1 - 2 hours', '3 - 4 hours', '2 - 3 hours', 'Less than 1 hour'],
        values: {
          current: [1, 84, 4, 22, 86],
          historical: [18, 57, 17, 52, 70],
        },
      },
      chart6: {
        labels: ['More than 4 hours', '1 - 2 hours', '3 - 4 hours', '2 - 3 hours', 'Less than 1 hour'],
        values: {
          current: [1, 84, 4, 22, 86],
          historical: [1, 29, 10, 19, 35],
        },
      },
    };

    $('.chart').each(function(i) {
      var d = data[$(this).data('indicator')];

      var currTotal = _.reduce(d.values.current, function(s, v){ return s + v; }, 0);
      var currValues = _.map(d.values.current, function(v) { return Math.round(v / currTotal * 100); });

      var histTotal = _.reduce(d.values.historical, function(s, v){ return s + v; }, 0);
      var histValues = _.map(d.values.historical, function(v) { return Math.round(v / histTotal * 100); });

      $(this).highcharts({
        chart: {type: 'column'},
        xAxis: {
          categories: d.labels,
          labels: {step: 1},
        },
        series: [{
          data: currValues,
          stack: 'current',
          name: 'Current cycle',
        }, {
          data: histValues,
          stack: 'historical',
          pointWidth: 10,
          name: 'Previous cycles',
          dataLabels: {
            enabled: false,
          },
        }],
      });
    });
  };
};

$(function() {
  Umibukela.site = new Umibukela.Site();
  Umibukela.site.init();
});
