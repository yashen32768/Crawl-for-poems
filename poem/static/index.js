$(function () {
    $.ajax({
        url: '{{ url_for("autocomplete") }}'
    }).done(function (data) {
        $('#myInput').autocomplete({
            source: data,
            minLength: 2
        });
    });
});