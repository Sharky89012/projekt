$(document).ready(function () {
    const container = $('#savings-list');
    let currentOffset = 0;
    const limit = 20;
    let hasMore = true;
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

    function renderItems(items) {
        items.forEach(item => {
            const isFrisch = isToday(item.datum);
            const formattedDatum = formatDate(item.datum);
            const datumClass = isFrisch ? 'datum-frisch' : 'datum-alt';

            const html = `
                <div class="col-lg-6 col-md-6 col-12 mb-4">
                    <div class="product-card p-4 border rounded h-100 shadow-sm">
                        <a href="/artikel/${item.id}/">
                        <div class="text-center mb-3">
                          
                            <img src="${item.picture}" alt="${item.title}" class="img-fluid" style="max-height: 300px; object-fit: contain;">
                        
                        </div>
                        </a>
                        <h4 class="text-center fw-semibold" style="font-size: 0.95rem; line-height: 1.3; max-height: 2.6em; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical;">
                            ${item.title.length > 150 ? item.title.slice(0, 150) + '…' : item.title}
                        </h4>
                        <div class="text-center" style="font-size: 1.3rem; color: #28a745; font-weight: 700; margin-bottom: 6px;">
                            ${item.preis}
                        </div>
                        ${item.saving ? `<p class="text-center" style="background-color: #ffeaea; color: #cc0000; font-weight: bold; padding: 6px 10px; margin: 8px auto; display: inline-block; border-radius: 6px; font-size: 0.95rem;">🔥 Ersparnis: ${item.saving}</p>` : ''}
                        <div class="text-center mb-3">
                            <a href="/artikel/${item.id}/" class="btn btn-sm" style="background-color: #f2f2f2; border: 1px solid #ccc; margin-right: 6px; font-size: 0.85rem; padding: 6px 12px;">Info</a>
                            <a href="https://www.amazon.de/dp/${item.asin}?tag=sharkylinkref-21" target="_blank" class="btn btn-sm" style="background-color: #ff9900; color: white; font-size: 0.85rem; padding: 6px 12px;">
                                <i class="bi bi-amazon"></i> Jetzt kaufen
                            </a>
                        </div>
                        <p class="text-muted small text-center" style="font-size: 0.75rem;">ASIN: ${item.asin}</p>
                        
                    </div>
                </div>`;
            container.append(html);
        });
        isLoading = false;
    }

    function loadMore() {
        if (!hasMore || isLoading) return;
        isLoading = true;

        fetch(`/api/all-produkte-sorted/?limit=${limit}&offset=${currentOffset}`)
            .then(res => res.json())
            .then(data => {
                if (data.results.length < limit) {
                    hasMore = false;
                }
                currentOffset += data.results.length;
                renderItems(data.results);
            })
            .catch(err => {
                console.error('Fehler beim Laden:', err);
            });
    }

    $(window).on('scroll', function () {
        const scrollTop = $(window).scrollTop();
        const windowHeight = $(window).height();
        const docHeight = $(document).height();

        if (!isLoading && scrollTop + windowHeight > docHeight * 0.5) {
            loadMore();
        }
    });

    loadMore();
});
