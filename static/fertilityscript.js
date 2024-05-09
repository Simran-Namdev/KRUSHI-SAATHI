// script.js

$(document).ready(function(){
    $('#prediction-form').submit(function(event){
        event.preventDefault();
        $.ajax({
            type: 'POST',
            url: '/fertility/predict',
            data: $(this).serialize(),
            success: function(response){
                $('#result').html("<p>Predicted Soil Fertility Level: " + response + "</p>");
            }
        });
    });
});
