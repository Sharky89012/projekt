document.querySelector('.search-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const query = document.getElementById('search').value.trim();
    if (query) {
        window.location.href = `/search?search=${encodeURIComponent(query)}`;
    }
});