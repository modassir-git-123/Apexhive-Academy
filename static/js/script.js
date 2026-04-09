// Smooth scrolling
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        document.querySelector(this.getAttribute('href')).scrollIntoView({
            behavior: 'smooth'
        });
    });
});

// OTP input auto-focus
document.addEventListener('DOMContentLoaded', function() {
    const otpInput = document.querySelector('input[name="otp"]');
    if (otpInput) {
        otpInput.addEventListener('input', function(e) {
            this.value = this.value.replace(/[^0-9]/g, '').slice(0, 6);
        });
    }
    
    // Animate course cards on scroll
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            }
        });
    });
    
    document.querySelectorAll('.course-card').forEach(card => {
        observer.observe(card);
    });
});