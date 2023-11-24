function submitForm() {
    const mainInput = document.getElementById('mainInput').value;

    // You can perform additional validation here

    fetchCrawledData(mainInput);
}

function fetchCrawledData(mainInput) {
    // You can use fetch API to make a request to your backend (Flask/Django) here
    // and update the #outputContainer with the result.
    // For simplicity, let's just display an alert for now.
    alert(`Crawling data for: ${mainInput}`);
}
