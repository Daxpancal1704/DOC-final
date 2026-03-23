 /* ── Custom Cursor ── */
    const dot  = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    let mx = 0, my = 0, rx = 0, ry = 0;
 
    document.addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      dot.style.left  = mx + 'px';
      dot.style.top   = my + 'px';
    });
 
    (function animateRing() {
      rx += (mx - rx) * 0.14;
      ry += (my - ry) * 0.14;
      ring.style.left = rx + 'px';
      ring.style.top  = ry + 'px';
      requestAnimationFrame(animateRing);
    })();
 
    /* ── Navbar scroll effect ── */
    const nav = document.getElementById('mainNav');
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 20);
    }, { passive: true });
 
    /* ── Top progress bar ── */
    const bar = document.getElementById('top-progress');
    let prog = 0;
    const tick = setInterval(() => {
      prog += Math.random() * 18;
      if (prog >= 90) { clearInterval(tick); prog = 90; }
      bar.style.width = prog + '%';
    }, 120);
    window.addEventListener('load', () => {
      clearInterval(tick);
      bar.style.width = '100%';
      setTimeout(() => { bar.style.opacity = '0'; bar.style.transition = 'opacity 0.5s'; }, 400);
    });
 
    /* ── Scroll-reveal for any .reveal elements ── */
    const observer = new IntersectionObserver(entries => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          e.target.style.opacity = '1';
          e.target.style.transform = 'translateY(0)';
        }
      });
    }, { threshold: 0.1 });
 
    document.querySelectorAll('.reveal').forEach(el => {
      el.style.opacity = '0';
      el.style.transform = 'translateY(30px)';
      el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
      observer.observe(el);
    });
 
    /* ── Auto-dismiss alerts ── */
    document.querySelectorAll('.alert').forEach(a => {
      setTimeout(() => {
        a.style.transition = 'opacity 0.6s, max-height 0.6s';
        a.style.opacity = '0';
        a.style.maxHeight = '0';
        a.style.overflow = 'hidden';
        setTimeout(() => a.remove(), 700);
      }, 5000);
    });