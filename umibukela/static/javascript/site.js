Umibukela.Site = function() {
  var self = this,
      orange = '#f6921d',
      yes = 'black',
      no = orange,
      neutral = 'white';

  self.init = function() {
    self.colours = ['black', '#ccc'];

    // TODO: do this better
    self.drawCharts();
  };

  self.pointColour = function(label, options) {
    return {
      Yes: yes,
      Positive: yes,
      No: no,
      Negative: no,
      Neutral: neutral,
      Maybe: neutral,
      Unsure: neutral,
    }[label];
  };

  self.drawCharts = function() {
    var pct = false;  // always use counts, not percentages
    var valueKey = pct ? 'pct' : 'count';

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
          return '<b>' + this.x + ': ' + this.y + (pct ? '%' : '') + '</b><br>' + this.series.name;
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
            format: '{y}' + (pct ? '%' : ''),
          },
        },
        bar: {
          dataLabels: {
            enabled: true,
            format: '{y}' + (pct ? '%' : ''),
          },
        },
      },
    });

    $('.chart').each(function(i) {
      var $e = $(this);
      var chartIdFields = $e.data('indicator').split(":");
      var key = chartIdFields[0];
      var gender = chartIdFields[1];
      var q = questions[key];
      var chartType = $e.hasClass('chart-bar') ? 'bar' : 'column';
      var labels = _.map(q.options, function(o) { return o.current.label; });
      var currValues = _.map(q.options, function(o) {
          return {
            y: Math.round(o.current[valueKey][gender]),
            color: self.pointColour(o.current.label, q.options),
            className: o.current.label,
          };
      });

      var series = [{
          data: currValues,
          stack: 'current',
          name: 'Current cycle',
          color: self.colours[0],
      }];

      var prevValues = [];
      _.map(q.options, function(o) {
          if (o.prev !== undefined) {
              prevValues.push(Math.round(o.prev[valueKey][gender]));
          }
      });

      if (prevValues.length === currValues.length) {
          var prevSeries = {
              data: prevValues,
              stack: 'historical',
              name: 'Previous cycle',
              dataLabels: {
                  enabled: false,
              },
              pointWidth: chartType == 'bar' ? 5 : 10,
              color: self.colours[1],
          };
          series.push(prevSeries);
          if (chartType == 'bar') {
              // show the current value on top. bar charts are drawn bottom up
              series = series.reverse();
          }
      }

      if (labels.length > 4 && chartType == 'bar') {
        $e.height($e.height() * Math.ceil(labels.length / 3));
      }

      $e.highcharts({
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
