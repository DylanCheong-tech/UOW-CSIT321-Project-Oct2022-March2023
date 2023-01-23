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
        .attr("max-width", "10vw")
        .attr("transform", function (d) { return "translate(" + arc_generator.centroid(d)[0] * 3.3 + ", " + arc_generator.centroid(d)[1] * 2.6 + ")"; })
        .style("text-anchor", "middle")
        .style("font-size", ".8em")

    svg.selectAll("slices")
        .data(data_ready)
        .enter()
        .append("text")
        .attr("dy", "1.2em")
        .text(function (d) { return "Count : " + d.data.value })
        .attr("transform", function (d) { return "translate(" + arc_generator.centroid(d)[0] * 3 + ", " + arc_generator.centroid(d)[1] * 2.6 + ")"; })
        .style("text-anchor", "middle")
        .style("font-size", ".8em")
}

function preprocess_vote_data(data){
    // data preprocessing 
    data = data.map(item => {
        return [item.option, item.result]
    })
    data = Object.fromEntries(data)

    return data
}

function hide_pop_out_message_box() {
    let message_box = document.getElementById("pop_out_message_box");
    message_box.style.display = "none";
}

function publishFinalResult(event) {
    event.preventDefault()

    document.getElementById("pop_out_message_box").style.display = "block";
    document.getElementById("message_content").innerHTML = "You are going ot publish the vote event results. <br /> Confirm to proceed ?"

    document.getElementById("confirm_btn").addEventListener("click", () => {
        document.querySelector("div#publish_button_bar form").submit()
    });
}