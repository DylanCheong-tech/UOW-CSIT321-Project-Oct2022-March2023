// singup.js 

function requestOTP() {
    let email_ele = document.querySelector("input[name=email]");
    let btn = document.getElementById("otp_request_btn");
    btn.disabled = true;
    //alert("OTP is sent to your email. You can request new OTP after 2 minutes.")
    setTimeout(()=>{
        btn.disabled = false;
        console.log('Button Activated')}, 120000)

    fetch("/evoting/eventowner/getOTP?email=" + email_ele.value)
        .then(console.log)
}

// password checker
function checkPassword(event) {
    let password = event.target.value;
    let on_indicator_color_stying = "#3F54BE";
    let off_indicator_color_stying = "#FFFFFF";

    // check for length 
    if (password.length >= 8 && password.length <= 32)
        document.getElementById("length_indicator").style.backgroundColor = on_indicator_color_stying
    else
        document.getElementById("length_indicator").style.backgroundColor = off_indicator_color_stying

    // check for spacing 
    if (!password.includes(" ") && password.length != 0)
        document.getElementById("spacing_indicator").style.backgroundColor = on_indicator_color_stying
    else
        document.getElementById("spacing_indicator").style.backgroundColor = off_indicator_color_stying

    // check for uppercase 
    upper_regex = new RegExp("[A-Z]")
    if (upper_regex.test(password))
        document.getElementById("uppercase_indicator").style.backgroundColor = on_indicator_color_stying
    else
        document.getElementById("uppercase_indicator").style.backgroundColor = off_indicator_color_stying

    // check for uppercase 
    lower_regex = new RegExp("[a-z]")
    if (lower_regex.test(password))
        document.getElementById("lowercase_indicator").style.backgroundColor = on_indicator_color_stying
    else
        document.getElementById("lowercase_indicator").style.backgroundColor = off_indicator_color_stying

    // check for digit 
    digit_regex = new RegExp("[0-9]")
    if (digit_regex.test(password))
        document.getElementById("digit_indicator").style.backgroundColor = on_indicator_color_stying
    else
        document.getElementById("digit_indicator").style.backgroundColor = off_indicator_color_stying

    // check for digit 
    special_char_regex = new RegExp("[_#?!@$%^&*-]")
    if (special_char_regex.test(password))
        document.getElementById("special_char_indicator").style.backgroundColor = on_indicator_color_stying
    else
        document.getElementById("special_char_indicator").style.backgroundColor = off_indicator_color_stying

}