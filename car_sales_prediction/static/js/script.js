/**
 * Car Sales Price Prediction System
 * Main JavaScript File
 */

// ================================================
// DOM Ready
// ================================================

document.addEventListener('DOMContentLoaded', function() {
    console.log('App initialized');
    
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form validation
    initializeFormValidation();
    
    // Initialize modals if any
    initializeModals();
});

// ================================================
// Bootstrap Tooltips Initialization
// ================================================

function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// ================================================
// Form Validation
// ================================================

function initializeFormValidation() {
    const forms = document.querySelectorAll('.needs-validation');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// ================================================
// Modal Functions
// ================================================

function initializeModals() {
    // Add any modal initializations here
}

// ================================================
// Prediction Functions
// ================================================

/**
 * Make AJAX prediction request
 */
async function makePrediction(formData) {
    try {
        const response = await fetch('/api/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (response.ok) {
            displayPredictionResult(data.predicted_price);
            return true;
        } else {
            showError(data.error || 'Prediction failed');
            return false;
        }
    } catch (error) {
        console.error('Error:', error);
        showError('An error occurred while making the prediction');
        return false;
    }
}

/**
 * Display prediction result
 */
function displayPredictionResult(price) {
    const resultDiv = document.getElementById('predictionResult');
    if (resultDiv) {
        resultDiv.innerHTML = `
            <div class="alert alert-success alert-dismissible fade show" role="alert">
                <i class="fas fa-check-circle"></i> 
                <strong>Prediction Successful!</strong> 
                Estimated Price: <strong>₹${price.toFixed(2)} Lakhs</strong>
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
}

// ================================================
// Delete Functions
// ================================================

/**
 * Delete a prediction with confirmation
 */
async function deletePrediction(predictionId) {
    if (confirm('Are you sure you want to delete this prediction?')) {
        try {
            const response = await fetch(`/delete_prediction/${predictionId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                showSuccess('Prediction deleted successfully');
                setTimeout(() => {
                    location.reload();
                }, 1000);
            } else {
                showError(data.error || 'Failed to delete prediction');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred while deleting the prediction');
        }
    }
}

/**
 * Delete a user (admin only)
 */
async function deleteUser(userId) {
    if (confirm('Are you sure? This will delete the user and all their predictions.')) {
        try {
            const response = await fetch(`/admin/delete_user/${userId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            const data = await response.json();
            
            if (data.success) {
                const userRow = document.getElementById(`user-${userId}`);
                if (userRow) {
                    userRow.remove();
                    showSuccess('User deleted successfully');
                }
            } else {
                showError(data.error || 'Failed to delete user');
            }
        } catch (error) {
            console.error('Error:', error);
            showError('An error occurred');
        }
    }
}

// ================================================
// Notification Functions
// ================================================

/**
 * Show success message
 */
function showSuccess(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-success alert-dismissible fade show';
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        <i class="fas fa-check-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid') || document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 4000);
}

/**
 * Show error message
 */
function showError(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-danger alert-dismissible fade show';
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        <i class="fas fa-exclamation-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid') || document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 4000);
}

/**
 * Show info message
 */
function showInfo(message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = 'alert alert-info alert-dismissible fade show';
    alertDiv.setAttribute('role', 'alert');
    alertDiv.innerHTML = `
        <i class="fas fa-info-circle"></i> ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    const container = document.querySelector('.container-fluid') || document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    setTimeout(() => {
        alertDiv.remove();
    }, 4000);
}

// ================================================
// Utility Functions
// ================================================

/**
 * Format currency
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-IN', {
        style: 'currency',
        currency: 'INR'
    }).format(amount);
}

/**
 * Format date
 */
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('en-IN', options);
}

/**
 * Debounce function
 */
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), wait);
    };
}

/**
 * Throttle function
 */
function throttle(func, limit) {
    let inThrottle;
    return function(...args) {
        if (!inThrottle) {
            func.apply(this, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// ================================================
// Local Storage Functions
// ================================================

/**
 * Save user preference
 */
function savePreference(key, value) {
    localStorage.setItem(key, JSON.stringify(value));
}

/**
 * Get user preference
 */
function getPreference(key, defaultValue = null) {
    const value = localStorage.getItem(key);
    return value ? JSON.parse(value) : defaultValue;
}

/**
 * Remove user preference
 */
function removePreference(key) {
    localStorage.removeItem(key);
}

// ================================================
// API Helper Functions
// ================================================

/**
 * Generic fetch wrapper
 */
async function apiCall(url, options = {}) {
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    const mergedOptions = {
        ...defaultOptions,
        ...options,
        headers: {
            ...defaultOptions.headers,
            ...options.headers
        }
    };
    
    try {
        const response = await fetch(url, mergedOptions);
        const data = await response.json();
        
        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }
        
        return data;
    } catch (error) {
        console.error('API Error:', error);
        throw error;
    }
}

// ================================================
// Analytics & Tracking (Optional)
// ================================================

/**
 * Track interaction
 */
function trackEvent(eventName, eventData = {}) {
    console.log(`Event: ${eventName}`, eventData);
    // Add your analytics code here (Google Analytics, Mixpanel, etc.)
}

/**
 * Track page view
 */
function trackPageView(pageName) {
    console.log(`Page View: ${pageName}`);
    // Add your page tracking code here
}

// ================================================
// Performance Optimization
// ================================================

/**
 * Lazy load images
 */
function lazyLoadImages() {
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        document.querySelectorAll('img.lazy').forEach(img => {
            imageObserver.observe(img);
        });
    }
}

// ================================================
// Export Functions
// ================================================

// Make functions globally available if needed
window.makePrediction = makePrediction;
window.deletePrediction = deletePrediction;
window.deleteUser = deleteUser;
window.showSuccess = showSuccess;
window.showError = showError;
window.showInfo = showInfo;
window.formatCurrency = formatCurrency;
window.formatDate = formatDate;
