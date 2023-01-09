// overview.js

// pop out message box 
function display_pop_out_message_box(event, confirm_fn) {
    let message_box = document.getElementById("pop_out_message_box");
    
    let confirm_btn = document.getElementById("confirm_btn");
    confirm_btn.addEventListener("click", function () {
        confirm_fn(event)
    }, event)

    message_box.style.display = "block";
}

function hide_pop_out_message_box(){
    let message_box = document.getElementById("pop_out_message_box");
    message_box.style.display = "none";
}

function confirm_delete_event(event){
    event.target.parentElement.submit();
}

