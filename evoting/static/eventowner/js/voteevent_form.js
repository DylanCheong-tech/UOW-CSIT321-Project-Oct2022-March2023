// voteevent_form.js

// add option fields
function addOptions() {
    vote_options = document.querySelectorAll("input[name=voteOption]");

    button_ele = document.querySelector("span#vote_options>button");
    frame_ele = document.getElementById("vote_options");

    newSpan = document.createElement("span");
    newSpan.classList.add("fields");

    newOptionField = document.createElement("input");
    newOptionField.type = "text";
    newOptionField.name = "voteOption";
    newOptionField.placeholder = "Vote Option";

    newRemoveButton = document.createElement("button");
    newRemoveButton.type = "button";
    newRemoveButton.innerHTML = "Remove";
    newRemoveButton.onclick = removeOptions.bind(event);

    newSpan.appendChild(newOptionField);
    newSpan.appendChild(newRemoveButton);

    // append the new element before the button element 
    frame_ele.insertBefore(newSpan, button_ele);
}

// remove the option fields
function removeOptions(event) {
    event.target.parentElement.remove();
}

document.addEventListener("DOMContentLoaded", () => {
    // download voter email csv template csv file 
    content = "data:text/csv;charset=utf-8,Voter Name,Email\nAdam,adam@mail.com\nBrabara,brabara@mail.com"
    document.getElementById("csv_downloader").href = encodeURI(content)
})

// back to home page button
function backToHomepage(){
    window.location.href = "/evoting/eventowner/homepage"
}

// preprocess the form data before submit 
function formSubmit(event) {
    options = document.querySelectorAll("input[name=voteOption]");
    options_str = ""
    // concat all the options to be submit 
    options.forEach((option, index) => {
        if (option.value.trim().length > 0) {
            if (index == options.length - 1)
                options_str += option.value
            else
                options_str += option.value + "|"
        }
    });

    options[options.length - 1].value = options_str
}