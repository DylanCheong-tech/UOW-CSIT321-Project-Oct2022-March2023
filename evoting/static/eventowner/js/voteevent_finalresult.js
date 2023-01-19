// voteevent_finalresult.js

// parameter: frame_id : DOM ID, data : JSON object 
function renderPieChart(frame_id, data) {
    let width = 300
    let height = 300
    let margin = 40

    let pie_radius = Math.min(width, height) / 2 - margin

    var svg = d3.select("#" + frame_id)
        .append("svg")
        .attr("width", width)
        .attr("height", height)
        .append("g")
        .attr("transform", "translate(" + width * 3 / 4 + "," + height / 2 + ")");

    var color = d3.scaleOrdinal()
        .domain(data)
        .range(d3.schemeSet1);

    var pie = d3.pie().value(function (d) { return d.value })
    var data_ready = pie(d3.entries(data))

    var arc_generator = d3.arc().innerRadius(0).outerRadius(pie_radius)

    svg.selectAll("slices")
        .data(data_ready)
        .enter()
        .append("path")
        .attr("d", arc_generator)
        .attr("fill", function (d) { return (color(d.data.key)) })
        .attr("stroke", "black")
        .style("stroke-width", "1px")
        .attr("opacity", 0.7)

    svg.selectAll("slices")
        .data(data_ready)
        .enter()
        .append("text")
        .text(function (d) { return "Option " + d.data.key })
        .attr("transform", function (d) { return "translate(" + arc_generator.centroid(d)[0] * 2.6 + ", " +arc_generator.centroid(d)[1] * 2.6 + ")"; })
        .style("text-anchor", "middle")
        .style("font-size", ".8em")

    svg.selectAll("slices")
        .data(data_ready)
        .enter()
        .append("text")
        .attr("dy", "1.2em")
        .text(function (d) { return "Count : " + d.data.value })
        .attr("transform", function (d) { return "translate(" + arc_generator.centroid(d)[0] * 2.6 + ", " +arc_generator.centroid(d)[1] * 2.6 + ")"; })
        .style("text-anchor", "middle")
        .style("font-size", ".8em")
}

document.addEventListener('DOMContentLoaded', doSomething, false);

function doSomething() {
    renderPieChart("vote_count_chart", { "a": 12, "b": 14 })
    renderPieChart("response_rate_chart", { "a": 89, "b": 14, "c": 13, "d" : 32, "pop" : 12 })
}