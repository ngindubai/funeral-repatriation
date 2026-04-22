/* Funeral Repatriation — Main JS
   Scroll reveal, header scroll state, mobile nav, FAQ accordion, quote form.
*/

(function () {
    'use strict';

    // ===== SCROLL REVEAL =====
    var revealEls = document.querySelectorAll('.reveal, .reveal-left, .reveal-right');
    if (revealEls.length && 'IntersectionObserver' in window) {
        var observer = new IntersectionObserver(function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });

        revealEls.forEach(function (el) { observer.observe(el); });
    } else {
        revealEls.forEach(function (el) { el.classList.add('visible'); });
    }

    // ===== PARALLAX HERO TEXT FADE =====
    var fadeEls = document.querySelectorAll('[data-parallax-fade]');
    var scrollHints = document.querySelectorAll('.scroll-hint');
    if (fadeEls.length) {
        var ticking = false;
        window.addEventListener('scroll', function () {
            if (!ticking) {
                window.requestAnimationFrame(function () {
                    var scrollY = window.scrollY;
                    var vh = window.innerHeight;
                    fadeEls.forEach(function (el) {
                        var progress = Math.min(scrollY / (vh * 0.6), 1);
                        el.style.opacity = 1 - progress;
                        el.style.transform = 'translateY(' + (scrollY * 0.3) + 'px)';
                    });
                    if (scrollY > 80) {
                        scrollHints.forEach(function (hint) { hint.style.opacity = '0'; });
                    } else {
                        scrollHints.forEach(function (hint) { hint.style.opacity = '1'; });
                    }
                    ticking = false;
                });
                ticking = true;
            }
        }, { passive: true });
    }

    // ===== HEADER SCROLL STATE =====
    var header = document.querySelector('.site-header');
    if (header) {
        var scrolled = false;
        window.addEventListener('scroll', function () {
            if (window.scrollY > 60 && !scrolled) {
                header.classList.add('scrolled');
                scrolled = true;
            } else if (window.scrollY <= 60 && scrolled) {
                header.classList.remove('scrolled');
                scrolled = false;
            }
        }, { passive: true });
    }

    // ===== MOBILE NAV TOGGLE =====
    var toggle = document.querySelector('.mobile-toggle');
    var nav = document.querySelector('.main-nav');
    if (toggle && nav) {
        toggle.addEventListener('click', function () {
            var expanded = toggle.getAttribute('aria-expanded') === 'true';
            toggle.setAttribute('aria-expanded', String(!expanded));
            nav.classList.toggle('open');
        });

        var navLinks = nav.querySelectorAll('a');
        navLinks.forEach(function (link) {
            link.addEventListener('click', function () {
                nav.classList.remove('open');
                toggle.setAttribute('aria-expanded', 'false');
            });
        });
    }

    // ===== FAQ ACCORDION =====
    var triggers = document.querySelectorAll('.faq-trigger');
    triggers.forEach(function (trigger) {
        trigger.addEventListener('click', function () {
            var expanded = trigger.getAttribute('aria-expanded') === 'true';
            var answerId = trigger.getAttribute('aria-controls');
            var answer = document.getElementById(answerId);
            if (!answer) return;

            trigger.setAttribute('aria-expanded', String(!expanded));
            answer.hidden = expanded;
        });
    });

    // ===== QUOTE FORM SUBMISSION =====
    var forms = document.querySelectorAll('.quote-form');
    forms.forEach(function (form) {
        var successMsg = form.parentElement.querySelector('.quote-success');
        if (!successMsg) return;

        form.addEventListener('submit', function (e) {
            e.preventDefault();

            var required = form.querySelectorAll('[required]');
            var valid = true;
            required.forEach(function (field) {
                if (!field.value.trim()) {
                    field.classList.add('field-error');
                    valid = false;
                } else {
                    field.classList.remove('field-error');
                }
            });

            var emailField = form.querySelector('[type="email"]');
            if (emailField && emailField.value && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(emailField.value)) {
                emailField.classList.add('field-error');
                valid = false;
            }

            // Honeypot check
            var honeypot = form.querySelector('[name="website"]');
            if (honeypot && honeypot.value) return;

            if (!valid) return;

            var data = new FormData(form);

            fetch(form.action, {
                method: 'POST',
                body: data,
                headers: { 'Accept': 'application/json' }
            }).then(function (response) {
                if (response.ok) {
                    form.style.display = 'none';
                    successMsg.hidden = false;
                }
            }).catch(function () {
                // Silently handle — form will remain visible
            });
        });
    });

})();
