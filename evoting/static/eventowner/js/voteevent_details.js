// voteevent_details.js 

document.addEventListener("DOMContentLoaded", () => {
    // check pop up message box for the publication result status 
    let publish_status = (new URLSearchParams(window.location.search)).get("publish_status")
    let view_final_status = (new URLSearchParams(window.location.search)).get("view_final")

    if (publish_status == "fail") {
        document.getElementById("message_content").innerHTML = "Final Result Published Failed !"
    }
    else if (view_final_status == "fail"){
        document.getElementById("message_content").innerHTML = "Final Result Is Not Ready !"
    }
    else{
        return;
    }

    document.getElementById("pop_out_message_box").style.display = "block";

    document.getElementById("confirm_btn").addEventListener("click", () => {
        document.getElementById("pop_out_message_box").style.display = "none";
        window.location.href = window.location.pathname;
    });
})