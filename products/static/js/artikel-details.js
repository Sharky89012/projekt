const detailContainer = document.getElementById('artikel-detail-container');

if (detailContainer) {
    const artikelId = detailContainer.dataset.id;

    fetch(`/api/artikel/${artikelId}/`)
        .then(response => response.json())
        .then(data => {
            const datum = new Date(data.datum);
            const heute = new Date();
            const istHeute = datum.toDateString() === heute.toDateString();
            const formattedDatum = `${datum.getMonth() + 1}.${datum.getDate()}.${datum.getFullYear()}`;

            const datumClass = istHeute ? 'datum-frisch' : 'datum-alt';
            const datumHinweis = istHeute ? '' : '<span class="datum-hinweis">(Der Preis kann abweichen – dieses Angebot ist alt)</span>';

            const html = `
                <div class="product-card p-4 border rounded">
                    <div class="text-center mb-4">
                        <img src="${data.picture}" alt="${data.title}" class="img-fluid" style="max-height: 300px;">
                    </div>
                    <h4 class="text-center fw-semibold">${data.title}</h4>
                    <div class="text-center preis-box mb-2">${data.preis}</div>
                    ${data.saving ? `<p class="text-center ersparnis-box">Ersparnis: ${data.saving}</p>` : ''}
                    <div class="text-center">
                        <a href="https://www.amazon.de/dp/${data.asin}?tag=sharkylinkref-21" target="_blank" class="amazon-btn">
                            <i class="bi bi-amazon"></i> Jetzt auf Amazon kaufen
                        </a>
                    </div>
                    <p class="mt-4 lh-lg text-justify">${data.beschreibung}</p>
                    <p class="text-muted small">ASIN: ${data.asin}</p>
                    <div class="text-center">
                        <span class="datum-badge ${datumClass}">Gefunden am: ${formattedDatum}</span>
                        ${datumHinweis}
                    </div>
                </div>`;
            detailContainer.innerHTML = html;
        })
        .catch(error => {
            detailContainer.innerHTML = '<p class="text-danger text-center">Fehler beim Laden der Artikeldaten.</p>';
            console.error('Fehler beim Laden des Artikels:', error);
        });
}
