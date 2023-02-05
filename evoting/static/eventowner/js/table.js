$(document).ready( function () {
    $('#votetable').DataTable({
        paging: false,
        scrollY: '40vh',
        scrollCollapse: true,
        "search": {
            "smart": false
        }
    });
} );

$.fn.dataTable.ext.errMode = 'none';