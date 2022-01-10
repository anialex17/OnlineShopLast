$(document).ready(function(){

    $('input[type="file"]').on('change', function(){
        var fullPath = $(this).val();
        if (fullPath) {
            var startIndex = (fullPath.indexOf('\\') >= 0 ? fullPath.lastIndexOf('\\') : fullPath.lastIndexOf('/'));
            var filename = fullPath.substring(startIndex);
            if (filename.indexOf('\\') === 0 || filename.indexOf('/') === 0) {
                filename = filename.substring(1);
            }
            $(this).parents('.form_block').addClass('uploaded');
            $(this).parents('.form_block').find('.file_name').text(filename);
        }
    });

    $('.file_delete').click(function(){
        $(this).parents('.form_block').removeClass('uploaded').find('input').val('');
    });

});