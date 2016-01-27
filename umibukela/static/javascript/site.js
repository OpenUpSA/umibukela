Umibukela.Site = function() {
  var self = this;

  self.init = function() {
    self.colours = ['#f6921d', '#ccc'];

    // TODO: do this better
    self.drawCharts();
  };

  self.drawCharts = function() {
    Highcharts.setOptions({
      credits: {enabled: false},
      chart: {animation: false},
      colors: self.colours,
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
        bar: {
          dataLabels: {
            enabled: true,
            format: '{y}%',
          },
        },
      },
    });

    $('.chart').each(function(i) {
      var $e = $(this);
      var chartIdFields = $e.data('indicator').split(":");
      var key = chartIdFields[0];
      var gender = chartIdFields[1];
      var d = questions.filter(function(q) {
          return q.key == key
      })[0];
      var chartType = $e.hasClass('chart-bar') ? 'bar' : 'column';
      var labels = _.map(d.options, function(o) { return o.label; });
      var currValues = _.map(d.options, function(o) { return Math.round(o.pct[gender]); });

      var series = [{
          data: currValues,
          stack: 'current',
          name: 'Current cycle',
          pointWidth: chartType == 'bar' ? 5 : 10,
          dataLabels: {
            enabled: false,
          },
          color: self.colours[0],
      }];

      $(this).highcharts({
        chart: {type: chartType},
        series: series,
        xAxis: {
          categories: labels,
          labels: {step: 1},
        },
      });
    });
  };
};

$(function() {
  Umibukela.site = new Umibukela.Site();
  Umibukela.site.init();
});
