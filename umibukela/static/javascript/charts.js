var PrintMaterials = function() {
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
    }
  }

  self.charts = {
    typeOne: function(options) {
      var response = options.el;
      var height = options.height;
      var width = options.width;
      var margin = options.margin;
      var optionKeys = options.optionKeys;

      var figureHeight = height * .75;
      var labelWidth = Math.floor(width / 5) - 3;
      var sideWidth = (width - labelWidth) / 2;
      var rightOffset = width / 2 + labelWidth / 2;
      var leftOffset = width / 2 - labelWidth / 2;
      var fontSize = height / 32;
      var legendWidth = width / 3;
      var icon = {
        height: height / 8,
        width: width / 13
      };
      var male_data = [];
      var female_data = [];
      var labels = [];

      var colorMale = self.colorMale;
      var colorFemale = self.colorFemale;

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
        .paddingOuter(0)
        .align(0);
      var y1 = d3.scaleBand()
        .domain(optionKeys)
        .rangeRound([0, y0.bandwidth()])
        .padding(0);
      var xRight = d3.scaleLinear()
        .domain([0,rightMax])
        .range([0,sideWidth - 20]);
      var xLeft = d3.scaleLinear()
        .domain([0,leftMax])
        .range([0,sideWidth - 20]);

      var svg = response.append('svg')
        .attr('height',height)
        .attr('width',width)
      .append('g');

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

      var labelOffset = y0.paddingInner();

      var centerBoxes = svg.selectAll('g.center')
          .data(labels)
        .enter().append('g')
          .attr('transform',function(d, i) {
            if(i == labels.length - 1) labelOffset = y0(d.key);

            return 'translate(' + leftOffset + ',' + (y0(d.key) + 1) + ')';
          })
          .attr('class','center');

      centerBoxes.append('rect')
        .attr('class','box')
        .attr('width',labelWidth)
        .attr('height',y0.bandwidth() - 2);

      centerBoxes.append('text')
          .attr('class','label')
          .attr('x',labelWidth / 2)
          .attr('y',labelOffset + 4)
          .text(function(d) { return d.label; })
          .call(self.wrap, labelWidth - 6, y0.bandwidth() - y0.paddingInner(), fontSize);

      var legend = svg.append('g')
          .attr('class','legend')
          .attr('transform','translate(' + legendWidth + ',' + (figureHeight + 10) + ')');

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

      var maleLabel = legend.append('text')
        .attr('class','male-label')
        .text(2015)
        .attr('font-size',fontSize);

      maleLabel.attr('x',maleLabel.node().getBBox().width / 3)
        .attr('y',icon.height + maleLabel.node().getBBox().height);

      var femaleLabel = legend.append('text')
        .attr('class','female-label')
        .text(2015)
        .attr('font-size',fontSize);

      femaleLabel.attr('x',legendWidth - femaleLabel.node().getBBox().width - femaleLabel.node().getBBox().width / 3)
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

      var male_data = [];
      var female_data = [];
      var labels = [];
      var legendLabels = [];

      var isBar = legendFormat == 'top-bar' || legendFormat == 'bottom-bar';

      var figureHeight = height * .75;
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

      optionKeys.reverse();

      for(var i=0;i < optionKeys.length;i++) {
        var period = optionKeys[i];

        male_data.push({ period: period, year: period == 'current' ? years[1] : years[0] });
        female_data.push({ period: period, year: period == 'current' ? years[1] : years[0] });
      }

      male_data.reverse();
      female_data.reverse();

      responses.forEach(function(response, i) {
        for(period in response) {
          var male_datum = _.find(male_data, function(item) { return item.period == period });
          var female_datum = _.find(female_data, function(item) { return item.period == period });
          var key = response[period].key;
          var label = response[period].label;

          if(key) labels.push(key);
          if(!_.contains(legendLabels, label)) legendLabels.push(label);

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

      for(var i = 0; i < male_data.length; i++) {
        male_data[i].total = 0;
        female_data[i].total = 0;

        labels.forEach(function(label) {
          male_data[i].total += male_data[i][label];
          female_data[i].total += female_data[i][label];
        });
      }

      var prevMax = d3.max(male_data.concat(female_data).map(function(d) { if(d.period == 'prev') return d.total; }));

      if(!prevMax) {
        years = years[0];
      }

      var maleMax = d3.max(male_data.map(function(d) { return d.total; }));
      var femaleMax = d3.max(female_data.map(function(d) { return d.total; }));
      var max = maleMax > femaleMax ? maleMax : femaleMax;

      male_data = self.normalize(male_data, maleMax, labels);
      female_data = self.normalize(female_data, femaleMax, labels);

      var male_stack = d3.stack().keys(labels)(male_data);
      var female_stack = d3.stack().keys(labels)(female_data);

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
            .attr('stroke',function(d) { return z(d.key) == self.WHITE ? self.BLACK : z(d.key); });
      }

      function setupBars(el, gender, addedShift) {
        if(!addedShift) addedShift = 0;

        return el.selectAll('rect')
            .data(function(d) { return d; })
          .enter().append('rect')
            .attr('x', function(d) {
              var period = d.data.period;
              var shift = 0;

              if(period == 'current') shift = .9 * x.bandwidth();

              var totalShift = x(d.data.period) - shift + addedShift;

              return isBar ? totalShift : totalShift + legendWidth;
            })
            .attr('y', function(d) { return y(d[1]); })
            .attr('height', function(d) { return (y(d[0]) - y(d[1])); })
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
            .attr('font-size',labelFontSize)
            .text(function(d) {
              var denormalizer = 1;

              if(d.data['normalization-factor']) denormalizer = 1 / d.data['normalization-factor'];

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

        return labels.attr('x',function(d, i) { return addedShift + (x.bandwidth() * 2) * i - labels.node().getBBox().width / 2 * i; });
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
              .attr('x',legendIcon.width + 5)
              .attr('y',legendIcon.height / 1.5 + i * (legendIcon.height + height / 20))
              .attr('font-size',legendFontSize)
              .text(label.toUpperCase());
          });
          break;
          case 'attitude':
            // Default to vertical alignment
            var icons = ['/static/img/negative_face.svg','/static/img/neutral_face.svg','/static/img/positive_face.svg'];
            var labelWidth = format == 'top-bar' ? figureWidth / 3 : 0;
            var data = [];

            icons.forEach(function(icon, i) {
              data.push({ icon: icon, label: labels[i] });
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
              //.call(self.wrap, labelWidth, legendIcon.height, legendFontSize);
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
        .range([figureHeight,5]);
      var z = d3.scaleOrdinal()
        .domain(labels)
        .range(zRange);

      var maleCurrentHeight = 0;
      var femaleCurrentHeight = 0;
      var malePreviousHeight = 0;
      var femalePreviousHeight = 0;

      male_stack.forEach(function(d){
        d.forEach(function(point){
          if(point.data.period == 'current') maleCurrentHeight += y(point[1]);
          else if(point.data.period == 'prev') malePreviousHeight += y(point[1]);
        });
      });

      female_stack.forEach(function(d){
        d.forEach(function(point){
          if(point.data.period == 'current') femaleCurrentHeight += y(point[1]);
          else if(point.data.period == 'prev') femalePreviousHeight += y(point[1]);
        });
      });

      var maleBarShift = isBar ? labelIcon.width : 0;
      var femaleBarShift = isBar ? labelIcon.width + colWidth + gutter : colWidth + gutter;
      var femaleCountShift = isBar ? colWidth * 2 + gutter : legendWidth + colWidth * 2 + gutter;
      var maleCountShift = isBar ? labelIcon.width + colWidth - 2 : legendWidth + colWidth - 2;
      var maleIconShift = isBar ? 0 : legendWidth - labelIcon.width;
      var femaleIconShift = isBar ? labelIcon.width + colWidth + gutter / 2 : legendWidth + colWidth + gutter / 2;
      var maleLabelShift = isBar ? labelIcon.width + 7 : legendWidth + 3;
      var femaleLabelShift = maleLabelShift + colWidth + gutter;
      var lineShift = isBar ? colWidth + gutter / 2 + 15 : legendWidth + colWidth + gutter / 3;

      var male = setupBands(svg, '.male', 'male', male_stack);
      var female = setupBands(svg, '.female', 'female', female_stack);
      var maleBars = setupBars(male, 'male',maleBarShift);
      var femaleBars = setupBars(female, 'female', femaleBarShift);
      var maleCount = setupCount(male, maleCountShift);
      var femaleCount = setupCount(female, femaleCountShift);
      var maleLabels = setupLabels(male, years, maleLabelShift);
      var femaleLabels = setupLabels(female, years, femaleLabelShift);
      var maleIcon = drawIcon(svg, '/static/img/man-icon.png', maleIconShift);
      var femaleIcon = drawIcon(svg, '/static/img/woman-icon.png', femaleIconShift);

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

      var male_data = [];
      var female_data = [];
      var labels = [];

      var gutter = height / 10 + 6;
      var colHeight = (height - gutter) / 2;
      var icon = { width: 15, height: 30 };
      var figureHeight = height * 0.8;
      var widthCoefficient = 0.8;
      var legendWidth = width * 0.2;
      var figureWidth = width * 0.8;
      var fontSize = Math.round(height / 7);
      var legendSquare = colHeight * 0.45;

      var optionKeys = _.keys(options.responses[0]);
      var years = cycleYears;

      for(var i=0;i < optionKeys.length;i++) {
        var period = optionKeys[i];

        male_data.push({ period: period, year: period == 'current' ? years[1] : years[0], total: 0 });
        female_data.push({ period: period, year: period == 'current' ? years[1] : years[0], total: 0 });
      }

      male_data.reverse();
      female_data.reverse();

      responses.forEach(function(response) {
        response.prev.key = response.current.key;

        for(period in response) {
          var male_datum = _.find(male_data, function(item) { return item.period == period; });
          var female_datum = _.find(female_data, function(item) { return item.period == period; });

          if(response[period].key && period == 'current') labels.push(response[period].key.toLowerCase());

          male_datum[response[period].key.toLowerCase()] = response[period].count.male;
          female_datum[response[period].key.toLowerCase()] = response[period].count.female;
        }
     });

      for(var i = 0;i < male_data.length; i++) {
        labels.forEach(function(label) {
          male_data[i].total += male_data[i][label];
          female_data[i].total += female_data[i][label];
        });
      }

      var maleMax = d3.max(male_data.map(function(d) { return d.total; }));
      var femaleMax = d3.max(female_data.map(function(d) { return d.total; }));
      var max = maleMax > femaleMax ? maleMax : femaleMax;
      var prevMax = d3.max(male_data.concat(female_data).map(function(d) { if(d.period == 'prev') return d.total; }));

      if(!prevMax) {
        years = years[0];
      }

      male_data = self.normalize(male_data, maleMax, labels);
      female_data = self.normalize(female_data, femaleMax, labels);

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
      var female_stack = d3.stack().keys(labels)(female_data);
      var male_stack = d3.stack().keys(labels)(male_data);

      var svg = response.append('svg')
        .attr('height', height + 16)
        .attr('width', width + 10)
      .append('g')
        .attr('transform','translate(0,12)');

      var female = svg.selectAll('.female')
          .data(female_stack)
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
            var shift = 0;

            if(period != 'current') shift = .5 * y.bandwidth();

            return y(d.data.period) + shift;
          })
          .attr('x', function(d) { return x(d[0]) * widthCoefficient + icon.width + 5; })
          .attr('width', function(d) {
            var barWidth = Math.abs(x(d[1]) - x(d[0])) * widthCoefficient;

            if(d.data.period == 'current' && barWidth) femaleBarWidth += barWidth;

            return barWidth - 1;
          })
          .attr('height', function(d) {
            var period = d.data.period;
            var coefficient = period == 'current' ? 1.5 : .5;

            return y.bandwidth() * coefficient - 2;
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
          .text(function(d) { return d.data.period == 'current' && d[1] - d[0] && d[1] - d[0] > 0 ? d[1] - d[0] : ''; });

      female.selectAll('text.year')
          .data(years)
        .enter().append('text')
          .attr('class','year')
          .attr('stroke','none')
          .attr('text-anchor','start')
          .attr('y', function(d,i) { return y.bandwidth() * (i + 1) + i * 2; })
          .attr('x', function(d) { return femaleBarWidth + icon.width + 8; })
          .attr('fill',self.BLACK)
          .attr('font-size',fontSize)
          .text(function(d) { return d; });

      var male = svg.selectAll('.male')
        .data(male_stack)
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
            var shift = 0;

            if(period != 'current') shift = .5 * y.bandwidth();
            return y(d.data.period) + shift + colHeight + gutter;
          })
          .attr('x', function(d) { return x(d[0]) * widthCoefficient + icon.width + 5; })
          .attr('width', function(d) {
            var barWidth = Math.abs(x(d[1]) - x(d[0])) * widthCoefficient;

            if(d.data.period == 'current' && barWidth) maleBarWidth += barWidth;

            return barWidth - 1;
          })
          .attr('height', function(d) {
            var period = d.data.period;
            var coefficient = period == 'current' ? 1.5 : .5;

            return y.bandwidth() * coefficient - 2;
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
          .text(function(d) { return d.data.period == 'current' && d[1] - d[0] && d[1] - d[0] > 0 ? d[1] - d[0] : ''; });

      male.selectAll('text.year')
          .data(years)
        .enter().append('text')
          .attr('class','year')
          .attr('stroke','none')
          .attr('y', function(d,i) { return colHeight + gutter + y.bandwidth() * (i + 1) + i * 2; })
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

      var legendLabels = labels.length > 2 ? ['<tspan dy="0">1</tspan><tspan font-size="5" dy="-5">st</tspan> <tspan dy="5">Visit</tspan>', '<tspan>2</tspan><tspan font-size="5" dy="-5">nd</tspan> <tspan dy="5">Visit</tspan>', '<tspan>3</tspan><tspan font-size="5" dy="-5">rd</tspan>  <tspan dy="5">Visit</tspan>'] : ['Yes','No'];

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
      console.log(width,renderedLegendWidth);

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
      var x = parseFloat(text.attr('x')) || 0;
      var y = parseFloat(text.attr('y')) || 0;
      var textHeight = text.node().getBBox().height;
      var tspan = text.text(null).append('tspan').attr('x',x).attr('y',y).attr('font-size',fontSize);

      text.attr('x',0).attr('y',0);

      while (word = words.pop()) {
        line.push(word);
        tspan.text(line.join(' '));
        if (tspan.node().getComputedTextLength() > boxWidth && line.length > 1) {
          var offset = !!boxHeight ? fontSize / 2 : 0;
          line.pop();
          tspan.text(line.join(' '));
          line = [word];
          tspan = text.append('tspan').attr('x',x).attr('y', ++lineNumber * fontSize * lineHeight + y - offset).attr('font-size',fontSize).text(word);
        }
      }

      var tspans = text.selectAll('tspan');
      var lineCount = tspans.size();
      var offset = y + (boxHeight - lineCount * fontSize) / 2;

      tspans.each(function(d, i) {
        var tspan = d3.select(this);

        tspan.attr('y',offset + i * (boxHeight - 4) / lineCount)
      });
    });
  }

  // Normalize the data
  self.normalize = function(data, maxValue, labels) {
    if(!!data && !!maxValue) {
      for(var i = 0; i < data.length; i++) {
        var normalizedMax = maxValue / data[i].total;

        if(normalizedMax > 1) {
          labels.forEach(function(label) {
            data[i][label] = Math.round(data[i][label] * normalizedMax);
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
          options.optionKeys = _.keys(questions[key].options[0]);
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
  new PrintMaterials().init();
});
