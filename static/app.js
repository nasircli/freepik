document.addEventListener('DOMContentLoaded', function() {
    const crawlButton = document.getElementById('crawlButton');
    crawlButton.addEventListener('click', submitForm);
});

function submitForm() {
    const mainInput = document.getElementById('mainInput').value;
    // Perform any necessary validation on mainInput before making the request

    // Make an asynchronous request to your server with the mainInput value
    fetch('/crawl', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ mainInput: mainInput }),
    })
    .then(response => response.json())
    .then(data => {
        // Update the outputContainer with the response from the server
        const outputContainer = document.getElementById('outputContainer');
        outputContainer.innerHTML = ''; // Clear previous content
        if (data.crawled_data) {
            const tagsList = document.createElement('ul');
            data.crawled_data.forEach(tag => {
                const tagItem = document.createElement('li');
                tagItem.textContent = tag;
                tagsList.appendChild(tagItem);
            });
            outputContainer.appendChild(tagsList);
        } else if (data.error_message) {
            const errorMessage = document.createElement('p');
            errorMessage.textContent = data.error_message;
            outputContainer.appendChild(errorMessage);
        } else {
            const noDataMessage = document.createElement('p');
            noDataMessage.textContent = 'No data available.';
            outputContainer.appendChild(noDataMessage);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        // Handle the error appropriately, e.g., display an error message to the user
    });
}
