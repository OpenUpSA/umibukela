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
          var optionTypes = options[0] ? Object.keys(options[0]) : [];
          var labels = [];

          if(type == '1') {
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
              .domain(optionTypes)
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
          } else if(type == '2') {
            var width = 340;
            var legendWidth = 50;
            var gutter = 70;
            var colWidth = (width - legendWidth - gutter) / 2;
            var optionKeys = Object.keys(options[0]);
            var labels = [];
            var male_data = [];
            var female_data = [];
            var years = [2014,2015];
            var icon = { width: 40, height: 175 };

            optionTypes.reverse();

            for(var i=0;i < optionKeys.length;i++) {
              var type = optionKeys[i];

              male_data.push({ type: type, year: type == 'current' ? years[1] : years[0] });
              female_data.push({ type: type, year: type == 'current' ? years[1] : years[0] });
            }

            male_data.reverse();
            female_data.reverse();

            options.forEach(function(option) {
              for(type in option) {
                var male_datum = male_data.find(function(item) { return item.type == type });
                var female_datum = female_data.find(function(item) { return item.type == type });

                if(option[type].key) labels.push(option[type].key);

                male_datum[option[type].label.toLowerCase()] = option[type].count.male;
                female_datum[option[type].label.toLowerCase()] = option[type].count.female;
              }
            });

            male_data.forEach(function(d) {
              d.total = d.yes + d.no;
            });

            female_data.forEach(function(d) {
              d.total = d.yes + d.no;
            });

            var max = d3.max(male_data.concat(female_data).map(function(d) { return d.total; }));

            var x = d3.scaleBand()
              .domain(optionTypes)
              .rangeRound([0, colWidth])
              .padding(0.2);
            var y = d3.scaleLinear()
              .domain([0, max])
              .range([height,0]);
            var z = d3.scaleOrdinal()
              .domain(labels)
              .range(['#00000',orange]);

            var male_stack = d3.stack().keys(labels)(male_data);
            var female_stack = d3.stack().keys(labels)(female_data);

            var svg = response.append('svg')
              .attr('height',figureHeight)
              .attr('width',width + margin.left + margin.right)
            .append('g')
              .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

            var male = svg.selectAll('.male')
                .data(male_stack)
              .enter().append('g')
                .attr('class','male')
                .attr('fill',function(d) { return z(d.key); });

            male.selectAll('rect')
                .data(function(d) { return d; })
              .enter().append('rect')
                .attr('x', function(d) {
                  var type = d.data.type;
                  var shift = 0;

                  if(type == 'current') shift = .9 * x.bandwidth();

                  return legendWidth + x(d.data.type) - shift;
                })
                .attr('y', function(d) { return y(d[1]); })
                .attr('height', function(d) { return y(d[0]) - y(d[1]); })
                .attr('width', function(d) {
                  var type = d.data.type;
                  var coefficient = type == 'current' ? 1.9 : .1;

                  return x.bandwidth() * coefficient;
                });

            male.selectAll('text.count')
                .data(function(d) { return d; })
              .enter().append('text')
                .attr('class','count')
                .attr('y',function(d) { return y(d[1]) + Math.abs(y(d[1]) - y(d[0])) / 2; })
                .attr('x',colWidth + legendWidth - 5)
                .attr('fill','#000')
                .attr('font-size','10px')
                .text(function(d) { return d.data.type == 'current' ? d[1] - d[0] : ''; });

            male.selectAll('text.year')
                .data(years)
              .enter().append('text')
                .attr('class','year')
                .attr('x',function(d,i) { return (x.bandwidth() * 1.25) * i + icon.width + 23; })
                .attr('y',height + 20)
                .attr('fill','#000')
                .text(function(d) { return d; });

            var female = svg.selectAll('.female')
                .data(female_stack)
              .enter().append('g')
                .attr('class','female')
                .attr('fill',function(d) { return z(d.key); });

            female.selectAll('rect')
                .data(function(d) { return d; })
              .enter().append('rect')
                .attr('x', function(d) {
                  var type = d.data.type;
                  var shift = 0;

                  if(type == 'current') shift = .9 * x.bandwidth();

                  return legendWidth + colWidth + gutter + x(d.data.type) - shift;
                })
                .attr('y', function(d) { return y(d[1]); })
                .attr('height', function(d) { return y(d[0]) - y(d[1]); })
                .attr('width', function(d) {
                  var type = d.data.type;
                  var coefficient = type == 'current' ? 1.9 : .1;

                  return x.bandwidth() * coefficient;
                });

            female.selectAll('text.count')
                .data(function(d) { return d; })
              .enter().append('text')
                .attr('class','count')
                .attr('y',function(d) { return y(d[1]) + Math.abs(y(d[1]) - y(d[0])) / 2; })
                .attr('x',colWidth * 2 + gutter + x.bandwidth() + 5)
                .attr('fill','#000')
                .attr('font-size','10px')
                .text(function(d) { return d.data.type == 'current' ? d[1] - d[0] : ''; });

            female.selectAll('text.year')
                .data(years)
              .enter().append('text')
                .attr('class','year')
                .attr('x',function(d,i) { return colWidth + gutter + (x.bandwidth() * 1.25) * i + icon.width + 23; })
                .attr('y',height + 20)
                .attr('fill','#000')
                .text(function(d) { return d; });

            svg.append('line')
              .attr('x1',legendWidth + colWidth + gutter / 3)
              .attr('x2',legendWidth + colWidth + gutter / 3)
              .attr('y1',0)
              .attr('y2',height)
              .attr('height',height)
              .attr('width',1)
              .attr('stroke','#000')
              .attr('stroke-dasharray','2,3');

              svg.append('image')
                .attr('xlink:href','/static/img/man-icon.png')
                .attr('x',0)
                .attr('y',max)
                .attr('height',icon.height)
                .attr('width',icon.width);

              svg.append('image')
                .attr('xlink:href','/static/img/woman-icon.png')
                .attr('x',legendWidth + colWidth + gutter / 2)
                .attr('y',max)
                .attr('height',icon.height)
                .attr('width',icon.width);

            var legend = svg.append('g')
              .attr('class','legend');

            legend.append('rect')
              .attr('fill','#000000')
              .attr('height',30)
              .attr('width',30);

            legend.append('rect')
              .attr('fill',orange)
              .attr('height',30)
              .attr('width',30)
              .attr('y',40);

            legend.append('text')
              .attr('x',40)
              .attr('y',20)
              .text('YES');

            legend.append('text')
              .attr('x',40)
              .attr('y',60)
              .text('NO');

          }
        }
      });
    }
  }
}

$(function() {
  var Poster = new Umibukela.Poster();

  Poster.init();
});
