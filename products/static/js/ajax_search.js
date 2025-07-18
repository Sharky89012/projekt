$(document).ready(function () {
    const query = new URLSearchParams(window.location.search).get('search');
    if (!query) return;

    const container = $('#results-container');  // WICHTIG: NEUER Container
    let allItems = [];
    let itemsPerLoad = 8;
    let currentIndex = 0;
    let isLoading = false;

    function formatDate(dateStr) {
        const date = new Date(dateStr);
        return `${date.getDate().toString().padStart(2, '0')}.${(date.getMonth() + 1).toString().padStart(2, '0')}.${date.getFullYear()}`;
    }

    function isToday(dateStr) {
        const date = new Date(dateStr);
        const today = new Date();
        return date.getDate() === today.getDate() &&
               date.getMonth() === today.getMonth() &&
               date.getFullYear() === today.getFullYear();
    }

    function renderItems() {
        const slice = allItems.slice(currentIndex, currentIndex + itemsPerLoad);
        slice.forEach(item => {
            const isFrisch = isToday(item.datum);
            const formattedDatum = formatDate(item.datum);
            const datumClass = isFrisch ? 'datum-frisch' : 'datum-alt';
            const datumHinweis = isFrisch ? '' : '<div class="text-muted small text-center">Nicht mehr ganz frisch</div>';

            card.innerHTML = `
            <a href="/artikel/${item.id}/">
            <div class="product-card">
        <div class="product-image-wrapper">
        
            <img src="${item.picture}" alt="${item.title}" class="img-fluid" loading="lazy">
        
            </div>
        <div class="product-title">${item.title}</div>
        <div class="product-info mt-2">
            <div class="product-badges mb-1">
                <div class="text-center preis-box mb-2">${item.preis}</div>
            </div>
            </a>
            ${item.saving ? `<div class="text-danger fw-bold mb-2">Ersparnis: ${item.saving}</div>` : ''}
        </div>
        
        <div class="text-center mt-3">
            <a href="/artikel/${item.id}/" 
               class="btn btn-sm" 
               style="background-color: #f2f2f2; border: 1px solid #ccc; margin: 4px 6px 0 6px; font-size: 0.85rem; padding: 6px 12px;">
               Info
            </a>
            <a href="https://www.amazon.de/dp/${item.asin}?tag=sharkylinkref-21" 
               target="_blank" 
               class="btn btn-sm" 
               style="background-color: #ff9900; color: white; font-size: 0.85rem; padding: 6px 12px; margin: 4px 6px 0 6px;">
               <i class="bi bi-amazon"></i> Kaufen
            </a>
        </div>

        <div class="text-center small mt-2 mb-0 datum-badge ${datumClass}">Gefunden am: ${formattedDatum}</div>
    </div>
`;

            container.append(html); // ⬅️ Sicherstellen, dass an NEUEM Container angehängt wird
        });

        currentIndex += itemsPerLoad;
        isLoading = false;
    }

    function handleScroll() {
        const scrollTop = $(window).scrollTop();
        const winHeight = $(window).height();
        const docHeight = $(document).height();

        if (!isLoading && (scrollTop + winHeight) > (docHeight - winHeight * 1.5)) {
            if (currentIndex < allItems.length) {
                isLoading = true;
                renderItems();
            }
        }
    }

    // Daten holen und rendern
    $.getJSON(`/api/search/?search=${query}`, function (data) {
        allItems = data.results.sort((a, b) => new Date(b.datum) - new Date(a.datum));
        if (allItems.length > 0) {
            renderItems();
            $(window).on('scroll', handleScroll);
        } else {
            container.html('<p class="text-center">Keine Artikel gefunden.</p>');
        }
    });
});
