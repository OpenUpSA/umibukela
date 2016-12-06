Umibukela.Poster = function() {
  var self = this;

  self.init = function() {
    self.draw();
  }

  self.draw = function() {
    if(!!questions) {
      var responses = d3.selectAll('.response');
      var margin = { top: 10, right: 10, bottom: 10, left: 10 };
      var height = 280 - margin.left - margin.right;
      var orange = '#f6921d';
      var colorMale = d3.scaleOrdinal()
        .range(['#000000',orange]);
      var colorFemale=d3.scaleOrdinal()
        .range(['#ffffff',orange])

      responses.each(function(d,i) {
        var response = d3.select(this);
        var key = response.attr('data-key');

        if(key) {
          var type = response.attr('data-type');
          var male_data = [];
          var female_data = [];

          questions[key].options.forEach(function(option) {
            male_data.push({ name: 'prev', value: option.prev.count.male, label: option.current.key });
            male_data.push({ name: 'current', value: option.current.count.male, label: option.current.key });
            female_data.push({ name: 'prev', value: option.prev.count.female, label: option.current.key });
            female_data.push({ name: 'current', value: option.current.count.female, label: option.current.key });
          });

          male_data.reverse();

          var max = d3.max(male_data.map(function(d) { return d.value }));
          var width = 380 - margin.top - margin.bottom;

          var y0 = d3.scaleBand()
            .domain(male_data.map(function(d) { return d.label }))
            .rangeRound([0, height]);
          var y1 = d3.scaleBand()
            .domain(['current','prev'])
            .rangeRound([0, y0.bandwidth()]);
          var x = d3.scaleLinear()
            .domain([0,max])
            .range([0,width]);
          var xAxis = d3.axisBottom()
            .scale(x);
          var yAxis = d3.axisLeft()
            .scale(y0);

          var svg = response.append('svg')
            .attr('height',height + margin.top + margin.bottom)
            .attr('width',width + margin.left + margin.right)
          .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

          svg.append('g')
            .attr('class','x axis')
            .attr('transform', 'translate(0,' + height + ')')
            .call(xAxis);

          svg.append('g')
            .attr('class','y axis')
            .call(yAxis);

          var time = svg.selectAll('.time')
              .data(male_data)
            .enter().append('g')
              .attr('class','time')
              .attr('transform', function(d) { return 'translate(0,' + y0(d.label) + ')'; })
              .append('rect')
              .attr('height', function(d) {
                var rectHeight = y1.bandwidth();

                if(d.name == 'prev') {
                  rectHeight = rectHeight / 3;
                }

                return rectHeight - 2;
              })
              .attr('x',0)
              .attr('y', function(d) { return y1(d.name); })
              .attr('width', function(d) { return x(d.value) - 2; })
              .attr('fill', function(d) { return colorMale(d.name); })
              .attr('stroke',function(d) { return d.name == 'current' ? '#000000' : orange; });

          svg.selectAll('.time')
            .append('text')
            .attr('x',function(d) { return x(d.value) + 5; })
            .attr('y',function(d) { return y1(d.name) + y1.bandwidth() / 2 + 4; })
            .attr('font-size','10px')
            .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

              male_data.forEach(function(d) {
                console.log(d.value,x(d.value));
              })
        }
      });
    }
  }
}

$(function() {
  var Poster = new Umibukela.Poster();

  Poster.init();
});
