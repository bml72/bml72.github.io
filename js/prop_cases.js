// Set the margins of the visualization.
var margin = {left: 80, right: 50, top: 50, bottom: 125};

// Set the width and height of the visualization.
var width = 250,
    height = 300;

// Create the variable for the SVG and reference the prop_cases div when creating it.
var prop_svg = d3.select('#prop_cases')
    .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
    .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

// Pull the data from the correct folder. Since the folder containing the data is different,
// we need to reference the directories above (../ goes to the "code" folder, and the second 
// ../ goes to the "Final Project" folder.).
d3.json('../data/proportionate_total_cases.json').then(function(mydata){
    mydata.forEach(function(d){
        d.proportionate_total_cases = +d.proportionate_total_cases;
    });

    // Create the x-axis and define the ticks.
    var x = d3.scaleBand()
        .domain(mydata.map(function(d){ return d.country; }))
        .range([0, width])
        .paddingInner(0.3)
        .paddingOuter(0.3);

    // Create the y-axis and define the ticks.
    var y = d3.scaleLinear()
        .domain([0, d3.max(mydata, function(d){ return d.proportionate_total_cases; }) + 0.15])
        .range([height, 0]);
    
    // Create an x-axis call to define where to apply the x-axis.
    var xAxisCall = d3.axisBottom(x);

    // Create an y-axis call to define where to apply the y-axis.
    var yAxisCall = d3.axisLeft(y)
        .ticks(3)
        .tickFormat(function(d, i){ return d3.format(',')(d) });

    // Taking care of the x-axis.
    prop_svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(xAxisCall)
            .selectAll('text')
                .attr('x', '-5')
                .attr('y', '10')
                .attr('text-anchor', 'end')
                .attr('transform', 'rotate(-40)');
    
    // Taking care of the x-axis text.
    prop_svg.append('text')
        .attr('x', width / 2)
        .attr('y', height + 90)
        .attr('font-size', '20px')
        .attr('text-anchor', 'middle')
        .text('Country')
        .style('font', '15.5px times');

    // Taking care of the y-axis.
    prop_svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxisCall)

    // Taking care of the y-axis text.
    prop_svg.append('text')
        .attr('x', -(height / 2))
        .attr('y', -70)
        .attr('font-size', '20px')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .text('Proportionate Total Cases (% of Pop)')
        .style('font', '15.5px times');
    
    // Taking care of the title text.
    prop_svg.append('text')
        .attr('x', width / 2)
        .attr('y', -10)
        .attr('font-size', '20px')
        .attr('text-anchor', 'middle')
        .text('Top Ten Countries by Proportionate Total Cases')
        .style('font', '15.5px times');

    // Assigning the tooltip and specifying what to display when a bar is hovered over.
    var tip = d3.tip().attr('class', 'd3-tip')
        .html(function(d){
            var text = "Country: <span style='color: #66C0C6'>" + d.country + '</span><br>';
                text += "Population: <span style='color: #FFF74A; text-transform: capitalize'>" + d3.format(',')(d.population) + '</span><br>';
                text += "Total Cases (% of Pop): <span style='color: #FFF74A; text-transform: capitalize'>" + d3.format(',%')(d.proportionate_total_cases) + '</span><br>';
            return text;
        });
    
    // Call the previously-defined tip variable to the SVG.
    prop_svg.call(tip);

    // Create the "bars" in the histogram. ".on" defines what to highlight the bars with when the mouse hovers over them.
    var rects = prop_svg.selectAll('rect')
        .data(mydata)
            .enter().append('rect')
                .attr('y', function(d, i){ return y(d.proportionate_total_cases); })
                .attr('x', function(d, i){ return x(d.country); })
                .attr('width', x.bandwidth)
                .attr('height', function(d, i){ return height - y(d.proportionate_total_cases); })
                .attr('fill', '#3EA199')
            .on('mouseover', function(d){
                tip.show(d);
                tempColor = this.style.fill;
                d3.select(this)
                    .transition()
                    .style('opacity', 0.5)
                    .style('fill', '#FFF74A')
            })
            .on('mouseout', function(d){
                tip.hide(d);
                d3.select(this)
                    .transition()
                    .style('opacity', 1)
                    .style('fill', tempColor)
            })
});