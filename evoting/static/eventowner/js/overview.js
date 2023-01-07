// overview.js


function deleteVoteEvent(event) {
    event.preventDefault()
    let confirmation = confirm("Do you want to delete the Vote Event ?");

    if (!confirmation) return;

    event.target.parentElement.submit();
}