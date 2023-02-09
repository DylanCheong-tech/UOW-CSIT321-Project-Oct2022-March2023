// voteevent_finalresult.js

// parameter: frame_id : DOM ID, data : JSON object 
function renderPieChart(frame_id, data) {
    let width = 200
    let height = 200
    let margin = 20

    let pie_radius = Math.min(width, height) / 2 - margin

    var svg = d3.select("#" + frame_id)
        .append("svg")
        .attr("display", "inline-block")
        .attr("width", "20vw")
        .attr("height", "25vh")
        .append("g")
        .attr("transform", "translate(" + width + "," + height / 2 + ")");

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
        .attr("transform", "translate(" + width / 2 + "," + 0 + ")");

    const legend = svg
        .append('g')
        .attr('transform', `translate(-${pie_radius * 2 + 20},-${pie_radius})`)

    legend
        .selectAll(null)
        .data(data_ready)
        .enter()
        .append('rect')
        .attr('y', d => 10 * d.index * 2.5)
        .attr('width', 12)
        .attr('height', 12)
        .attr('fill', d => color(d.data.key))
        .attr('stroke', 'grey')
        .style('stroke-width', '1px');

    legend
        .selectAll(null)
        .data(data_ready)
        .enter()
        .append('text')
        .text(d => (d.data.key + " : Votes : " + d.data.value))
        .attr('x', 12 * 1.5)
        .attr('y', d => 12 * d.index * 2.2 + 10)
        .style('font-size', `${.8}em`);

        
}

function preprocess_vote_data(data) {
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
    document.getElementById("message_content").innerHTML = "You are going to publish the vote event results. <br /> Confirm to proceed ?"

    document.getElementById("confirm_btn").addEventListener("click", () => {
        document.querySelector("div#publish_button_bar form").submit();
    });
}

document.addEventListener("DOMContentLoaded", () => {
    // check pop up message box for the publication result status 
    let publish_status = (new URLSearchParams(window.location.search)).get("publish_status")

    if (publish_status == "success") {
        document.getElementById("pop_out_message_box").style.display = "block";
        document.getElementById("message_content").innerHTML = "Final Result Published Successfully !"

        document.getElementById("cancel_btn").style.display = "none";
        document.getElementById("confirm_btn").addEventListener("click", () => {
            document.getElementById("pop_out_message_box").style.display = "none";
            window.location.href = window.location.pathname;
        });
    }
})

