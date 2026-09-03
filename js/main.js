/* =========================================================
   BETARATIO — Site JavaScript
   Mobile nav, tabs, sidebar product filters, form handling
   ========================================================= */
(function () {
  "use strict";

  /* ---------- Mobile nav toggle ---------- */
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".main-nav");
  var overlay = document.querySelector(".nav-overlay");

  function closeNav() {
    if (nav) nav.classList.remove("open");
    if (overlay) overlay.classList.remove("show");
    document.body.style.overflow = "";
  }
  function openNav() {
    if (nav) nav.classList.add("open");
    if (overlay) overlay.classList.add("show");
    document.body.style.overflow = "hidden";
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      if (nav && nav.classList.contains("open")) closeNav();
      else openNav();
    });
  }
  if (overlay) overlay.addEventListener("click", closeNav);

  /* On mobile, tapping a has-mega link expands its submenu instead of navigating away */
  document.querySelectorAll(".main-nav li.has-mega > a").forEach(function (a) {
    a.addEventListener("click", function (e) {
      if (window.innerWidth <= 860) {
        e.preventDefault();
        a.parentElement.classList.toggle("mega-open");
      }
    });
  });

  /* ---------- Tabs (homepage core products) ---------- */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var buttons = group.querySelectorAll(".tab-btn");
    var panels = group.querySelectorAll(".tab-panel");
    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        buttons.forEach(function (b) { b.classList.remove("active"); });
        panels.forEach(function (p) { p.classList.remove("active"); });
        btn.classList.add("active");
        var target = group.querySelector('[data-panel="' + btn.dataset.tab + '"]');
        if (target) target.classList.add("active");
      });
    });
  });

  /* ---------- Sidebar product filters ---------- */
  document.querySelectorAll("[data-filter-scope]").forEach(function (scope) {
    var checkboxes = scope.querySelectorAll(".filter-sidebar input[type=checkbox]");
    var cards = scope.querySelectorAll("[data-card]");
    var countEl = scope.querySelector("[data-result-count]");
    var resetBtn = scope.querySelector("[data-filter-reset]");

    function activeFilters() {
      var groups = {};
      checkboxes.forEach(function (cb) {
        if (cb.checked) {
          var key = cb.dataset.group;
          groups[key] = groups[key] || [];
          groups[key].push(cb.value);
        }
      });
      return groups;
    }

    function apply() {
      var groups = activeFilters();
      var visible = 0;
      cards.forEach(function (card) {
        var show = true;
        Object.keys(groups).forEach(function (key) {
          var cardVals = (card.dataset[key] || "").split("|");
          var match = groups[key].some(function (v) { return cardVals.indexOf(v) !== -1; });
          if (!match) show = false;
        });
        card.style.display = show ? "" : "none";
        if (show) visible++;
      });
      if (countEl) countEl.textContent = visible;
    }

    checkboxes.forEach(function (cb) { cb.addEventListener("change", apply); });
    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        checkboxes.forEach(function (cb) { cb.checked = false; });
        apply();
      });
    }
    apply();
  });

  /* ---------- Product matrix dropdown filter ---------- */
  document.querySelectorAll("[data-matrix-filter]").forEach(function (bar) {
    var selects = bar.querySelectorAll("select[data-mf]");
    var resetBtn = bar.querySelector("[data-mf-reset]");
    var countEl = bar.querySelector("[data-mf-count]");
    var wrap = bar.parentElement;
    var table = wrap ? wrap.querySelector("[data-mf-table]") : null;
    var emptyEl = wrap ? wrap.querySelector("[data-mf-empty]") : null;
    if (!table) return;
    var rows = table.querySelectorAll("tbody tr");

    function apply() {
      var groupSel = bar.querySelector('[data-mf="group"]');
      var indSel = bar.querySelector('[data-mf="industry"]');
      var groupVal = groupSel ? groupSel.value : "";
      var indVal = indSel ? indSel.value : "";
      var visible = 0;
      rows.forEach(function (row) {
        var rowGroup = row.dataset.mgroup || "";
        var rowInds = (row.dataset.minds || "").split("|");
        var show = true;
        if (groupVal && rowGroup !== groupVal) show = false;
        if (indVal && rowInds.indexOf(indVal) === -1) show = false;
        row.style.display = show ? "" : "none";
        if (show) visible++;
      });
      if (countEl) countEl.textContent = visible;
      table.style.display = visible === 0 ? "none" : "";
      if (emptyEl) emptyEl.style.display = visible === 0 ? "" : "none";
    }

    selects.forEach(function (sel) { sel.addEventListener("change", apply); });
    if (resetBtn) {
      resetBtn.addEventListener("click", function () {
        selects.forEach(function (sel) { sel.value = ""; });
        apply();
      });
    }
    apply();
  });

  /* ---------- Contact / RFQ form (submits to Formspree via AJAX) ---------- */
  var rfqForm = document.querySelector("[data-rfq-form]");
  if (rfqForm) {
    var rfqSubmitBtn = rfqForm.querySelector("[data-rfq-submit]");
    var rfqSubmitLabel = rfqSubmitBtn ? rfqSubmitBtn.innerHTML : "";

    function showNote(msg, ok) {
      var note = rfqForm.querySelector("[data-form-note]");
      if (!note) return;
      note.textContent = msg;
      note.style.display = "block";
      note.style.background = ok ? "#eefaf7" : "#fdecec";
      note.style.border = "1px solid " + (ok ? "#c7ece7" : "#f3c6c6");
      note.style.color = ok ? "var(--teal-600)" : "#c0392b";
    }

    rfqForm.addEventListener("submit", function (e) {
      e.preventDefault();
      if (rfqSubmitBtn) { rfqSubmitBtn.disabled = true; rfqSubmitBtn.textContent = "Đang gửi..."; }

      fetch(rfqForm.action, {
        method: "POST",
        body: new FormData(rfqForm),
        headers: { "Accept": "application/json" }
      }).then(function (response) {
        if (response.ok) {
          showNote("Cảm ơn bạn! Yêu cầu đã được gửi thành công. Đội ngũ kỹ thuật Betaratio sẽ liên hệ trong vòng 24 giờ làm việc.", true);
          rfqForm.reset();
        } else {
          return response.json().then(function (data) {
            var msg = (data && data.errors && data.errors.length) ?
              data.errors.map(function (er) { return er.message; }).join(", ") :
              "Có lỗi xảy ra, vui lòng thử lại hoặc liên hệ trực tiếp qua email/điện thoại bên dưới.";
            showNote(msg, false);
          });
        }
      }).catch(function () {
        showNote("Không thể kết nối tới máy chủ gửi yêu cầu. Vui lòng thử lại hoặc liên hệ trực tiếp qua email/điện thoại bên dưới.", false);
      }).finally(function () {
        if (rfqSubmitBtn) { rfqSubmitBtn.disabled = false; rfqSubmitBtn.innerHTML = rfqSubmitLabel; }
      });
    });
  }

  /* ---------- Active nav link highlight fallback (in case not server-rendered) ---------- */
  var current = window.location.pathname.split("/").pop();
  document.querySelectorAll(".main-nav a.nav-link").forEach(function (link) {
    var href = link.getAttribute("href").split("/").pop();
    if (href === current && current !== "") link.classList.add("active");
  });

  /* ---------- Set current year in footer ---------- */
  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });

  /* ---------- Hero carousel (diagonal split, auto-rotate + dots) ---------- */
  document.querySelectorAll("[data-hero-carousel]").forEach(function (hero) {
    var slides = hero.querySelectorAll(".hero-d-slide");
    var dots = hero.querySelectorAll(".hero-dot");
    if (slides.length < 2) return;
    var current = 0;
    var timer;

    function show(i) {
      current = (i + slides.length) % slides.length;
      slides.forEach(function (s, idx) { s.classList.toggle("active", idx === current); });
      dots.forEach(function (d, idx) { d.classList.toggle("active", idx === current); });
    }
    function next() { show(current + 1); }
    function restart() {
      clearInterval(timer);
      timer = setInterval(next, 6500);
    }
    dots.forEach(function (dot) {
      dot.addEventListener("click", function () {
        show(parseInt(dot.dataset.goto, 10));
        restart();
      });
    });
    restart();
  });

  /* ---------- Horizontal carousel scroll arrows (industry strip) ---------- */
  document.querySelectorAll(".carousel-head").forEach(function (head) {
    var track = head.parentElement.querySelector("[data-carousel]");
    if (!track) return;
    head.querySelectorAll("[data-scroll]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var dir = parseInt(btn.dataset.scroll, 10);
        track.scrollBy({ left: dir * 260, behavior: "smooth" });
      });
    });
  });
})();
