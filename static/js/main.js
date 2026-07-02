// Footer year
(function () {
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();
})();

// Bounce demo video: the raw recording is slow, so default it to 2x on first play.
// Talks to the embed via YouTube's postMessage protocol (needs enablejsapi=1 on the
// iframe src); only forces the rate once so viewers can still slow it back down.
(function () {
  var iframe = document.getElementById('bounce-demo');
  if (!iframe) return;

  var YT_ORIGIN = 'https://www.youtube.com';
  var forced = false;

  window.addEventListener('message', function (e) {
    if (forced || e.origin !== YT_ORIGIN || typeof e.data !== 'string') return;
    var d;
    try { d = JSON.parse(e.data); } catch (err) { return; }
    if (d.info && d.info.playerState === 1) { // 1 = playing
      forced = true;
      iframe.contentWindow.postMessage(
        JSON.stringify({ event: 'command', func: 'setPlaybackRate', args: [2] }),
        YT_ORIGIN
      );
    }
  });

  function listen() {
    iframe.contentWindow.postMessage(JSON.stringify({ event: 'listening', id: 'bounce-demo' }), YT_ORIGIN);
  }
  iframe.addEventListener('load', listen);
  listen();
})();

// Certification lightbox (homepage only)
(function () {
  var cards = Array.prototype.slice.call(document.querySelectorAll('.cert-card'));
  var lightbox = document.getElementById('lightbox');
  if (!cards.length || !lightbox) return;

  var lbImg = document.getElementById('lightboxImg');
  var lbCaption = document.getElementById('lightboxCaption');
  var current = 0;

  function show(i) {
    current = (i + cards.length) % cards.length;
    var img = cards[current].querySelector('img');
    lbImg.src = img.src;
    lbImg.alt = img.alt;
    lbCaption.textContent = img.alt;
  }

  cards.forEach(function (card, i) {
    card.addEventListener('click', function () { show(i); lightbox.showModal(); });
  });

  document.getElementById('lightboxClose').addEventListener('click', function () { lightbox.close(); });
  document.getElementById('lightboxNext').addEventListener('click', function () { show(current + 1); });
  document.getElementById('lightboxPrev').addEventListener('click', function () { show(current - 1); });

  // Click on the backdrop (outside the image/controls) closes
  lightbox.addEventListener('click', function (e) {
    if (e.target === lightbox) lightbox.close();
  });

  // Esc & focus-trap are handled natively by <dialog>; we add arrow keys
  lightbox.addEventListener('keydown', function (e) {
    if (e.key === 'ArrowRight') show(current + 1);
    else if (e.key === 'ArrowLeft') show(current - 1);
  });

  // Swipe navigation on touch devices
  var touchX = null;
  lightbox.addEventListener('touchstart', function (e) { touchX = e.changedTouches[0].clientX; }, { passive: true });
  lightbox.addEventListener('touchend', function (e) {
    if (touchX === null) return;
    var dx = e.changedTouches[0].clientX - touchX;
    if (Math.abs(dx) > 50) show(current + (dx < 0 ? 1 : -1));
    touchX = null;
  }, { passive: true });
})();
