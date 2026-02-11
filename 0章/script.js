// ===================================
// Smooth Scroll
// ===================================
document.querySelectorAll('a.smooth-scroll').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const targetId = this.getAttribute('href');
        if (!targetId || !targetId.startsWith('#')) return;

        const targetElement = document.querySelector(targetId);
        if (!targetElement) return;

        const headerOffset = 70;
        const elementPosition = targetElement.getBoundingClientRect().top;
        const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

        window.scrollTo({
            top: offsetPosition,
            behavior: 'smooth'
        });
    });
});

// ===================================
// Page Top Button
// ===================================
const pageTopButton = document.getElementById('pageTop');
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        pageTopButton.classList.add('show');
    } else {
        pageTopButton.classList.remove('show');
    }
});

// ===================================
// Header Shadow on Scroll
// ===================================
const header = document.querySelector('.header');
window.addEventListener('scroll', () => {
    if (window.pageYOffset > 80) {
        header.style.boxShadow = '0 6px 18px rgba(0, 0, 0, 0.12)';
    } else {
        header.style.boxShadow = 'none';
    }
});

// ===================================
// Reveal Animation
// ===================================
const revealElements = document.querySelectorAll('.reveal');
if (revealElements.length > 0) {
    const observer = new IntersectionObserver((entries, obs) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('is-visible');
                obs.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    revealElements.forEach(el => observer.observe(el));
}
