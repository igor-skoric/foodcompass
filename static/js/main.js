(function () {
  const nav = document.querySelector('[data-nav]');
  const burger = document.querySelector('[data-burger]');
  const mobile = document.querySelector('[data-mobile]');
  const backdrop = document.querySelector('[data-backdrop]');
  const html = document.documentElement;
  const backToTop = document.querySelector('.back-to-top');
  const loader = document.querySelector('[data-home-loader]');

  function setOpen(open) {
    if (!nav || !burger || !mobile) return;
    nav.classList.toggle('is-open', open);
    burger.classList.toggle('is-active', open);
    mobile.classList.toggle('is-open', open);
    if (backdrop) backdrop.classList.toggle('is-open', open);
    burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    burger.setAttribute('aria-label', open ? 'Zatvori meni' : 'Otvori meni');
    mobile.setAttribute('aria-hidden', open ? 'false' : 'true');
    html.classList.toggle('nav-open', open);
    if (nav.classList.contains('nav--home')) {
      const solid = open || window.scrollY > 32;
      nav.classList.toggle('is-transparent', !solid);
      nav.classList.toggle('is-solid', solid);
    }
  }

  if (burger) {
    burger.addEventListener('click', function () {
      setOpen(!nav.classList.contains('is-open'));
    });
  }
  if (backdrop) backdrop.addEventListener('click', function () { setOpen(false); });

  document.addEventListener('click', function (event) {
    document.querySelectorAll('.lang-switch__drop[open]').forEach(function (drop) {
      if (!drop.contains(event.target)) drop.removeAttribute('open');
    });
  });

  if (nav && nav.classList.contains('nav--home')) {
    const onScroll = function () {
      const solid = window.scrollY > 32 || nav.classList.contains('is-open');
      nav.classList.toggle('is-transparent', !solid);
      nav.classList.toggle('is-solid', solid);
    };
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
  }

  document.querySelectorAll('.reveal').forEach(function (el) {
    const observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15, rootMargin: '0px 0px -40px 0px' }
    );
    observer.observe(el);
  });

  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  const journey = document.querySelector('[data-journey]');
  if (journey) {
    if (reducedMotion) {
      journey.classList.add('is-playing', 'is-static');
    } else {
      const observer = new IntersectionObserver(
        function (entries) {
          if (entries[0] && entries[0].isIntersecting) {
            journey.classList.add('is-playing');
            observer.disconnect();
          }
        },
        { threshold: 0.18, rootMargin: '0px 0px -6% 0px' }
      );
      observer.observe(journey);
    }
  }

  const journeyPage = document.querySelector('[data-journey-page]');
  if (journeyPage) {
    const map = journeyPage.querySelector('[data-journey-map]');
    const progress = journeyPage.querySelector('[data-journey-progress]');
    const chapters = journeyPage.querySelectorAll('[data-journey-chapter]');
    const links = journeyPage.querySelectorAll('[data-journey-link]');

    function setJourneyActive(id) {
      links.forEach(function (link) {
        const on = link.getAttribute('data-journey-link') === id;
        link.classList.toggle('is-active', on);
        if (on) link.setAttribute('aria-current', 'step');
        else link.removeAttribute('aria-current');
      });
    }

    function playWhenVisible(el, threshold) {
      if (!el) return;
      if (reducedMotion) {
        el.classList.add('is-playing', 'is-static');
        return;
      }
      const observer = new IntersectionObserver(
        function (entries) {
          if (entries[0] && entries[0].isIntersecting) {
            el.classList.add('is-playing');
            observer.disconnect();
          }
        },
        { threshold: threshold || 0.2, rootMargin: '0px 0px -8% 0px' }
      );
      observer.observe(el);
    }

    playWhenVisible(map, 0.18);
    chapters.forEach(function (chapter) {
      playWhenVisible(chapter, 0.22);
    });

    if (progress && map) {
      const mapWatch = new IntersectionObserver(
        function (entries) {
          const inView = entries[0] && entries[0].isIntersecting;
          progress.classList.toggle('is-visible', !inView);
        },
        { threshold: 0, rootMargin: '-72px 0px 0px 0px' }
      );
      mapWatch.observe(map);
    }

    if (chapters.length) {
      const spy = new IntersectionObserver(
        function (entries) {
          const visible = entries
            .filter(function (entry) { return entry.isIntersecting; })
            .sort(function (a, b) { return b.intersectionRatio - a.intersectionRatio; })[0];
          if (visible) setJourneyActive(visible.target.getAttribute('data-journey-chapter'));
        },
        { rootMargin: '-28% 0px -46% 0px', threshold: [0.12, 0.35, 0.6] }
      );
      chapters.forEach(function (chapter) { spy.observe(chapter); });
      setJourneyActive(chapters[0].getAttribute('data-journey-chapter'));
    }
  }

  if (backToTop) {
    const onScrollTop = function () {
      backToTop.classList.toggle('is-visible', window.scrollY > 320);
    };
    onScrollTop();
    window.addEventListener('scroll', onScrollTop, { passive: true });
    backToTop.addEventListener('click', function () {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }

  const heroSlider = document.querySelector('[data-hero-slider]');
  if (heroSlider) {
    const slides = heroSlider.querySelectorAll('.hero__photo');
    if (slides.length > 1) {
      let index = 0;
      window.setInterval(function () {
        slides[index].classList.remove('is-active');
        index = (index + 1) % slides.length;
        slides[index].classList.add('is-active');
      }, 3000);
    }
  }

  if (loader) {
    if (sessionStorage.getItem('fc-home-loader-v3')) {
      loader.remove();
    } else {
      html.classList.add('is-loading');
      window.setTimeout(function () {
        loader.classList.add('is-leaving');
        window.setTimeout(function () {
          sessionStorage.setItem('fc-home-loader-v3', '1');
          loader.remove();
          html.classList.remove('is-loading');
        }, 500);
      }, 2800);
    }
  }
})();
