(function() {
    var overlay = document.getElementById('enquiry-overlay');
    var drawer = document.getElementById('enquiry-drawer');
    var closeBtn = document.getElementById('enquiry-close');
    var form = document.getElementById('enquiry-form');
    var formContainer = document.getElementById('enquiry-form-container');
    var successDiv = document.getElementById('enquiry-success');
    var submitBtn = document.getElementById('enquiry-submit-btn');
    var btnText = document.getElementById('enquiry-btn-text');
    var btnSpinner = document.getElementById('enquiry-btn-spinner');

    var CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function getKey() { return 'enquiry_popup_shown'; }
    function getSubmittedKey() { return 'enquiry_submitted'; }

    function openDrawer() {
        overlay.classList.remove('hidden');
        drawer.classList.remove('translate-x-full');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer(reset) {
        drawer.classList.add('translate-x-full');
        overlay.classList.add('hidden');
        document.body.style.overflow = '';
        if (reset !== false) {
            resetForm();
        }
    }

    function resetForm() {
        formContainer.classList.remove('hidden');
        successDiv.classList.add('hidden');
        form.reset();
    }

    function showSuccess() {
        formContainer.classList.add('hidden');
        successDiv.classList.remove('hidden');
    }

    function canAutoOpen() {
        if (sessionStorage.getItem(getKey())) return false;
        if (sessionStorage.getItem(getSubmittedKey())) return false;
        return true;
    }

    function markShown() { sessionStorage.setItem(getKey(), '1'); }

    function tryAutoOpen() {
        if (!canAutoOpen()) return;
        markShown();
        openDrawer();
    }

    // auto-open: 5 seconds
    setTimeout(function() {
        tryAutoOpen();
    }, 5000);

    // auto-open: 30% scroll
    var scrolled = false;
    window.addEventListener('scroll', function() {
        if (scrolled) return;
        var scrollPct = window.scrollY / (document.documentElement.scrollHeight - window.innerHeight);
        if (scrollPct >= 0.30) {
            scrolled = true;
            tryAutoOpen();
        }
    });

    // close on X
    closeBtn.addEventListener('click', function() { closeDrawer(); });

    // close on overlay click
    overlay.addEventListener('click', function() { closeDrawer(); });

    // escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !drawer.classList.contains('translate-x-full')) {
            closeDrawer();
        }
    });

    // form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // clear previous errors
        document.querySelectorAll('[data-error]').forEach(function(el) {
            el.classList.add('hidden');
            el.textContent = '';
        });
        document.querySelectorAll('input, select, textarea').forEach(function(el) {
            el.classList.remove('border-red-500');
        });

        var formData = new FormData(form);
        var payload = {};
        formData.forEach(function(value, key) {
            payload[key] = value;
        });

        btnText.textContent = 'Sending...';
        btnSpinner.classList.remove('hidden');
        submitBtn.disabled = true;

        fetch(window.APP_URLS.submitEnquiry, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': CSRF_TOKEN,
            },
            body: JSON.stringify(payload),
        })
        .then(function(res) {
            return res.json().then(function(data) {
                if (!res.ok) {
                    throw data;
                }
                return data;
            });
        })
        .then(function(data) {
            if (data.success) {
                sessionStorage.setItem(getSubmittedKey(), '1');
                showSuccess();
            }
        })
        .catch(function(err) {
            if (err && err.errors) {
                Object.keys(err.errors).forEach(function(field) {
                    var errorEl = document.querySelector('[data-error="' + field + '"]');
                    var inputEl = document.getElementById('enq-' + field);
                    if (errorEl) {
                        errorEl.textContent = err.errors[field];
                        errorEl.classList.remove('hidden');
                    }
                    if (inputEl) {
                        inputEl.classList.add('border-red-500');
                    }
                });
            }
        })
        .finally(function() {
            btnText.textContent = 'Send Enquiry';
            btnSpinner.classList.add('hidden');
            submitBtn.disabled = false;
        });
    });

})();
