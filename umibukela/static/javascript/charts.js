var PrintMaterials = function() {
  var self = this;

  self.init = function() {
    self.draw();
  }

  self.ORANGE = '#f6921d';
  self.BLACK = '#000000';
  self.WHITE = '#ffffff';
  self.RED = '#c9423f';
  self.BLUE = '#1561db';
  self.PINK = '#ff4da6';

  self.colorFemale = d3.scaleOrdinal()
    .range([self.BLACK,self.ORANGE]);
  self.colorMale = d3.scaleOrdinal()
    .range([self.WHITE,self.ORANGE]);

  self.drawChart = function(options) {
    switch(options.type) {
      case '1':
        self.charts.typeOne(options);
      break;
      case '2':
        self.charts.typeTwo(options);
      break;
      case '3':
        self.charts.typeThree(options);
      break;
      case '4':
        self.charts.typeFour(options);
      break;
      case '5':
        self.charts.typeFive(options);
      break;
      case '6':
        self.charts.typeSix(options);
      break;
      case '7':
        self.charts.typeSeven(options);
      break;
      case '8':
        self.charts.typeEight(options);
      break;
      case '9':
        self.charts.typeNine(options);
      break;
      case '10':
        self.charts.typeTen(options);
      break;
    }
  }

  self.charts = {
    typeOne: function(options) {
      var response = options.el;
      var height = options.height;
      var width = options.width;
      var margin = options.margin;
      var optionKeys = options.optionKeys;

      var labelWidth = Math.floor(width / 5) - 3;
      var sideWidth = (width - labelWidth) / 2;
      var rightOffset = width / 2 + labelWidth / 2 + 1;
      var leftOffset = width / 2 - labelWidth / 2;
      var fontSize = height / 32;
      var legendWidth = width / 2.5;
      var gutter = height / 13;
      var icon = {
        height: height / 7,
        width: width / 12
      };
      var maleData = [];
      var femaleData = [];
      var labels = [];

      var colorMale = self.colorMale;
      var colorFemale = self.colorFemale;

      options.responses.forEach(function(response) {
        var key = response.current.key;
        var label = response.current.label;

        maleData.push({ name: 'current', value: response.current.count.male, label: key });
        femaleData.push({ name: 'current', value: response.current.count.female, label: key });

        if(response.prev) {
            maleData.push({ name: 'prev', value: response.prev.count.male, label: key });
            femaleData.push({ name: 'prev', value: response.prev.count.female, label: key });
        }

        labels.push({ key: key, label: label.toUpperCase() });
      });

      labels.reverse();

      var rightMax = d3.max(femaleData.map(function(d) { return d.value }));
      var leftMax = d3.max(maleData.map(function(d) { return d.value }));
      var max = rightMax > leftMax ? rightMax : leftMax;

      var svg = response.append('svg')
        .attr('height',height)
        .attr('width',width)
      .append('g');

      // Create legend first so that its height can be subtracted from figureHeight
      var legend = svg.append('g')
          .attr('class','legend');

      legend.append('image')
        .attr('xlink:href','/static/img/man-icon.png')
        .attr('x',0)
        .attr('y',0)
        .attr('height',icon.height)
        .attr('width',icon.width);

      legend.append('image')
        .attr('xlink:href','/static/img/woman-icon.png')
        .attr('x',legendWidth - icon.width)
        .attr('y',0)
        .attr('height',icon.height)
        .attr('width',icon.width);

      legend.append('rect')
        .attr('fill',self.ORANGE)
        .attr('width',icon.width)
        .attr('height',icon.height / 2)
        .attr('x',legendWidth / 2 - icon.width / 2)
        .attr('y',icon.height / 2);

      var figureHeight = height - legend.node().getBBox().height - gutter;

      legend.attr('transform','translate(' + ((width - legendWidth) / 2) + ',' + figureHeight + ')');

      var y0 = d3.scaleBand()
        .domain(maleData.map(function(d) { return d.label; }))
        .rangeRound([0, figureHeight])
        .paddingInner(0.2)
        .paddingOuter(0)
        .align(0);
      var y1 = d3.scaleBand()
        .domain(optionKeys)
        .rangeRound([0.25, y0.bandwidth()])
        .padding(0);
      var xRight = d3.scaleLinear()
        .domain([0,max])
        .range([0,sideWidth - 20]);
      var xLeft = d3.scaleLinear()
        .domain([0,max])
        .range([0,sideWidth - 20]);

      var right = svg.selectAll('g.right')
        .data(femaleData)
      .enter().append('g')
        .attr('transform', function(d) { return 'translate(' + rightOffset + ',' + y0(d.label) + ')'; })
        .attr('class','right');

      var scalingFactor = 1;
      var isTwoPeriods = _.contains(optionKeys,'prev');

      right.append('rect')
        .attr('height', function(d) {
          var barHeight = y1.bandwidth();

          if(d.name == 'prev') {
            scalingFactor = 1 / 3;
          } else if(isTwoPeriods && d.name == 'current') {
            scalingFactor = 5 / 3;
          }

          return barHeight * scalingFactor;
        })
        .attr('y', function(d) {
          if(d.name == 'prev') return y1(d.name) * 5 / 3;
          else return y1(d.name) - 0.5;
        })
        .attr('width', function(d) { return xRight(d.value) - 0.5; })
        .attr('fill', function(d) { ;return colorFemale(d.name); })
        .attr('stroke',function(d) { return d.name == 'current' ? self.BLACK : self.ORANGE; })
        .attr('stroke-width','0.25');

      right.append('text')
        .attr('x',function(d) { return xRight(d.value) + 2.5; })
        .attr('y',function(d) {
          var barWidth = y1.bandwidth();

          if(isTwoPeriods) barWidth *= 5 / 3;

          return (barWidth - fontSize) / 2 + fontSize;
        })
        .attr('font-size',fontSize)
        .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

      var left = svg.selectAll('g.left')
        .data(maleData)
      .enter().append('g')
        .attr('transform', function(d) { return 'translate(0,' + y0(d.label) + ')'; })
        .attr('class','left');

      scalingFactor = 1;

      left.append('rect')
        .attr('height', function(d) {
          var barHeight = y1.bandwidth();

          if(d.name == 'prev') {
            scalingFactor = 1 / 3;
          } else if(_.contains(optionKeys,'prev')) {
            scalingFactor = 5 / 3;
          }

          return barHeight * scalingFactor;
        })
        .attr('x',function(d) { return sideWidth - xLeft(d.value); })
        .attr('y', function(d) {
          if(d.name == 'prev') return y1(d.name) * 5 / 3;
          else return y1(d.name) - 0.4;
        })
        .attr('width', function(d) { return xLeft(d.value) - 0.5; })
        .attr('fill', function(d) { return colorMale(d.name); })
        .attr('stroke',function(d) { return d.name == 'current' ? self.BLACK : self.ORANGE; })
        .attr('stroke-width', '0.4');

      var count = left.append('text')
        .attr('y',function(d) {
          var barWidth = y1.bandwidth();

          if(isTwoPeriods) barWidth *= 5 / 3;

          return (barWidth - fontSize) / 2 + fontSize;
        })
        .attr('font-size',fontSize)
        .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

      count.attr('x',function(d) { return sideWidth - xLeft(d.value) - d3.select(this).node().getBBox().width - 5; });

      var labelOffset = y0.paddingInner();

      var centerBoxes = svg.selectAll('g.center')
          .data(labels)
        .enter().append('g')
          .attr('transform',function(d, i) {
            return 'translate(' + leftOffset + ',' + (y0(d.key) + 0.25) + ')';
          })
          .attr('class','center');

      centerBoxes.append('rect')
        .attr('class','box')
        .attr('width',labelWidth)
        .attr('height',y0.bandwidth());

      centerBoxes.append('text')
          .attr('class','label')
          .attr('x',labelWidth / 2)
          .attr('y',labelOffset + 4)
          .text(function(d) { return d.label; })
          .call(self.wrap, labelWidth - 6, y0.bandwidth() - y0.paddingInner(), fontSize);

      var maleLabel = legend.append('text')
        .attr('class','male-label')
        .text(2015)
        .attr('font-size',fontSize);

      maleLabel.attr('x',maleLabel.node().getBBox().width / 2)
        .attr('y',icon.height + maleLabel.node().getBBox().height);

      var femaleLabel = legend.append('text')
        .attr('class','female-label')
        .text(2015)
        .attr('font-size',fontSize);

      femaleLabel.attr('x',legendWidth - femaleLabel.node().getBBox().width - femaleLabel.node().getBBox().width / 2.5)
      .attr('y',icon.height + femaleLabel.node().getBBox().height);

      var prevLabel = legend.append('text')
        .attr('class','prev-label')
        .text(2014)
        .attr('font-size',fontSize);

      prevLabel.attr('x',legendWidth / 2 - prevLabel.node().getBBox().width / 2)
        .attr('y',icon.height + prevLabel.node().getBBox().height)
    },
    typeTwo: function(options) {
      var responses = options.responses;
      var response = options.el;
      var height = options.height;
      var width = options.width;
      var margin = options.margin;
      var legendType = options.legendType;
      var legendFormat = options.legendFormat;
      var optionKeys = options.optionKeys;

      var maleData = [];
      var femaleData = [];
      var labels = [];
      var legendLabels = [];

      var isBar = legendFormat == 'top-bar' || legendFormat == 'bottom-bar';

      var figureHeight = options.figureHeight || height * .75;
      var figureWidth = width * .8;
      var legendWidth = width * .22;
      var legendHeight = height * .2;
      var gutter = figureWidth * .2;
      var labelIcon = {
        width: width / 10,
        height: height / 5
      };
      var legendIcon = {
        height: (height + width) / 25,
        width: (height + width) / 25
      };
      var legendFontSize = width / 30;
      var labelFontSize = width / 30;
      var colWidth = isBar ? (figureWidth - gutter) / 2 : (figureWidth - gutter - legendWidth) / 2;
      var years = cycleYears;
      var hasTwoPeriods = _.contains(optionKeys,'current') && _.contains(optionKeys,'prev');

      optionKeys.reverse();

      for(var i=0;i < optionKeys.length;i++) {
        var period = optionKeys[i];

        maleData.push({ period: period, year: period == 'current' ? years[1] : years[0] });
        femaleData.push({ period: period, year: period == 'current' ? years[1] : years[0] });
      }

      responses.forEach(function(response, i) {
        for(period in response) {
          var male_datum = _.find(maleData, function(item) { return item.period == period });
          var female_datum = _.find(femaleData, function(item) { return item.period == period });
          var key = response[period].key;
          var label = response[period].label;

          if(key) labels.push(key);
          if(!_.contains(legendLabels, label)) legendLabels.push(label);

          male_datum[labels[i]] = response[period].count.male;
          female_datum[labels[i]] = response[period].count.female;
        }
      });

      // Range depends on number of response types
      var zRange = legendType == 'yes/no' ? [self.ORANGE,self.BLACK] : [self.ORANGE,self.WHITE,self.BLACK];

      labels = legendType == 'yes/dk/no' ? [labels[1],labels[2],labels[0]] : labels;

      for(var i = 0; i < maleData.length; i++) {
        maleData[i].total = 0;
        femaleData[i].total = 0;

        labels.forEach(function(label) {
          maleData[i].total += maleData[i][label];
          femaleData[i].total += femaleData[i][label];
        });
      }

      var prevMax = d3.max(maleData.concat(femaleData).map(function(d) { if(d.period == 'prev') return d.total; }));

      if(!prevMax) {
        years = [years[1]];
      }

      var maleMax = d3.max(maleData.map(function(d) { return d.total; }));
      var femaleMax = d3.max(femaleData.map(function(d) { return d.total; }));
      var max = maleMax > femaleMax ? maleMax : femaleMax;

      maleData = self.normalize(maleData, maleMax, labels);
      femaleData = self.normalize(femaleData, femaleMax, labels);

      var maleStack = d3.stack().keys(labels)(maleData);
      var femaleStack = d3.stack().keys(labels)(femaleData);

      function setupBands(el, selector, className, data) {
        return el.append('g')
          .attr('transform',function() {
            if(legendFormat == 'top-bar') return 'translate(0,' + legendHeight + ')';
            else return 'translate(0,0)';
          })
          .selectAll(selector)
            .data(data)
          .enter().append('g')
            .attr('class',className)
            .attr('fill',function(d) { return z(d.key); })
            .attr('stroke',function(d) { return z(d.key) == self.WHITE ? self.BLACK : z(d.key); })
            .attr('stroke-width','0.25')
            .attr('transform','translate(0,0)');
      }

      function setupBars(el, gender, addedShift) {
        if(!addedShift) addedShift = 0;

        return el.selectAll('rect')
            .data(function(d) { return d; })
          .enter().append('rect')
            .attr('x', function(d) {
              var period = d.data.period;
              var periodShift = 5;

              if(hasTwoPeriods) periodShift = period == 'current' ? .9 * x.bandwidth() : 0;

              var totalShift = x(d.data.period) - periodShift + addedShift;

              return isBar ? totalShift : totalShift + legendWidth;
            })
            .attr('y', function(d) { return y(d[1]); })
            .attr('height', function(d) { return (y(d[0]) - y(d[1])); })
            .attr('width', function(d) {
              var period = d.data.period;
              var scalingFactor = 1.25;

              if(hasTwoPeriods) {
                if(period == 'current') scalingFactor = 1.9;
                else scalingFactor = .1;
              }

              return x.bandwidth() * scalingFactor;
            });
      }

      function setupCount(el, shift) {
        if(!shift) shift = 0;

        return el.selectAll('text.count')
            .data(function(d) { return d; })
          .enter().append('text')
            .attr('class','count')
            .attr('y',function(d, i) {
              var countShift = d[1] != d.data['normalized-total'] ? 5 : 0;

              return y(d[1]) + Math.abs(y(d[1]) - y(d[0])) / 2 + countShift;
            })
            .attr('x',shift)
            .attr('fill',self.BLACK)
            .attr('stroke','none')
            .attr('font-size',labelFontSize)
            .text(function(d) {
              var denormalizer = d.data['normalization-factor'] ? 1 / d.data['normalization-factor'] : 1;

              return d.data.period == 'current' && d[1] - d[0] > 0 ? Math.round((d[1] - d[0]) * denormalizer) : '';
            });
      }

      function setupLabels(el, labels, addedShift) {
        if(!addedShift) addedShift = 0;

        var labels = el.selectAll('text.year')
            .data(labels)
          .enter().append('text')
            .attr('class','year')
            .attr('y',figureHeight + legendIcon.height)
            .attr('fill',self.BLACK)
            .attr('stroke','none')
            .attr('font-size',labelFontSize)
            .text(function(d) { return d; });

        return labels.attr('x',function(d, i) {
          var periodShift = hasTwoPeriods ? -(labels.node().getBBox().width / 2 * i) : labels.node().getBBox().width / 2;

          return addedShift + (x.bandwidth() * 2) * i + periodShift;
        });
      }

      function drawLegend(svg, type, format, labels) {
        var legend = svg.append('g')
          .attr('transform','translate(0,0)')
          .attr('class','legend');

        switch(type) {
          case 'yes/no':
              var isBottomBar = format == 'bottom-bar';

              if(isBottomBar) legend.attr('transform','translate(' + (figureWidth / 3) + ',' + (figureHeight + 30) + ')');

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
              .attr('y',isBottomBar ? 0 : legendIcon.height + height / 20)
              .attr('x',isBottomBar ? legendIcon.width + 40 : 0);

            legend.append('text')
              .attr('x',legendIcon.width + 5)
              .attr('y',legendFontSize)
              .attr('font-size',legendFontSize)
              .text('YES');

            legend.append('text')
              .attr('x',isBottomBar ? legendIcon.width * 2 + 45 : legendIcon.width + 5)
              .attr('y',isBottomBar ? legendFontSize : legendIcon.height / 1.5 + legendIcon.height + height / 20)
              .attr('font-size',legendFontSize)
              .text('NO');
          break;
          case 'yes/dk/no':
          zRange.slice(0).reverse().forEach(function(color,i) {
            legend.append('rect')
              .attr('fill',color)
              .attr('height',legendIcon.height)
              .attr('width',legendIcon.width)
              .attr('stroke',function() { return color == self.WHITE ? self.BLACK : color })
              .attr('stroke-width','0.25')
              .attr('x',0)
              .attr('y',i * (legendIcon.height + height / 20));
          });

          labels.slice(0).forEach(function(label,i) {
            legend.append('text')
              .attr('x',legendIcon.width + 5)
              .attr('y',legendIcon.height / 1.5 + i * (legendIcon.height + height / 20))
              .attr('font-size',legendFontSize)
              .text(label.toUpperCase());
          });
          break;
          case 'attitude':
            // Default to vertical alignment
            var icons = ['/static/img/positive_face.svg','/static/img/neutral_face.svg','/static/img/negative_face.svg'];
            var labelWidth = format == 'top-bar' ? figureWidth / 3 : 0;
            var data = [];
            var legendLabels = labels.slice(0).reverse();

            icons.forEach(function(icon, i) {
              data.push({ icon: icon, label: legendLabels[i] });
            });

            var g = legend.selectAll('g')
                .data(data)
              .enter().append('g')
                .attr('transform', function(d, i) {
                  var iconOffset = format == 'top-bar' ? i * labelWidth : i * (legendIcon.height + 3);

                  if(format == 'top-bar') {
                    return 'translate(' + iconOffset + ',' + 0 + ')';
                  } else {
                    return 'translate(' + 0 + ',' + iconOffset + ')';
                  }
                });

            g.append('image')
              .attr('xlink:href',function(d) { return d.icon })
              .attr('width',legendIcon.width)
              .attr('height',legendIcon.height);

            g.append('text')
              .attr('font-size',legendFontSize)
              .attr('x',legendIcon.width + 3)
              .attr('y',(legendIcon.height - legendFontSize * 1.1) / 2 + legendFontSize)
              .text(function(d) { return d.label.toUpperCase() });
          break;
        }

        return legend;
      }

      function drawIcon(el, href, xShift) {
        if(!xShift) xShift = 0;

        return el.append('image')
          .attr('xlink:href',href)
          .attr('x',xShift)
          .attr('y',figureHeight - labelIcon.height / 2)
          .attr('height',labelIcon.height)
          .attr('width',labelIcon.width);
      }

      // Draw chart
      var svg = response.append('svg')
        .attr('height',height - margin.top)
        .attr('width',width - margin.right - margin.left)
      .append('g');
      var legend = drawLegend(svg, legendType, legendFormat, legendLabels);
      var legendHeight = legend.node().getBBox().height;

      if(legendType == 'top-bar' || legendType == 'bottom-bar') figureHeight = height - legendHeight;

      var x = d3.scaleBand()
        .domain(optionKeys)
        .rangeRound([0, colWidth])
        .padding(0.2);
      var y = d3.scaleLinear()
        .domain([0, max])
        .range([figureHeight,labelFontSize]);
      var z = d3.scaleOrdinal()
        .domain(labels)
        .range(zRange);

      var maleCurrentHeight = 0;
      var femaleCurrentHeight = 0;
      var malePreviousHeight = 0;
      var femalePreviousHeight = 0;

      maleStack.forEach(function(d){
        d.forEach(function(point){
          if(point.data.period == 'current') maleCurrentHeight += y(point[1]);
          else if(point.data.period == 'prev') malePreviousHeight += y(point[1]);
        });
      });

      femaleStack.forEach(function(d){
        d.forEach(function(point){
          if(point.data.period == 'current') femaleCurrentHeight += y(point[1]);
          else if(point.data.period == 'prev') femalePreviousHeight += y(point[1]);
        });
      });

      var maleBarShift = isBar ? labelIcon.width : 0;
      var femaleBarShift = isBar ? labelIcon.width + colWidth + gutter : colWidth + gutter;
      var femaleCountShift = isBar ? colWidth * 2 + gutter : legendWidth + colWidth * 2 + gutter;
      var maleCountShift = isBar ? labelIcon.width + colWidth : legendWidth + colWidth;
      var maleIconShift = isBar ? 0 : legendWidth - labelIcon.width;
      var femaleIconShift = isBar ? labelIcon.width + colWidth + gutter / 2 - 2 : legendWidth + colWidth + gutter / 2 - 2;
      var maleLabelShift = isBar ? labelIcon.width + 7 : legendWidth + 3;
      var femaleLabelShift = maleLabelShift + colWidth + gutter;
      var lineShift = isBar ? colWidth + gutter / 2 + 15 : legendWidth + colWidth + gutter / 3;

      var male = setupBands(svg, '.male', 'male', maleStack);
      var female = setupBands(svg, '.female', 'female', femaleStack);
      var maleBars = setupBars(male, 'male',maleBarShift);
      var femaleBars = setupBars(female, 'female', femaleBarShift);
      var maleCount = setupCount(male, maleCountShift);
      var femaleCount = setupCount(female, femaleCountShift);
      var maleLabels = setupLabels(male, years, maleLabelShift);
      var femaleLabels = setupLabels(female, years, femaleLabelShift);
      var maleIcon = drawIcon(svg, '/static/img/man-icon.png', maleIconShift);
      var femaleIcon = drawIcon(svg, '/static/img/woman-icon.png', femaleIconShift);

      var lastLabel = null;

      maleCount.each(function(d, i) {
          var label = d3.select(this);
          var labelY = label.attr('y');

        if(lastLabel && lastLabel.attr('y') - labelY < labelFontSize) {
          lastLabel.attr('y',labelY + labelFontSize / 2);
        }
      });

      svg.append('line')
        .attr('x1',lineShift)
        .attr('x2',lineShift)
        .attr('y1',0)
        .attr('y2',figureHeight + labelFontSize)
        .attr('height',figureHeight)
        .attr('width',1)
        .attr('stroke',self.BLACK)
        .attr('stroke-dasharray','2,3');
    },
    typeThree: function(options) {
      var responses = options.responses;
      var response = options.el;
      var height = options.height;
      var width = options.width; // 370
      var margin = options.margin;
      var optionKeys = options.optionKeys;

      var maleData = [];
      var femaleData = [];
      var labels = [];

      var gutter = height / 10 + 6;
      var colHeight = (height - gutter) / 2;
      var icon = { width: 15, height: 30 };
      var figureHeight = height * 0.8;
      var widthCoefficient = 0.8;
      var legendWidth = width * 0.2;
      var figureWidth = width * 0.8;
      var fontSize = Math.round(height / 8);
      var legendSquare = colHeight * 0.45;

      var optionKeys = _.keys(options.responses[0]);
      var years = cycleYears;
      var yearsReversed = [years[1],years[0]];
      var hasTwoPeriods = _.contains(optionKeys,'current') && _.contains(optionKeys,'prev');

      for(var i=0;i < optionKeys.length;i++) {
        var period = optionKeys[i];

        maleData.push({ period: period, year: period == 'current' ? years[1] : years[0], total: 0 });
        femaleData.push({ period: period, year: period == 'current' ? years[1] : years[0], total: 0 });
      }

      maleData.reverse();
      femaleData.reverse();

      responses.forEach(function(response) {
        if (response.prev) response.prev.key = response.current.key;

        for(period in response) {
          var male_datum = _.find(maleData, function(item) { return item.period == period; });
          var female_datum = _.find(femaleData, function(item) { return item.period == period; });

          if(response[period].key && period == 'current') labels.push(response[period].key.toLowerCase());

          male_datum[response[period].key.toLowerCase()] = response[period].count.male;
          female_datum[response[period].key.toLowerCase()] = response[period].count.female;
        }
     });

      for(var i = 0;i < maleData.length; i++) {
        labels.forEach(function(label) {
          maleData[i].total += maleData[i][label];
          femaleData[i].total += femaleData[i][label];
        });
      }

      var maleMax = d3.max(maleData.map(function(d) { return d.total; }));
      var femaleMax = d3.max(femaleData.map(function(d) { return d.total; }));
      var max = maleMax > femaleMax ? maleMax : femaleMax;
      var prevMax = d3.max(maleData.concat(femaleData).map(function(d) { if(d.period == 'prev') return d.total; }));

      if(!prevMax) {
        yearsReversed = [yearsReversed[0]];
      }

      maleData = self.normalize(maleData, maleMax, labels);
      femaleData = self.normalize(femaleData, femaleMax, labels);

      var zRange = labels.length > 2 ? [self.BLACK,self.WHITE,self.ORANGE] : [self.BLACK,self.ORANGE];

      var y = d3.scaleBand()
        .domain(optionKeys)
        .rangeRound([0, colHeight])
        .paddingInner(0.1);
      var x = d3.scaleLinear()
        .domain([0, max])
        .range([0, figureWidth]);
      var z = d3.scaleOrdinal()
        .domain(labels)
        .range(zRange);
      var femaleStack = d3.stack().keys(labels)(femaleData);
      var maleStack = d3.stack().keys(labels)(maleData);

      var svg = response.append('svg')
        .attr('height', height + 16)
        .attr('width', width + 10)
      .append('g')
        .attr('transform','translate(0,12)');

      var female = svg.selectAll('.female')
          .data(femaleStack)
        .enter().append('g')
          .attr('class','female')
          .attr('stroke',function(d) { return z(d.key) == self.WHITE ? self.BLACK : z(d.key); })
          .attr('fill',function(d) { return z(d.key); });

      var femaleBarWidth = 0;

      female.selectAll('rect')
          .data(function(d) { return d; })
        .enter().append('rect')
          .attr('y', function(d) {
            var period = d.data.period;
            var periodShift = 0;

            if(period != 'current') periodShift = .5 * y.bandwidth();

            return y(d.data.period) + periodShift;
          })
          .attr('x', function(d) { return x(d[0]) * widthCoefficient + icon.width + 5; })
          .attr('width', function(d) {
            var barWidth = Math.abs(x(d[1]) - x(d[0])) * widthCoefficient;

            if(d.data.period == 'current' && barWidth) femaleBarWidth += barWidth;

            return barWidth - 1;
          })
          .attr('height', function(d) {
            var period = d.data.period;
            var scalingFactor = 1;
            var barPadding = !hasTwoPeriods ? 0 : -2;

            if(hasTwoPeriods) scalingFactor = period == 'current' ? 1.5 : .5;

            return y.bandwidth() * scalingFactor + barPadding;
          });

      female.selectAll('text.count')
          .data(function(d) { return d; })
        .enter().append('text')
          .attr('class','count')
          .attr('stroke','none')
          .attr('x', function(d) {
            var barWidth = Math.abs(x(d[1]) - x(d[0])) ? Math.abs(x(d[1]) - x(d[0])) : 0;

            return x(d[0]) * widthCoefficient + barWidth * widthCoefficient / 2 + icon.width;
          })
          .attr('y',-2)
          .attr('fill',self.BLACK)
          .attr('font-size',fontSize)
          .attr('text-anchor','start')
          .text(function(d) { return d.data.period == 'current' && d[1] - d[0] && d[1] - d[0] > 0 ? Math.round(d[1] - d[0]) : ''; });

      female.selectAll('text.year')
          .data(yearsReversed)
        .enter().append('text')
          .attr('class','year')
          .attr('stroke','none')
          .attr('text-anchor','start')
          .attr('y', function(d,i) {
            if(hasTwoPeriods) {
              if(i == 0) return y.bandwidth();
              else return y.bandwidth() * 2;
            } else return fontSize * 2;
          })
          .attr('x', function(d) { return femaleBarWidth + icon.width + 8; })
          .attr('fill',self.BLACK)
          .attr('font-size',fontSize)
          .text(function(d) { return d; });

      var male = svg.selectAll('.male')
        .data(maleStack)
      .enter().append('g')
        .attr('class','male')
        .attr('stroke', function(d) { return z(d.key) == self.WHITE ? self.BLACK : z(d.key); })
        .attr('fill',function(d) { return z(d.key); });

      var maleBarWidth = 0;

      male.selectAll('rect')
          .data(function(d) { return d; })
        .enter().append('rect')
          .attr('y', function(d) {
            var period = d.data.period;
            var periodShift = 0;

            if(period != 'current') periodShift = .5 * y.bandwidth();
            return y(d.data.period) + periodShift + colHeight + gutter;
          })
          .attr('x', function(d) { return x(d[0]) * widthCoefficient + icon.width + 5; })
          .attr('width', function(d) {
            var barWidth = Math.abs(x(d[1]) - x(d[0])) * widthCoefficient;

            if(d.data.period == 'current' && barWidth) maleBarWidth += barWidth;

            return barWidth - 1;
          })
          .attr('height', function(d) {
            var period = d.data.period;
            var scalingFactor = 1;
            var barPadding = !hasTwoPeriods ? 0 : -2;

            if(hasTwoPeriods) scalingFactor = period == 'current' ? 1.5 : .5;

            return y.bandwidth() * scalingFactor + barPadding;
          });

      male.selectAll('text.count')
          .data(function(d) { return d; })
        .enter().append('text')
          .attr('class','count')
          .attr('stroke','none')
          .attr('x', function(d) {
            var barWidth = Math.abs(x(d[1]) - x(d[0])) ? Math.abs(x(d[1]) - x(d[0])) : 0;

            return x(d[0]) * widthCoefficient + barWidth * widthCoefficient / 2 + icon.width;
          })
          .attr('y', function(d) { return colHeight + gutter - 2; })
          .attr('fill',self.BLACK)
          .attr('font-size',fontSize)
          .text(function(d) { return d.data.period == 'current' && d[1] - d[0] && d[1] - d[0] > 0 ? Math.round(d[1] - d[0]) : ''; });

      male.selectAll('text.year')
          .data(yearsReversed)
        .enter().append('text')
          .attr('class','year')
          .attr('stroke','none')
          .attr('y', function(d,i) {
            var shift = colHeight + gutter;

            if(hasTwoPeriods) {
              if(i == 0) return shift + y.bandwidth();
              else return shift + y.bandwidth() * 2;
            } else return shift + fontSize * 2;
           })
          .attr('x', function(d) { return maleBarWidth + icon.width + 8; })
          .attr('fill',self.BLACK)
          .attr('font-size',fontSize)
          .text(function(d) { return d; });

        svg.append('image')
          .attr('xlink:href','/static/img/man-icon.png')
          .attr('x',0)
          .attr('y',colHeight + gutter)
          .attr('height',colHeight)
          .attr('width',colHeight * 0.5);

        svg.append('image')
          .attr('xlink:href','/static/img/woman-icon.png')
          .attr('x',0)
          .attr('y',0)
          .attr('height',colHeight)
          .attr('width',colHeight * 0.5);

      var legend = svg.append('g')
        .attr('class','legend');

      var legendLabels = labels.length > 2 ? ['<tspan dy="0">1</tspan><tspan font-size="' + (fontSize / 2) + '" dy="-' + (fontSize / 2) + '">st</tspan> <tspan dy="' + (fontSize / 2) + '">Visit</tspan>', '<tspan>2</tspan><tspan font-size="' + (fontSize / 2) + '" dy="-' + (fontSize / 2) + '">nd</tspan> <tspan dy="' + (fontSize / 2) + '">Visit</tspan>', '<tspan>3</tspan><tspan font-size="' + (fontSize / 2) + '" dy="-' + (fontSize / 2) + '">rd</tspan>  <tspan dy="' + (fontSize / 2) + '">Visit</tspan>'] : ['Yes','No'];

      legend.selectAll('rect')
          .data(zRange)
        .enter().append('rect')
          .attr('fill',function(d) { return d; })
          .attr('height', legendSquare)
          .attr('width', legendSquare)
          .attr('stroke', function(d) { return d == self.WHITE ? self.BLACK : ''; })
          .attr('y',function(d,i) { return (legendSquare + 5) * i; });

      var text = legend.selectAll('text')
          .data(legendLabels)
        .enter().append('text')
          .attr('x',legendSquare + 5)
          .attr('y',function(d,i) { return Math.round(height / 7) + (legendSquare + 5) * i; })
          .attr('font-size',Math.round(height / 7))
          .html(function(d) { return d.toUpperCase(); });

      var maxTextWidth = 0;

      text.each(function(d) {
        if(text.node().getBBox().width > maxTextWidth) maxTextWidth = text.node().getBBox().width;
      });

      var renderedLegendWidth = legendSquare + 5 + maxTextWidth;

      legend.attr('transform','translate(' + (width + 10 - renderedLegendWidth) + ',' + (height - labels.length * (legendSquare + 2)) + ')');
    },
    typeFour: function(options) {
      var responses = options.responses;
      var data = [];
      var response = options.el;
      var labels = [];
      var count = [];

      data.push({
        type: 'Affiliated',
        total: 0
      });

      data.push({
        type: 'Not affiliated',
        total: 0
      });

      responses.forEach(function(response){
        if(response.current) {
          if(response.current.key != 'none') {
            data[0].total += response.current.count.male;
            data[0].total += response.current.count.female;
          } else {
            data[1].total += response.current.count.male;
            data[1].total += response.current.count.female;
          }
        }

        var label = response.current.label;

        if(label !== 'none') {
          labels.push(label);
          count.push(response.current.count.male + response.current.count.female);
        }
      });

      var affiliatedTotal = data[0].total;
      var unaffiliatedTotal = data[1].total;

      var width = options.width - 10,
        height = options.height,
        radius = height / 2.5;

      var color = d3.scaleOrdinal()
        .range([self.ORANGE, self.BLACK]);

      var arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

      var pie = d3.pie()
        .sort(null)
        .value(function (d) {
          return d.total;
      });

      var svg = response.append('svg')
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(10, 0)");

        var g = svg.selectAll(".arc")
            .data(pie(data))
          .enter().append("g")
            .attr('transform','translate(' + radius + ',' + radius + ')')
            .attr("class", "arc");

        g.append("path")
          .attr("d", arc)
          .style("fill", function (d) {
            return color(d.data.type);
        });

        svg.append('line')
          .attr('x1', radius * 2)
          .attr('x2', 180)
          .attr('y1', radius)
          .attr('y2', radius)
          .attr('width',1)
          .attr('stroke',self.BLACK);

        // Legend
        var legend = svg.append('g')
          .attr('class','legend');

        legend.append('rect')
          .attr('fill',self.ORANGE)
          .attr('height',15)
          .attr('width',15);

        legend.append('rect')
          .attr('fill',self.BLACK)
          .attr('height',15)
          .attr('width',15)
          .attr('x', 80);

        legend.append('text')
          .attr('y',11)
          .attr('x', 20)
          .attr('font-size','9px')
          .text('AFFILIATED');

        legend.append('text')
          .attr('y',11)
          .attr('x', 100)
          .attr('font-size','9px')
          .text('NOT AFFILIATED');

        legend.attr('transform','translate(' + 0 + ',' + (height - legend.node().getBBox().height - 10) + ')')

        var affText = legend.append("text")
          .attr('class','aff-count')
          .attr('y',25)
          .attr('font-size','9px')
          .text(affiliatedTotal);

        affText.attr('x',(15 - affText.node().getBBox().width) / 2);

        var unaffText = legend.append("text")
          .attr('class','unaff-count')
          .attr('y',25)
          .attr('font-size','9px')
          .text(unaffiliatedTotal);

        unaffText.attr('x',80 + (15 - unaffText.node().getBBox().width) / 2);

        // Table
        var table = svg.append('g')
          .attr('class','table')
          .attr('transform','translate(' + (width - 210) + ',' + 0 + ')');

        table.append('rect')
          .attr('fill', 'none')
          .style("stroke", self.BLACK)
          .attr('height', 120)
          .attr('width', 180);

        var text = d3.select('.table').append('g')
          .selectAll('text')
            .data(labels)
          .enter()
            .append('text')
            .attr('font-size','8px')
            .text(function(d) { return d; })
            .attr('x', 10)
            .attr('y', function(d,i) { return (i + 1) * 10.5 + 5 });

        var count = d3.select('.table').append('g')
          .selectAll('text')
            .data(count)
          .enter()
            .append('text')
            .text(function(d){return d});
            count.attr('x', 162)
            count.attr('y', function(d,i) { return (i + 1) * 10.5 + 5 })
            count.attr('font-size','8px');
    },

    typeFive: function(options) {
      var responses = options.responses;
      var chart = options.el;
      var height = options.height;
      var width = options.width;

      var max = 0;
      var optionKeys = _.keys(responses[0]);

      var data = responses.map(function(response, i) {
        var count = i;
        var datum = {
          label: response.current.label
        };

        for(var period in response) {
          var total = response[period].count.male + response[period].count.female;

          max = max < total ? total : max;

          datum[period + '-total'] = total;
        }

        return datum;
      });

      var x = d3.scaleLinear()
        .domain([0,max])
        .range([0,width - 15]);
      var y = d3.scaleBand()
        .domain(data.map(function(d,i) { return i; }))
        .range([0,height])
        .paddingInner(0.5);

      var svg = chart.append('svg')
          .attr('height', height)
          .attr('width', width)
        .append('g');

      // Bars
      var bars = svg.selectAll('g')
          .data(data)
        .enter().append('g')
          .attr('class','bar')
          .attr('transform',function(d,i) { return 'translate(' + 0 + ',' + y(i) + ')'; })

      bars.append('rect')
        .attr('class','current')
        .attr('width',function(d) { return x(d['current-total']); })
        .attr('height',function(d) { return y.bandwidth() * (5 / 7); })
        .attr('fill',self.BLACK);

      bars.append('rect')
        .attr('class','prev')
        .attr('width', function(d) { return x(d['prev-total']); })
        .attr('height', function(d) { return y.bandwidth() * (1 / 7); })
        .attr('y', function(d) { return y.bandwidth() * (5 / 7) + 1; })
        .attr('fill',self.ORANGE);

      bars.append('text')
        .attr('class','type')
        .attr('y',y.bandwidth() + 9)
        .attr('font-size','8')
        .text(function(d) { return d.label.toUpperCase(); });

      bars.append('text')
        .attr('class','count')
        .attr('y',y.bandwidth() - 7.5)
        .attr('x',function(d) { return x(d['current-total']) + 5; })
        .attr('font-size','8')
        .text(function(d) { return d['current-total']; });
    },

    typeSix: function(options) {
      var height = options.height;
      var width = options.width;
      var chart = options.el;
      var data = _.values(options.responses);
      var maxCategory = _.max(data, function(d) { return d.count.male + d.count.female; });

      var chartLabels = ['60+','41 - 60','26-40','<25'];

      var x = d3.scaleLinear()
        .domain([0,maxCategory.count.male + maxCategory.count.female])
        .range([0,width - 60]);
      var y = d3.scaleBand()
        .domain(data.map(function(d) { return d.label; }))
        .range([0,height - 50])
        .paddingInner(0.3);

      var svg = chart.append('svg')
          .attr('height',height)
          .attr('width',width)
        .append('g')
          .attr('transform','translate(0,40)');

      var bars = svg.selectAll('g')
          .data(data)
        .enter().append('g')
          .attr('transform',function(d) { return 'translate(' + 0 + ',' + y(d.label) + ')'; });

      bars.append('rect')
          .attr('height',y.bandwidth())
          .attr('width',function(d) { return x(d.count.male + d.count.female); })
          .attr('x',45)
          .attr('fill',self.BLACK);

      bars.append('text')
        .attr('x',35)
        .attr('y',y.bandwidth() / 2 + 5)
        .attr('font-size','10px')
        .attr('text-anchor','end')
        .text(function(d,i) { return chartLabels[i]; });

      var count = bars.append('text')
        .attr('y',y.bandwidth() / 2 + 5)
        .attr('font-size','15px')
        .text(function(d) { return d.count.male + d.count.female; });

      var outsideCount = [];

      count.attr('x',function(d, i) {
        var textWidth = d3.select(this).node().getBBox().width;
        var barWidth = x(d.count.male + d.count.female);

        if(textWidth < barWidth) return 45 + (barWidth - textWidth) / 2;
        else {
          outsideCount.push(i);

          return 45 + barWidth + 5;
        }
      })
      .attr('fill',function(d, i) {
        if(_.indexOf(outsideCount, i) >= 0) {
          outsideCount = false;

          return self.BLACK;
        }
        else return self.WHITE;
      })
    },

    typeSeven: function(options) {
      var height = options.height;
      var width = options.width;
      var chart = options.el;
      var labelType = options.labelType;
      var legendType = options.legendType;
      var data = _.filter(_.values(options.responses), function(d) { return d.count.male + d.count.female > 0; });
      var colors = [];

      var legendLabels = [];

      if(labelType) {
        switch(labelType) {
          case 1:
          legendLabels = [
            'Regular check-up/Medication',
            'Not feeling well',
            'Pregnant / for children',
            'Other',
            'Test label'
          ];
          break;
          case 2:
          legendLabels = [
            'Apply for a new grant',
            '\'Proof of Life\' certificate',
            'Existing grant problem',
            'Other',
            'Test label'
          ];
          break;
          case 3:
          legendLabels = [
            'Government grant',
            'No income',
            'Temporary employment',
            'Other',
            'Test label'
          ];
          break;
        }
      }

      legendLabels = _.values(data).map(function(d) { return d.label });

      switch(data.length) {
        case 1:
        colors = [self.ORANGE];
        break;
        case 2:
        colors = [self.ORANGE, self.RED];
        break;
        case 3:
        colors = [self.ORANGE, self.RED, self.WHITE];
        break;
        case 4:
        colors = [self.ORANGE, self.RED, self.WHITE, self.BLUE];
        break;
        case 5:
        colors = [self.ORANGE, self.RED, self.WHITE, self.BLUE, self.BLACK];
        break;
        case 6:
        colors = [self.ORANGE, self.RED, self.WHITE, self.BLUE, self.BLACK, self.PINK];
        break;
        case 7:
        colors = [self.ORANGE, self.RED, self.WHITE, self.BLUE, self.BLACK, self.PINK];
        break;
      }

      var radius = (height + width) / 6.5;

      var svg = chart.append('svg')
          .attr('height',height)
          .attr('width',width)
        .append('g')
          .attr('transform','translate(25,5)');

      var color = d3.scaleOrdinal()
        .range(colors);

      var arc = d3.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

      var pie = d3.pie()
        .sort(null)
        .value(function (d) {
          return d.count.male + d.count.female;
      });

      var g = svg.selectAll(".arc")
          .data(pie(data))
        .enter().append('g')
          .attr('transform','translate(' + radius + ',' + radius + ')')
          .attr('class', 'arc');

      g.append('path')
        .attr('d', arc)
        .style('stroke', function(d) {
          var arcColor = color(d.data.label);

          return arcColor == self.WHITE ? self.BLACK : color(d.data.label);
        })
        .style('fill', function (d) { return color(d.data.label); });

      g.append('text')
        .attr('transform', function(d) {
          //we have to make sure to set these before calling arc.centroid
          d.outerRadius = radius; // Set Outer Coordinate
          d.innerRadius = radius / 2; // Set Inner Coordinate
          return "translate(" + arc.centroid(d) + ")rotate(0)";
        })
        .attr('fill',function(d, i) { return i == 2 ? self.BLACK : self.WHITE ; })
        .attr('text-anchor','middle')
        .text(function(d) { return d.value; });

      var legendX = 10;
      var legendY = radius * 2 + 5;

      if(legendType && legendType == 'side') {
        legendX = radius * 2 + 10;
        legendY = 30;
      }

      var legend = svg.append('g')
        .attr('class','legend')
        .attr('transform','translate('+ legendX + ',' + legendY + ')');

      legend.selectAll('rect')
          .data(data)
        .enter().append('rect')
          .attr('height',15)
          .attr('width',25)
          .attr('y', function(d, i) { return 20 * i })
          .attr('fill', function(d) { return color(d.label); })
          .attr('stroke', function(d) {
            var iconColor = color(d.label);

            return iconColor == self.WHITE ? self.BLACK : color(d.label);
          });

      legend.selectAll('text')
          .data(legendLabels)
        .enter().append('text')
          .attr('x',30)
          .attr('y', function(d, i) { return (20 * i) + 11; })
          .attr('font-size','10px')
          .text(function(d) { return d; });

      function angle(d) {
        var a = (d.startAngle + d.endAngle) * 90 / Math.PI - 90;
        return a > 90 ? a - 180 : a;
      }
    },

    typeEight: function(options) {
      var height = options.height;
      var width = options.width;
      var chart = options.el;
      var data = _.values(options.responses);
      var axisLabels = ['male','female'];
      var responseLabels = ['positive','neutral','negative'];
      var max = _.reduce(_.values(_.max(data, function(d) { return d.count.male + d.count.female; }).count), function(memo, num) { return memo + num });
      var colors = [self.BLACK,self.WHITE,self.ORANGE];
      var barWidth = width / 4;
      var icon = {
        width: 30,
        height: 40
      };
      var marginTop = 10;
      var legendIcon = {
        width: 25,
        height: 25
      };
      var legendFontSize = 10;

      var legendIcons = ['/static/img/negative_face.svg','/static/img/neutral_face.svg','/static/img/positive_face.svg'];

      var maleData = [{
        'positive': data[0].count.male,
        'neutral': data[1].count.male,
        'negative': data[2].count.male
      }];

      var femaleData = [{
        'positive': data[0].count.female,
        'neutral': data[1].count.female,
        'negative': data[2].count.female
      }];

      var svg = chart.append('svg')
          .attr('height',height)
          .attr('width',width)
        .append('g')
          .attr('transform','translate(10,' + marginTop + ')');

      var x = d3.scaleOrdinal()
        .domain(axisLabels)
        .range([0,2 * width / 3]);
      var y = d3.scaleLinear()
        .domain([0,max])
        .range([height - icon.height * 1.5,0]);
      var z = d3.scaleOrdinal()
        .domain(responseLabels)
        .range(colors);

      var maleStack = d3.stack().keys(responseLabels)(maleData);
      var femaleStack = d3.stack().keys(responseLabels)(femaleData);

      var maleMax = _.max(data, function(d) { return d.count.male; }).count.male;
      var femaleMax = _.max(data, function(d) { return d.count.female; }).count.female;

      var male = svg.selectAll('g.male')
          .data(maleStack)
        .enter().append('g')
          .attr('class','male')
          .attr('fill',function(d, i) { return z(d.key) })
          .attr('stroke',function(d, i) {
            return z(d.key) == self.WHITE ? self.BLACK : z(d.key);
          });

      male.selectAll('rect')
        .data(function(d) { return d; })
      .enter().append('rect')
        .attr('y',function(d) { return y(d[1]); })
        .attr('height',function(d) { return y(d[0]) - y(d[1]); })
        .attr('width',barWidth);

      male.selectAll('text')
          .data(function(d) { return d; })
        .enter().append('text')
          .filter(function(d) { return d[1] == maleMax; })
          .attr('fill',self.WHITE)
          .attr('stroke',self.WHITE)
          .attr('font-size','15px')
          .attr('x',barWidth / 2)
          .attr('text-anchor','middle')
          .attr('stroke-width','0.5')
          .attr('y',function(d) { return (y(d[0]) + y(d[1])) / 2; })
          .text(function(d) { return d.data.positive; });

      var female = svg.selectAll('g.female')
          .data(femaleStack)
        .enter().append('g')
          .attr('class','female')
          .attr('fill',function(d, i) { return z(d.key) })
          .attr('stroke',function(d, i) {
            return z(d.key) == self.WHITE ? self.BLACK : z(d.key);
          });

      female.selectAll('rect')
        .data(function(d) { return d; })
      .enter().append('rect')
        .attr('x',barWidth + 15)
        .attr('y',function(d) { return y(d[1]); })
        .attr('height',function(d) { return y(d[0]) - y(d[1]); })
        .attr('width',barWidth);

      female.selectAll('text')
          .data(function(d) { return d; })
        .enter().append('text')
          .filter(function(d) { return d[1] == femaleMax; })
          .attr('fill',self.WHITE)
          .attr('stroke',self.WHITE)
          .attr('font-size','15px')
          .attr('x',3 * barWidth / 2 + 15)
          .attr('text-anchor','middle')
          .attr('stroke-width','0.5')
          .attr('y',function(d) { return (y(d[0]) + y(d[1])) / 2; })
          .text(function(d) { return d.data.positive; });

      var labels = svg.append('g')
          .attr('class','labels')
          .attr('transform','translate(0,' + (height - icon.height * 1.5 + 5) + ')');

        labels.append('image')
          .attr('xlink:href','/static/img/man-icon.png')
          .attr('x',barWidth / 3 - 5)
          .attr('height',icon.height)
          .attr('width',icon.width);

        labels.append('image')
          .attr('xlink:href','/static/img/woman-icon.png')
          .attr('x',3 * barWidth / 2)
          .attr('height',icon.height)
          .attr('width',icon.width);

      var legend = svg.append('g')
        .attr('class','legend')
        .attr('transform','translate(' + (2 * barWidth + 27) + ',0)');

      var legendLabels = ['Positive','Neutral','Negative'];

      legend.selectAll('image')
          .data(legendIcons)
        .enter().append('image')
          .attr('xlink:href',function(d) { return d; })
          .attr('y',function(d, i) { return (legendIcon.height + 5) * i; })
          .attr('width',legendIcon.width)
          .attr('height',legendIcon.height);

      legend.selectAll('text')
          .data(legendLabels)
        .enter().append('text')
          .attr('font-size',legendFontSize)
          .attr('x',legendIcon.width + 3)
          .attr('y',function(d, i) { return (legendIcon.height + 5) * i + (legendIcon.height - legendFontSize * 1.1) / 2 + legendFontSize; })
          .text(function(d) { return d.toUpperCase() });

    },

    typeNine: function(options) {
      var height = options.height;
      var width = options.width;
      var data = options.responses;
      var chart = options.el;
      var labels=['yes','no'];
      var colors = [self.BLACK,self.ORANGE];

      data = [{
        yes: data.yes.count.male + data.yes.count.female,
        no: data.no.count.male + data.no.count.female
      }];

      var svg = chart.append('svg')
          .attr('height',height)
          .attr('width',width)
        .append('g')
          .attr('transform','translate(10,10)');

      var stack = d3.stack().keys(labels)(data);
      var total = data[0].yes + data[0].no;

      var y = d3.scaleLinear()
        .domain([0,total])
        .range([height,60]);
      var z = d3.scaleOrdinal()
        .domain(labels)
        .range(colors);

      var bars = svg.selectAll('g')
          .data(stack)
        .enter().append('g')
          .attr('fill', function(d) { return z(d.key) })

      bars.selectAll('rect')
          .data(function(d) { return d; })
        .enter().append('rect')
        .attr('x',width / 3.4)
        .attr('y',function(d) { return y(d[1]); })
        .attr('width',width / 2.5)
        .attr('height', function(d) { return y(d[0]) - y(d[1])});

    var text = bars.selectAll('text.response')
        .data(function(d) { return d; })
      .enter().append('text')
      .attr('class','response')
      .attr('text-anchor','middle')
      .attr('x', width / 2)
      .attr('y', function(d) { return y(d[1]) + 20; })
      .attr('font-size', '20px')
      .attr('font-weight','bold')
      .text(function(d) { return d[1] == total ? 'NO' : 'YES'; });

    var textHeight = text.node().getBBox().height;

    var count = bars.selectAll('text.count')
        .data(function(d) { return d; })
      .enter().append('text')
      .attr('class','count')
      .attr('text-anchor','middle')
      .attr('font-size','20px')
      .attr('x',width / 2)
      .attr('y', function(d) { return y(d[0]) - 5; })
      .text(function(d) { return d[1] == total ? d.data.no : d.data.yes; });

    var countHeight = count.node().getBBox().height;

    text.attr('fill', function(d) {
      var barHeight = y(d[0]) - y(d[1]);
      if(textHeight + countHeight < barHeight) return d[1] == total ? self.BLACK : self.ORANGE;
      else return d[1] == total ? self.ORANGE : self.BLACK;
    });

    count.attr('fill', function(d) {
      var barHeight = y(d[0]) - y(d[1]);

      if(textHeight + countHeight < barHeight) return d[1] == total ? self.BLACK : self.ORANGE;
      else return d[1] == total ? self.ORANGE : self.BLACK;
    });
    },

    typeTen: function(options) {
      var height = options.height;
      var width = options.width;
      var chart = options.el;
      var labels = ['yes','no'];
      var colors = [self.BLACK,self.ORANGE];
      var data = options.responses;

      data = [{
        yes: data.yes.count.male + data.yes.count.female,
        no: data.no.count.male + data.no.count.female
      }];

      var svg = chart.append('svg')
          .attr('height',height)
          .attr('width',width)
        .append('g')
          .attr('transform','translate(10,10)');

      var stack = d3.stack().keys(labels)(data);
      var total = data[0].yes + data[0].no;

      var x = d3.scaleLinear()
        .domain([0,total])
        .range([0,width - 40]);
      var z = d3.scaleOrdinal()
        .domain(labels)
        .range(colors);

      var bars = svg.selectAll('g')
          .data(stack)
        .enter().append('g')
          .attr('fill', function(d) { return z(d.key) })

      bars.selectAll('rect')
          .data(function(d) { return d; })
        .enter().append('rect')
        .attr('x',function(d) { return x(d[0]) })
        .attr('y',40)
        .attr('width',function(d) { return x(d[1]) - x(d[0])})
        .attr('height', height / 2);

    var text = bars.selectAll('text.response')
        .data(function(d) { return d; })
      .enter().append('text')
      .attr('class','response')
      .attr('text-anchor','middle')
      .attr('y', height / 2 - 10)
      .attr('x', function(d) { return x(d[0]) + 30; })
      .attr('font-size', '20px')
      .attr('font-weight','bold')
      .text(function(d) { return d[1] == total ? 'NO' : 'YES'; });

    var textWidth = text.node().getBBox().width;

    var count = bars.selectAll('text.count')
        .data(function(d) { return d; })
      .enter().append('text')
      .attr('class','count')
      .attr('text-anchor','middle')
      .attr('font-size','20px')
      .attr('y',height / 2 + 10)
      .attr('x', function(d) { return x(d[0]) + 30; })
      .text(function(d) { return d[1] == total ? d.data.no : d.data.yes; });

    var countWidth = count.node().getBBox().width;

    text.attr('fill', function(d) {
      var barWidth = x(d[1]) - x(d[0]);
      var maxWidth = textWidth > countWidth ? textWidth : countWidth;

      if(maxWidth < barWidth) return d[1] == total ? self.BLACK : self.ORANGE;
      else return d[1] == total ? self.ORANGE : self.BLACK;
    });

    count.attr('fill', function(d) {
      var barWidth = x(d[1]) - x(d[0]);
      var maxWidth = textWidth > countWidth ? textWidth : countWidth;

      if(maxWidth < barWidth) return d[1] == total ? self.BLACK : self.ORANGE;
      else return d[1] == total ? self.ORANGE : self.BLACK;
    });
    }
  }

  self.wrap = function(textNodes, boxWidth, boxHeight, fontSize) {
    textNodes.each(function() {
      var text = d3.select(this);
      var words = text.text().split(/\s+/).reverse();
      var word;
      var line = [];
      var lineNumber = 0;
      var lineHeight = 1.1;
      var textHeight = text.node().getBBox().height;
      var x = text.attr('x') || 0;
      var tspan = text.text(null).append('tspan').attr('x',x).attr('y',0).attr('font-size',fontSize);

      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(' '));
        if (tspan.node().getComputedTextLength() > boxWidth && line.length > 1) {
          line.pop();
          tspan.text(line.join(' '));
          line = [word];
          tspan = text.append('tspan').attr('x',x).attr('font-size',fontSize).text(word);
        }
      }

      var tspans = text.selectAll('tspan');
      var lineCount = tspans.size();

      tspans.each(function(d, i) {
        var tspan = d3.select(this);

        tspan.attr('y',(boxHeight - fontSize * lineCount * lineHeight) / 2 + (fontSize * lineHeight) * i + fontSize / 2)
      });
    });
  }

  // Normalize bar data to generate even-height bar pairings
  self.normalize = function(data, maxValue, labels) {
    if(!!data && !!maxValue) {
      for(var i = 0; i < data.length; i++) {
        var normalizedMax = maxValue / data[i].total;

        data[i]['normalized-total'] = data[i].total;

        if(normalizedMax > 1) {
          data[i]['normalized-total'] = 0;

          labels.forEach(function(label) {
            data[i][label] = data[i][label] * normalizedMax;
            data[i]['normalized-total'] += data[i][label];
          });

          data[i]['normalization-factor'] = normalizedMax;
        }
      }
    }

    return data;
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
          options.margin = {
            top: parseFloat(response.attr('data-margin-top')) || 10,
            right: parseFloat(response.attr('data-margin-right')) || 10,
            bottom: parseFloat(response.attr('data-margin-bottom')) || 10,
            left: parseFloat(response.attr('data-margin-left')) || 10
          };
          options.optionKeys = ['current','prev'];
          options.height = parseInt(response.attr('data-height'));
          options.width = parseInt(response.attr('data-width'));
          options.legendFormat = response.attr('data-legend-format');
          options.figureHeight = parseInt(response.attr('data-figure-height'));
          options.labelType = parseInt(response.attr('data-label-type'));
          options.key = key;
          self.drawChart(options);
        }
      });
    }
  }
}

$(function() {
  new PrintMaterials().init();
});
