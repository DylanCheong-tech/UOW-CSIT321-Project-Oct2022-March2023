// login.js 

const MD5_Hash = new Hashes.MD5();

function submit_login(){
    input_ele = document.getElementById("password_input");
    input_ele.value = MD5_Hash.hex(input_ele.value);
}

function checkForm(){
    if(!document.getElementById("g-recaptcha-response").value){
        alert("Please tick the captcha box!");
        return false;
    }else{
        document.getElementById("form_submit_btn").type = "submit";         
        return true;
    }
}