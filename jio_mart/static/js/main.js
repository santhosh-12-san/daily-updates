document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('search-input');
    const suggestionBox = document.getElementById('suggestion-box');

    if (!searchInput) return;

    searchInput.addEventListener('keyup', () => {
        const query = searchInput.value.trim();

        if (query.length <= 1) {
            suggestionBox.style.display = 'none';
            return;
        }

        fetch(`/search_suggestions?q=${query}`)
            .then(response => response.json())
            .then(data => {
                suggestionBox.innerHTML = '';

                if (!data.length) {
                    suggestionBox.style.display = 'none';
                    return;
                }

                suggestionBox.style.display = 'block';

                data.forEach(item => {
                    const link = document.createElement('a');
                    link.className = 'suggestion-item';
                    link.textContent = item;
                    link.href = '#';

                    suggestionBox.appendChild(link);
                });
            });
    });

    document.addEventListener('click', event => {
        if (!searchInput.contains(event.target)) {
            suggestionBox.style.display = 'none';
        }
    });
});
