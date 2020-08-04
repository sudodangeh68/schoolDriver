document.ready(function () {
    $('.searchbtn').click(function () {
        $(this).toggleClass('bg-blue');
        $('.fas').toggleClass('color-white');
        $('.input').focus().toggleClass('active-width').val('');
    })
});