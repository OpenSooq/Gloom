$(document).ready(function(){
    var clipboard = new ClipboardJS('.form-copy');
    clipboard.on('success', function(e) {
        console.log(e);
    });
    clipboard.on('error', function(e) {
        console.log(e);
    });

   $('body').on('click','[data-role="search-stats"]',function(e){
        e.stopPropagation();
        if(!$('#longUrl').val() == ""){
            var code = $('#longUrl').val();
            window.location.href = window.location.origin+'/'+code+'+'   
            return false;
        }
    });
});