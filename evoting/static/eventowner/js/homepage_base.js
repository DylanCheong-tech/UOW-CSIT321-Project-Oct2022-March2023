// homepage_base.js

// idle time counter 
let idle_time = 0

idle_timer_runner = setInterval(() => {
    idle_time++;

    // prompt the message in 8 minutes 
    if (idle_time > 8 * 60)
        document.getElementById("session_timeout_alert").style.display = "block";

    // auto logout after 10 minutes
    if (idle_time > 10 * 60)
        window.location.reload();

}, 1000);

// "Ok" button function from the alert message box 
function confirming_session() {
    document.getElementById("session_timeout_alert").style.display = "none";

    // make any request to refresh the session 
    fetch("/harpocryption/eventowner/homepage")
        .then(console.log)

    idle_time = 0;
}