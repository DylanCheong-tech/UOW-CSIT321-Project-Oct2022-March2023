// vote_form.js

function submitVoteForm(){
    let auth_token = (new URLSearchParams(window.location.search)).get("auth");
    console.log(auth_token)

    document.querySelector("div#vote_booth form input[name=voterAuth]").value = auth_token;
}
