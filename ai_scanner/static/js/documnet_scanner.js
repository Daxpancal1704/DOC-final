  /* Show loader on form submit */
  document.getElementById('scanForm').addEventListener('submit', function() {
    document.getElementById('scanLoader').classList.add('active');
    document.getElementById('scanBtn').disabled = true;
  });

  /* Drag-over highlight */
  const zone = document.getElementById('uploadZone');
  if (zone) {
    zone.addEventListener('dragover', e => { e.preventDefault(); zone.classList.add('drag-over'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', e => { e.preventDefault(); zone.classList.remove('drag-over'); });
  }

  /* Animate metric bars on load */
  window.addEventListener('load', () => {
    document.querySelectorAll('.metric-bar-fill').forEach(el => {
      el.style.width = el.style.getPropertyValue('--target');
    });
    /* Gauge */
    const gauge = document.querySelector('.gauge-fill');
    if (gauge) {
      const conf = parseFloat(gauge.style.getPropertyValue('--conf') || gauge.getAttribute('style').match(/--conf:\s*([\d.]+)/)?.[1] || 0);
      const total = 251.3;
      gauge.style.strokeDashoffset = total - (total * conf / 100);
    }
  });

  /* Stagger sentence rows */
  document.querySelectorAll('.sentence-row').forEach((row, i) => {
    row.style.animationDelay = (i * 0.05) + 's';
  });