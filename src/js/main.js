// Main JavaScript for St. Stephen's Capital Website

document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS (Animate On Scroll)
    initAnimations();
    
    // Initialize counters for stats section
    initCounters();
    
    // Add smooth scrolling for anchor links
    initSmoothScroll();
    
    // Add active class to current nav item
    highlightCurrentPage();
    
    // Mobile menu toggle behavior
    initMobileMenu();
});

// Initialize animations for elements
function initAnimations() {
    const fadeElements = document.querySelectorAll('.fade-in');
    const slideElements = document.querySelectorAll('.slide-up');
    
    // Create an observer for fade-in elements
    const fadeObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                fadeObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    // Create an observer for slide-up elements
    const slideObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.transform = 'translateY(0)';
                entry.target.style.opacity = '1';
                slideObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });
    
    // Apply initial styles and observe elements
    fadeElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transition = 'opacity 1s ease-in-out';
        fadeObserver.observe(el);
    });
    
    slideElements.forEach(el => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(50px)';
        el.style.transition = 'transform 0.8s ease-in-out, opacity 0.8s ease-in-out';
        slideObserver.observe(el);
    });
}

// Initialize counters for statistics
function initCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = entry.target;
                const countTo = parseInt(target.getAttribute('data-count'));
                const duration = 2000; // 2 seconds
                let count = 0;
                const step = Math.ceil(countTo / (duration / 30)); // Update every 30ms
                
                const timer = setInterval(() => {
                    count += step;
                    if (count >= countTo) {
                        target.textContent = countTo.toLocaleString();
                        clearInterval(timer);
                    } else {
                        target.textContent = count.toLocaleString();
                    }
                }, 30);
                
                counterObserver.unobserve(target);
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// Smooth scrolling for anchor links
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL without page reload
                history.pushState(null, null, targetId);
            }
        });
    });
}

// Highlight current page in navigation
function highlightCurrentPage() {
    const currentPage = window.location.pathname.split('/').pop();
    
    document.querySelectorAll('.nav-link').forEach(link => {
        const linkHref = link.getAttribute('href');
        
        if (linkHref === currentPage || 
            (currentPage === '' && linkHref === 'index.html') || 
            (currentPage === '/' && linkHref === 'index.html')) {
            link.classList.add('active');
        }
    });
}

// Mobile menu behavior
function initMobileMenu() {
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');
    
    if (navbarToggler && navbarCollapse) {
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            const isNavbarToggler = navbarToggler.contains(e.target);
            const isNavbarCollapse = navbarCollapse.contains(e.target);
            
            if (!isNavbarToggler && !isNavbarCollapse && navbarCollapse.classList.contains('show')) {
                // Use Bootstrap's collapse API to hide the menu
                bootstrap.Collapse.getInstance(navbarCollapse).hide();
            }
        });
        
        // Close mobile menu when clicking on a nav link
        document.querySelectorAll('.navbar-nav .nav-link').forEach(link => {
            link.addEventListener('click', function() {
                if (navbarCollapse.classList.contains('show')) {
                    bootstrap.Collapse.getInstance(navbarCollapse).hide();
                }
            });
        });
    }
}

// Testimonial carousel controls
function nextTestimonial() {
    const carousel = document.querySelector('#testimonialCarousel');
    if (carousel) {
        bootstrap.Carousel.getInstance(carousel).next();
    }
}

function prevTestimonial() {
    const carousel = document.querySelector('#testimonialCarousel');
    if (carousel) {
        bootstrap.Carousel.getInstance(carousel).prev();
    }
}

// Form validation
function validateForm(formId) {
    const form = document.getElementById(formId);
    if (!form) return false;
    
    if (!form.checkValidity()) {
        event.preventDefault();
        event.stopPropagation();
        form.classList.add('was-validated');
        return false;
    }
    
    form.classList.add('was-validated');
    return true;
}
