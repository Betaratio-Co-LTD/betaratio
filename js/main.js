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

  /* ---------- Contact / RFQ form (static-site friendly demo handler) ---------- */
  var rfqForm = document.querySelector("[data-rfq-form]");
  if (rfqForm) {
    rfqForm.addEventListener("submit", function (e) {
      e.preventDefault();
      var note = rfqForm.querySelector("[data-form-note]");
      if (note) {
        note.textContent = "Cảm ơn bạn! Yêu cầu đã được ghi nhận. Đội ngũ kỹ thuật Betaratio sẽ liên hệ trong vòng 24 giờ làm việc.";
        note.style.display = "block";
      }
      rfqForm.reset();
      /* NOTE: Connect this form to your email service / backend
         (e.g. Formspree, Google Forms, or a serverless function)
         before going live — see README.md for instructions. */
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
})();
