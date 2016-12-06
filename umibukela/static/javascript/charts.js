Umibukela.Poster = function() {
  var self = this;

  self.init = function() {
    self.draw();
  }

  self.draw = function() {
    if(!!questions) {
      var responses = d3.selectAll('.response');
      var color = d3.scaleOrdinal()
        .range(['#000000','#f6921d']);
      var height = 280;

      responses.each(function(d,i) {
        var response = d3.select(this);
        var key = response.attr('data-key');

        if(key) {
          var type = response.attr('data-type');
          var male_data = [];
          var female_data = [];
          var y0 = d3.scaleBand()
            .rangeRound([0, height]);
          var y1 = d3.scaleOrdinal();

          questions[key].options.forEach(function(option) {
            male_data.push({ name: 'current', value: option.current.count.male });
            male_data.push({ name: 'prev', value: option.prev.count.male });
            female_data.push({ name: 'current', value: option.current.count.female });
            female_data.push({ name: 'prev', value: option.prev.count.female });
          });

          var max = d3.max(male_data.concat(female_data).map(function(d) { return d.value }));

          var svg = response.append('svg')
            .attr('height',height)
            .attr('width',max * 2)
            .append('g');

          var time = svg.selectAll('.time')
              .data(male_data)
            .enter().append('g')
              .attr('class','time');

          time.selectAll('rect')
              .data(function(d) { return d; })
            .enter().append('rect')
              .attr('width', 15)
              .attr('x', function(d) { return d.value; })
              .attr('y', 0)
              .attr('fill', function(d) { return color(d.name); });


        }
      });
    }
  }
}

$(function() {
  var Poster = new Umibukela.Poster();

  Poster.init();
});
