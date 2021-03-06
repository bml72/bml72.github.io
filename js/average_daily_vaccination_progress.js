// Set the margins of the visualization.
var margin = {left: 80, right: 50, top: 50, bottom: 125};

// Set the width and height of the visualization.
var width = 850,
    height = 300;

// Create the variable for the SVG and reference the average_daily_vacc_progress div when creating it.
var average_vacc_svg = d3.select('#average_daily_vaccination_progress')
    .append('svg')
        .attr('width', width + margin.left + margin.right)
        .attr('height', height + margin.top + margin.bottom)
    .append('g')
        .attr('transform', 'translate(' + margin.left + ', ' + margin.top + ')');

// Pull the data from the correct folder. Since the folder containing the data is different,
// we need to reference the directories above (../ goes to the "code" folder, and the second 
// ../ goes to the "Final Project" folder.).
d3.json('../data/average_daily_vaccination_progress.json').then(function(mydata){
    mydata.forEach(function(d){
        d.prop_daily_vaccinations = +d.prop_daily_vaccinations;
    });

    // Create the x-axis and define the ticks.
    var x = d3.scaleBand()
        .domain(mydata.map(function(d){ return d.country; }))
        .range([0, width])
        .paddingInner(0.3)
        .paddingOuter(0.3);

    // Create the y-axis and define the ticks.
    var y = d3.scaleLinear()
        .domain([0, d3.max(mydata, function(d){ return d.prop_daily_vaccinations; }) + 0.02])
        .range([height, 0]);
    
    // Create an x-axis call to define where to apply the x-axis.
    var xAxisCall = d3.axisBottom(x);

    // Create an y-axis call to define where to apply the y-axis.
    var yAxisCall = d3.axisLeft(y)
        .ticks(3)
        .tickFormat(function(d, i){ return d3.format(',')(d) });

    // Taking care of the x-axis.
    average_vacc_svg.append('g')
        .attr('class', 'x-axis')
        .attr('transform', 'translate(0, ' + height + ')')
        .call(xAxisCall)
            .selectAll('text')
                .attr('x', '-5')
                .attr('y', '10')
                .attr('text-anchor', 'end')
                .attr('transform', 'rotate(-40)');
    
    // Taking care of the x-axis text.
    average_vacc_svg.append('text')
        .attr('x', width / 2)
        .attr('y', height + 90)
        .attr('font-size', '20px')
        .attr('text-anchor', 'middle')
        .text('Country')
        .style('font', '15.5px times');

    // Taking care of the y-axis.
    average_vacc_svg.append('g')
        .attr('class', 'y-axis')
        .call(yAxisCall)

    // Taking care of the y-axis text.
    average_vacc_svg.append('text')
        .attr('x', -(height / 2))
        .attr('y', -60)
        .attr('font-size', '20px')
        .attr('text-anchor', 'middle')
        .attr('transform', 'rotate(-90)')
        .text('Percentage of Population Vaccinated Daily (%)')
        .style('font', '15.5px times');
    
    // Taking care of the title text.
    average_vacc_svg.append('text')
        .attr('x', width / 2)
        .attr('y', -10)
        .attr('font-size', '20px')
        .attr('text-anchor', 'middle')
        .text('Top 30 Countries - Percentage of Population Vaccinated Daily')
        .style('font', '15.5px times');

    // Assigning the tooltip and specifying what to display when a bar is hovered over.
    var tip = d3.tip().attr('class', 'd3-tip')
        .html(function(d){
            var text = "Country: <span style='color: #ff4e4e'>" + d.country + '</span><br>';
                text += "Population: <span style='color: #fb8c00; text-transform: capitalize'>" + d3.format(',')(d.population) + '</span><br>';
                text += "Total Vaccinations: <span style='color: #fb8c00; text-transform: capitalize'>" + d3.format(',')(d.total_vaccinations) + '</span><br>';
                text += "People Fully Vaccinated: <span style='color: #fb8c00; text-transform: capitalize'>" + d3.format(',')(d.people_fully_vaccinated) + '</span><br>';
                text += "Percentage of Population Vaccinated Daily: <span style='color: #fb8c00; text-transform: capitalize'>" + d3.format(',%')(d.prop_daily_vaccinations) + '</span><br>';
            return text;
        });
    
    // Call the previously-defined tip variable to the SVG.
    average_vacc_svg.call(tip);

    // Create the "bars" in the histogram. ".on" defines what to highlight the bars with when the mouse hovers over them.
    var rects = average_vacc_svg.selectAll('rect')
        .data(mydata)
            .enter().append('rect')
                .attr('y', function(d, i){ return y(d.prop_daily_vaccinations); })
                .attr('x', function(d, i){ return x(d.country); })
                .attr('width', x.bandwidth)
                .attr('height', function(d, i){ return height - y(d.prop_daily_vaccinations); })
                .attr('fill', '#7d1919')
            .on('mouseover', function(d){
                tip.show(d);
                tempColor = this.style.fill;
                d3.select(this)
                    .transition()
                    .style('opacity', 0.5)
                    .style('fill', '#fb8c00')
            })
            .on('mouseout', function(d){
                tip.hide(d);
                d3.select(this)
                    .transition()
                    .style('opacity', 1)
                    .style('fill', tempColor)
            })
});