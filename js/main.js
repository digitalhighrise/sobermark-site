// Sobermark marketing site — progressive enhancement only.
// All content is in the HTML; this adds motion and the calculator.

const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ---------- sticky nav ---------- */
const navWrap = document.getElementById('navWrap');
const onScroll = () => navWrap.classList.toggle('is-scrolled', window.scrollY > 12);
window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

/* ---------- scroll reveal ---------- */
const revealEls = document.querySelectorAll('[data-reveal]');
if (reducedMotion || !('IntersectionObserver' in window)) {
  revealEls.forEach(el => el.classList.add('is-shown'));
} else {
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      const delay = Number(e.target.dataset.delay || 0);
      e.target.style.transitionDelay = delay + 'ms';
      e.target.classList.add('is-shown');
      io.unobserve(e.target);
    });
  }, { threshold: 0.14, rootMargin: '0px 0px -8% 0px' });
  revealEls.forEach(el => io.observe(el));
}

/* ---------- count-up ---------- */
const formats = {
  int: v => Math.round(v).toLocaleString('en-US'),
  money: v => '$' + Math.round(v).toLocaleString('en-US'),
  millions: v => (v / 1000000).toFixed(1) + 'M',
  'money-millions': v => '$' + (v / 1000000).toFixed(1) + 'M',
  pct: v => Math.round(v) + '%',
  rating: v => v.toFixed(1) + '★',
};
document.querySelectorAll('[data-countup]').forEach(el => {
  const target = Number(el.dataset.target);
  const fmt = formats[el.dataset.fmt] || formats.int;
  if (reducedMotion || !('IntersectionObserver' in window)) return; // keep static value
  const io = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (!e.isIntersecting) return;
      io.unobserve(el);
      const duration = 1600;
      const t0 = performance.now();
      const tick = now => {
        const p = Math.min(1, (now - t0) / duration);
        const eased = 1 - Math.pow(1 - p, 3);
        el.textContent = fmt(target * eased);
        if (p < 1) requestAnimationFrame(tick);
      };
      requestAnimationFrame(tick);
    });
  }, { threshold: 0.5 });
  io.observe(el);
});

/* ---------- savings calculator ---------- */
const perWeek = document.getElementById('perWeek');
const costEach = document.getElementById('costEach');
if (perWeek && costEach) {
  const money = v => '$' + Math.round(v).toLocaleString('en-US');
  const paintTrack = input => {
    const pct = ((input.value - input.min) / (input.max - input.min)) * 100;
    input.style.background = `linear-gradient(to right, var(--blue-500) ${pct}%, var(--slate-200) ${pct}%)`;
  };
  const update = () => {
    const n = Number(perWeek.value);
    const c = Number(costEach.value);
    const weekly = n * c;
    const yearly = weekly * 52;
    document.getElementById('perWeekOut').textContent = n;
    document.getElementById('costEachOut').textContent = '$' + c;
    document.getElementById('calcYearly').textContent = money(yearly);
    document.getElementById('calcWeekly').textContent = `that's ${money(weekly)} every week`;
    document.getElementById('calcFive').textContent = money(yearly * 5);
    document.getElementById('calcHours').textContent = Math.round(n * 1.5 * 52) + 'h';
    paintTrack(perWeek);
    paintTrack(costEach);
  };
  perWeek.addEventListener('input', update);
  costEach.addEventListener('input', update);
  update();
}

/* ---------- Bern companion lines ---------- */
document.querySelectorAll('#bernLines .bern-line').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#bernLines .bern-line').forEach(b => {
      b.classList.toggle('is-active', b === btn);
      b.setAttribute('aria-expanded', b === btn ? 'true' : 'false');
    });
  });
});

/* ---------- FAQ accordion ---------- */
document.querySelectorAll('#faqList .faq-item').forEach(item => {
  item.querySelector('.faq-q').addEventListener('click', () => {
    const isOpen = item.classList.contains('is-open');
    document.querySelectorAll('#faqList .faq-item').forEach(i => {
      i.classList.remove('is-open');
      i.querySelector('.faq-q').setAttribute('aria-expanded', 'false');
    });
    if (!isOpen) {
      item.classList.add('is-open');
      item.querySelector('.faq-q').setAttribute('aria-expanded', 'true');
    }
  });
});
