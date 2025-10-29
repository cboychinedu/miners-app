
const emailForm = document.getElementById('emailForm');
const resetForm = document.getElementById('resetForm');
const alertBox = document.getElementById('alertBox');
const sendCodeBtn = document.getElementById('sendCodeBtn');
const resetBtn = document.getElementById('resetBtn');

// Function to display messages in the alert box
function displayMessage(message, type = 'info') {
    alertBox.textContent = message;
    alertBox.className = 'text-sm font-medium';
    if (type === 'success') {
        alertBox.classList.add('text-primary');
    } else if (type === 'error') {
        alertBox.classList.add('text-red-400');
    } else { // info
        alertBox.classList.add('text-yellow-400');
    }
}

// --- Step 1: Send Verification Code ---
async function sendVerificationCode(event) {
    event.preventDefault();
    const email = document.getElementById('recovery-email').value;

    if (!email) {
        displayMessage("Please enter your email address.", 'error');
        return;
    }

    displayMessage("Sending code...", 'info');
    sendCodeBtn.disabled = true;
    sendCodeBtn.textContent = 'Sending...';

    // 1. Send request to Flask route
    try {
        const response = await fetch('/api/forgot-password/send-code', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            displayMessage(result.message, 'success');
            // Hide email form and show reset form
            emailForm.classList.add('hidden');
            resetForm.classList.remove('hidden');
        } else {
            displayMessage(result.message || "Failed to send code. Please check your email.", 'error');
        }

    } catch (error) {
        console.error('Error sending verification code:', error);
        displayMessage("Network error. Could not reach server.", 'error');
    } finally {
        sendCodeBtn.disabled = false;
        sendCodeBtn.textContent = 'Send Verification Code';
    }
}

// --- Step 2: Reset Password ---
async function resetPassword(event) {
    event.preventDefault();
    const email = document.getElementById('recovery-email').value; // Still needed
    const code = document.getElementById('verification-code').value;
    const newPassword = document.getElementById('new-password').value;

    if (!code || !newPassword) {
        displayMessage("Verification code and new password are required.", 'error');
        return;
    }

    if (newPassword.length < 8) {
        displayMessage("New password must be at least 8 characters long.", 'error');
        return;
    }

    displayMessage("Resetting password...", 'info');
    resetBtn.disabled = true;
    resetBtn.textContent = 'Processing...';

    // 2. Send reset request to Flask route
    try {
        const response = await fetch('/api/forgot-password/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email: email,
                code: code,
                new_password: newPassword
            })
        });

        const result = await response.json();

        if (response.ok && result.success) {
            displayMessage("Password successfully reset! Redirecting to login...", 'success');
            // Redirect after a short delay
            setTimeout(() => {
                window.location.href = '/login'; 
            }, 2000); 
        } else {
            displayMessage(result.message || "Password reset failed. Check your code.", 'error');
        }

    } catch (error) {
        console.error('Error resetting password:', error);
        displayMessage("Network error. Could not reach server.", 'error');
    } finally {
        resetBtn.disabled = false;
        resetBtn.textContent = 'Reset Password';
    }
}