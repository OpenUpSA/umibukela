Umibukela.Poster = function() {
  var self = this;

  self.init = function() {
    self.draw();
  }

  self.ORANGE = '#f6921d';
  self.BLACK = '#000000';
  self.WHITE = '#ffffff';

  self.colorFemale = d3.scaleOrdinal()
    .range([self.BLACK,self.ORANGE]);
  self.colorMale = d3.scaleOrdinal()
    .range(['#ffffff',self.ORANGE]);

  self.drawChart = function(options) {
    switch(options.type) {
      case '1':
        self.charts.typeOne(options);
      break;
      case '2':
        self.charts.typeTwo(options);
      break;
    }
  }

  self.charts = {
    typeOne: function(options) {
      var response = options.el;
      var height = options.height;
      var width = options.width;
      var figureHeight = height * .75;
      var labelWidth = Math.floor(width / 5) - 3;
      var sideWidth = (width - labelWidth) / 2;
      var rightOffset = width / 2 + labelWidth / 2;
      var leftOffset = width / 2 - labelWidth / 2;
      var fontSize = height / 32;
      var icon = {
        height: height / 8,
        width: width / 13
      };
      var male_data = [];
      var female_data = [];
      var labels = [];
      var optionTypes = options.optionTypes;
      var colorMale = self.colorMale;
      var colorFemale = self.colorFemale;
      var margin = options.margin;

      options.responses.forEach(function(response) {
        var key = response.current.key;
        var label = response.current.label;

        male_data.push({ name: 'current', value: response.current.count.male, label: key });
        female_data.push({ name: 'current', value: response.current.count.female, label: key });

        if(response.prev) {
            male_data.push({ name: 'prev', value: response.prev.count.male, label: key });
            female_data.push({ name: 'prev', value: response.prev.count.female, label: key });
        }

        labels.push({ key: key, label: label });
      });

      male_data.reverse();
      female_data.reverse();

      var rightMax = d3.max(female_data.map(function(d) { return d.value }));
      var leftMax = d3.max(male_data.map(function(d) { return d.value }));

      var y0 = d3.scaleBand()
        .domain(male_data.map(function(d) { return d.label; }))
        .rangeRound([0, figureHeight])
        .paddingInner(0.2)
        .paddingOuter(0);
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
        .attr('height',height)
        .attr('width',width + margin.left + margin.right)
      .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      var right = svg.selectAll('g.right')
        .data(female_data)
      .enter().append('g')
        .attr('transform', function(d) { return 'translate(' + rightOffset + ',' + (y0(d.label) + 1) + ')'; })
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
        .attr('fill', function(d) { ;return colorFemale(d.name); })
        .attr('stroke',function(d) { return d.name == 'current' ? self.BLACK : self.ORANGE; });

      right.append('text')
        .attr('dx',function(d) { return xRight(d.value) + 5; })
        .attr('dy',function(d) { return y1.bandwidth() / 2 + parseFloat(fontSize) / 2; })
        .attr('font-size',fontSize)
        .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

      var left = svg.selectAll('g.left')
        .data(male_data)
      .enter().append('g')
        .attr('transform', function(d) { return 'translate(0,' + (y0(d.label) + 1) + ')'; })
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
        .attr('width', function(d) { return xLeft(d.value); })
        .attr('fill', function(d) { return colorMale(d.name); })
        .attr('stroke',function(d) { return d.name == 'current' ? self.BLACK : self.ORANGE; });

      left.append('text')
        .attr('dx',function(d) { return sideWidth - xLeft(d.value) - 20; })
        .attr('dy',function(d) { return y1.bandwidth() / 2 + 4; })
        .attr('font-size',fontSize)
        .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

      var labelOffset = 0;

      var centerBoxes = svg.selectAll('g.center')
          .data(labels)
        .enter().append('g')
          .attr('transform',function(d, i) {
            if(i == labels.length - 1) labelOffset = y0(d.key);

            return 'translate(' + leftOffset + ',' + y0(d.key) + ')';
          })
          .attr('class','center');

      centerBoxes.append('rect')
        .attr('class','box')
        .attr('width',labelWidth)
        .attr('height',y0.bandwidth());

      centerBoxes.append('text')
          .attr('class','label')
          .attr('x',labelWidth / 2)
          .attr('y',labelOffset)
          .text(function(d) { return d.label; })
          .call(self.wrap, labelWidth - 6, fontSize, y0.bandwidth());

      var legend = svg.append('g')
          .attr('class','legend')
          .attr('transform','translate(' + (width / 2 - 75) + ',' + (figureHeight + 10) + ')');

      legend.append('image')
        .attr('xlink:href','/static/img/man-icon.png')
        .attr('x',5)
        .attr('y',0)
        .attr('height',icon.height)
        .attr('width',icon.width);

      legend.append('image')
        .attr('xlink:href','/static/img/woman-icon.png')
        .attr('x',105)
        .attr('y',0)
        .attr('height',icon.height)
        .attr('width',icon.width);

      legend.append('rect')
        .attr('fill',self.ORANGE)
        .attr('width',20)
        .attr('height',15)
        .attr('x',65)
        .attr('y',20);

      legend.append('text')
        .attr('class','male')
        .text(2015)
        .attr('dx',13)
        .attr('dy',55)
        .attr('font-size',fontSize);

      legend.append('text')
        .attr('class','female')
        .text(2015)
        .attr('dx',112)
        .attr('dy',55)
        .attr('font-size',fontSize);

      legend.append('text')
        .attr('class','previous')
        .text(2014)
        .attr('dx',62)
        .attr('dy',47 )
        .attr('font-size',fontSize);
    },
    typeTwo: function(options) {
      var responses = options.responses;
      var response = options.el;
      var male_data = [];
      var female_data = [];
      var height = options.height;
      var width = options.width;
      var legendWidth = 50;
      var gutter = 70;
      var colWidth = (width - legendWidth - gutter) / 2;
      var optionTypes = options.optionTypes;
      var optionKeys = Object.keys(options.responses[0]);
      var labels = [];
      var legendLabels = [];
      var male_data = [];
      var female_data = [];
      var years = [2014,2015];
      var icon = { width: width / 10, height: height / 5 };
      var colorMale = self.colorMale;
      var colorFemale = self.colorFemale;
      var margin = options.margin;
      var figureHeight = height * .8;
      var figureWidth = width * .8;
      var legendType = options.legendType;
      var legendIcon = {
        height: height / 10,
        width: width / 10
      };
      var legendFontSize = legendIcon.width * .6;
      var labelFontSize = width / 20;
      var legendFormat = options.legendFormat;

      optionTypes.reverse();

      for(var i=0;i < optionKeys.length;i++) {
        var period = optionKeys[i];

        male_data.push({ period: period, year: period == 'current' ? years[1] : years[0] });
        female_data.push({ period: period, year: period == 'current' ? years[1] : years[0] });
      }

      male_data.reverse();
      female_data.reverse();

      responses.forEach(function(response, i) {
        for(period in response) {
          var male_datum = male_data.find(function(item) { return item.period == period });
          var female_datum = female_data.find(function(item) { return item.period == period });
          var key = response[period].key;
          var label = response[period].label;

          if(key) labels.push(key);
          if(!legendLabels.includes(label)) legendLabels.push(label);

          male_datum[labels[i]] = response[period].count.male;
          female_datum[labels[i]] = response[period].count.female;
        }
      });

      // Range depends on number of response types
      var zRange;

      if(legendType == 'yes/no') {
        zRange = [self.BLACK,self.ORANGE];
      } else {
        zRange = [self.BLACK,self.WHITE,self.ORANGE];

        switch(legendType) {
          case 'attitude':
            labels.reverse();
          break;
          case 'yes/dk/no':
            labels = [labels[1],labels[2],labels[0]];
            legendLabels = labels;
          break;
        }
      }

      male_data.forEach(function(d) {
        d.total = 0;

        labels.forEach(function(label) {
          d.total += d[label];
        });
      });

      female_data.forEach(function(d) {
        d.total = 0;

        labels.forEach(function(label) {
          d.total += d[label];
        });
      });

      var max = d3.max(male_data.concat(female_data).map(function(d) { return d.total; }));

      var male_stack = d3.stack().keys(labels)(male_data);
      var female_stack = d3.stack().keys(labels)(female_data);

      var svg = response.append('svg')
        .attr('height',height + margin.bottom)
        .attr('width',width + margin.right + margin.left)
      .append('g')
        .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

      function setupBands(el, selector, className, data) {
        return el.append('g')
          .attr('transform',function() {
            if(legendFormat == 'bar') return 'translate(0,' + legendHeight + ')';
            else return 'translate(0,0)';
          })
          .selectAll(selector)
            .data(data)
          .enter().append('g')
            .attr('class',className)
            .attr('fill',function(d) { return z(d.key); })
            .attr('stroke',function(d) { return z(d.key) == self.WHITE ? self.BLACK : z(d.key); });
      }

      function setupRect(el, addedShift) {
        if(!addedShift) addedShift = 0;

        return el.selectAll('rect')
            .data(function(d) { return d; })
          .enter().append('rect')
            .attr('x', function(d) {
              var period = d.data.period;
              var shift = 0;

              if(period == 'current') shift = .9 * x.bandwidth();

              return legendWidth + x(d.data.period) - shift + addedShift;
            })
            .attr('y', function(d) { return y(d[1]); })
            .attr('height', function(d) { return y(d[0]) - y(d[1]); })
            .attr('width', function(d) {
              var period = d.data.period;
              var coefficient = period == 'current' ? 1.9 : .1;

              return x.bandwidth() * coefficient;
            });
      }

      function setupCount(el, shift) {
        if(!shift) shift = 0;

        return el.selectAll('text.count')
            .data(function(d) { return d; })
          .enter().append('text')
            .attr('class','count')
            .attr('y',function(d) { return y(d[1]) + Math.abs(y(d[1]) - y(d[0])) / 2; })
            .attr('x',shift)
            .attr('fill',self.BLACK)
            .attr('stroke','none')
            .attr('font-size','10px')
            .text(function(d) { return d.data.period == 'current' && d[1] - d[0] > 0 ? d[1] - d[0] : ''; });
      }

      function setupLabels(el, labels, addedShift) {
        if(!addedShift) addedShift = 0;

        return el.selectAll('text.year')
            .data(labels)
          .enter().append('text')
            .attr('class','year')
            .attr('x',function(d,i) { return addedShift + (x.bandwidth() * 2) * i + icon.width + width / 10; })
            .attr('y',figureHeight + 20)
            .attr('fill',self.BLACK)
            .attr('stroke','none')
            .attr('font-size',labelFontSize)
            .text(function(d) { return d; });
      }

      function drawLegend(svg, type, format, labels) {
        var legend = svg.append('g')
          .attr('transform','translate(0,0)')
          .attr('class','legend');

        switch(type) {
          case 'yes/no':
            legend.append('rect')
              .attr('fill',self.BLACK)
              .attr('height',legendIcon.height)
              .attr('width',legendIcon.width)
              .attr('x',0)
              .attr('y',0);

            legend.append('rect')
              .attr('fill',self.ORANGE)
              .attr('height',legendIcon.height)
              .attr('width',legendIcon.width)
              .attr('y',legendIcon.height + height / 20)
              .attr('x',0);

            legend.append('text')
              .attr('x',40)
              .attr('y',legendIcon.height / 1.5)
              .attr('font-size',legendFontSize)
              .text('YES');

            legend.append('text')
              .attr('x',40)
              .attr('y',legendIcon.height / 1.5 + legendIcon.height + height / 20)
              .attr('font-size',legendFontSize)
              .text('NO');
          break;
          case 'yes/dk/no':
          zRange.reverse().forEach(function(color,i) {
            legend.append('rect')
              .attr('fill',color)
              .attr('height',legendIcon.height)
              .attr('width',legendIcon.width)
              .attr('stroke',function() { return color == self.WHITE ? self.BLACK : color })
              .attr('x',0)
              .attr('y',i * (legendIcon.height + height / 20));
          });

          labels.forEach(function(label,i) {
            legend.append('text')
              .attr('x',40)
              .attr('y',legendIcon.height / 1.5 + i * (legendIcon.height + height / 20))
              .attr('font-size',legendFontSize)
              .text(label.toUpperCase());
          });
          break;
          case 'attitude':
            // Default to vertical alignment
            var icons = ['/static/img/negative_face.png','/static/img/neutral_face.png','/static/img/positive_face.png'];
            var labelWidth = format == 'bar' ? figureWidth / 3 : 0;
            var data = [];

            icons.forEach(function(icon, i) {
              data.push({ icon: icon, label: labels[i] });
            });

            var g = legend.selectAll('g')
                .data(data)
              .enter().append('g')
                .attr('transform', function(d, i) {
                  var iconOffset = format == 'bar' ? i * labelWidth : i * (legendIcon.height + height / 20);
                  console.log('icon offset',iconOffset);

                  if(format == 'bar') {
                    return 'translate(' + iconOffset + ',' + 0 + ')';
                  } else {
                    return 'translate(' + 0 + ',' + iconOffset + ')';
                  }
                });


            g.append('image')
              .attr('xlink:href',function(d) { return d.icon })
              .attr('width',legendIcon.height)
              .attr('height',legendIcon.width)
              .attr('dy',0)
              .attr('dx',0);

            g.append('text')
              .attr('font-size',legendFontSize)
              .attr('x',legendIcon.width + width / 20)
              .attr('y',(legendIcon.height - legendFontSize) / 2)
              .text(function(d) { return d.label })
              .call(self.wrap, labelWidth * .8, legendFontSize, 0);
          break;
        }

        return legend;
      }

      function drawIcon(el, href, xShift) {
        if(!xShift) xShift = 0;

        return el.append('image')
          .attr('xlink:href',href)
          .attr('x',xShift)
          .attr('y',figureHeight - icon.height / 2)
          .attr('height',icon.height)
          .attr('width',icon.width);
      }

      var legend = drawLegend(svg, legendType, legendFormat, legendLabels);
      var legendHeight = legend.node().getBBox().height;

      if(legendType == 'bar') figureHeight = height - legendHeight;

      var x = d3.scaleBand()
        .domain(optionTypes)
        .rangeRound([0, colWidth])
        .padding(0.2);
      var y = d3.scaleLinear()
        .domain([0, max])
        .range([figureHeight,0]);
      var z = d3.scaleOrdinal()
        .domain(labels)
        .range(zRange);

      var male = setupBands(svg, '.male', 'male', male_stack);
      var female = setupBands(svg, '.female', 'female', female_stack);
      var maleRect = setupRect(male);
      var femaleRect = setupRect(female, colWidth + gutter);
      var maleCount = setupCount(male, colWidth + legendWidth - 2);
      var femaleCount = setupCount(female, legendWidth + colWidth * 2 + gutter);
      var maleLabels = setupLabels(male, years);
      var femaleLabels = setupLabels(female, years, colWidth + gutter);
      var maleIcon = drawIcon(svg, '/static/img/man-icon.png');
      var femaleIcon = drawIcon(svg, '/static/img/woman-icon.png', legendWidth + colWidth + gutter / 2);

      svg.append('line')
        .attr('x1',legendWidth + colWidth + gutter / 3)
        .attr('x2',legendWidth + colWidth + gutter / 3)
        .attr('y1',0)
        .attr('y2',figureHeight + labelFontSize)
        .attr('height',figureHeight)
        .attr('width',1)
        .attr('stroke',self.BLACK)
        .attr('stroke-dasharray','2,3');
    }
  }

  self.wrap = function(textNodes, width, fontSize, boxHeight) {
    textNodes.each(function() {
      var text = d3.select(this),
          words = text.text().split(/\s+/).reverse(),
          word,
          line = [],
          lineNumber = 0,
          lineHeight = 1.1,
          x = parseFloat(text.attr('x')) || 0,
          y = parseFloat(text.attr('y')) || 0;
      var textHeight = text.node().getBBox().height;

      if(!!boxHeight) y += (boxHeight - textHeight) / 2;

      var tspan = text.text(null).append('tspan').attr('x',x).attr('y',y).attr('font-size',fontSize);
      text.attr('x',0).attr('y',0);
      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(' '));
        if (tspan.node().getComputedTextLength() > width && line.length > 1) {
          var offset = !!boxHeight ? fontSize / 2 : 0;
          line.pop();
          //tspan.text(line.join(' ')).attr('y',y - offset);
          line = [word];
          tspan = text.append('tspan').attr('x',x).attr('y', ++lineNumber * fontSize * lineHeight + y - offset).attr('font-size',fontSize).text(word);
        }
      }
    });
  }

  self.draw = function() {
    if(!!questions) {
      var responses = d3.selectAll('.response');
      var margin = { top: 15, right: 20, bottom: 15, left: 20 };

      responses.each(function(d,i) {
        var response = d3.select(this);
        var key = response.attr('data-key');
        if(key) {
          var options = {};

          options.el = response;
          options.type = response.attr('data-type');
          options.legendType = response.attr('data-legend');
          options.responses = questions[key].options;
          options.optionTypes = options.responses[0] ? Object.keys(options.responses[0]) : [];
          options.margin = {
            top: parseFloat(response.attr('data-margin-top')) || 10,
            right: parseFloat(response.attr('data-margin-right')) || 10,
            bottom: parseFloat(response.attr('data-margin-bottom')) || 10,
            left: parseFloat(response.attr('data-margin-left')) || 10
          };
          options.height = parseInt(response.attr('data-height'));
          options.width = parseInt(response.attr('data-width'));
          options.legendFormat = response.attr('data-legend-format');
          options.figureHeight = options.height - margin.top - margin.bottom;
          options.key = key;
          self.drawChart(options);
        }
      });
    }
  }
}

$(function() {
  var Poster = new Umibukela.Poster();

  Poster.init();
});
