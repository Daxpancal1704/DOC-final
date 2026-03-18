/**
 * Register Form - JavaScript Enhancement
 */

// Toggle password visibility
function togglePassword(fieldId) {
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
  const form = document.querySelector('.register-form');
  if (!form) return;

  const inputs = form.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');

  // Add focus/blur animations
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.parentElement.closest('.form-group').style.opacity = '1';
    });

    input.addEventListener('blur', function() {
      validateField(this);
    });

    // Real-time validation for password match
    if (input.name === 'password2') {
      input.addEventListener('input', function() {
        const password1 = form.querySelector('input[name="password1"]');
        if (password1 && password1.value && this.value && password1.value !== this.value) {
          this.parentElement.classList.add('password-mismatch');
        } else {
          this.parentElement.classList.remove('password-mismatch');
        }
      });
    }
  });

  // Form submission
  form.addEventListener('submit', function(e) {
    let isValid = true;

    // Only validate on client-side if Django hasn't already caught errors
    const hasErrors = form.querySelector('.form-error') ||
                     Array.from(inputs).some(input => {
                       return input.parentElement.closest('.form-group')?.querySelector('.error-text');
                     });

    if (!hasErrors) {
      inputs.forEach(input => {
        if (!validateField(input)) {
          isValid = false;
        }
      });

      if (!isValid) {
        e.preventDefault();
        animateError();
      }
    }
  });

  // Style Django form errors
  styleDjangoErrors();
});

// Style Django form errors properly
function styleDjangoErrors() {
  const formGroups = document.querySelectorAll('.form-group');

  formGroups.forEach(group => {
    const errorDiv = group.querySelector('.error-text');
    const input = group.querySelector('input');

    if (errorDiv && errorDiv.textContent.trim() && input) {
      input.style.borderColor = 'var(--error)';
      input.style.background = 'rgba(239, 68, 68, 0.05)';
    }
  });

  // Also check for ul.errorlist format
  const errorLists = document.querySelectorAll('ul.errorlist');
  errorLists.forEach(list => {
    const formGroup = list.closest('.form-group');
    if (formGroup) {
      const input = formGroup.querySelector('input');
      if (input) {
        input.style.borderColor = 'var(--error)';
        input.style.background = 'rgba(239, 68, 68, 0.05)';
      }
    }
  });
}

// Field validation
function validateField(field) {
  const formGroup = field.parentElement.closest('.form-group');

  if (!field.value.trim()) {
    addFieldError(formGroup, 'This field is required');
    return false;
  }

  if (field.name === 'email' && !isValidEmail(field.value)) {
    addFieldError(formGroup, 'Please enter a valid email');
    return false;
  }

  if (field.name === 'password1' && field.value.length < 8) {
    addFieldError(formGroup, 'Password must be at least 8 characters');
    return false;
  }

  if (field.name === 'password2') {
    const password1 = document.querySelector('input[name="password1"]');
    if (password1 && field.value !== password1.value) {
      addFieldError(formGroup, 'Passwords do not match');
      return false;
    }
  }

  removeFieldError(formGroup);
  return true;
}

// Email validation
function isValidEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

// Add error to field
function addFieldError(formGroup, message) {
  let errorDiv = formGroup.querySelector('.error-text');

  if (!errorDiv) {
    errorDiv = document.createElement('div');
    errorDiv.className = 'error-text';
    formGroup.appendChild(errorDiv);
  }

  errorDiv.textContent = message;
  formGroup.classList.add('has-error');

  const input = formGroup.querySelector('input');
  if (input) {
    input.style.borderColor = 'var(--error)';
    input.style.background = 'rgba(239, 68, 68, 0.05)';
  }
}

// Remove error from field
function removeFieldError(formGroup) {
  const errorDiv = formGroup.querySelector('.error-text');
  if (errorDiv && !errorDiv.textContent.includes('This field is required')) {
    errorDiv.remove();
  }
  formGroup.classList.remove('has-error');

  const input = formGroup.querySelector('input');
  if (input) {
    input.style.borderColor = '';
    input.style.background = '';
  }
}

// Animate error state
function animateError() {
  const container = document.querySelector('.register-container');
  if (container) {
    container.style.animation = 'none';
    setTimeout(() => {
      container.style.animation = 'shakeError 0.4s';
    }, 10);
  }
}

// Handle button loading state
document.addEventListener('DOMContentLoaded', function() {
  const form = document.querySelector('.register-form');
  if (!form) return;

  const button = form.querySelector('.btn-register');
  if (!button) return;

  form.addEventListener('submit', function() {
    // Only disable if there are no existing errors
    if (!form.querySelector('.form-error') && !form.querySelector('.error-text')) {
      button.disabled = true;
      button.textContent = 'Creating Account...';
    }
  });
});

// Accessibility improvements
document.addEventListener('DOMContentLoaded', function() {
  const inputs = document.querySelectorAll('input[type="text"], input[type="email"], input[type="password"]');
  
  inputs.forEach(input => {
    input.addEventListener('focus', function() {
      this.style.outline = 'none';
    });
    
    input.addEventListener('blur', function() {
      this.style.outline = 'none';
    });
  });
});