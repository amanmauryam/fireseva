(function() {
    var form = document.getElementById('contact-form');
    var formContainer = form;
    var successDiv = document.getElementById('contact-success');
    var submitBtn = document.getElementById('contact-submit-btn');
    var btnText = document.getElementById('contact-btn-text');
    var btnSpinner = document.getElementById('contact-btn-spinner');

    var CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]').value;

    function clearErrors() {
        document.querySelectorAll('[data-contact-error]').forEach(function(el) {
            el.classList.add('hidden');
            el.textContent = '';
        });
        document.querySelectorAll('#contact-form input, #contact-form select, #contact-form textarea').forEach(function(el) {
            el.classList.remove('border-red-500');
        });
    }

    function showError(field, msg) {
        var errorEl = document.querySelector('[data-contact-error="' + field + '"]');
        var inputEl = document.getElementById('contact-' + field);
        if (errorEl) {
            errorEl.textContent = msg;
            errorEl.classList.remove('hidden');
        }
        if (inputEl) {
            inputEl.classList.add('border-red-500');
        }
    }

    function setLoading(loading) {
        if (loading) {
            btnText.textContent = 'Sending...';
            btnSpinner.classList.remove('hidden');
            submitBtn.disabled = true;
        } else {
            btnText.textContent = 'Send Message';
            btnSpinner.classList.add('hidden');
            submitBtn.disabled = false;
        }
    }

    function showSuccess() {
        formContainer.classList.add('hidden');
        successDiv.classList.remove('hidden');
    }

    function resetForm() {
        formContainer.classList.remove('hidden');
        successDiv.classList.add('hidden');
        form.reset();
    }

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        clearErrors();

        var formData = new FormData(form);
        var payload = {};
        formData.forEach(function(value, key) {
            payload[key] = value;
        });

        setLoading(true);

        fetch(window.CONTACT_URLS.submitEnquiry, {
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
                showSuccess();
            }
        })
        .catch(function(err) {
            if (err && err.errors) {
                Object.keys(err.errors).forEach(function(field) {
                    showError(field, err.errors[field]);
                });
            } else {
                showError('name', 'Something went wrong. Please try again.');
            }
        })
        .finally(function() {
            setLoading(false);
        });
    });

})();
