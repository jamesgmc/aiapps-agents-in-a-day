// Basic JavaScript for the tournament site

// Auto-refresh functionality for active tournaments
function enableAutoRefresh() {
    const refreshInterval = 5000; // 5 seconds
    setInterval(function() {
        if (document.querySelector('.tournament-inprogress')) {
            location.reload();
        }
    }, refreshInterval);
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Add any initialization code here
    console.log('RPS Tournament application loaded');
});

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const alertClass = `alert-${type}`;
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert ${alertClass} alert-dismissible fade show position-fixed`;
    alertDiv.style.top = '20px';
    alertDiv.style.right = '20px';
    alertDiv.style.zIndex = '9999';
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alertDiv);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.parentNode.removeChild(alertDiv);
        }
    }, 5000);
}