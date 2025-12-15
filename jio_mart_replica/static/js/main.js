document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search-input');
    const suggestionBox = document.getElementById('suggestion-box');

    if (searchInput) {
        searchInput.addEventListener('keyup', function() {
            let query = this.value;
            
            if(query.length > 1) {
                fetch(`/search_suggestions?q=${query}`)
                .then(response => response.json())
                .then(data => {
                    suggestionBox.innerHTML = '';
                    if(data.length > 0) {
                        suggestionBox.style.display = 'block';
                        data.forEach(item => {
                            let div = document.createElement('a');
                            div.className = 'suggestion-item';
                            div.textContent = item;
                            div.href = '#'; // In a real app, link to product details
                            suggestionBox.appendChild(div);
                        });
                    } else {
                        suggestionBox.style.display = 'none';
                    }
                });
            } else {
                suggestionBox.style.display = 'none';
            }
        });

        // Close suggestions when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target)) {
                suggestionBox.style.display = 'none';
            }
        });
    }
});