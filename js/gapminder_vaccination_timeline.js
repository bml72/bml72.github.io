// Set the margins of the visualization.
var margin = {left: 120, right: 120, top: 50, bottom: 100};

// Set the width and height of the visualization.
var height = 500 - margin.top - margin.bottom,
    width = 800 - margin.left - margin.right;

// Create the variable for the SVG and reference the chart-area div when creating it.
var svg = d3.select("#gapminder_vaccination_timeline")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

// Represent March 1, 2021.
var time = 0;

// This is for handling the animation.
var interval;

// Establish a global variable for the animation update process.
var formattedData;

// Assigning the tooltip and specifying what to display when a bubble is hovered over.
var tip = d3.tip().attr("class", "d3-tip")
    .html(function(d){
        var text = "Country: <span style='color:#33c6e3'>" + d.country + "</span><br>";
        text += "Continent: <span style='color:#ffafc7; text-transform: capitalize;'>" + d.continent + "</span><br>";
        text += "Population: <span style='color:#ff9456'>" + d3.format(",.0f")(d.population) + "</span><br>";
        text += "Total Vaccinations: <span style='color:#ffc300'>" + d3.format(",.0f")(d.total_vaccinations) + "</span><br>";
        text += "People Fully Vaccinated: <span style='color:#9bca38'>" + d3.format(",.0f")(d.people_fully_vaccinated) + "</span><br>";
        return text;
    });

// Call the previously-defined tip variable to the SVG.
svg.call(tip);

// Create the x-axis and define the ticks. The x-axis is the number of total vaccinations. 
// I had to play around with the domain and range; I'm still trying to understand how this
// completely works, but I got it to look acceptable for now.
var x = d3.scaleLinear()
    .domain([0, 200000000])
    .range([0, width + 70]);

// Create the y-axis and define the ticks. The y-axis is the number of people fully vaccinated.
var y = d3.scaleLinear()
    .domain([0, 92500000])
    .range([height, 25]);

// Compute the area of the bubbles.
var area = d3.scaleLinear()
    .range([25*Math.PI, 1500*Math.PI])
    .domain([1000, 8000000000]);

// Initialize a variable to take care of the color of the bubbles based on the continent value.
var continentColor = d3.scaleOrdinal(d3.schemeDark2);

// Taking care of the title.
var title = svg.append("text")
    .attr("y", height-350)
    .attr("x", (width/2) + 40)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("People Fully Vaccinated vs Total Vaccinations (March 2021)");

// Taking care of the x-axis.
var xLabel = svg.append("text")
    .attr("y", height+80)
    .attr("x", (width/2) + 40)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Total Vaccinations");

// Taking care of the y-axis.
var yLabel = svg.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -90)
    .attr("x", -180)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("People Fully Vaccinated");    

// Taking care of the time label month; this portion doesn't change and is 
// purely to represent the month of March.
var timeLabelMonth = svg.append("text")
    .attr("y", height-10)
    .attr("x", width-100)
    .attr("font-size", "30px")
    .attr("opacity", "0.4")
    .attr("text-anchor", "middle")
    .text("March");

// Taking care of the time label; this will change based on the formattedData 
// function and what iteration the time variable is on.
var timeLabel = svg.append("text")
    .attr("y", height-10)
    .attr("x", width-30)
    .attr("font-size", "30px")
    .attr("opacity", "0.4")
    .attr("text-anchor", "middle")
    .text("1");

// Taking care of the time label year; this portion doesn't change and is 
// purely to represent the year 2021.
var timeLabelYear = svg.append("text")
    .attr("y", height-10)
    .attr("x", width+30)
    .attr("font-size", "30px")
    .attr("opacity", "0.4")
    .attr("text-anchor", "middle")
    .text(", 2021");

// Taking care of the x-axis values.
var xAxis = d3.axisBottom(x)
    .tickValues([0, 25000000, 50000000, 75000000, 100000000, 125000000, 150000000, 175000000])
    .tickFormat(d3.format(","));

// Appending the x-axis values to the SVG.
svg.append("g")
    .attr("transform", "translate(0, " + height + ")")
    .call(xAxis)
    .selectAll('text')
        .attr('x', -20)
        .attr('y', 15)
        .attr('transform', 'rotate(-45)');

// Taking care of the y-axis values.
var yAxis = d3.axisLeft(y)
    .tickValues([0, 25000000, 50000000, 75000000])
    .tickFormat(d3.format(","));

// Appending the y-axis values to the SVG.
svg.append("g")
    .call(yAxis);

// Initializing an array for the continent options.
var continents = ["europe", "asia", "americas"];

// Adding a legend to the graphic.
var legend = svg.append("g")
    .attr("transform", "translate(" + (width+10) + ", " + (height-125) + ")");

// Appending the values in the continents array to the legend.
continents.forEach(function(continent, i){
    var legendRow = legend.append("g")
        .attr("transform", "translate(0, " + (i*20) + ")");

    legendRow.append("rect")
        .attr("width", 10)
        .attr("height", 10)
        .attr("x", 50)
        .attr("y", 20)
        .attr("fill", continentColor(continent));

    legendRow.append("text")
        .attr("x", 30)
        .attr("y", 30)
        .attr("text-anchor", "end")
        .style("text-transform", "capitalize")
        .text(continent);
});

// Reading in and cleaning the data.
d3.json("../data/total_vaccinations_march.json").then(function(myData){
    formattedData = myData.map(function(date2){
        return date2['countries'].filter(function(country){
            var dataExists = (country.total_vaccinations && country.people_fully_vaccinated);
            return dataExists;
        })
    })

    // Initial run of the visualization; starts at time 0.
    update(formattedData[0]);
});

// Assign functions to the buttons created in the HTML file.
$("#play-button")
    .on("click", function(){
        // Grabbing the value of the current selection.
        var button = $(this);
        if (button.text() == "Play"){
            button.text("Pause");
            interval = setInterval(step, 200);
        } else {
            button.text("Play");
            clearInterval(interval);
        }
    });

// Resetting the date to March 1, 2021.
$("#reset-button")
    .on("click", function(){
        time=0; 
        update(formattedData[0]);
    });

// Assigning functions to the continent selection button.
$("#continent-select")
    .on("change", function(){
        update(formattedData[time]);
    });

// Assigning functions to the date slider. Note the minimum is 
// 1 (i.e. March 1, 2021) and the max is 31 (i.e. March 31, 2021).
$("#date-slider").slider({
    max: 31,
    min: 1,
    step: 1,
    slide: function(event, ui){
        time = ui.value;
        update(formattedData[time]);
    }
});


// The buttons above use this function to step through iterations of
// the "time" variable.
function step(){
    time = (time < 31) ? time+1 : 0;
    update(formattedData[time]);
}


// This function updates the data and also filters what's shown based 
// on the continent selection.
function update(my_data) {
    var continent = $("#continent-select").val();

    var my_data = my_data.filter(function(d){
        if (continent == "all") { 
            return true;
        } else {
            return d.continent == continent;
        }
    });

    // Join the new data with the old country elements.
    var circles = svg.selectAll("circle")
        .data(my_data, function(d){ return d.country; });

    // Remove old elements not present in the new data.
    circles.exit().remove();

    // Append new elements present in the new data. Show tips
    // based on whether the mouse is hovering over the circle 
    // object.
    circles.enter()
        .append("circle")
            .attr("fill", function(d,i){ return continentColor(d.continent); })
            .on("mouseover", tip.show)
            .on("mouseout", tip.hide)
            .merge(circles)
            .attr("cy", function(d,i){ return y(d.people_fully_vaccinated); })
            .attr("cx", function(d,i){ return x(d.total_vaccinations); })
            .attr("r", function(d,i){ return Math.sqrt(area(d.population)/Math.PI); });

    // Update the timeLabel variable based on the current iteration of
    // the "time" variable.
    timeLabel.text(+(time + 1));
    // Change the date label next to the date slider.
    $("#date")[0].innerHTML = +(time + 1);

    // Move the date slider and iterate the "time" variable accordingly.
    $("#date-slider").slider("value", +(time + 1));
}
