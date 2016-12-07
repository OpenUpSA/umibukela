Umibukela.Poster = function() {
  var self = this;

  self.init = function() {
    self.draw();
  }

  self.draw = function() {
    if(!!questions) {
      var responses = d3.selectAll('.response');
      var margin = { top: 10, right: 10, bottom: 10, left: 10 };
      var height = 350 - margin.left - margin.right;
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
                console.log('six');
              break;
              case 'four_six':
                labels.push({ key: 'four_six', label: '4-6 hrs' });
                console.log('four');
              break;
              case 'two_four':
                labels.push({ key: 'two_four', label: '2-4 hrs' });
                console.log('two');
              break;
              case 'one_two':
                labels.push({ key: 'one_two', label: '1-2 hrs' });
                console.log('one');
              break;
              case 'thirty_one':
                labels.push({ key: 'thirty_one', label: '30mins-1hr' });
                console.log('thirty');
              break;
              case 'under_thirty':
                labels.push({ key: 'under_thirty', label: '>30 mins' });
                console.log('under');
              break;
            }

            console.log(labels);
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
            .paddingInner(0);
          var y1 = d3.scaleBand()
            .domain(['current','prev'])
            .rangeRound([0, y0.bandwidth()]);
          var xRight = d3.scaleLinear()
            .domain([0,rightMax])
            .range([0,sideWidth]);
          var xLeft = d3.scaleLinear()
            .domain([0,leftMax])
            .range([0,sideWidth]);

          var svg = response.append('svg')
            .attr('height',height + margin.top + margin.bottom)
            .attr('width',width + margin.left + margin.right)
          .append('g')
            .attr('transform', 'translate(' + margin.left + ',' + margin.top + ')');

          var right = svg.selectAll('rect.right')
              .data(female_data)
            .enter().append('rect')
              .attr('transform', function(d) { return 'translate(0,' + y0(d.label) + ')'; })
              .attr('class','right')
              .attr('height', function(d) {
                var rectHeight = y1.bandwidth();

                if(d.name == 'prev') {
                  rectHeight = rectHeight / 3;
                }

                return rectHeight - 2;
              })
              .attr('x',rightOffset)
              .attr('y', function(d) { return y1(d.name); })
              .attr('width', function(d) { return xRight(d.value) - 2; })
              .attr('fill', function(d) { return colorFemale(d.name); })
              .attr('stroke',function(d) { return d.name == 'current' ? '#000000' : orange; });

          var left = svg.selectAll('rect.left')
              .data(male_data)
            .enter().append('rect')
              .attr('transform', function(d) { return 'translate(0,' + y0(d.label) + ')'; })
              .attr('class','left')
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

          var rightLabels = svg.selectAll('text.right')
            .data(female_data)
          .enter().append('text')
            .attr('x',function(d) { return rightOffset + xRight(d.value) + 5; })
            .attr('y',function(d) { return y0(d.label) + y1.bandwidth() / 2 + 4; })
            .attr('font-size','10px')
            .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

          var leftLabels = svg.selectAll('text.left')
            .data(male_data)
          .enter().append('text')
            .attr('x',function(d) { return sideWidth - xLeft(d.value) - 15; })
            .attr('y',function(d) { return y0(d.label) + y1.bandwidth() / 2 + 4; })
            .attr('font-size','10px')
            .text(function(d) { return d.value > 0 && d.name == 'current' ? d.value : ''; });

          var centerLabels = svg.selectAll('text.label')
            .data(labels)
          .enter().append('text')
            .attr('class','label')
            .attr('width',70)
            .attr('height',35)
            .attr('x', leftOffset)
            .attr('y', function(d) { return y0(d.key) + y1.bandwidth() / 2; })
            .attr('font-size','11px')
            .text(function(d) { return d.label; });
        }
      });
    }
  }
}

$(function() {
  var Poster = new Umibukela.Poster();

  Poster.init();
});
