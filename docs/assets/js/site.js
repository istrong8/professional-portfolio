/* Irais Strong — portfolio interactions
   1. Mobile navigation
   2. Scroll reveal + active section
   3. Fig. 1  — analog Monte Carlo neutron transport in a slab
   4. Fig. P  — circumbinary orbit, velocity-Verlet, with energy-drift check
   Every animation pauses off-screen and when the tab is hidden, and
   respects prefers-reduced-motion. */
(function () {
  "use strict";
  document.documentElement.classList.add("js");

  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  /* ---------- 1. Mobile navigation ---------- */
  var toggle = document.querySelector(".navtoggle");
  var nav = document.getElementById("sitenav");
  if (toggle && nav) {
    var setOpen = function (open) {
      toggle.setAttribute("aria-expanded", String(open));
      nav.classList.toggle("is-open", open);
    };
    toggle.addEventListener("click", function () {
      setOpen(toggle.getAttribute("aria-expanded") !== "true");
    });
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) setOpen(false); });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && nav.classList.contains("is-open")) { setOpen(false); toggle.focus(); }
    });
  }

  /* ---------- 2. Reveal + active section ---------- */
  if ("IntersectionObserver" in window) {
    var revealEls = document.querySelectorAll(".section__head, .case, .domain, .diagram, .tools, .timeline li, .degree, .standards li, .beyond, .contact");
    revealEls.forEach(function (el) { el.classList.add("reveal"); });
    var ro = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add("is-in"); ro.unobserve(en.target); } });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    revealEls.forEach(function (el) { ro.observe(el); });

    var links = {};
    document.querySelectorAll('.sitenav a[href^="#"]').forEach(function (a) { links[a.getAttribute("href").slice(1)] = a; });
    var so = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        var a = links[en.target.id];
        if (a && en.isIntersecting) {
          Object.keys(links).forEach(function (k) { links[k].removeAttribute("aria-current"); });
          a.setAttribute("aria-current", "true");
        }
      });
    }, { rootMargin: "-45% 0px -50% 0px" });
    Object.keys(links).forEach(function (id) { var s = document.getElementById(id); if (s) so.observe(s); });
  }

  /* ---------- shared canvas helpers ---------- */
  function fitCanvas(canvas) {
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    var r = canvas.getBoundingClientRect();
    var w = Math.max(1, Math.round(r.width * dpr));
    var h = Math.max(1, Math.round(r.height * dpr));
    if (canvas.width !== w || canvas.height !== h) { canvas.width = w; canvas.height = h; }
    return { w: w, h: h, dpr: dpr };
  }

  // Runs `step` on rAF only while the element is visible and the tab is active.
  function visibleLoop(el, step) {
    var visible = false, running = false, paused = false, raf = 0;
    function frame(t) { if (!running) return; step(t); raf = requestAnimationFrame(frame); }
    function update() {
      var should = visible && !paused && !document.hidden;
      if (should && !running) { running = true; raf = requestAnimationFrame(frame); }
      else if (!should && running) { running = false; cancelAnimationFrame(raf); }
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (e) { visible = e[0].isIntersecting; update(); }, { threshold: 0.01 }).observe(el);
    } else { visible = true; }
    document.addEventListener("visibilitychange", update);
    update();
    return { setPaused: function (p) { paused = p; update(); }, isPaused: function () { return paused; } };
  }

  /* ---------- 3. Monte Carlo neutron transport ----------
     Units: lengths in mean free paths (Σt = 1). Slab occupies 0 ≤ x ≤ T.
     Each collision: absorbed with probability 1 − c, otherwise isotropic scatter.
     Directions are sampled in 3-D (μ = cosθ uniform on [−1, 1]); the drawn
     track is the projection onto the x–y plane. */
  (function transport() {
    var canvas = document.getElementById("transport");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");
    var T = 3, C = 0.7;
    var X0 = -1.5, X1 = 4.5;               // visible x-range in mfp
    var trail = document.createElement("canvas");
    var tctx = trail.getContext("2d");
    var dims, scale, cy;
    var tally = { n: 0, t: 0, r: 0, a: 0, u: 0 };
    var out = {};
    document.querySelectorAll("[data-r]").forEach(function (el) { out[el.getAttribute("data-r")] = el; });
    var VIOLET = "167,139,250", HI = "217,204,255", BLUE = "142,160,255";

    function resize() {
      dims = fitCanvas(canvas);
      trail.width = dims.w; trail.height = dims.h;
      scale = dims.w / (X1 - X0);
      cy = dims.h / 2;
    }
    function px(x) { return (x - X0) * scale; }
    function py(y) { return cy - y * scale; }

    // Build one complete history as a polyline + fate.
    function history() {
      var x = 0, y = (Math.random() - 0.5) * 1.1, mu = 1, v = 0;   // normally incident
      var pts = [[x, y]], collided = false, fate;
      for (var k = 0; k < 200; k++) {
        var s = -Math.log(1 - Math.random());
        var nx = x + mu * s, ny = y + v * s;
        if (nx >= T || nx <= 0) {
          // leak: extend to view edge for drawing
          var edge = nx >= T ? X1 + 0.2 : X0 - 0.2;
          var f = (edge - x) / (mu || 1e-9);
          pts.push([edge, y + v * f]);
          fate = nx >= T ? "t" : "r";
          break;
        }
        x = nx; y = ny; pts.push([x, y]); collided = true;
        if (Math.random() > C) { fate = "a"; break; }
        mu = 2 * Math.random() - 1;
        var phi = 2 * Math.PI * Math.random();
        v = Math.sqrt(1 - mu * mu) * Math.cos(phi);
      }
      if (!fate) fate = "a";
      tally.n++; tally[fate]++;
      if (fate === "t" && !collided) tally.u++;
      return { pts: pts, fate: fate, seg: 0, f: 0 };
    }

    function pct(k) { return tally.n ? (100 * tally[k] / tally.n).toFixed(1) + "%" : "—"; }
    function writeReadout() {
      out.n.textContent = tally.n.toLocaleString("en-US");
      out.t.textContent = pct("t"); out.r.textContent = pct("r");
      out.a.textContent = pct("a");
      if (tally.n) {
        var pu = tally.u / tally.n, sig = Math.sqrt(pu * (1 - pu) / tally.n);
        out.u.textContent = (100 * pu).toFixed(2) + " ± " + (100 * sig).toFixed(2) + "%";
      }
    }

    function drawSlab() {
      var x0 = px(0), x1 = px(T);
      var g = ctx.createLinearGradient(x0, 0, x1, 0);
      g.addColorStop(0, "rgba(" + VIOLET + ",.07)");
      g.addColorStop(1, "rgba(" + VIOLET + ",.025)");
      ctx.fillStyle = g; ctx.fillRect(x0, 0, x1 - x0, dims.h);
      ctx.strokeStyle = "rgba(" + VIOLET + ",.55)"; ctx.lineWidth = dims.dpr;
      ctx.beginPath(); ctx.moveTo(x0, 0); ctx.lineTo(x0, dims.h); ctx.moveTo(x1, 0); ctx.lineTo(x1, dims.h); ctx.stroke();
      // mfp ticks
      ctx.strokeStyle = "rgba(205,190,255,.08)";
      ctx.beginPath();
      for (var i = 1; i < T; i++) { ctx.moveTo(px(i), 0); ctx.lineTo(px(i), dims.h); }
      ctx.stroke();
      // incident beam marker
      ctx.fillStyle = "rgba(" + HI + ",.55)";
      ctx.font = "500 " + 10 * dims.dpr + "px 'IBM Plex Mono', monospace";
      ctx.fillText("beam →", px(-1.35), cy - 0.75 * scale);
    }

    function strokeSeg(c, a, b, color, alpha, w) {
      c.strokeStyle = "rgba(" + color + "," + alpha + ")"; c.lineWidth = w;
      c.beginPath(); c.moveTo(px(a[0]), py(a[1])); c.lineTo(px(b[0]), py(b[1])); c.stroke();
    }
    function dot(c, p, color, alpha, r) {
      c.fillStyle = "rgba(" + color + "," + alpha + ")";
      c.beginPath(); c.arc(px(p[0]), py(p[1]), r, 0, Math.PI * 2); c.fill();
    }

    resize();

    if (reduceMotion) {
      // Static: run statistics once, draw a fixed sample of complete tracks.
      var sample = [];
      for (var i = 0; i < 40000; i++) { var h = history(); if (i < 70) sample.push(h); }
      var paintStatic = function () {
        resize();
        ctx.fillStyle = "#0a0911"; ctx.fillRect(0, 0, dims.w, dims.h);
        drawSlab();
        sample.forEach(function (h) {
          for (var j = 1; j < h.pts.length; j++) strokeSeg(ctx, h.pts[j - 1], h.pts[j], h.fate === "t" ? BLUE : VIOLET, .45, dims.dpr);
        });
      };
      paintStatic(); writeReadout();
      new ResizeObserver(paintStatic).observe(canvas);
      var b = document.querySelector("[data-sim-toggle]"); if (b) b.hidden = true;
      return;
    }
    new ResizeObserver(function () { resize(); }).observe(canvas);

    var live = [], SPEED = 0.06, last = 0, warm = 0;
    // Warm statistics in the background so numbers are meaningful quickly.
    function warmup() { for (var i = 0; i < 400; i++) history(); warm += 400; }

    var loop = visibleLoop(canvas, function (t) {
      if (warm < 40000) warmup();
      if (live.length < 26 && Math.random() < 0.55) live.push(history());
      // fade trail layer
      tctx.globalCompositeOperation = "destination-out";
      tctx.fillStyle = "rgba(0,0,0,.035)"; tctx.fillRect(0, 0, dims.w, dims.h);
      tctx.globalCompositeOperation = "source-over";

      for (var i = live.length - 1; i >= 0; i--) {
        var p = live[i], a = p.pts[p.seg], b = p.pts[p.seg + 1];
        if (!b) {
          if (p.fate === "a") dot(tctx, a, HI, .9, 2.2 * dims.dpr);
          live.splice(i, 1); continue;
        }
        var L = Math.hypot(b[0] - a[0], b[1] - a[1]) || 1e-6;
        var f0 = p.f; p.f = Math.min(1, p.f + SPEED / L);
        var s = [a[0] + (b[0] - a[0]) * f0, a[1] + (b[1] - a[1]) * f0];
        var e = [a[0] + (b[0] - a[0]) * p.f, a[1] + (b[1] - a[1]) * p.f];
        var col = p.fate === "t" ? BLUE : VIOLET;
        strokeSeg(tctx, s, e, col, .8, 1.2 * dims.dpr);
        if (p.f >= 1) { p.seg++; p.f = 0; if (p.seg < p.pts.length - 1) dot(tctx, b, col, .5, 1.2 * dims.dpr); }
        live[i].head = e;
      }

      ctx.fillStyle = "#0a0911"; ctx.fillRect(0, 0, dims.w, dims.h);
      drawSlab();
      ctx.drawImage(trail, 0, 0);
      live.forEach(function (p) { if (p.head) dot(ctx, p.head, HI, 1, 1.8 * dims.dpr); });

      if (t - last > 250) { writeReadout(); last = t; }
    });

    var btn = document.querySelector("[data-sim-toggle]");
    if (btn) btn.addEventListener("click", function () {
      var p = !loop.isPaused(); loop.setPaused(p);
      btn.textContent = p ? "Resume" : "Pause"; btn.setAttribute("aria-pressed", String(p));
    });
  })();

  /* ---------- 4. Circumbinary orbit (velocity-Verlet) ----------
     G = 1. Binary m1 = 1, m2 = 0.45 on a circular orbit of separation 1;
     a light planet on a near-circular orbit at r = 3.2 about the barycentre.
     Displays relative energy drift |ΔE/E₀| as a running verification. */
  (function orbit() {
    var canvas = document.getElementById("orbit");
    if (!canvas) return;
    var ctx = canvas.getContext("2d");
    var driftEl = document.querySelector('[data-o="drift"]');
    var m = [1, 0.45, 1e-5];
    var M = m[0] + m[1];
    // positions/velocities about the barycentre
    var a = 1, w = Math.sqrt(M / (a * a * a));
    var r1 = a * m[1] / M, r2 = a * m[0] / M;
    var rp = 3.2, vp = Math.sqrt(M / rp);
    var x = [[-r1, 0], [r2, 0], [rp, 0]];
    var v = [[0, -w * r1], [0, w * r2], [0, vp]];
    var acc = accel(x);
    var E0 = energy(), dt = 0.004, maxDrift = 0;
    var trails = [[], [], []], dims, scale;

    function accel(p) {
      var out = [[0, 0], [0, 0], [0, 0]];
      for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) {
        if (i === j) continue;
        var dx = p[j][0] - p[i][0], dy = p[j][1] - p[i][1];
        var r2_ = dx * dx + dy * dy, inv = m[j] / (r2_ * Math.sqrt(r2_));
        out[i][0] += dx * inv; out[i][1] += dy * inv;
      }
      return out;
    }
    function energy() {
      var K = 0, U = 0;
      for (var i = 0; i < 3; i++) {
        K += 0.5 * m[i] * (v[i][0] * v[i][0] + v[i][1] * v[i][1]);
        for (var j = i + 1; j < 3; j++) U -= m[i] * m[j] / Math.hypot(x[j][0] - x[i][0], x[j][1] - x[i][1]);
      }
      return K + U;
    }
    function step() {
      for (var i = 0; i < 3; i++) {
        v[i][0] += 0.5 * dt * acc[i][0]; v[i][1] += 0.5 * dt * acc[i][1];
        x[i][0] += dt * v[i][0];         x[i][1] += dt * v[i][1];
      }
      acc = accel(x);
      for (var k = 0; k < 3; k++) { v[k][0] += 0.5 * dt * acc[k][0]; v[k][1] += 0.5 * dt * acc[k][1]; }
    }
    function resize() { dims = fitCanvas(canvas); scale = Math.min(dims.w, dims.h) / 8.2; }
    function P(p) { return [dims.w / 2 + p[0] * scale, dims.h / 2 - p[1] * scale * 0.62]; } // tilted view

    function draw() {
      ctx.fillStyle = "#08070d"; ctx.fillRect(0, 0, dims.w, dims.h);
      // reference rings
      ctx.strokeStyle = "rgba(205,190,255,.06)"; ctx.lineWidth = dims.dpr;
      [1.6, 3.2, 4.6].forEach(function (r) {
        ctx.beginPath(); ctx.ellipse(dims.w / 2, dims.h / 2, r * scale, r * scale * 0.62, 0, 0, Math.PI * 2); ctx.stroke();
      });
      var cols = ["255,236,214", "142,160,255", "217,204,255"];
      for (var i = 0; i < 3; i++) {
        var tr = trails[i];
        for (var k = 1; k < tr.length; k++) {
          ctx.strokeStyle = "rgba(" + cols[i] + "," + (k / tr.length * (i === 2 ? .75 : .35)) + ")";
          ctx.lineWidth = (i === 2 ? 1.4 : 1) * dims.dpr;
          ctx.beginPath(); ctx.moveTo(tr[k - 1][0], tr[k - 1][1]); ctx.lineTo(tr[k][0], tr[k][1]); ctx.stroke();
        }
        var q = P(x[i]), rad = [6, 4, 3][i] * dims.dpr;
        var g = ctx.createRadialGradient(q[0], q[1], 0, q[0], q[1], rad * 4);
        g.addColorStop(0, "rgba(" + cols[i] + ",.55)"); g.addColorStop(1, "rgba(" + cols[i] + ",0)");
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(q[0], q[1], rad * 4, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = "rgb(" + cols[i] + ")"; ctx.beginPath(); ctx.arc(q[0], q[1], rad, 0, Math.PI * 2); ctx.fill();
      }
    }
    function advance(n) {
      for (var s = 0; s < n; s++) step();
      for (var i = 0; i < 3; i++) { trails[i].push(P(x[i])); if (trails[i].length > (i === 2 ? 420 : 90)) trails[i].shift(); }
      var d = Math.abs((energy() - E0) / E0); if (d > maxDrift) maxDrift = d;
    }

    resize();

    if (reduceMotion) {
      for (var k = 0; k < 600; k++) advance(6);
      // trails are stored in pixels; rebuild them after a resize
      new ResizeObserver(function () {
        resize(); trails = [[], [], []]; for (var k = 0; k < 420; k++) advance(6); draw();
      }).observe(canvas);
      draw();
      if (driftEl) driftEl.textContent = "max |ΔE/E₀| = " + maxDrift.toExponential(1);
      return;
    }
    new ResizeObserver(function () { resize(); trails = [[], [], []]; }).observe(canvas);
    var lastText = 0;
    visibleLoop(canvas, function (t) {
      advance(6); draw();
      if (driftEl && t - lastText > 500) { driftEl.textContent = "max |ΔE/E₀| = " + maxDrift.toExponential(1); lastText = t; }
    });
  })();
})();

/* NSEN 6684 talk: swap the poster for a YouTube player once data-youtube holds a video ID. */
(function () {
  document.querySelectorAll('.talk__media[data-youtube]').forEach(function (box) {
    var id = (box.getAttribute('data-youtube') || '').trim();
    if (!/^[A-Za-z0-9_-]{11}$/.test(id)) return;
    var f = document.createElement('iframe');
    f.src = 'https://www.youtube-nocookie.com/embed/' + id;
    f.title = box.getAttribute('data-title') || 'Video';
    f.loading = 'lazy';
    f.allow = 'accelerometer; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
    f.allowFullscreen = true;
    box.innerHTML = '';
    box.appendChild(f);
  });
})();
