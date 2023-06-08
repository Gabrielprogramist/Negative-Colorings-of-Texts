document.getElementById('classification-form').addEventListener('submit', function(event) {
  event.preventDefault();

  // Get form data
  var formData = new FormData(this);

  // Get CSRF token
  var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // Show loading message
  document.getElementById('loading').style.display = 'block';

  // Send a POST request to the server
  fetch('/', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrfToken
    }
  })
  .then(response => response.json())
  .then(data => {
    // Hide loading message
    document.getElementById('loading').style.display = 'none';

    // Display the classification results
    var resultsContainer = document.getElementById('classification-results');
    resultsContainer.innerHTML = '';
    for (var i = 0; i < data.classification.length; i++) {
      var result = data.classification[i];
      resultsContainer.innerHTML += '<h3>' + result[0] + ': ' + (result[1] * 100).toFixed(2) + '%</h3>';
    }
  })
  .catch(error => {
    // Hide loading message
    document.getElementById('loading').style.display = 'none';

    console.error('Error:', error);
  });
});
