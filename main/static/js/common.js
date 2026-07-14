/* ============================================================
   FireMitra - Fire Safety Installation Services Landing Page
   Custom JavaScript
   ============================================================ */

(function () {
  'use strict';

  // ============================================================
  // 1. PRELOADER
  // ============================================================
  var preloader = document.getElementById('preloader');
  if (preloader) {
    window.addEventListener('load', function () {
      preloader.classList.add('hidden');
      setTimeout(function () { preloader.style.display = 'none'; }, 600);
    });
    setTimeout(function () {
      if (!preloader.classList.contains('hidden')) {
        preloader.classList.add('hidden');
        setTimeout(function () { preloader.style.display = 'none'; }, 600);
      }
    }, 3000);
  }

  // ============================================================
  // 2. DEBOUNCE UTILITY
  // ============================================================
  function debounce(fn, delay) {
    var timer;
    return function () {
      var ctx = this, args = arguments;
      clearTimeout(timer);
      timer = setTimeout(function () { fn.apply(ctx, args); }, delay);
    };
  }

  function isInView(el, offset) {
    if (!el) return false;
    offset = offset || 0;
    var rect = el.getBoundingClientRect();
    var vh = window.innerHeight || document.documentElement.clientHeight;
    return rect.top <= vh - offset && rect.bottom >= offset;
  }

  // ============================================================
  // 3. NAVBAR SCROLL EFFECT
  // ============================================================
  var navbar = document.querySelector('nav');

  function handleNavbar() {
    navbar.classList.toggle('scrolled', window.scrollY > 60);
  }
  window.addEventListener('scroll', debounce(handleNavbar, 10), { passive: true });
  handleNavbar();

  // ============================================================
  // 4. RESPONSIVE TOGGLE (desktop links vs hamburger)
  // ============================================================
  var desktopLinks = document.getElementById('desktopLinks');
  var menuToggle = document.getElementById('menuToggle');
  var ctaBtn = document.getElementById('ctaBtn');

  function handleResponsive() {
    if (!desktopLinks || !menuToggle || !ctaBtn) return;
    var wide = window.innerWidth >= 900;
    desktopLinks.style.display = wide ? 'block' : 'none';
    menuToggle.style.display = wide ? 'none' : 'flex';
    ctaBtn.style.display = wide ? 'inline-flex' : 'none';
  }
  if (desktopLinks && menuToggle && ctaBtn) {
    window.addEventListener('resize', debounce(handleResponsive, 100));
    handleResponsive();
  }

  // ============================================================
  // 5. MOBILE MENU
  // ============================================================
  var mobileMenu = document.getElementById('mobileMenu');
  var mobileOverlay = document.getElementById('mobileOverlay');
  var closeBtn = document.getElementById('closeMobile');

  function openMobile() {
    mobileMenu.classList.add('open');
    mobileOverlay.classList.add('open');
    document.body.style.overflow = 'hidden';
  }
  function closeMobile() {
    mobileMenu.classList.remove('open');
    mobileOverlay.classList.remove('open');
    document.body.style.overflow = '';
  }
  if (menuToggle) menuToggle.addEventListener('click', openMobile);
  if (closeBtn) closeBtn.addEventListener('click', closeMobile);
  if (mobileOverlay) mobileOverlay.addEventListener('click', closeMobile);

  document.querySelectorAll('.mobile-link').forEach(function (link) {
    link.addEventListener('click', closeMobile);
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && mobileMenu && mobileMenu.classList.contains('open')) closeMobile();
  });

  // ============================================================
  // 6. ACTIVE NAV LINK
  // ============================================================
  var sections = document.querySelectorAll('section[id]');
  var navLinks = document.querySelectorAll('.nav-link[data-nav="d"]');

  function updateActive() {
    var scrollY = window.scrollY + 120;
    var current = '';
    sections.forEach(function (s) {
      var top = s.offsetTop;
      var bottom = top + s.offsetHeight;
      if (scrollY >= top && scrollY < bottom) current = s.id;
    });
    navLinks.forEach(function (l) {
      l.classList.toggle('active', l.getAttribute('href') === '#' + current);
    });
  }
  window.addEventListener('scroll', debounce(updateActive, 50), { passive: true });
  window.addEventListener('load', updateActive);

  // ============================================================
  // 7. SMOOTH SCROLL
  // ============================================================
  document.querySelectorAll('a[href^="#"]').forEach(function (a) {
    a.addEventListener('click', function (e) {
      var target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        var offset = navbar ? navbar.offsetHeight : 70;
        window.scrollTo({ top: target.getBoundingClientRect().top + window.scrollY - offset, behavior: 'smooth' });
      }
    });
  });

  // ============================================================
  // 8. SCROLL REVEAL (IntersectionObserver)
  // ============================================================
  var revealEls = document.querySelectorAll('.reveal, .reveal-l, .reveal-r, .reveal-s');
  if ('IntersectionObserver' in window) {
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

  // ============================================================
  // 9. COUNTER ANIMATION
  // ============================================================
  var counterEls = document.querySelectorAll('.counter-value[data-target]');
  var counted = false;

  function startCounters() {
    if (counted) return;
    var holder = counterEls[0];
    if (!holder) return;
    if (!isInView(holder.closest('section') || holder.parentElement, 80)) return;
    counted = true;

    counterEls.forEach(function (el) {
      var target = parseInt(el.getAttribute('data-target'), 10);
      var duration = 2000;
      var start = null;
      function step(ts) {
        if (!start) start = ts;
        var p = Math.min((ts - start) / duration, 1);
        var eased = 1 - Math.pow(1 - p, 3);
        el.textContent = Math.floor(eased * target);
        if (p < 1) requestAnimationFrame(step);
        else el.textContent = target;
      }
      requestAnimationFrame(step);
    });
  }

  var counterParent = counterEls[0];
  if (counterParent && 'IntersectionObserver' in window) {
    var counterObs = new IntersectionObserver(function (entries) {
      entries.forEach(function (e) { if (e.isIntersecting) { startCounters(); counterObs.unobserve(e.target); } });
    }, { threshold: 0.3 });
    counterObs.observe(counterParent.closest('section') || counterParent.parentElement);
  } else {
    setTimeout(startCounters, 800);
  }

  // ============================================================
  // 10. PARTICLE CANVAS (Hero)
  // ============================================================
  var canvas = document.getElementById('particle-canvas');
  if (canvas) {
    var ctx = canvas.getContext('2d');
    var particles = [];
    var pCount = 50;
    var mouseX = -9999, mouseY = -9999;

    function resize() {
      canvas.width = canvas.parentElement.offsetWidth;
      canvas.height = canvas.parentElement.offsetHeight;
    }
    resize();
    window.addEventListener('resize', debounce(resize, 200));

    document.addEventListener('mousemove', function (e) {
      var rect = canvas.getBoundingClientRect();
      mouseX = e.clientX - rect.left;
      mouseY = e.clientY - rect.top;
    });

    function createParticles() {
      particles = [];
      for (var i = 0; i < pCount; i++) {
        particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 2 + 0.5,
          sx: (Math.random() - 0.5) * 0.25,
          sy: (Math.random() - 0.5) * 0.25,
          o: Math.random() * 0.3 + 0.1
        });
      }
    }
    createParticles();

    function drawConnections() {
      for (var i = 0; i < particles.length; i++) {
        for (var j = i + 1; j < particles.length; j++) {
          var dx = particles[i].x - particles[j].x;
          var dy = particles[i].y - particles[j].y;
          var d = Math.sqrt(dx * dx + dy * dy);
          if (d < 130) {
            var alpha = (1 - d / 130) * 0.06;
            ctx.beginPath();
            ctx.moveTo(particles[i].x, particles[i].y);
            ctx.lineTo(particles[j].x, particles[j].y);
            ctx.strokeStyle = 'rgba(220, 38, 38, ' + alpha + ')';
            ctx.lineWidth = 0.5;
            ctx.stroke();
          }
        }
      }
    }

    function animate() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      for (var i = 0; i < particles.length; i++) {
        var p = particles[i];
        p.x += p.sx;
        p.y += p.sy;
        var dx = mouseX - p.x;
        var dy = mouseY - p.y;
        var d = Math.sqrt(dx * dx + dy * dy);
        if (d < 250 && d > 0) {
          var f = (250 - d) / 250 * 0.002;
          p.x += dx * f;
          p.y += dy * f;
        }
        if (p.x < -10) p.x = canvas.width + 10;
        if (p.x > canvas.width + 10) p.x = -10;
        if (p.y < -10) p.y = canvas.height + 10;
        if (p.y > canvas.height + 10) p.y = -10;
        ctx.beginPath();
        ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
        ctx.fillStyle = 'rgba(220, 38, 38, ' + p.o + ')';
        ctx.fill();
      }
      drawConnections();
      requestAnimationFrame(animate);
    }
    animate();

    window.addEventListener('resize', function () { resize(); createParticles(); });
  }

  // ============================================================
  // 11. HERO PARALLAX
  // ============================================================
  var hero = document.querySelector('.hero');
  if (hero) {
    var glow = hero.querySelector('.hero-glow');
    var content = hero.querySelector('.container');
    window.addEventListener('scroll', function () {
      var sy = window.scrollY;
      var hh = hero.offsetHeight;
      if (sy > hh) return;
      if (glow) glow.style.transform = 'translateY(' + (sy * 0.12) + 'px)';
      if (content) {
        content.style.transform = 'translateY(' + (sy * 0.06) + 'px)';
        content.style.opacity = 1 - (sy / hh) * 0.35;
      }
    }, { passive: true });
  }

  // ============================================================
  // 12. SERVICE CARD TILT
  // ============================================================
  document.querySelectorAll('.service-card').forEach(function (card) {
    card.addEventListener('mousemove', function (e) {
      var r = card.getBoundingClientRect();
      var x = e.clientX - r.left;
      var y = e.clientY - r.top;
      var rx = (y - r.height / 2) / (r.height / 2) * -3;
      var ry = (x - r.width / 2) / (r.width / 2) * 3;
      card.style.transform = 'perspective(800px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg) translateY(-6px)';
    });
    card.addEventListener('mouseleave', function () { card.style.transform = ''; });
  });

  // ============================================================
  // 13. BOUNCE KEYFRAME FOR SCROLL INDICATOR
  // ============================================================
  var style = document.createElement('style');
  style.textContent =
    '@keyframes bounceDown { 0%,100% { transform: translateX(-50%) translateY(0); } 50% { transform: translateX(-50%) translateY(6px); } }';
  document.head.appendChild(style);

})();



function toggleMobileMenu() {
    document.getElementById('mobile-menu').classList.toggle('hidden');
}

document.querySelectorAll('.nav-link').forEach(link => {
    link.addEventListener('click', function(e) {
        document.querySelectorAll('.nav-link').forEach(l => {
            l.classList.remove('active');
        });
        this.classList.add('active');
    });
});

function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

window.addEventListener('scroll', function() {
    const btn = document.getElementById('backToTop');
    if (window.scrollY > 400) {
        btn.classList.remove('hidden');
        btn.classList.add('flex');
    } else {
        btn.classList.add('hidden');
        btn.classList.remove('flex');
    }
});

function toggleWhatsApp() {
    document.getElementById('whatsapp-card').classList.toggle('hidden');
}



function openEnquiry() {
    document.getElementById('enquiry-drawer').classList.remove('translate-x-full');
    document.getElementById('enquiry-overlay').classList.remove('hidden');
}

function closeEnquiry() {
    document.getElementById('enquiry-drawer').classList.add('translate-x-full');
    document.getElementById('enquiry-overlay').classList.add('hidden');
}
document.getElementById('enquiry-overlay').addEventListener('click', closeEnquiry);