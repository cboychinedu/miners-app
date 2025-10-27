// On document load, add the event listener 
document.addEventListener('DOMContentLoaded', () => {
    // --- Mobile Menu Toggle Logic ---
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    const openIcon = document.getElementById('menu-icon-open');
    const closeIcon = document.getElementById('menu-icon-close');

    menuButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
        openIcon.classList.toggle('hidden');
        closeIcon.classList.toggle('hidden');
    });
    
    // --- Scroll Reveal Logic ---
    // Options for the Intersection Observer
    const observerOptions = {
        root: null, // relative to the viewport
        rootMargin: '0px',
        threshold: 0.2 // Trigger when 20% of the item is visible
    };

    // Getting the observer 
    const observer = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                // Add the 'visible' class to trigger CSS transition
                entry.target.classList.add('visible');
                // Stop observing after it becomes visible
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Find all elements marked for scroll reveal and apply initial classes
    document.querySelectorAll('[class*="scroll-reveal"]').forEach(element => {
        // Apply the initial transformation class if not already present
        if (!element.classList.contains('slide-up') && !element.classList.contains('slide-left') && !element.classList.contains('slide-right') && !element.classList.contains('zoom-in')) {
                element.classList.add('slide-up'); // Default to slide-up if no specific animation is set
        }
        observer.observe(element);
    });
});