// script.js

$(document).ready(function(){
    $('#recommendation-form').submit(function(event){
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/fertilizer/recommend',
            data: $(this).serialize(),
            success: function(response){
                $('#result').html("<p>Recommended Fertilizer: " + response.recommended_fertilizer + "</p>");
            }
        });
    });
});
