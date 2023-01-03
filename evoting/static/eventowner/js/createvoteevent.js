// createvoteevent.js

// add option fields
function addOptions(){
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
function removeOptions(event){
    event.target.parentElement.remove();
}