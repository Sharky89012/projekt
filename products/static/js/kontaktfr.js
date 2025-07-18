document.querySelector('.subscribe-form').addEventListener('submit', function(e) {
    e.preventDefault();

    const email = document.getElementById('subscribe-email').value.trim();

    // Vorherige Nachricht entfernen
    const oldMessage = document.querySelector('.subscribe-message');
    if (oldMessage) oldMessage.remove();

    if (!email.includes('@')) {
        showMessage("Bitte gib eine gültige E-Mail-Adresse ein.", false);
        return;
    }

    fetch('/api/subscribe/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: `email=${encodeURIComponent(email)}`
    })
    .then(response => response.json())
    .then(data => {
        showMessage(data.message, data.success);
        if (data.success) {
            document.getElementById('subscribe-email').value = '';
        }
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function showMessage(text, isSuccess) {
        const msg = document.createElement('div');
        msg.className = 'subscribe-message';
        msg.style.marginTop = '12px';
        msg.style.padding = '10px';
        msg.style.borderRadius = '8px';
        msg.style.fontWeight = '500';
        msg.style.textAlign = 'center';
        msg.style.transition = 'opacity 0.3s ease';
        msg.style.opacity = '0';
        msg.style.backgroundColor = isSuccess ? '#d4edda' : '#f8d7da';
        msg.style.color = isSuccess ? '#155724' : '#721c24';
        msg.innerText = isSuccess ? 'Alles klar! Wir halten dich auf dem Laufenden 📬' : text;

        // Einfügen nach dem Formular
        document.querySelector('.subscribe-form-wrap').appendChild(msg);

        // Sichtbar machen
        setTimeout(() => { msg.style.opacity = '1'; }, 100);

        // Nach 6 Sekunden automatisch entfernen
        setTimeout(() => {
            msg.style.opacity = '0';
            setTimeout(() => msg.remove(), 300);
        }, 6000);
    }
});