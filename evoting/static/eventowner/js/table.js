$(document).ready( function () {
    $('#votetable').DataTable({
        paging: false,
        scrollY: '40vh',
        scrollCollapse: true,
    });
} );

$.fn.dataTable.ext.errMode = 'none';