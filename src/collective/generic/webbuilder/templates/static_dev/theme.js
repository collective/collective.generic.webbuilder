$(document).ready(function(){
    $('a.option-desc-url').html('<i class="fa fa-external-link"></i>');
    $(document).on('click', 'a[data-toggle="collapse"]', function(){
        var $close = $(this).find('i.fa-caret-square-o-right');
        var $open = $(this).find('i.fa-caret-square-o-down');
        if ($close.length == 1){
            $close.replaceWith('<i class="fa fa-caret-square-o-down"></i>');
        }else if ($open.length == 1){
            $open.replaceWith('<i class="fa fa-caret-square-o-right"></i>');
        }
    });
});