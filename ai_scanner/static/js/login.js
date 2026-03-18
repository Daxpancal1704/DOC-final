/**
 * Login Form - JavaScript Enhancement
 */

// Toggle password visibility
function togglePasswordVisibility(fieldId) {
  const field = document.getElementById(fieldId);
  const toggle = event.target;

  if (field.type === 'password') {
    field.type = 'text';
    toggle.textContent = '🙈';
  } else {
    field.type = 'password';
    toggle.textContent = '👁';
  }
}

// Initialize form on DOM ready
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  if (!form) return;

  // Add password toggle if it exists
  const passwordField = form.querySelector('input[name="password"]');
  if (passwordField) {
    // Wrap password field with password-wrapper for toggle
    const wrapper = document.createElement('div');
    wrapper.className = 'password-wrapper';
    passwordField.parentNode.insertBefore(wrapper, passwordField);
    wrapper.appendChild(passwordField);

    // Add toggle button
    const toggle = document.createElement('span');
    toggle.className = 'password-toggle';
    toggle.textContent = '👁';
    toggle.onclick = function(e) {
      e.preventDefault();
      if (passwordField.type === 'password') {
        passwordField.type = 'text';
        toggle.textContent = '🙈';
      } else {
        passwordField.type = 'password';
        toggle.textContent = '👁';
      }
    };
    wrapper.appendChild(toggle);
  }

  // Add focus animations
  const inputs = form.querySelectorAll('.form-control');
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.closest('.form-group')?.style.opacity = '1';
    });

    input.addEventListener('blur', function() {
      validateField(this);
    });
  });

  // Form submission
  form.addEventListener('submit', function(e) {
    let isValid = true;

    // Check if there are existing Django errors
    const hasErrors = form.querySelector('.error-message') ||
                     Array.from(inputs).some(input => {
                       return input.parentElement.closest('.form-group')?.querySelector('.field-error');
                     });

    if (!hasErrors) {
      inputs.forEach(input => {
        if (!validateField(input)) {
          isValid = false;
        }
      });

      if (!isValid) {
        e.preventDefault();
        animateError(form);
      }
    }
  });

  // Style any existing errors
  styleDjangoErrors(form);
});

// Validate individual field
function validateField(field) {
  const formGroup = field.parentElement.closest('.form-group');
  if (!formGroup) return true;

  if (!field.value.trim()) {
    addFieldError(formGroup, 'This field is required');
    return false;
  }

  if (field.name === 'username' && field.value.length < 3) {
    addFieldError(formGroup, 'Username must be at least 3 characters');
    return false;
  }

  if (field.name === 'password' && field.value.length < 6) {
    addFieldError(formGroup, 'Password must be at least 6 characters');
    return false;
  }

  removeFieldError(formGroup);
  return true;
}

// Add error to field
function addFieldError(formGroup, message) {
  let errorDiv = formGroup.querySelector('.field-error');

  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    formGroup.appendChild(errorDiv);
  }

  errorDiv.textContent = message;
  formGroup.classList.add('has-error');
}

// Remove error from field
function removeFieldError(formGroup) {
  const errorDiv = formGroup.querySelector('.field-error');
  if (errorDiv) {
    errorDiv.remove();
  }
  formGroup.classList.remove('has-error');
}

// Animate error state
function animateError(form) {
  const box = form.closest('.login-box');
  if (box) {
    box.style.animation = 'none';
    setTimeout(() => {
      box.style.animation = 'shakeError 0.4s';
    }, 10);
  }
}

// Style Django form errors
function styleDjangoErrors(form) {
  const formGroups = form.querySelectorAll('.form-group');

  formGroups.forEach(group => {
    const errorDiv = group.querySelector('.field-error');
    const input = group.querySelector('.form-control');

    if (errorDiv && errorDiv.textContent.trim() && input) {
      input.style.borderColor = 'var(--error)';
      input.style.background = 'rgba(239, 68, 68, 0.05)';
    }
  });
}

// Handle button loading state
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  if (!form) return;

  const button = form.querySelector('.login-btn');
  if (!button) return;

  form.addEventListener('submit', function() {
    // Only disable if there are no existing errors
    if (!form.querySelector('.error-message') &&
        !form.querySelector('.field-error')) {
      button.disabled = true;
      button.textContent = 'Logging in...';
    }
  });
});

// Enter key to submit
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  if (!form) return;

  const inputs = form.querySelectorAll('.form-control');
  inputs.forEach(input => {
    input.addEventListener('keypress', function(e) {
      if (e.key === 'Enter') {
        e.preventDefault();
        form.dispatchEvent(new Event('submit'));
      }
    });
  });
});

// Smooth focus indicator
document.addEventListener('DOMContentLoaded', function() {
  const inputs = document.querySelectorAll('.form-control');

  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.style.outline = 'none';
    });

    input.addEventListener('blur', function() {
      this.style.outline = 'none';
    });
  });
});

// Remember username (optional)
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  if (!form) return;

  const usernameField = form.querySelector('input[name="username"]');
  if (!usernameField) return;

  // Load saved username
  const savedUsername = localStorage.getItem('login_username');
  if (savedUsername) {
    usernameField.value = savedUsername;
  }

  // Save username on change
  usernameField.addEventListener('change', function() {
    localStorage.setItem('login_username', this.value);
  });
});

// Add visual feedback on successful input
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  if (!form) return;

  const inputs = form.querySelectorAll('.form-control');
  inputs.forEach(input => {
    input.addEventListener('input', function() {
      if (this.value.trim().length > 0) {
        this.style.borderColor = 'var(--border-dark)';
      } else {
        this.style.borderColor = '';
      }
    });
  });
});

// Prevent autocomplete issues
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('form');
  if (!form) return;

  // Allow browser autocomplete but handle it gracefully
  const inputs = form.querySelectorAll('.form-control');
  inputs.forEach(input => {
    input.addEventListener('autofill', function() {
      this.style.boxShadow = 'inset 0 0 0 1000px var(--bg-secondary)';
    });
  });
});