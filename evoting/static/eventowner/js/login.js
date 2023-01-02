// login.js 

const MD5_Hash = new Hashes.MD5();

function submit_login(){
    input_ele = document.getElementById("password_input");
    input_ele.value = MD5_Hash.hex(input_ele.value);
}