Umibukela.Poster = function() {
  var self = this;

  self.init = function() {
    self.draw();
  }

  self.draw = function() {
    if(!!questions) {
      var responses = d3.selectAll('.response');
      var margin = { top: 10, right: 10, bottom: 10, left: 10 };
      var figureHeight = 455 - margin.top - margin.bottom;
      var height = 350;
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
          var options = questions[key].options;
          var labels = [];

          options.forEach(function(option) {
            var key = option.current.key;

            male_data.push({ name: 'prev', value: option.prev.count.male, label: key });
            male_data.push({ name: 'current', value: option.current.count.male, label: key });
            female_data.push({ name: 'prev', value: option.prev.count.female, label: key });
            female_data.push({ name: 'current', value: option.current.count.female, label: key });

            switch(key) {
              case 'more-six':
                labels.push({ key: 'more-six', label: '6 hrs +' });
              break;
              case 'four_six':
                labels.push({ key: 'four_six', label: '4-6 hrs' });
              break;
              case 'two_four':
                labels.push({ key: 'two_four', label: '2-4 hrs' });
              break;
              case 'one_two':
                labels.push({ key: 'one_two', label: '1-2 hrs' });
              break;
              case 'thirty_one':
                labels.push({ key: 'thirty_one', label: '30mins-1hr' });
              break;
              case 'under_thirty':
                labels.push({ key: 'under_thirty', label: '>30 mins' });
              break;
            }
          });

          male_data.reverse();
          female_data.reverse();

          var rightMax = d3.max(female_data.map(function(d) { return d.value }));
          var leftMax = d3.max(male_data.map(function(d) { return d.value }));
          var width = 540 - margin.top - margin.bottom;
          var sideWidth = (width - 70) / 2;
          var rightOffset = width / 2 + 35;
          var leftOffset = width / 2 - 35;

          var y0 = d3.scaleBand()
            .domain(male_data.map(function(d) { return d.label }))
            .rangeRound([0, height])
            .padding(0);
          var y1 = d3.scaleBand()
            .domain(['current','prev'])
            .rangeRound([0, y0.bandwidth()])
            .padding(0);
          var xRight = d3.scaleLinear()
            .domain([0,rightMax])
            .range([0,sideWidth]);
          var xLeft = d3.scaleLinear()
            .domain([0,leftMax])
            .range([0,sideWidth]);

          var svg = response.append('svg')
            .attr('height',figureHeight)
            .attr('width',width + margin.left + margin.right)
          .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

          var right = svg.selectAll('g.right')
            .data(female_data)
          .enter().append('g')
            .attr('transform', function(d) { return 'translate(' + rightOffset + ',' + y0(d.label) + ')'; })
            .attr('class','right');

          right.append('rect')
            .attr('height', function(d) {
              var rectHeight = y1.bandwidth();

              if(d.name == 'prev') {
                rectHeight = rectHeight / 3;
              }

              return rectHeight - 2;
            })
            .attr('y', function(d) { return y1(d.name); })
            .attr('width', function(d) { return xRight(d.value) - 2; })
            .attr('fill', function(d) { return colorFemale(d.name); })
            .attr('stroke',function(d) { return d.name == 'current' ? '#000000' : orange; });

          right.append('text')
            .attr('dx',function(d) { return xRight(d.value) + 5; })
            .attr('dy',function(d) { return y1.bandwidth() / 2 + 4; })
            .attr('font-size','10px')
            .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

          var left = svg.selectAll('g.left')
            .data(male_data)
          .enter().append('g')
            .attr('transform', function(d) { return 'translate(0,' + y0(d.label) + ')'; })
            .attr('class','left');

          left.append('rect')
            .attr('height', function(d) {
              var rectHeight = y1.bandwidth();

              if(d.name == 'prev') {
                rectHeight = rectHeight / 3;
              }

              return rectHeight - 2;
            })
            .attr('x',function(d) { return sideWidth - xLeft(d.value); })
            .attr('y', function(d) { return y1(d.name); })
            .attr('width', function(d) { return xLeft(d.value) - 2; })
            .attr('fill', function(d) { return colorMale(d.name); })
            .attr('stroke',function(d) { return d.name == 'current' ? '#000000' : orange; });

          left.append('text')
            .attr('dx',function(d) { return sideWidth - xLeft(d.value) - 15; })
            .attr('dy',function(d) { return y1.bandwidth() / 2 + 4; })
            .attr('font-size','10px')
            .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

          var centerBoxes = svg.selectAll('g.center')
              .data(labels)
            .enter().append('g')
              .attr('transform',function(d) { return 'translate(' + (leftOffset - 1) + ',' + (y0(d.key) + 1) + ')' })
              .attr('class','center');

          centerBoxes.append('rect')
            .attr('class','box')
            .attr('width',70)
            .attr('height',34);

          centerBoxes.append('text')
            .attr('class','label')
            .attr('dx', 35)
            .attr('dy', 17.5)
            .attr('font-size','11px')
            .text(function(d) { return d.label; });

          var legend = svg.append('svg')
              .attr('class','legend')
              //.attr('transform','translate(' + (width / 2 - 108) + ',' + (figureHeight - 124) + ')')
              .attr('x',width / 2 - 75)
              .attr('y',figureHeight - 105)
              .attr('width',150)
              .attr('height',105);

          legend.append('image')
            .attr('xlink:href','/static/img/man-icon.png')
            .attr('x',5)
            .attr('y',0)
            .attr('height',74)
            .attr('width',40);

          legend.append('image')
            .attr('xlink:href','/static/img/woman-icon.png')
            .attr('x',105)
            .attr('y',0)
            .attr('height',74)
            .attr('width',40);

          legend.append('rect')
            .attr('fill',orange)
            .attr('width',40)
            .attr('height',20)
            .attr('x',55)
            .attr('y',20);

          legend.append('text')
            .attr('class','male')
            .text(2015)
            .attr('dx',8)
            .attr('dy',91);

          legend.append('text')
            .attr('class','female')
            .text(2015)
            .attr('dx',107)
            .attr('dy',91);

          legend.append('text')
            .attr('class','previous')
            .text(2014)
            .attr('dx',57)
            .attr('dy',60);

          legend.append()
        }
      });
    }
  }
}

$(function() {
  var Poster = new Umibukela.Poster();

  Poster.init();
});
