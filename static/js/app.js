$(function() {
    $('.acc_item').on('click', function () {
        var name = $(this).text();
        $('#megafon_table').empty();
        setTimeout(function() {
            load_megafon_table(name);
        }, 1000);
    });
});

function load_megafon_table(name) {
    console.log(name);
    $( "#megafon_table").html($('<div />', { "class": 'ajax-loader'}));
    var url = $BASE_URL + 'load_megafon_table/name=' + name;
    $( "#megafon_table" ).load( url ,
        function() {
        }
    );
}