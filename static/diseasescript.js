document.getElementById('uploadForm').addEventListener('submit', function(event) {
    event.preventDefault();
    var formData = new FormData();
    var fileInput = document.getElementById('fileInput');
    formData.append('file', fileInput.files[0]);
    
    fetch('/disease/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('resultDiv').innerText = 'Predicted Disease: ' + data.result;
        document.getElementById('resultDiv').style.display = 'block';
    })
    .catch(error => console.error('Error:', error));
});
