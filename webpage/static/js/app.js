////////////////////// Sentiment Plot //////////////////////////////

// Define SVG area dimensions
var svgWidth = 660;
var svgHeight = 660;

// Define the chart's margins as an object
var chartMargin = {
  top: 30,
  right: 30,
  bottom: 60,
  left: 50
};

// Define dimensions of the chart area
var chartWidth = svgWidth - chartMargin.left - chartMargin.right;
var chartHeight = svgHeight - chartMargin.top - chartMargin.bottom;

// Select body, append SVG area to it, and set the dimensions
var svg = d3.select("#sentiment-plot")
  .append("svg")
  .attr("height", svgHeight)
  .attr("width", svgWidth);

// Append a group to the SVG area and shift ('translate') it to the right and to the bottom
var chartGroup = svg.append("g")
  .attr("transform", `translate(${chartMargin.left}, ${chartMargin.top})`);

// Load data from num_restaurants_ca-of-tv-watched.csv
var url = '/data/data.json'
d3.json(url).then(function(response) {

  console.log(response);

// Cast the num_restaurants_ca value to a number for each piece of response
  response.forEach(function(d) {
    d.num_restaurants = +d.num_restaurants;
  });

  // Configure a band scale for the horizontal axis with a padding of 0.1 (10%)
  var xBandScale = d3.scaleBand()
    .domain(response.map(d => d.price_range))
    .range([0, chartWidth])
    .padding(0.1);

  // Create a linear scale for the vertical axis.
  var yLinearScale = d3.scaleLinear()
    .domain([0, d3.max(response, d => d.num_restaurants)])
    .range([chartHeight, 0]);

  // Create two new functions passing our scales in as arguments
  // These will be used to create the chart's axes
  var bottomAxis = d3.axisBottom(xBandScale);
  var leftAxis = d3.axisLeft(yLinearScale).ticks(10);

  // Append two SVG group elements to the chartGroup area,
  // and create the bottom and left axes inside of them
  chartGroup.append("g")
    .call(leftAxis);

  chartGroup.append("g")
    .attr("transform", `translate(0, ${chartHeight})`)
    .call(bottomAxis);

  // Create one SVG rectangle per piece of response
  // Use the linear and band scales to position each rectangle within the chart
  var barsGroup = chartGroup.selectAll(".bar")
                    .data(response)
                    .enter()
                    .append("rect")
                    .attr("class", "bar")
                    .attr("x", d => xBandScale(d.price_range))
                    .attr("y", d => yLinearScale(d.num_restaurants))
                    .attr("width", xBandScale.bandwidth())
                    .attr("height", d => chartHeight - yLinearScale(d.num_restaurants))

  // append y axis
  chartGroup.append("text")
      .attr("transform", "rotate(-90)")
      .attr("y", 0 - chartMargin.left)
      .attr("x", 0 - (chartHeight / 2))
      .attr("dy", "1em")
      .classed("active", true)
      .text("Number of Restaurants");

  // append x axis
  chartGroup.append("text")
      .attr("transform", `translate(${chartWidth / 2}, ${chartHeight + chartMargin.top + 15})`)
      .attr("class", "active")
      .text("Price Range");

  var barToolTip = d3.tip()
    .attr("class", "d3-tip")
    .offset([0, 0])
    .html(function(d) {
      return (`Price Range: ${d.price_range}<br>Number of Restaruants: ${d.num_restaurants}`)
    });
  barsGroup.call(barToolTip);

  barsGroup.on("mouseover", function(data) {
    barToolTip.show(data, this);

  barsGroup.on("mouseout", function(data) {
    barToolTip.hide(data, this);
  })
});


}).catch(function(error) {
console.log(error);

});