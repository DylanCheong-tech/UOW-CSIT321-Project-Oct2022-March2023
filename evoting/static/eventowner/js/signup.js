// singup.js 

function requestOTP() {
    email_ele = document.querySelector("input[name=email]");

    fetch("/evoting/eventowner/getOTP?email=" + email_ele.value)
        .then(console.log)
}