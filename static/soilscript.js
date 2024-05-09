document.getElementById('upload-form').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData(this);
    fetch('/soil/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('result').innerText = data;
        document.getElementById('result').style.display = "block";
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
