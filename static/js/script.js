// Service PRO JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Confirm delete actions
    var deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            var message = this.getAttribute('data-confirm-delete') || 'Are you sure you want to delete this item?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        });
    });

    // Format phone numbers as user types
    var phoneInputs = document.querySelectorAll('input[type="tel"]');
    phoneInputs.forEach(function(input) {
        input.addEventListener('input', function(e) {
            var value = e.target.value.replace(/\D/g, '');
            if (value.length <= 10) {
                e.target.value = value;
            }
        });
    });

    // Auto-resize textareas
    var textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = (this.scrollHeight) + 'px';
        });
    });

    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading state to forms
    var forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(e) {
            var submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                var originalText = submitBtn.innerHTML;
                submitBtn.innerHTML = '<span class="loading me-2"></span>Processing...';

                // Re-enable after 10 seconds as fallback
                setTimeout(function() {
                    submitBtn.disabled = false;
                    submitBtn.innerHTML = originalText;
                }, 10000);
            }
            // Continue with form submission
        });
    });

    // Password strength indicator
    var passwordInputs = document.querySelectorAll('input[type="password"]');
    passwordInputs.forEach(function(input) {
        if (input.id !== 'confirm_password') {
            input.addEventListener('input', function() {
                var strength = checkPasswordStrength(this.value);
                showPasswordStrength(strength);
            });
        }
    });

    // Initialize date/time pickers
    initializeDateTimePickers();

    // Real-time search functionality
    var searchInputs = document.querySelectorAll('input[data-search]');
    searchInputs.forEach(function(input) {
        var targetTable = document.querySelector(input.getAttribute('data-search'));
        if (targetTable) {
            input.addEventListener('input', function() {
                filterTable(targetTable, this.value);
            });
        }
    });
});

// Password strength checker
function checkPasswordStrength(password) {
    var strength = 0;
    var feedback = [];

    if (password.length >= 8) strength += 1;
    else feedback.push('At least 8 characters');

    if (/[a-z]/.test(password)) strength += 1;
    else feedback.push('Lowercase letter');

    if (/[A-Z]/.test(password)) strength += 1;
    else feedback.push('Uppercase letter');

    if (/[0-9]/.test(password)) strength += 1;
    else feedback.push('Number');

    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    else feedback.push('Special character');

    return {
        score: strength,
        feedback: feedback,
        text: getStrengthText(strength),
        color: getStrengthColor(strength)
    };
}

function getStrengthText(score) {
    if (score <= 1) return 'Very Weak';
    if (score <= 2) return 'Weak';
    if (score <= 3) return 'Fair';
    if (score <= 4) return 'Good';
    return 'Strong';
}

function getStrengthColor(score) {
    if (score <= 1) return 'danger';
    if (score <= 2) return 'warning';
    if (score <= 3) return 'info';
    if (score <= 4) return 'primary';
    return 'success';
}

function showPasswordStrength(strength) {
    var indicator = document.getElementById('password-strength-indicator');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'password-strength-indicator';
        indicator.className = 'mt-2';

        var passwordInput = document.querySelector('input[type="password"]:not(#confirm_password)');
        if (passwordInput && passwordInput.parentNode) {
            passwordInput.parentNode.appendChild(indicator);
        }
    }

    if (strength.score === 0) {
        indicator.innerHTML = '';
        return;
    }

    var progressBar = '<div class="progress" style="height: 5px;">' +
        '<div class="progress-bar bg-' + strength.color + '" style="width: ' + (strength.score * 20) + '%"></div>' +
        '</div>';

    var feedbackHtml = '<small class="text-' + strength.color + '">' +
        strength.text + ' password';

    if (strength.feedback.length > 0) {
        feedbackHtml += '<br><em>Suggestions: ' + strength.feedback.join(', ') + '</em>';
    }

    feedbackHtml += '</small>';

    indicator.innerHTML = progressBar + feedbackHtml;
}

// Initialize datetime-local inputs
function initializeDateTimePickers() {
    var dateTimeInputs = document.querySelectorAll('input[type="datetime-local"]');
    dateTimeInputs.forEach(function(input) {
        // Set minimum to current date/time
        var now = new Date();
        var offset = now.getTimezoneOffset();
        var localNow = new Date(now.getTime() - offset * 60000);
        var formattedNow = localNow.toISOString().slice(0, 16);

        if (!input.value) {
            input.min = formattedNow;
        }
    });
}

// Filter table based on search input
function filterTable(table, searchTerm) {
    var rows = table.querySelectorAll('tbody tr');
    var term = searchTerm.toLowerCase();

    rows.forEach(function(row) {
        var text = row.textContent.toLowerCase();
        var shouldShow = text.includes(term);
        row.style.display = shouldShow ? '' : 'none';
    });
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Utility function to format date
function formatDate(dateString) {
    var date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Show loading overlay
function showLoading(message = 'Loading...') {
    var overlay = document.createElement('div');
    overlay.id = 'loading-overlay';
    overlay.className = 'd-flex justify-content-center align-items-center position-fixed w-100 h-100';
    overlay.style.backgroundColor = 'rgba(0, 0, 0, 0.5)';
    overlay.style.zIndex = '9999';
    overlay.innerHTML = '<div class="text-center text-white">' +
        '<div class="loading mb-2"></div>' +
        '<div>' + message + '</div>' +
        '</div>';
    document.body.appendChild(overlay);
}

// Hide loading overlay
function hideLoading() {
    var overlay = document.getElementById('loading-overlay');
    if (overlay) {
        overlay.remove();
    }
}

// AJAX helper function
function ajaxRequest(url, method = 'GET', data = null) {
    return fetch(url, {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: data ? JSON.stringify(data) : null
    })
    .then(response => response.json())
    .catch(error => {
        console.error('AJAX Error:', error);
        throw error;
    });
}