/**
 * Cart JavaScript - Handle add to cart, update quantity, and remove operations
 */

// Add to cart functionality
document.addEventListener('DOMContentLoaded', function() {
    // Handle all add-to-cart forms
    const addToCartForms = document.querySelectorAll('.add-to-cart-form');
    
    addToCartForms.forEach(form => {
        form.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const button = form.querySelector('button[type="submit"]');
            const originalText = button.innerHTML;
            
            // Disable button and show loading
            button.disabled = true;
            button.innerHTML = 'Adding...';
            
            try {
                const response = await fetch('/cart/add', {
                    method: 'POST',
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Update cart count in navbar
                    updateCartCount(data.cart_count);
                    
                    // Show success toast
                    showToast('Product added to cart!', 'success');
                    
                    // Reset button
                    button.innerHTML = '✓ Added';
                    setTimeout(() => {
                        button.innerHTML = originalText;
                        button.disabled = false;
                    }, 2000);
                } else {
                    showToast(data.message || 'Failed to add to cart', 'error');
                    button.innerHTML = originalText;
                    button.disabled = false;
                }
            } catch (error) {
                console.error('Error:', error);
                showToast('An error occurred', 'error');
                button.innerHTML = originalText;
                button.disabled = false;
            }
        });
    });
});

// Update cart quantity
async function updateQuantity(productId, newQuantity) {
    if (newQuantity < 1) {
        // If quantity is 0, remove the item
        removeFromCart(productId);
        return;
    }
    
    const formData = new FormData();
    formData.append('product_id', productId);
    formData.append('quantity', newQuantity);
    
    try {
        const response = await fetch('/cart/update', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Reload page to update cart display
            location.reload();
        } else {
            showToast(data.message || 'Failed to update cart', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('An error occurred', 'error');
    }
}

// Remove from cart
async function removeFromCart(productId) {
    if (!confirm('Remove this item from cart?')) {
        return;
    }
    
    const formData = new FormData();
    formData.append('product_id', productId);
    
    try {
        const response = await fetch('/cart/remove', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Reload page to update cart display
            location.reload();
        } else {
            showToast(data.message || 'Failed to remove from cart', 'error');
        }
    } catch (error) {
        console.error('Error:', error);
        showToast('An error occurred', 'error');
    }
}

// Update cart count in navbar
function updateCartCount(count) {
    const cartCountElement = document.getElementById('cart-count');
    if (cartCountElement) {
        cartCountElement.textContent = count;
        
        // Animate the badge
        cartCountElement.classList.add('scale-125');
        setTimeout(() => {
            cartCountElement.classList.remove('scale-125');
        }, 300);
    }
}

// Show toast notification
function showToast(message, type = 'success') {
    const toast = document.getElementById('toast');
    
    if (!toast) {
        // Create toast if it doesn't exist
        const toastDiv = document.createElement('div');
        toastDiv.id = 'toast';
        toastDiv.className = 'fixed bottom-4 right-4 px-6 py-3 rounded-lg shadow-lg transform translate-y-20 transition-transform duration-300';
        toastDiv.innerHTML = `<p class="font-medium"></p>`;
        document.body.appendChild(toastDiv);
    }
    
    const toastElement = document.getElementById('toast');
    const messageElement = toastElement.querySelector('p');
    
    // Set message and style
    messageElement.textContent = message;
    
    if (type === 'success') {
        toastElement.className = 'fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg transform transition-transform duration-300';
    } else {
        toastElement.className = 'fixed bottom-4 right-4 bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg transform transition-transform duration-300';
    }
    
    // Show toast
    setTimeout(() => {
        toastElement.classList.remove('translate-y-20');
    }, 100);
    
    // Hide toast after 3 seconds
    setTimeout(() => {
        toastElement.classList.add('translate-y-20');
    }, 3000);
}
