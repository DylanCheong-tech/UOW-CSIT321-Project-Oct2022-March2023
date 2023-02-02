// overview.js

// pop out message box 
function display_pop_out_message_box(event,message_text) {
    let message_box = document.getElementById("pop_out_message_box");
    document.getElementById("message_content").innerHTML = message_text;
    
    let confirm_btn = document.getElementById("confirm_btn");
    confirm_btn.addEventListener("click", function () {
        confirm_submit_event(event)
    }, event)

    message_box.style.display = "block";
}

function hide_pop_out_message_box(){
    let message_box = document.getElementById("pop_out_message_box");
    message_box.style.display = "none";
}

function confirm_submit_event(event){
    event.target.parentElement.submit();
}

// check for the url params 
document.addEventListener("DOMContentLoaded", () => {
    // check pop up message box for the publication result status 
    let create_status = (new URLSearchParams(window.location.search)).get("create_status")
    let update_status = (new URLSearchParams(window.location.search)).get("update_status")

    if (create_status == "success") {
        document.getElementById("message_content").innerHTML = "Vote Event Created Successfully !"
    }
    else if (update_status == "success"){
        document.getElementById("message_content").innerHTML = "Vote Event Update Successfully !"
    }
    else{
        return;
    }

    document.getElementById("pop_out_message_box").style.display = "block";
    document.getElementById("cancel_btn").style.display = "none";

    document.getElementById("confirm_btn").addEventListener("click", () => {
        document.getElementById("pop_out_message_box").style.display = "none";
        window.location.href = window.location.pathname;
    });
})