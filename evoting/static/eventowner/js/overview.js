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