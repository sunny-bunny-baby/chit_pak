// Search form handling
const searchForm = document.getElementById('searchForm');
if (searchForm) {
    searchForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const searchInput = document.getElementById('searchInput');
        const url = new URL(window.location.href);
        url.searchParams.set('search', searchInput.value);
        window.location.href = url.toString();
    });
}

// Cart quantity update
document.querySelectorAll('.cart-quantity').forEach(input => {
    input.addEventListener('change', async (e) => {
        const itemId = input.dataset.itemId;
        const quantity = e.target.value;

        const formData = new FormData();
        formData.append('quantity', quantity);

        const response = await fetch(`/cart/update/${itemId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        if (response.ok) {
            location.reload();
        }
    });
});

// Helper function for CSRF token
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