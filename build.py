#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
BETARATIO website generator.
Builds the full static multi-page site from the content/data below into
the surrounding folder structure (css/, js/, images/, industries/, products/).

This script is a build-time authoring tool only — the *output* is plain
static HTML/CSS/JS with no server or build step required to host it
(e.g. on GitHub Pages). You do not need Python to run the finished site.
"""
import os
import re
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))

SITE_NAME = "Betaratio"
SITE_TAGLINE = "Công nghệ Lọc & Phân tách Công nghiệp"
SITE_DOMAIN_PLACEHOLDER = "https://your-betaratio-site.example"
PHONE = "+84 (0) 28 xxxx xxxx"
EMAIL = "sales@betaratio.com"
ADDRESS = "Khu Công nghiệp, TP. Hồ Chí Minh, Việt Nam"

# =========================================================================
# ICON LIBRARY (Feather-style, MIT-licensed path data, inlined as <svg>)
# =========================================================================
ICON_PATHS = {
    "menu": '<line x1="3" y1="12" x2="21" y2="12"></line><line x1="3" y1="6" x2="21" y2="6"></line><line x1="3" y1="18" x2="21" y2="18"></line>',
    "x": '<line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line>',
    "droplet": '<path d="M12 2.69l5.66 5.66a8 8 0 1 1-11.31 0z"></path>',
    "wind": '<path d="M9.59 4.59A2 2 0 1 1 11 8H2m10.59 11.41A2 2 0 1 0 14 16H2m15.73-8.27A2.5 2.5 0 1 1 19.5 12H2"></path>',
    "check-circle": '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path><polyline points="22 4 12 14.01 9 11.01"></polyline>',
    "check": '<polyline points="20 6 9 17 4 12"></polyline>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>',
    "shield-check": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path><polyline points="9 12 11 14 15 10"></polyline>',
    "cpu": '<rect x="4" y="4" width="16" height="16" rx="2" ry="2"></rect><rect x="9" y="9" width="6" height="6"></rect><line x1="9" y1="1" x2="9" y2="4"></line><line x1="15" y1="1" x2="15" y2="4"></line><line x1="9" y1="20" x2="9" y2="23"></line><line x1="15" y1="20" x2="15" y2="23"></line><line x1="1" y1="9" x2="4" y2="9"></line><line x1="20" y1="9" x2="23" y2="9"></line><line x1="1" y1="15" x2="4" y2="15"></line><line x1="20" y1="15" x2="23" y2="15"></line>',
    "zap": '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"></polygon>',
    "coffee": '<path d="M18 8h1a4 4 0 0 1 0 8h-1"></path><path d="M2 8h16v9a4 4 0 0 1-4 4H6a4 4 0 0 1-4-4V8z"></path><line x1="6" y1="1" x2="6" y2="4"></line><line x1="10" y1="1" x2="10" y2="4"></line><line x1="14" y1="1" x2="14" y2="4"></line>',
    "activity": '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>',
    "layers": '<polygon points="12 2 2 7 12 12 22 7 12 2"></polygon><polyline points="2 17 12 22 22 17"></polyline><polyline points="2 12 12 17 22 12"></polyline>',
    "link": '<path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.71"></path><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.71-1.71"></path>',
    "cylinder": '<ellipse cx="12" cy="6" rx="7" ry="3"></ellipse><path d="M5 6v12a7 3 0 0 0 14 0V6"></path>',
    "bag": '<path d="M6 2l-1.2 4H3a1 1 0 0 0-1 1.14l1.38 12.02A2 2 0 0 0 5.36 21h13.28a2 2 0 0 0 1.98-1.84L21.99 7.14A1 1 0 0 0 21 6h-1.8L18 2"></path><path d="M8 10a4 4 0 0 0 8 0"></path>',
    "tank": '<ellipse cx="12" cy="5" rx="9" ry="3"></ellipse><path d="M21 12c0 1.66-4.03 3-9 3s-9-1.34-9-3"></path><path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5"></path>',
    "flask": '<path d="M9 2v6.5L4 18a2 2 0 0 0 1.8 3h12.4a2 2 0 0 0 1.8-3l-5-9.5V2"></path><line x1="8" y1="2" x2="16" y2="2"></line>',
    "sliders": '<line x1="4" y1="21" x2="4" y2="14"></line><line x1="4" y1="10" x2="4" y2="3"></line><line x1="12" y1="21" x2="12" y2="12"></line><line x1="12" y1="8" x2="12" y2="3"></line><line x1="20" y1="21" x2="20" y2="16"></line><line x1="20" y1="12" x2="20" y2="3"></line><line x1="1" y1="14" x2="7" y2="14"></line><line x1="9" y1="8" x2="15" y2="8"></line><line x1="17" y1="16" x2="23" y2="16"></line>',
    "search": '<circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line>',
    "phone": '<path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.127.96.361 1.903.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.907.339 1.85.573 2.81.7A2 2 0 0 1 22 16.92z"></path>',
    "mail": '<path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path><polyline points="22,6 12,13 2,6"></polyline>',
    "map-pin": '<path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle>',
    "clock": '<circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline>',
    "arrow-right": '<line x1="5" y1="12" x2="19" y2="12"></line><polyline points="12 5 19 12 12 19"></polyline>',
    "chevron-down": '<polyline points="6 9 12 15 18 9"></polyline>',
    "download": '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"></path><polyline points="7 10 12 15 17 10"></polyline><line x1="12" y1="15" x2="12" y2="3"></line>',
    "award": '<circle cx="12" cy="8" r="7"></circle><polyline points="8.21 13.89 7 23 12 20 17 23 15.79 13.88"></polyline>',
    "file-text": '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line>',
    "users": '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><path d="M23 21v-2a4 4 0 0 0-3-3.87"></path><path d="M16 3.13a4 4 0 0 1 0 7.75"></path>',
    "target": '<circle cx="12" cy="12" r="10"></circle><circle cx="12" cy="12" r="6"></circle><circle cx="12" cy="12" r="2"></circle>',
    "eye": '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle>',
    "scissors": '<circle cx="6" cy="6" r="3"></circle><circle cx="6" cy="18" r="3"></circle><line x1="20" y1="4" x2="8.12" y2="15.88"></line><line x1="14.47" y1="14.48" x2="20" y2="20"></line><line x1="8.12" y1="8.12" x2="12" y2="12"></line>',
    "settings": '<circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z"></path>',
    "package": '<line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line>',
    "trending-up": '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"></polyline><polyline points="17 6 23 6 23 12"></polyline>',
    "book-open": '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"></path><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"></path>',
    "grid": '<rect x="3" y="3" width="7" height="7"></rect><rect x="14" y="3" width="7" height="7"></rect><rect x="14" y="14" width="7" height="7"></rect><rect x="3" y="14" width="7" height="7"></rect>',
    "thermometer": '<path d="M14 4v10.54a4 4 0 1 1-4 0V4a2 2 0 0 1 4 0z"></path>',
    "linkedin": '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle>',
    "facebook": '<path d="M18 2h-3a5 5 0 0 0-5 5v3H7v4h3v8h4v-8h3l1-4h-4V7a1 1 0 0 1 1-1h3z"></path>',
    "youtube": '<path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19c1.72.46 8.6.46 8.6.46s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"></path><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"></polygon>',
    "external-link": '<path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path><polyline points="15 3 21 3 21 9"></polyline><line x1="10" y1="14" x2="21" y2="3"></line>',
}

def icon(name, cls=""):
    d = ICON_PATHS.get(name, "")
    klass = f' class="{cls}"' if cls else ""
    return f'<svg{klass} viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{d}</svg>'

# =========================================================================
# LAYOUT HELPERS
# =========================================================================
def rel(path, depth):
    """Turn a root-relative path like 'css/style.css' or 'index.html' into
    the correct relative path from a page nested `depth` folders deep."""
    return ("../" * depth) + path


INDUSTRY_NAV = [
    ("food-beverage", "Thực phẩm & Đồ uống", "Chống nhiễm xơ sợi, đạt chuẩn tiếp xúc thực phẩm", "coffee"),
    ("pharmaceuticals", "Dược phẩm", "Vô trùng tuyệt đối, an toàn chống cháy nổ", "activity"),
    ("electronics", "Điện tử & Bán dẫn", "Lọc siêu mịn cho nước siêu tinh khiết (UPW)", "cpu"),
    ("high-tech-cleanrooms", "Công nghệ cao & Phòng sạch", "Kiểm soát hạt bụi, chống tĩnh điện", "shield"),
    ("energy-heavy-industries", "Năng lượng & CN nặng", "Lưu lượng lớn, môi trường ăn mòn mạnh", "zap"),
]

PRODUCT_NAV_LIQUID = [
    ("Lõi lọc / Cột lọc", "products/liquid-filtration.html#cartridges"),
    ("Túi lọc dung dịch lỏng", "products/liquid-filtration.html#bags"),
    ("Vải lọc máy công nghiệp", "products/liquid-filtration.html#cloths"),
    ("Bình lọc chất lỏng", "products/liquid-filtration.html#vessels"),
]
PRODUCT_NAV_GAS = [
    ("Túi sấy tầng sôi", "products/gas-separation.html#fluidbed"),
    ("Túi lọc bụi / thu hồi bột mịn", "products/gas-separation.html#collector"),
    ("Túi thông áp bồn chứa", "products/gas-separation.html#vent"),
    ("Khớp nối mềm bằng vải", "products/gas-separation.html#connector"),
]

MAIN_NAV = [
    ("index.html", "Trang chủ", "home", None),
    ("industries.html", "Ngành công nghiệp", "industries", "industries"),
    ("products/index.html", "Sản phẩm", "products", "products"),
    ("custom-oem.html", "Gia công theo yêu cầu", "oem", None),
    ("resources.html", "Tài nguyên kỹ thuật", "resources", None),
    ("about.html", "Về Betaratio", "about", None),
]


def HEAD(title, description, depth, path="", extra=""):
    css = rel("css/style.css", depth)
    fav = rel("images/favicon.svg", depth)
    canonical = f"{SITE_DOMAIN_PLACEHOLDER}/{path}" if path else SITE_DOMAIN_PLACEHOLDER
    return f"""<!doctype html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} | {SITE_NAME}</title>
<meta name="description" content="{description}">
<link rel="canonical" href="{canonical}">
<meta property="og:title" content="{title} | {SITE_NAME}">
<meta property="og:description" content="{description}">
<meta property="og:type" content="website">
<meta name="theme-color" content="#0a1e30">
<link rel="icon" type="image/svg+xml" href="{fav}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{css}">
{extra}</head>
<body>
"""


def MEGA_INDUSTRIES(depth):
    items = ""
    for slug, name, desc, ic in INDUSTRY_NAV:
        href = rel(f"industries/{slug}.html", depth)
        items += f"""<a href="{href}"><span class="ic">{icon(ic)}</span><span><strong>{name}</strong><span>{desc}</span></span></a>\n"""
    return f'<div class="mega mega-single">{items}</div>'


def MEGA_PRODUCTS(depth):
    liquid = "".join(
        f'<a href="{rel(href, depth)}"><span class="ic">{icon("droplet")}</span><span><strong>{name}</strong></span></a>\n'
        for name, href in PRODUCT_NAV_LIQUID
    )
    gas = "".join(
        f'<a href="{rel(href, depth)}"><span class="ic">{icon("wind")}</span><span><strong>{name}</strong></span></a>\n'
        for name, href in PRODUCT_NAV_GAS
    )
    return f"""<div class="mega">
<div class="mega-title">Lọc chất lỏng</div>
{liquid}
<div class="mega-title">Lọc khí &amp; Sàng lọc</div>
{gas}
</div>"""


def HEADER(active, depth):
    nav_items = ""
    for href, label, key, mega in MAIN_NAV:
        is_active = " active" if key == active else ""
        link = rel(href, depth)
        if mega == "industries":
            nav_items += f"""<li class="has-mega"><a class="nav-link{is_active}" href="{link}">{label}{icon("chevron-down", "chev")}</a>{MEGA_INDUSTRIES(depth)}</li>\n"""
        elif mega == "products":
            nav_items += f"""<li class="has-mega"><a class="nav-link{is_active}" href="{link}">{label}{icon("chevron-down", "chev")}</a>{MEGA_PRODUCTS(depth)}</li>\n"""
        else:
            nav_items += f"""<li><a class="nav-link{is_active}" href="{link}">{label}</a></li>\n"""

    contact_active = " active" if active == "contact" else ""
    return f"""<header class="site-header">
  <div class="header-inner">
    <a class="brand" href="{rel('index.html', depth)}">
      <span class="mark">{icon("droplet")}</span>
      <span>{SITE_NAME}<small>Filtration &amp; Separation</small></span>
    </a>
    <nav class="main-nav">
      <ul>
        {nav_items}
      </ul>
    </nav>
    <div class="header-cta">
      <div class="utility-row">
        <a class="utility-btn" href="tel:{PHONE.replace(' ', '')}" aria-label="Gọi điện thoại" title="{PHONE}">{icon('phone')}</a>
        <a class="utility-btn" href="{rel('contact.html', depth)}" aria-label="Gửi yêu cầu báo giá" title="Yêu cầu báo giá">{icon('mail')}</a>
      </div>
      <a href="{rel('contact.html', depth)}" class="btn btn-primary btn-sm">Yêu cầu báo giá</a>
      <button class="nav-toggle" aria-label="Mở menu">{icon("menu")}</button>
    </div>
  </div>
</header>
<div class="nav-overlay"></div>
"""


def FOOTER(depth):
    r = lambda p: rel(p, depth)
    return f"""<footer class="site-footer">
  <div class="container">
    <div class="footer-grid">
      <div class="footer-brand">
        <a class="brand" href="{r('index.html')}">
          <span class="mark">{icon("droplet")}</span>
          <span>{SITE_NAME}<small>Filtration &amp; Separation</small></span>
        </a>
        <p>Công nghệ lọc và phân tách chuyên sâu: nâng tầm chất lượng, tối ưu chi phí vận hành cho nhà máy của bạn.</p>
        <div class="social-row">
          <a href="#" aria-label="LinkedIn">{icon("linkedin")}</a>
          <a href="#" aria-label="Facebook">{icon("facebook")}</a>
          <a href="#" aria-label="YouTube">{icon("youtube")}</a>
        </div>
      </div>
      <div>
        <h5>Ngành công nghiệp</h5>
        <ul>
          {"".join(f'<li><a href="{r(f"industries/{slug}.html")}">{name}</a></li>' for slug, name, _, _ in INDUSTRY_NAV)}
        </ul>
      </div>
      <div>
        <h5>Sản phẩm</h5>
        <ul>
          <li><a href="{r('products/liquid-filtration.html')}">Lọc chất lỏng</a></li>
          <li><a href="{r('products/gas-separation.html')}">Lọc khí &amp; Sàng lọc</a></li>
          <li><a href="{r('custom-oem.html')}">Gia công theo yêu cầu</a></li>
          <li><a href="{r('products/index.html')}">Ma trận sản phẩm</a></li>
        </ul>
      </div>
      <div>
        <h5>Công ty</h5>
        <ul>
          <li><a href="{r('about.html')}">Về Betaratio</a></li>
          <li><a href="{r('resources.html')}">Tài nguyên kỹ thuật</a></li>
          <li><a href="{r('resources.html')}#certifications">Chứng nhận</a></li>
          <li><a href="{r('contact.html')}">Liên hệ</a></li>
        </ul>
      </div>
      <div class="footer-hq">
        <h5>Trụ sở chính</h5>
        <address>
          {ADDRESS}<br>
          <a href="tel:{PHONE.replace(' ', '')}">{PHONE}</a><br>
          <a href="mailto:{EMAIL}">{EMAIL}</a>
        </address>
        <a href="{r('contact.html')}" class="btn btn-primary btn-sm">Liên hệ chúng tôi</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© <span data-year></span> {SITE_NAME}. Bảo lưu mọi quyền.</span>
      <div class="legal-links">
        <a href="#">Chính sách bảo mật</a>
        <a href="#">Điều khoản sử dụng</a>
        <a href="{r('resources.html')}#certifications">Chứng nhận</a>
      </div>
    </div>
  </div>
</footer>
<script src="{r('js/main.js')}"></script>
</body>
</html>"""


def PAGE(title, description, path, depth, active, body, extra_head=""):
    return HEAD(title, description, depth, path, extra_head) + HEADER(active, depth) + body + FOOTER(depth)


def write_page(rel_path, html):
    full = os.path.join(ROOT, rel_path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(html)
    print("wrote", rel_path)

# =========================================================================
# REAL PHOTOGRAPHY (optional — drop files into images/photos/, see the
# README.md in that folder for exact filenames/sizes). Anywhere a slot has
# no matching file yet, the build falls back to the decorative SVG below.
# =========================================================================
PHOTOS_DIR = os.path.join(ROOT, "images", "photos")
PHOTO_EXTS = (".jpg", ".jpeg", ".png", ".webp")


def find_photo(slot):
    """If images/photos/<slot>.{jpg,jpeg,png,webp} exists, return its
    root-relative path (e.g. 'images/photos/hero/home-hero.jpg'). Else None."""
    if not slot:
        return None
    for ext in PHOTO_EXTS:
        if os.path.isfile(os.path.join(PHOTOS_DIR, slot + ext)):
            return f"images/photos/{slot}{ext}"
    return None


def slugify(name):
    """ASCII-safe, filename-friendly slug from a (possibly Vietnamese) name."""
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_name.lower()).strip("-")
    return slug or "san-pham"


def hero_media(depth=0):
    """Full-bleed hero photo if provided, else the abstract mesh graphic."""
    photo = find_photo("hero/home-hero")
    if photo:
        return (f'<img class="hero-photo" src="{rel(photo, depth)}" '
                f'alt="Nhà máy sản xuất Betaratio" loading="eager">'
                f'<div class="hero-photo-scrim"></div>')
    return hero_art()


def product_media(name, ic, depth=1, ar="16/11"):
    """Product-card thumbnail: real photo if images/photos/products/<slug>
    exists, else the placeholder icon. `name` is auto-slugified."""
    photo = find_photo(f"products/{slugify(name)}")
    if photo:
        return (f'<div class="img-frame" style="--ar:{ar}">'
                f'<img src="{rel(photo, depth)}" alt="{name}" loading="lazy"></div>')
    return f'<div class="img-frame" style="--ar:{ar}">{icon(ic)}</div>'


def case_media(ic, slot, depth=0):
    """Case-study thumbnail: real photo if provided, else placeholder icon."""
    photo = find_photo(slot)
    if photo:
        return (f'<div class="img-frame dark" style="--ar:16/10">'
                f'<img src="{rel(photo, depth)}" alt="" loading="lazy"></div>')
    return f'<div class="img-frame dark" style="--ar:16/10">{icon(ic)}</div>'


# =========================================================================
# DECORATIVE SVG BLOCKS (placeholder visuals — swap for real photography)
# =========================================================================
def hero_art():
    """Abstract filtration-mesh graphic used in the homepage hero panel."""
    return f"""<div class="art-panel art-mesh">
  <svg viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg">
    <circle cx="100" cy="100" r="72" stroke="rgba(255,255,255,.35)" stroke-width="1.4"/>
    <circle cx="100" cy="100" r="52" stroke="rgba(255,255,255,.5)" stroke-width="1.4"/>
    <circle cx="100" cy="100" r="30" stroke="#ffffff" stroke-width="2"/>
    <g stroke="rgba(255,255,255,.55)" stroke-width="1">
      <line x1="100" y1="10" x2="100" y2="190"/>
      <line x1="10" y1="100" x2="190" y2="100"/>
      <line x1="34" y1="34" x2="166" y2="166"/>
      <line x1="166" y1="34" x2="34" y2="166"/>
    </g>
    <g fill="#ffffff">
      <circle cx="100" cy="30" r="4"/>
      <circle cx="100" cy="170" r="4"/>
      <circle cx="30" cy="100" r="4"/>
      <circle cx="170" cy="100" r="4"/>
    </g>
    <g fill="#ee8a34">
      <circle cx="140" cy="60" r="5"/>
      <circle cx="60" cy="140" r="3"/>
    </g>
    <path d="M100 100 L100 28" stroke="#3fc4bd" stroke-width="2.4" stroke-linecap="round"/>
  </svg>
</div>"""


def img_frame(ic, caption, ar="4/3", dark=False, slot=None, depth=0):
    darkcls = " dark" if dark else ""
    photo = find_photo(slot)
    if photo:
        return f"""<div class="img-frame{darkcls}" style="--ar:{ar}">
  <img src="{rel(photo, depth)}" alt="{caption}" loading="lazy">
</div>"""
    return f"""<div class="img-frame{darkcls}" style="--ar:{ar}">
  {icon(ic)}
  <span class="cap">{caption}</span>
</div>"""


def gradient_style(a, b):
    return f'style="--grad-a:{a};--grad-b:{b}"'


# =========================================================================
# DATA — INDUSTRIES
# =========================================================================
INDUSTRIES = [
    dict(
        slug="food-beverage", nav_ic="coffee",
        name="Thực phẩm & Đồ uống", name_en="Food & Beverage",
        grad=("#164b3c", "#0b8f8a"),
        summary="Chống nhiễm xơ sợi, đạt chuẩn tiếp xúc thực phẩm trực tiếp cho dây chuyền siro, nước ngọt, bia rượu.",
        challenge_title="Thách thức ngành Thực phẩm & Đồ uống",
        challenges=[
            "Nguy cơ phơi nhiễm vật lý (xơ sợi rơi vào sản phẩm) từ vật liệu lọc kém chất lượng.",
            "Ô nhiễm vi sinh vật trong quá trình lọc siro, nước giải khát, đồ uống có cồn.",
            "Yêu cầu vệ sinh an toàn thực phẩm khắt khe, kiểm tra định kỳ nghiêm ngặt từ cơ quan quản lý.",
        ],
        solutions=[
            "Vật liệu đạt chuẩn tiếp xúc thực phẩm trực tiếp (QCVN 12-1:2011/BYT, FDA 21 CFR).",
            "Công nghệ túi hàn nhiệt không may (Welded Seam) — triệt tiêu hoàn toàn nguy cơ xơ tua rơi vào thực phẩm.",
            "Lõi lọc xếp nếp (Pleated Membrane) lọc tuyệt đối 99.99% vi sinh vật và hạt mịn trong siro, nước ngọt, bia rượu.",
        ],
        products=[
            ("Túi lọc EF Mesh", "Lọc bề mặt, giữ hạt không biến dạng, tái sử dụng được", "bag"),
            ("Lõi lọc xếp nếp (Pleated)", "Lọc tuyệt đối, tiệt trùng vi sinh cho dịch lỏng", "cylinder"),
            ("Vải lọc máy ép khung bản thực phẩm", "Tách rắn – lỏng quy mô lớn, đạt chuẩn FDA", "layers"),
        ],
    ),
    dict(
        slug="pharmaceuticals", nav_ic="activity",
        name="Dược phẩm", name_en="Pharmaceuticals",
        grad=("#1e2f5c", "#0b8f8a"),
        summary="Vô trùng tuyệt đối và an toàn phòng chống cháy nổ khi sấy hạt, sấy bột thuốc khô.",
        challenge_title="Thách thức ngành Dược phẩm",
        challenges=[
            "Đảm bảo độ vô trùng tuyệt đối trong toàn bộ quy trình lọc và sấy nguyên liệu.",
            "An toàn phòng chống cháy nổ khi sấy hạt, sấy bột thuốc khô — nguy cơ tích điện gây phóng tia lửa.",
            "Yêu cầu khả năng tiệt trùng lặp lại nhiều lần bằng hơi nước nóng (autoclave) mà không suy giảm hiệu suất lọc.",
        ],
        solutions=[
            "Lõi lọc màng xếp nếp (PTFE/PES) chịu tiệt trùng autoclave/hơi nước nóng hơn 50 lần, đạt chứng nhận tiêu chuẩn dược phẩm.",
            "Túi sấy tầng sôi chống tĩnh điện tích hợp sợi Carbon hoặc SS316L, điện trở bề mặt an toàn 10³–10⁶ Ohm.",
            "Triệt tiêu nguy cơ phóng điện gây cháy nổ bụi mịn trong buồng sấy tầng sôi.",
        ],
        products=[
            ("Túi sấy tầng sôi chống tĩnh điện", "Sợi Carbon/SS316L, điện trở bề mặt an toàn", "wind"),
            ("Lõi lọc màng xếp nếp Absolute", "Tiệt trùng autoclave, lọc tuyệt đối vi sinh", "cylinder"),
            ("Túi lọc thông áp vô trùng bồn chứa", "Ngăn nhiễm chéo, cấp lọc siêu mịn", "bag"),
        ],
    ),
    dict(
        slug="electronics", nav_ic="cpu",
        name="Điện tử & Linh kiện bán dẫn", name_en="Electronics & Semiconductors",
        grad=("#1b2a4a", "#3fc4bd"),
        summary="Kiểm soát tạp chất dưới micron, đáp ứng yêu cầu nước siêu tinh khiết (UPW) cho rửa bảng mạch.",
        challenge_title="Thách thức ngành Điện tử & Bán dẫn",
        challenges=[
            "Kiểm soát tạp chất ở kích thước dưới micron — sai số cực nhỏ cũng gây lỗi vi mạch.",
            "Yêu cầu nước siêu tinh khiết (Ultra Pure Water – UPW) để rửa bảng mạch không để lại cặn ion.",
            "Vật liệu lọc phải trơ hóa học tuyệt đối, không phát sinh ô nhiễm thứ cấp vào dòng nước.",
        ],
        solutions=[
            "Lõi lọc màng xếp nếp Absolute cấp lọc siêu mịn từ 0.04 đến 0.1 micron, kiểm soát bụi bẩn tuyệt đối.",
            "Vật liệu lọc trơ về mặt hóa học, chịu nhiệt tốt, không phôi nhiễm hạt/ion vào dòng nước siêu tinh khiết.",
            "Vỏ bình lọc inox SS316L đánh bóng vi sinh gương (mirror polish) hạn chế bám bẩn và ăn mòn.",
        ],
        products=[
            ("Lõi lọc Pleated Membrane PTFE/PES", "Cấp lọc 0.04–0.1 micron cho UPW", "cylinder"),
            ("Vỏ bình lọc inox SS316L Mirror Polish", "Đánh bóng vi sinh, trơ hóa học tuyệt đối", "tank"),
            ("Lõi lọc Melt-blown siêu mịn", "Lọc sâu tinh, giữ hạt mịn hiệu quả cao", "cylinder"),
        ],
    ),
    dict(
        slug="high-tech-cleanrooms", nav_ic="shield",
        name="Công nghệ cao & Phòng sạch", name_en="High-Tech & Cleanrooms",
        grad=("#1b2a4a", "#0b8f8a"),
        summary="Kiểm soát hạt bụi trong không khí và triệt tiêu tĩnh điện cho linh kiện điện tử nhạy cảm.",
        challenge_title="Thách thức ngành Công nghệ cao & Phòng sạch",
        challenges=[
            "Kiểm soát hạt bụi trong không khí đạt tiêu chuẩn phòng sạch nghiêm ngặt.",
            "Sự tích tụ tĩnh điện có thể phá hủy các linh kiện điện tử nhạy cảm (ESD).",
            "Cần khớp nối linh hoạt giữa các máy móc rung động mà không phát thải bụi ra môi trường.",
        ],
        solutions=[
            "Khớp nối mềm bằng vải kỹ thuật cao cấp, may đo kín khít theo đúng biên dạng máy.",
            "Túi thông áp, túi thu hồi bụi phòng sạch tích hợp sợi chống tĩnh điện, triệt tiêu điện tích bề mặt.",
            "Gia công cắt laser chính xác, đường biên sạch, hạn chế phát sinh xơ sợi ra môi trường phòng sạch.",
        ],
        products=[
            ("Khớp nối mềm bằng vải kỹ thuật", "May đo theo biên dạng máy, chống rung", "link"),
            ("Túi lọc thông áp phòng sạch", "Cấp lọc siêu mịn, tránh nhiễm chéo", "bag"),
            ("Túi thu hồi bụi Carbon", "Sợi chống tĩnh điện, an toàn ESD", "wind"),
        ],
    ),
    dict(
        slug="energy-heavy-industries", nav_ic="zap",
        name="Năng lượng & Công nghiệp nặng", name_en="Energy & Heavy Industries",
        grad=("#3a2a12", "#0b8f8a"),
        summary="Lưu lượng lọc cực lớn, môi trường hóa chất ăn mòn mạnh, tối ưu chi phí thu hồi khoáng sản/dầu khí.",
        challenge_title="Thách thức ngành Năng lượng & Công nghiệp nặng",
        challenges=[
            "Lưu lượng lọc cực lớn, đòi hỏi hệ thống thiết bị công suất cao, vận hành liên tục.",
            "Môi trường hóa chất ăn mòn mạnh, chênh lệch áp suất lớn gây hao mòn nhanh vật liệu lọc.",
            "Áp lực tối ưu chi phí thu hồi khoáng sản, dầu khí trong bối cảnh biến động giá nguyên liệu.",
        ],
        solutions=[
            "Hệ thống vải lọc máy ép khung bản (Filter Press Cloth), máy lọc ly tâm (Centrifuge Cloth) may viền gia cố chịu lực cơ học cao.",
            "Lõi lọc sợi quấn (String Wound) cấu trúc lỗ gradient, tối ưu dung tích chứa cặn thô.",
            "Hệ thống vỏ bình lọc đa túi (Multi-bag Filter Vessel) công suất lên tới 2.238 lít, xử lý lưu lượng cực đại.",
        ],
        products=[
            ("Vải lọc máy ép khung bản nặng", "May viền gia cố, chịu ứng suất lớn", "layers"),
            ("Lõi lọc sợi quấn Cotton/Thủy tinh", "Cấu trúc gradient, dung tích cặn lớn", "cylinder"),
            ("Bình lọc đa túi công nghiệp", "Công suất đến 2.238 lít, lưu lượng cực đại", "tank"),
        ],
    ),
]

INDUSTRY_BY_SLUG = {i["slug"]: i for i in INDUSTRIES}

# =========================================================================
# DATA — PRODUCT FILTER MATRIX (Phần 4 của tài liệu gốc)
# =========================================================================
PRODUCT_MATRIX = [
    dict(name="Lõi lọc Melt-blown", group="Lõi lọc lỏng", app="Lọc sâu tinh / Giữ hạt mịn",
         industries="Thực phẩm, Dược phẩm, Điện tử", standard="FDA, QCVN 12-1:2011/BYT, NSF 42",
         industries_list=["Thực phẩm", "Dược phẩm", "Điện tử"]),
    dict(name="Lõi lọc Sợi quấn", group="Lõi lọc lỏng", app="Lọc thô / Gradient pore",
         industries="Thực phẩm, Năng lượng, Công nghiệp nặng", standard="QCVN 12-1:2011/BYT, Chịu nhiệt",
         industries_list=["Thực phẩm", "Năng lượng", "Công nghiệp nặng"]),
    dict(name="Lõi lọc Màng xếp nếp (Pleated)", group="Lõi lọc lỏng", app="Lọc tuyệt đối / Tiệt trùng vi sinh",
         industries="Dược phẩm, Thực phẩm, Điện tử, Công nghệ cao", standard="FDA, EC Food, Chịu Autoclave 121°C",
         industries_list=["Dược phẩm", "Thực phẩm", "Điện tử", "Công nghệ cao"]),
    dict(name="Túi lọc lưới EF Series", group="Túi lọc lỏng", app="Lọc bề mặt / Loại hạt không biến dạng",
         industries="Thực phẩm, Năng lượng", standard="FDA, QCVN 12-1:2011/BYT, Tái sử dụng",
         industries_list=["Thực phẩm", "Năng lượng"]),
    dict(name="Túi lọc nỉ FF Series", group="Túi lọc lỏng", app="Lọc sâu đa lớp / Hạt mềm lơ lửng",
         industries="Thực phẩm, Công nghiệp", standard="FDA, QCVN 12-1:2011/BYT, Dung tích cặn lớn",
         industries_list=["Thực phẩm", "Công nghiệp"]),
    dict(name="Túi lọc đa sợi MF Series", group="Túi lọc lỏng", app="Lọc lai (bề mặt & sâu)",
         industries="Thực phẩm, Công nghiệp", standard="FDA, QCVN 12-1:2011/BYT, Bền cơ học",
         industries_list=["Thực phẩm", "Công nghiệp"]),
    dict(name="Vải lọc máy (Ép khung bản...)", group="Vải lọc máy", app="Tách rắn – lỏng quy mô cực lớn",
         industries="Năng lượng, Thực phẩm, Công nghiệp nặng", standard="FDA, EC, QCVN, Chịu ứng suất lớn",
         industries_list=["Năng lượng", "Thực phẩm", "Công nghiệp nặng"]),
    dict(name="Túi sấy tầng sôi (Fluid Bed)", group="Lọc sấy khí", app="Thu hồi bột mịn / Sấy khô bột",
         industries="Dược phẩm, Thực phẩm", standard="Chống tĩnh điện Carbon/SS316L, Chống nổ",
         industries_list=["Dược phẩm", "Thực phẩm"]),
    dict(name="Túi lọc thông áp (Vent Bag)", group="Lọc khí", app="Thông gió bồn chứa / Ngừa nhiễm vi sinh",
         industries="Thực phẩm, Dược phẩm, Công nghệ cao", standard="Cấp lọc siêu mịn, Tránh nhiễm chéo",
         industries_list=["Thực phẩm", "Dược phẩm", "Công nghệ cao"]),
    dict(name="Khớp nối mềm bằng vải", group="Phụ kiện máy", app="Kết nối rung động / Ngừa phát thải bụi",
         industries="Thực phẩm, Dược phẩm, Công nghệ cao", standard="Cắt laser chuẩn xác, May đo theo máy",
         industries_list=["Thực phẩm", "Dược phẩm", "Công nghệ cao"]),
    dict(name="Bình lọc chất lỏng (Vessels)", group="Thiết bị vỏ bồn", app="Vỏ chứa túi/lõi lọc áp suất",
         industries="Tất cả các ngành (Thực phẩm, Điện tử, Dược...)", standard="SS304/SS316/SS316L, Nhựa",
         industries_list=["Thực phẩm", "Dược phẩm", "Điện tử", "Năng lượng", "Công nghiệp nặng", "Công nghiệp", "Công nghệ cao"]),
]

# =========================================================================
# HOME PAGE
# =========================================================================
def home_page():
    depth = 0

    industry_scroll_cards = ""
    for ind in INDUSTRIES:
        a, b = ind["grad"]
        photo = find_photo(f"industries/{ind['slug']}")
        if photo:
            isc_media = f'<img src="{rel(photo, depth)}" alt="{ind["name"]}" loading="lazy">'
            isc_style = ""
        else:
            isc_media = icon(ind['nav_ic'])
            isc_style = gradient_style(a, b)
        industry_scroll_cards += f"""<a class="industry-scroll-card" href="industries/{ind['slug']}.html">
      <div class="isc-title">{ind['name']}</div>
      <div class="isc-photo" {isc_style}>{isc_media}</div>
    </a>\n"""

    liquid_products = [
        ("Lõi lọc / Cột lọc", "0.04 – 2000 µm · PP, PES, PTFE", "cylinder"),
        ("Túi lọc dung dịch lỏng", "EF / FF / MF Series", "bag"),
        ("Vải lọc máy công nghiệp", "Ép khung bản, ly tâm", "layers"),
        ("Bình lọc chất lỏng", "SS304 / SS316 / SS316L", "tank"),
    ]
    gas_products = [
        ("Túi sấy tầng sôi", "Chống tĩnh điện Carbon/SS316L", "wind"),
        ("Túi lọc bụi & thu hồi bột mịn", "Product Collector Bags", "bag"),
        ("Túi thông áp bồn chứa", "Vent Bags — cấp lọc siêu mịn", "wind"),
        ("Khớp nối mềm bằng vải", "Cắt laser, may đo theo máy", "link"),
    ]

    def product_tab_cards(items):
        cards = ""
        for name, meta, ic in items:
            cards += f"""<div class="product-card">
        {product_media(name, ic, depth)}
        <div class="pc-body">
          <span class="pc-meta">Sản phẩm tiêu chuẩn</span>
          <h4>{name}</h4>
          <p>{meta}</p>
          <div class="pc-foot">
            <a href="products/index.html" class="btn btn-ghost-navy btn-sm">Chi tiết</a>
          </div>
        </div>
      </div>\n"""
        return cards

    hero_slides = [
        dict(eyebrow="Betaratio Filtration &amp; Separation",
             h1="Công nghệ lọc và phân tách chuyên sâu: nâng tầm chất lượng, tối ưu chi phí vận hành.",
             lead="Betaratio thiết kế và gia công các giải pháp lọc &amp; phân tách vừa vặn cho từng thiết bị nhà máy — từ lõi lọc, túi lọc chất lỏng đến túi lọc khí và khớp nối kỹ thuật, đạt chuẩn FDA, ISO 9001:2015 và QCVN.",
             cta=('Nhận tư vấn giải pháp kỹ thuật', 'contact.html', 'btn-primary'),
             cta2=('Tải Catalogue 2026', 'resources.html', 'btn-outline')),
        dict(eyebrow="Custom Engineering / OEM",
             h1="Không chỉ bán những gì có sẵn — chúng tôi kiến tạo giải pháp vừa vặn nhất cho thiết bị của bạn.",
             lead="Thiết kế may đo CAD 2D/3D, cắt laser tự động và hàn siêu âm hiện đại — khớp chính xác biên dạng bồn lọc, máy sấy của từng nhà máy.",
             cta=('Khám phá năng lực OEM/ODM', 'custom-oem.html', 'btn-primary'),
             cta2=('Yêu cầu thiết kế riêng', 'contact.html', 'btn-outline')),
        dict(eyebrow="Trust &amp; Compliance",
             h1="Bảo chứng niềm tin kỹ thuật cho những nhà máy yêu cầu khắt khe nhất.",
             lead="Đạt chuẩn ISO 9001:2015, SGS FDA 21 CFR và QCVN 12-1:2011/BYT — kiểm định qua phòng thí nghiệm kỹ thuật cao trước khi xuất xưởng.",
             cta=('Xem chứng nhận tiêu chuẩn', 'resources.html#certifications', 'btn-primary'),
             cta2=('Về Betaratio', 'about.html', 'btn-outline')),
    ]
    hero_slide_html = ""
    for i, s in enumerate(hero_slides):
        active = " active" if i == 0 else ""
        hero_slide_html += f"""<div class="hero-d-slide{active}" data-slide="{i}">
      <div class="hero-d-media">{hero_media(depth)}</div>
      <div class="hero-d-panel">
        <div class="eyebrow">{s['eyebrow']}</div>
        <h1>{s['h1']}</h1>
        <p class="lead">{s['lead']}</p>
        <div class="cta-row">
          <a href="{s['cta'][1]}" class="btn {s['cta'][2]}">{s['cta'][0]}</a>
          <a href="{s['cta2'][1]}" class="btn {s['cta2'][2]}">{s['cta2'][0]}</a>
        </div>
      </div>
    </div>\n"""
    hero_dots = "".join(
        f'<button class="hero-dot{" active" if i == 0 else ""}" data-goto="{i}" aria-label="Xem slide {i+1}"></button>'
        for i in range(len(hero_slides))
    )

    body = f"""
<section class="hero-d" data-hero-carousel>
  {hero_slide_html}
  <div class="hero-d-dots">{hero_dots}</div>
</section>

<section>
  <div class="container">
    <div class="carousel-head">
      <div class="section-head" style="margin-bottom:0">
        <div class="eyebrow">Lựa chọn theo ngành</div>
        <h2>Giải pháp cho mọi ngành công nghiệp</h2>
        <p>Điều hướng đến trang giải pháp phù hợp với bài toán vận hành thực tế của nhà máy bạn chỉ sau một cú click.</p>
      </div>
      <div class="carousel-arrows">
        <button class="carousel-arrow" data-scroll="-1" aria-label="Cuộn trái">{icon('arrow-right', 'rot-180')}</button>
        <button class="carousel-arrow" data-scroll="1" aria-label="Cuộn phải">{icon('arrow-right')}</button>
      </div>
    </div>
    <div class="industry-scroll" data-carousel>
      {industry_scroll_cards}
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Dải sản phẩm chính</div>
      <h2>Khám phá dải sản phẩm Lọc chất lỏng &amp; Lọc khí</h2>
      <p>Hai nhóm giải pháp cốt lõi của Betaratio, mỗi sản phẩm đều đi kèm thông số kỹ thuật và chứng nhận tiêu chuẩn.</p>
    </div>
    <div data-tabs>
      <div class="tabs text-center" style="justify-content:center">
        <button class="tab-btn active" data-tab="liquid">{icon('droplet')} Lọc chất lỏng</button>
        <button class="tab-btn" data-tab="gas">{icon('wind')} Lọc khí &amp; Sàng lọc</button>
      </div>
      <div class="tab-panel active" data-panel="liquid">
        <div class="grid grid-4">{product_tab_cards(liquid_products)}</div>
      </div>
      <div class="tab-panel" data-panel="gas">
        <div class="grid grid-4">{product_tab_cards(gas_products)}</div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="feature-row">
      <div class="col-text">
        <div class="eyebrow">Năng lực may đo / tùy biến</div>
        <h2>Đúng giải pháp, đúng sản phẩm — kích thước vừa khớp thiết bị của bạn</h2>
        <p>Betaratio không chỉ bán những gì có sẵn — chúng tôi kiến tạo giải pháp lọc vừa vặn nhất, từ hình dạng đơn giản đến phức tạp, khớp chính xác biên dạng máy móc nhà máy bạn.</p>
        <ul class="feature-list">
          <li><span class="fi">{icon('scissors')}</span><div><strong>Cắt laser tự động</strong><p>Kích thước chính xác tuyệt đối, biên cắt sạch, không xơ sợi.</p></div></li>
          <li><span class="fi">{icon('zap')}</span><div><strong>Hàn siêu âm &amp; hàn nhiệt</strong><p>Đường hàn kín khít, loại bỏ nguy cơ rò rỉ qua chân kim dệt.</p></div></li>
          <li><span class="fi">{icon('flask')}</span><div><strong>Phòng thử nghiệm kỹ thuật cao</strong><p>Kiểm định độ thấm khí, điện trở bề mặt, cấu trúc vải trước khi xuất xưởng.</p></div></li>
        </ul>
        <div class="cta-row" style="margin-top:26px">
          <a href="custom-oem.html" class="btn btn-navy">Khám phá năng lực OEM/ODM</a>
        </div>
      </div>
      <div class="col-media">{img_frame('settings', 'Quy trình thiết kế may đo CAD 2D/3D', '4/3.4', slot='process/cad-design', depth=depth)}</div>
    </div>
  </div>
</section>

<section class="stats-band">
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Quy mô &amp; năng lực</div>
      <h2>Betaratio trong con số</h2>
      <p>Nền tảng kỹ thuật và dải sản phẩm giúp Betaratio đồng hành cùng nhiều ngành công nghiệp khác nhau.</p>
    </div>
    <div class="stats-band-grid">
      <div class="stat-big"><b>11+</b><span>Dòng sản phẩm lọc &amp; phân tách</span></div>
      <div class="stat-big"><b>5</b><span>Ngành công nghiệp trọng điểm</span></div>
      <div class="stat-big"><b>3</b><span>Thiết bị lab kiểm định kỹ thuật cao</span></div>
      <div class="stat-big"><b>ISO 9001</b><span>Hệ thống quản lý chất lượng</span></div>
    </div>
  </div>
</section>

<section class="section-navy" id="certifications">
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Bảo chứng niềm tin kỹ thuật</div>
      <h2>Chất lượng &amp; tiêu chuẩn quốc tế</h2>
      <p>Các chứng nhận cốt lõi giúp Betaratio đồng hành cùng những nhà máy quy mô lớn, yêu cầu khắt khe về an toàn và vệ sinh.</p>
    </div>
    <div class="cert-strip">
      <div class="cert-badge" style="background:rgba(255,255,255,.04); border-color:rgba(255,255,255,.14)">
        <span class="badge-ic">{icon('shield-check')}</span>
        <div><strong style="color:#fff">ISO 9001:2015</strong><span style="color:var(--gray-300)">Hệ thống quản lý chất lượng</span></div>
      </div>
      <div class="cert-badge" style="background:rgba(255,255,255,.04); border-color:rgba(255,255,255,.14)">
        <span class="badge-ic">{icon('award')}</span>
        <div><strong style="color:#fff">SGS FDA 21 CFR</strong><span style="color:var(--gray-300)">Chuẩn tiếp xúc thực phẩm quốc tế</span></div>
      </div>
      <div class="cert-badge" style="background:rgba(255,255,255,.04); border-color:rgba(255,255,255,.14)">
        <span class="badge-ic">{icon('check-circle')}</span>
        <div><strong style="color:#fff">QCVN 12-1:2011/BYT</strong><span style="color:var(--gray-300)">An toàn vệ sinh thực phẩm &amp; dược phẩm</span></div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Dự án tiêu biểu</div>
      <h2>Tin tức kỹ thuật &amp; Case Studies</h2>
      <p>Một số bài toán vận hành Betaratio đã cùng đối tác tối ưu — minh họa cho năng lực kỹ thuật thực tế.</p>
    </div>
    <div class="news-list">
      <div class="news-row">
        <div><span class="news-date">Dự án tiêu biểu</span><span class="news-tag">Dược phẩm</span></div>
        <div>
          <h3>Kéo dài tuổi thọ túi sấy tầng sôi</h3>
          <p>Tối ưu cấu trúc sợi và cấp lọc giúp giảm tần suất thay thế túi sấy tầng sôi cho dây chuyền sấy bột dược phẩm.</p>
        </div>
      </div>
      <div class="news-row">
        <div><span class="news-date">Dự án tiêu biểu</span><span class="news-tag">Công nghệ cao</span></div>
        <div>
          <h3>Triệt tiêu tĩnh điện, chống cháy nổ</h3>
          <p>Tích hợp sợi dẫn điện Carbon/SS316L vào túi lọc khí, đưa điện trở bề mặt về ngưỡng an toàn cho khu vực bụi mịn dễ cháy nổ.</p>
        </div>
      </div>
      <div class="news-row">
        <div><span class="news-date">Dự án tiêu biểu</span><span class="news-tag">Thực phẩm &amp; Đồ uống</span></div>
        <div>
          <h3>Loại bỏ hoàn toàn xơ sợi rơi vào sản phẩm</h3>
          <p>Chuyển đổi từ túi may chỉ truyền thống sang túi hàn nhiệt siêu âm (welded seam) cho dây chuyền lọc siro.</p>
        </div>
      </div>
    </div>
    <div class="news-foot">
      <a href="resources.html" class="btn btn-ghost-navy btn-sm">Xem tất cả tài nguyên kỹ thuật {icon('arrow-right')}</a>
    </div>
    <p class="field-note" style="margin-top:14px">Các ví dụ trên minh họa năng lực kỹ thuật của Betaratio; số liệu chi tiết theo từng dự án sẽ được cung cấp khi có yêu cầu báo giá cụ thể.</p>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Sẵn sàng tối ưu chi phí lọc &amp; phân tách cho nhà máy của bạn?</h2>
        <p>Gửi bản vẽ hoặc mẫu thiết bị thực tế — đội ngũ kỹ thuật Betaratio phản hồi phương án trong 24 giờ làm việc.</p>
      </div>
      <a href="contact.html" class="btn btn-primary">Yêu cầu báo giá kỹ thuật {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Trang chủ",
        "Betaratio — Công nghệ lọc và phân tách công nghiệp chuyên sâu: lõi lọc, túi lọc, vải lọc máy, bình lọc và giải pháp gia công theo yêu cầu, đạt chuẩn FDA, ISO 9001, QCVN.",
        "index.html", depth, "home", body,
    )

# =========================================================================
# INDUSTRIES HUB PAGE
# =========================================================================
def industries_hub_page():
    depth = 0
    cards = ""
    for ind in INDUSTRIES:
        a, b = ind["grad"]
        photo = find_photo(f"industries/{ind['slug']}")
        if photo:
            isc_media = f'<img src="{rel(photo, depth)}" alt="{ind["name"]}" loading="lazy">'
            isc_style = ""
        else:
            isc_media = icon(ind['nav_ic'])
            isc_style = gradient_style(a, b)
        cards += f"""<a class="industry-scroll-card" href="industries/{ind['slug']}.html" style="flex-basis:auto">
      <div class="isc-title">{ind['name']}</div>
      <div class="isc-photo" {isc_style}>{isc_media}</div>
      <div style="padding:16px 18px">
        <p style="margin:0;font-size:13.5px">{ind['summary']}</p>
        <span class="tag" style="color:var(--teal-600);font-weight:700;display:inline-flex;gap:6px;align-items:center;margin-top:10px">Xem giải pháp {icon('arrow-right')}</span>
      </div>
    </a>\n"""

    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Trang chủ</a><span class="sep">/</span><span>Ngành công nghiệp</span></div>
    <div class="eyebrow">Industry-first approach</div>
    <h1>Giải pháp lọc &amp; phân tách theo từng ngành công nghiệp</h1>
    <p class="lead">Khách hàng B2B thường tìm giải pháp cho bài toán của ngành mình trước khi tìm sản phẩm cụ thể. Chọn đúng ngành để xem thách thức vận hành thường gặp và giải pháp kỹ thuật Betaratio đề xuất.</p>
  </div>
</section>
<section>
  <div class="container">
    <div class="grid grid-3">
      {cards}
    </div>
  </div>
</section>
<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Chưa chắc ngành của bạn thuộc nhóm nào?</h2>
        <p>Gửi mô tả quy trình vận hành — đội ngũ kỹ thuật Betaratio sẽ tư vấn giải pháp lọc &amp; phân tách phù hợp nhất.</p>
      </div>
      <a href="contact.html" class="btn btn-primary">Liên hệ tư vấn kỹ thuật {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Ngành công nghiệp",
        "Giải pháp lọc & phân tách theo ngành: Thực phẩm & Đồ uống, Dược phẩm, Điện tử & Bán dẫn, Công nghệ cao & Phòng sạch, Năng lượng & Công nghiệp nặng.",
        "industries.html", depth, "industries", body,
    )


# =========================================================================
# INDUSTRY DETAIL PAGE (one per industry)
# =========================================================================
def industry_page(ind):
    depth = 1
    a, b = ind["grad"]

    pain_items = "".join(f"<li>{c}</li>" for c in ind["challenges"])
    sol_items = "".join(f"<li>{s}</li>" for s in ind["solutions"])

    prod_cards = ""
    for name, desc, ic in ind["products"]:
        prod_cards += f"""<div class="product-card">
      {product_media(name, ic, depth)}
      <div class="pc-body">
        <span class="pc-meta">Sản phẩm đề xuất</span>
        <h4>{name}</h4>
        <p>{desc}</p>
        <div class="pc-foot">
          <a href="../products/index.html" class="btn btn-ghost-navy btn-sm">Xem sản phẩm</a>
        </div>
      </div>
    </div>\n"""

    other_industries = ""
    for other in INDUSTRIES:
        if other["slug"] == ind["slug"]:
            continue
        other_industries += f'<a class="pill" href="{other["slug"]}.html">{other["name"]}</a>\n'

    body = f"""
<section class="page-hero" {gradient_style(a, b)} style="background:linear-gradient(160deg, var(--grad-a), var(--grad-b))">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a><span class="sep">/</span><a href="../industries.html">Ngành công nghiệp</a><span class="sep">/</span><span>{ind['name']}</span></div>
    <div class="eyebrow">{ind['name_en']}</div>
    <h1>Giải pháp lọc &amp; phân tách cho ngành {ind['name']}</h1>
    <p class="lead">{ind['summary']}</p>
    <div class="page-hero-badges">
      <span>{icon('shield-check', 'cap-ic')} Đạt chuẩn FDA / QCVN</span>
      <span>{icon('settings', 'cap-ic')} Tùy biến theo thiết bị</span>
      <span>{icon('flask', 'cap-ic')} Kiểm định trước xuất xưởng</span>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">Thách thức &amp; Giải pháp</div>
      <h2>{ind['challenge_title']}</h2>
    </div>
    <div class="pain-solution">
      <div class="psblock pain">
        <h3>{icon('activity')} Thách thức thường gặp</h3>
        <ul>{pain_items}</ul>
      </div>
      <div class="psblock solution">
        <h3>{icon('check-circle')} Giải pháp từ Betaratio</h3>
        <ul>{sol_items}</ul>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">Đề xuất cho ngành {ind['name']}</div>
      <h2>Sản phẩm khuyến nghị</h2>
      <p>Các dòng sản phẩm Betaratio phù hợp nhất với đặc thù vận hành ngành {ind['name'].lower()}.</p>
    </div>
    <div class="grid grid-3">
      {prod_cards}
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Cần tư vấn giải pháp riêng cho nhà máy {ind['name'].lower()}?</h2>
        <p>Gửi thông số dây chuyền hoặc mẫu thiết bị — Betaratio phản hồi phương án kỹ thuật trong 24 giờ làm việc.</p>
      </div>
      <a href="../contact.html" class="btn btn-primary">Yêu cầu báo giá kỹ thuật {icon('arrow-right')}</a>
    </div>
  </div>
</section>

<section class="section-tight">
  <div class="container">
    <h4 style="font-size:12.5px;text-transform:uppercase;letter-spacing:.05em;color:var(--gray-500);margin-bottom:14px">Xem thêm các ngành khác</h4>
    <div class="pill-list">{other_industries}</div>
  </div>
</section>
"""
    return PAGE(
        ind["name"],
        f"Giải pháp lọc & phân tách Betaratio cho ngành {ind['name']}: {ind['summary']}",
        f"industries/{ind['slug']}.html", depth, "industries", body,
    )

# =========================================================================
# PRODUCTS HUB PAGE (with full classification matrix — Phần 4 tài liệu gốc)
# =========================================================================
def products_hub_page():
    depth = 1  # lives at products/index.html

    matrix_groups = sorted({row['group'] for row in PRODUCT_MATRIX})
    matrix_industries = sorted({ind for row in PRODUCT_MATRIX for ind in row['industries_list']})
    group_options = "".join(f'<option value="{g}">{g}</option>' for g in matrix_groups)
    industry_options = "".join(f'<option value="{i}">{i}</option>' for i in matrix_industries)

    matrix_rows = ""
    for row in PRODUCT_MATRIX:
        inds = "|".join(row['industries_list'])
        matrix_rows += f"""<tr data-mgroup="{row['group']}" data-minds="{inds}">
      <td><strong>{row['name']}</strong></td>
      <td>{row['group']}</td>
      <td>{row['app']}</td>
      <td>{row['industries']}</td>
      <td>{row['standard']}</td>
    </tr>\n"""

    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a><span class="sep">/</span><span>Sản phẩm</span></div>
    <div class="eyebrow">Multi-dimensional product navigation</div>
    <h1>Dải sản phẩm lọc &amp; phân tách Betaratio</h1>
    <p class="lead">Tìm sản phẩm theo nhóm kỹ thuật (lõi lọc, túi lọc, vải lọc máy, bình lọc) hoặc theo chức năng lọc (tách rắn – lỏng, tách rắn – khí). Chọn một trong hai nhóm chính bên dưới để xem bộ lọc kỹ thuật chi tiết.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="grid grid-2">
      <a class="card" href="liquid-filtration.html" style="padding:34px">
        <span class="ic-badge">{icon('droplet')}</span>
        <h3>Thiết bị Lọc Chất lỏng</h3>
        <p>Lõi lọc / cột lọc, túi lọc dung dịch lỏng, vải lọc máy công nghiệp, bình lọc chất lỏng — giải pháp tách rắn–lỏng cho thực phẩm, dược phẩm, điện tử, năng lượng.</p>
        <span class="tag" style="color:var(--teal-600);font-weight:700;display:inline-flex;gap:6px;align-items:center;margin-top:10px">Xem sản phẩm &amp; bộ lọc kỹ thuật {icon('arrow-right')}</span>
      </a>
      <a class="card" href="gas-separation.html" style="padding:34px">
        <span class="ic-badge">{icon('wind')}</span>
        <h3>Thiết bị Lọc Khí &amp; Sàng lọc</h3>
        <p>Túi sấy tầng sôi, túi lọc bụi &amp; thu hồi bột mịn, túi thông áp bồn chứa, khớp nối mềm bằng vải kỹ thuật — giải pháp tách rắn–khí và an toàn chống tĩnh điện.</p>
        <span class="tag" style="color:var(--teal-600);font-weight:700;display:inline-flex;gap:6px;align-items:center;margin-top:10px">Xem sản phẩm &amp; bộ lọc kỹ thuật {icon('arrow-right')}</span>
      </a>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">Phân loại sản phẩm</div>
      <p>Tra cứu nhanh theo nhóm thiết bị, ứng dụng lọc, ngành công nghiệp phù hợp và tiêu chuẩn chất lượng cốt lõi.</p>
    </div>
    <div class="matrix-filter-bar" data-matrix-filter>
      <div class="mf-select">
        <label for="mf-group">Nhóm thiết bị</label>
        <select id="mf-group" data-mf="group">
          <option value="">Tất cả nhóm thiết bị</option>
          {group_options}
        </select>
      </div>
      <div class="mf-select">
        <label for="mf-industry">Ngành phù hợp</label>
        <select id="mf-industry" data-mf="industry">
          <option value="">Tất cả ngành</option>
          {industry_options}
        </select>
      </div>
      <button type="button" class="btn btn-ghost-navy btn-sm" data-mf-reset>Xóa bộ lọc</button>
      <span class="mf-count"><strong data-mf-count>{len(PRODUCT_MATRIX)}</strong> / {len(PRODUCT_MATRIX)} sản phẩm</span>
    </div>
    <div class="table-wrap">
      <table class="matrix" data-mf-table>
        <thead><tr><th>Tên sản phẩm</th><th>Nhóm thiết bị</th><th>Ứng dụng lọc</th><th>Ngành phù hợp</th><th>Tiêu chuẩn cốt lõi</th></tr></thead>
        <tbody>{matrix_rows}</tbody>
      </table>
      <p class="mf-empty" data-mf-empty style="display:none">Không tìm thấy sản phẩm phù hợp với bộ lọc đã chọn.</p>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Không chắc dòng sản phẩm nào phù hợp?</h2>
        <p>Gửi bản vẽ hoặc thông số kỹ thuật thiết bị — Betaratio tư vấn đúng sản phẩm, đúng giải pháp.</p>
      </div>
      <a href="../contact.html" class="btn btn-primary">Yêu cầu tư vấn kỹ thuật {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Sản phẩm",
        "Dải sản phẩm lọc & phân tách Betaratio: lõi lọc, túi lọc, vải lọc máy, bình lọc, túi sấy tầng sôi, túi thông áp, khớp nối mềm — cùng ma trận phân loại sản phẩm đầy đủ.",
        "products/index.html", depth, "products", body,
    )


def filter_sidebar(scope_id, groups, result_default):
    """groups: list of (title, group_key, [(label, value), ...])"""
    html = f'<aside class="filter-sidebar">\n'
    for title, gkey, opts in groups:
        html += f'<h4>{title}</h4>\n<div class="filter-group">\n'
        for label, val in opts:
            html += f'<label><input type="checkbox" data-group="{gkey}" value="{val}"> {label}</label>\n'
        html += '</div>\n'
    html += f'<button class="btn btn-ghost-navy btn-sm btn-block filter-reset" data-filter-reset type="button">Xóa bộ lọc</button>\n'
    html += '</aside>'
    return html


def product_card(name, meta, desc, spec, ic, data_attrs, depth=1):
    attrs = " ".join(f'data-{k}="{v}"' for k, v in data_attrs.items())
    return f"""<div class="product-card" data-card {attrs}>
  {product_media(name, ic, depth)}
  <div class="pc-body">
    <span class="pc-meta">{meta}</span>
    <h4>{name}</h4>
    <p>{desc}</p>
    <div class="pc-foot">
      <span class="pc-spec">{spec}</span>
      <a href="../contact.html" class="btn btn-ghost-navy btn-sm">Yêu cầu báo giá</a>
    </div>
  </div>
</div>"""

# =========================================================================
# LIQUID FILTRATION PAGE
# =========================================================================
def liquid_filtration_page():
    depth = 1

    sidebar = filter_sidebar("liquid", [
        ("Theo nhóm thiết bị", "type", [
            ("Lõi lọc / Cột lọc", "cartridge"), ("Túi lọc dung dịch lỏng", "bag"),
            ("Vải lọc máy công nghiệp", "cloth"), ("Bình lọc chất lỏng", "vessel"),
        ]),
        ("Theo dòng sản phẩm", "series", [
            ("EF Series (lưới monofilament)", "EF"), ("FF Series (nỉ kim lọc sâu)", "FF"),
            ("MF Series (đa sợi lai)", "MF"),
        ]),
        ("Theo vật liệu", "material", [
            ("Polypropylene (PP)", "PP"), ("Polyester (PE)", "PE"),
            ("Nylon (Polyamide)", "Nylon"), ("PTFE", "PTFE"), ("Thép không gỉ SS304/316", "SS"),
        ]),
        ("Theo cấp độ lọc (Micron)", "micron", [
            ("Dưới 1 µm (tuyệt đối)", "sub1"), ("1 – 10 µm", "1-10"),
            ("10 – 100 µm", "10-100"), ("100 – 2000 µm", "100-2000"),
        ]),
        ("Theo loại cổ túi (Collar)", "collar", [
            ("Vòng nhựa PP/PE", "plastic"), ("Vòng thép SS304", "steel"), ("Dây rút", "drawstring"),
        ]),
        ("Kiểu gia công đường biên (Seam)", "seam", [
            ("May chỉ truyền thống (Sewn)", "sewn"), ("Hàn nhiệt siêu âm (Welded)", "welded"),
        ]),
    ], 10)

    cartridge_cards = "".join([
        product_card("Lõi lọc Melt-blown", "Lõi lọc lỏng", "Lọc sâu tinh, giữ hạt mịn hiệu quả cao — FDA, QCVN 12-1:2011/BYT, NSF 42.", "1 – 10 µm · PP",
                      "cylinder", {"type": "cartridge", "material": "PP", "micron": "1-10"}),
        product_card("Lõi lọc Sợi quấn (String Wound)", "Lõi lọc lỏng", "Lọc thô, cấu trúc lỗ gradient tối ưu dung tích chứa cặn thô — chịu nhiệt tốt.", "10 – 100 µm · PP/Cotton",
                      "cylinder", {"type": "cartridge", "material": "PP", "micron": "10-100"}),
        product_card("Lõi lọc Màng xếp nếp (Pleated)", "Lõi lọc lỏng", "Lọc tuyệt đối, tiệt trùng vi sinh — FDA, EC Food, chịu Autoclave 121°C.", "Dưới 1 µm · PTFE/PES",
                      "cylinder", {"type": "cartridge", "material": "PTFE", "micron": "sub1"}),
    ])
    bag_cards = "".join([
        product_card("Túi lọc lưới EF Series", "Túi lọc lỏng", "Lọc bề mặt, giữ hạt không biến dạng, có thể tái sử dụng — FDA, QCVN 12-1:2011/BYT.", "10 – 2000 µm · PP/Nylon",
                      "bag", {"type": "bag", "series": "EF", "material": "PP", "micron": "100-2000", "collar": "plastic", "seam": "sewn"}),
        product_card("Túi lọc nỉ FF Series", "Túi lọc lỏng", "Lọc sâu đa lớp cho hạt mềm lơ lửng, dung tích chứa cặn lớn — FDA, QCVN 12-1:2011/BYT.", "1 – 10 µm · PE/PP",
                      "bag", {"type": "bag", "series": "FF", "material": "PE", "micron": "1-10", "collar": "steel", "seam": "welded"}),
        product_card("Túi lọc đa sợi MF Series", "Túi lọc lỏng", "Lọc lai (bề mặt &amp; sâu), độ bền cơ học cao — FDA, QCVN 12-1:2011/BYT.", "1 – 10 µm · PP/Nylon",
                      "bag", {"type": "bag", "series": "MF", "material": "Nylon", "micron": "1-10", "collar": "drawstring", "seam": "welded"}),
    ])
    cloth_cards = "".join([
        product_card("Vải lọc máy ép khung bản", "Vải lọc máy", "Tách rắn – lỏng quy mô cực lớn, may viền gia cố chịu lực cơ học cao — FDA, EC, QCVN.", "Theo yêu cầu · PP",
                      "layers", {"type": "cloth", "material": "PP", "micron": "10-100"}),
        product_card("Vải lọc máy ly tâm (Centrifuge Cloth)", "Vải lọc máy", "Chịu ứng suất lớn, tối ưu cho máy lọc ly tâm công suất cao.", "Theo yêu cầu · PE",
                      "layers", {"type": "cloth", "material": "PE", "micron": "10-100"}),
    ])
    vessel_cards = "".join([
        product_card("Bình lọc đơn túi/lõi", "Thiết bị vỏ bồn", "Vỏ chứa túi/lõi lọc áp suất cho dây chuyền quy mô vừa — thép không gỉ SS304.", "Áp suất tiêu chuẩn · SS304",
                      "tank", {"type": "vessel", "material": "SS", "micron": "10-100"}),
        product_card("Bình lọc đa túi công nghiệp (Multi-bag)", "Thiết bị vỏ bồn", "Công suất lên tới 2.238 lít, xử lý lưu lượng cực đại — thép không gỉ SS316L.", "Đến 2.238 lít · SS316L",
                      "tank", {"type": "vessel", "material": "SS", "micron": "10-100"}),
    ])

    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a><span class="sep">/</span><a href="index.html">Sản phẩm</a><span class="sep">/</span><span>Lọc chất lỏng</span></div>
    <div class="eyebrow">Liquid Filtration</div>
    <h1>Thiết bị Lọc Chất lỏng công nghiệp Betaratio</h1>
    <p class="lead">Đạt chuẩn tiếp xúc thực phẩm trực tiếp của FDA và QCVN Việt Nam. Giải pháp hoàn hảo cho lọc thô, lọc tinh và lọc sâu — từ lõi lọc, túi lọc đến vải lọc máy và bình lọc áp suất.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="filter-layout" data-filter-scope="liquid">
      {sidebar}
      <div>
        <div class="results-bar">
          <span class="count"><strong data-result-count>10</strong> sản phẩm phù hợp</span>
          <span class="field-note mb-0">Đánh dấu vào bộ lọc bên trái để thu hẹp kết quả theo nhu cầu kỹ thuật</span>
        </div>

        <h3 id="cartridges" style="font-size:19px;color:var(--navy-900);margin-top:6px">Lõi lọc / Cột lọc (Filter Cartridges)</h3>
        <div class="grid grid-3" style="margin-bottom:40px">{cartridge_cards}</div>

        <h3 id="bags" style="font-size:19px;color:var(--navy-900)">Túi lọc dung dịch lỏng (Liquid Filter Bags)</h3>
        <div class="grid grid-3" style="margin-bottom:40px">{bag_cards}</div>

        <h3 id="cloths" style="font-size:19px;color:var(--navy-900)">Vải lọc máy công nghiệp (Filter Press / Centrifuge Cloths)</h3>
        <div class="grid grid-3" style="margin-bottom:40px">{cloth_cards}</div>

        <h3 id="vessels" style="font-size:19px;color:var(--navy-900)">Bình lọc chất lỏng (Liquid Filter Vessels)</h3>
        <div class="grid grid-3">{vessel_cards}</div>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Cần thông số kỹ thuật chi tiết hoặc bản vẽ tùy biến?</h2>
        <p>Gửi yêu cầu báo giá kỹ thuật kèm thông số thiết bị — Betaratio phản hồi trong 24 giờ làm việc.</p>
      </div>
      <a href="../contact.html" class="btn btn-primary">Yêu cầu báo giá kỹ thuật {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Thiết bị Lọc Chất lỏng",
        "Lõi lọc, túi lọc EF/FF/MF Series, vải lọc máy công nghiệp và bình lọc chất lỏng Betaratio — đạt chuẩn FDA, QCVN 12-1:2011/BYT.",
        "products/liquid-filtration.html", depth, "products", body,
    )


# =========================================================================
# GAS SEPARATION / SIFTING PAGE
# =========================================================================
def gas_separation_page():
    depth = 1

    sidebar = filter_sidebar("gas", [
        ("Theo loại sản phẩm", "type", [
            ("Túi sấy tầng sôi", "fluidbed"), ("Túi lọc bụi / thu hồi bột mịn", "collector"),
            ("Túi thông áp bồn chứa", "vent"), ("Khớp nối mềm bằng vải", "connector"),
        ]),
        ("Theo vật liệu", "material", [
            ("Polypropylene (PP)", "PP"), ("Polyester (PE)", "PE"),
            ("Sợi Carbon chống tĩnh điện", "Carbon"), ("Sợi SS316L", "SS316L"),
        ]),
        ("Theo ứng dụng", "app", [
            ("Sấy khô bột / hạt", "drying"), ("Thu hồi bột mịn", "recovery"),
            ("Thông gió bồn chứa", "venting"), ("Kết nối rung động", "connecting"),
        ]),
        ("Yêu cầu an toàn", "safety", [
            ("Chống tĩnh điện (ESD)", "esd"), ("Chống cháy nổ bụi mịn", "explosion"),
        ]),
    ], 8)

    fluidbed_cards = "".join([
        product_card("Túi sấy tầng sôi — Sợi Carbon", "Lọc sấy khí", "Chống tĩnh điện tích hợp sợi Carbon, điện trở bề mặt an toàn 10³–10⁶ Ohm.", "Chống nổ · Carbon",
                      "wind", {"type": "fluidbed", "material": "Carbon", "app": "drying", "safety": "esd|explosion"}),
        product_card("Túi sấy tầng sôi — Sợi SS316L", "Lọc sấy khí", "Tích hợp sợi kim loại SS316L, độ bền cơ học và khả năng dẫn điện cao.", "Chống nổ · SS316L",
                      "wind", {"type": "fluidbed", "material": "SS316L", "app": "drying", "safety": "esd|explosion"}),
    ])
    collector_cards = "".join([
        product_card("Túi lọc bụi & thu hồi bột mịn", "Lọc khí", "Product Collector Bags — thu hồi tối đa bột mịn, giảm thất thoát nguyên liệu.", "Cấp lọc mịn · PP/PE",
                      "bag", {"type": "collector", "material": "PP", "app": "recovery", "safety": ""}),
    ])
    vent_cards = "".join([
        product_card("Túi lọc thông áp (Vent Bag)", "Lọc khí", "Thông gió bồn chứa, ngăn nhiễm vi sinh — cấp lọc siêu mịn, tránh nhiễm chéo.", "Siêu mịn · PE",
                      "wind", {"type": "vent", "material": "PE", "app": "venting", "safety": "esd"}),
    ])
    connector_cards = "".join([
        product_card("Khớp nối mềm bằng vải kỹ thuật", "Phụ kiện máy", "Kết nối rung động giữa các máy móc, ngừa phát thải bụi — cắt laser chuẩn xác, may đo theo máy.", "May đo theo máy · PP",
                      "link", {"type": "connector", "material": "PP", "app": "connecting", "safety": ""}),
    ])

    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="../index.html">Trang chủ</a><span class="sep">/</span><a href="index.html">Sản phẩm</a><span class="sep">/</span><span>Lọc khí &amp; Sàng lọc</span></div>
    <div class="eyebrow">Gas Separation &amp; Sifting</div>
    <h1>Thiết bị Lọc Khí &amp; Sàng lọc Betaratio</h1>
    <p class="lead">Giải pháp tách rắn – khí cho sấy tầng sôi, thu hồi bột mịn, thông gió bồn chứa và kết nối rung động — tích hợp công nghệ chống tĩnh điện, an toàn phòng chống cháy nổ.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="filter-layout" data-filter-scope="gas">
      {sidebar}
      <div>
        <div class="results-bar">
          <span class="count"><strong data-result-count>5</strong> sản phẩm phù hợp</span>
          <span class="field-note mb-0">Đánh dấu vào bộ lọc bên trái để thu hẹp kết quả theo nhu cầu kỹ thuật</span>
        </div>

        <h3 id="fluidbed" style="font-size:19px;color:var(--navy-900);margin-top:6px">Túi sấy tầng sôi (Fluid Bed Dryer Bags)</h3>
        <div class="grid grid-3" style="margin-bottom:40px">{fluidbed_cards}</div>

        <h3 id="collector" style="font-size:19px;color:var(--navy-900)">Túi lọc bụi &amp; Thu hồi bột mịn (Product Collector Bags)</h3>
        <div class="grid grid-3" style="margin-bottom:40px">{collector_cards}</div>

        <h3 id="vent" style="font-size:19px;color:var(--navy-900)">Túi thông áp / Thông gió bồn chứa (Vent Bags)</h3>
        <div class="grid grid-3" style="margin-bottom:40px">{vent_cards}</div>

        <h3 id="connector" style="font-size:19px;color:var(--navy-900)">Khớp nối mềm bằng vải kỹ thuật (Flexible Connectors)</h3>
        <div class="grid grid-3">{connector_cards}</div>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Cần giải pháp chống tĩnh điện / chống cháy nổ chuyên biệt?</h2>
        <p>Đội ngũ kỹ thuật Betaratio đo lường điện trở bề mặt và tư vấn cấu trúc sợi phù hợp với khu vực sản xuất của bạn.</p>
      </div>
      <a href="../contact.html" class="btn btn-primary">Yêu cầu báo giá kỹ thuật {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Thiết bị Lọc Khí & Sàng lọc",
        "Túi sấy tầng sôi, túi lọc bụi & thu hồi bột mịn, túi thông áp bồn chứa, khớp nối mềm bằng vải kỹ thuật — chống tĩnh điện, an toàn cháy nổ.",
        "products/gas-separation.html", depth, "products", body,
    )

# =========================================================================
# CUSTOM OEM / DESIGN & MANUFACTURING PAGE
# =========================================================================
def custom_oem_page():
    depth = 0
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Trang chủ</a><span class="sep">/</span><span>Gia công theo yêu cầu</span></div>
    <div class="eyebrow">Custom Engineering / OEM · ODM</div>
    <h1>Năng lực gia công theo yêu cầu (Custom Design &amp; Manufacturing)</h1>
    <p class="lead">"Chúng tôi không chỉ bán những gì có sẵn — chúng tôi kiến tạo giải pháp vừa vặn nhất cho thiết bị của bạn." Đây là năng lực khẳng định vị thế công ty kỹ thuật chuyên sâu của Betaratio, khác biệt so với các nhà phân phối thương mại thông thường.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Quy trình 3 bước</div>
      <h2>Thiết kế may đo (Tailored Engineering)</h2>
      <p>Tiếp nhận bản vẽ hoặc mẫu thực tế từ nhà máy, lên bản vẽ CAD 2D/3D khớp chính xác biên dạng bồn lọc/máy sấy của khách hàng.</p>
    </div>
    <div class="steps">
      <div class="step">
        <span class="num">1</span>
        <h4>Tiếp nhận bản vẽ / mẫu thực tế</h4>
        <p>Kỹ sư Betaratio thu thập bản vẽ kỹ thuật hoặc mẫu vật thực tế từ thiết bị của nhà máy để xác định chính xác biên dạng cần gia công.</p>
      </div>
      <div class="step">
        <span class="num">2</span>
        <h4>Dựng bản vẽ CAD 2D/3D</h4>
        <p>Chuyển hóa dữ liệu thu thập thành bản vẽ CAD 2D/3D khớp chính xác biên dạng bồn lọc, máy sấy hoặc hệ thống đường ống của khách hàng.</p>
      </div>
      <div class="step">
        <span class="num">3</span>
        <h4>Sản xuất &amp; kiểm định chất lượng</h4>
        <p>Gia công trên dây chuyền cắt laser và hàn siêu âm hiện đại, kiểm định qua phòng thí nghiệm kỹ thuật trước khi xuất xưởng.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="feature-row">
      <div class="col-media">{img_frame('scissors', 'Máy cắt Laser tự động', '4/3.4', True, slot='process/laser-cutting', depth=depth)}</div>
      <div class="col-text">
        <div class="eyebrow">Công nghệ sản xuất tiên tiến</div>
        <h2>Máy cắt Laser tự động</h2>
        <p>Đảm bảo kích thước tuyệt đối chính xác, biên cắt sạch, không xơ sợi — nền tảng cho các sản phẩm yêu cầu độ chính xác cao như khớp nối mềm và túi lọc phòng sạch.</p>
        <ul class="feature-list">
          <li><span class="fi">{icon('target')}</span><div><strong>Dung sai kích thước cực nhỏ</strong><p>Khớp chính xác biên dạng thiết bị, giảm thiểu hao phí lắp đặt.</p></div></li>
          <li><span class="fi">{icon('shield-check')}</span><div><strong>Biên cắt sạch, không xơ sợi</strong><p>Phù hợp cho môi trường yêu cầu vệ sinh nghiêm ngặt (thực phẩm, dược phẩm, phòng sạch).</p></div></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="feature-row reverse">
      <div class="col-media">{img_frame('zap', 'Máy hàn siêu âm & hàn nhiệt', '4/3.4', True, slot='process/ultrasonic-welding', depth=depth)}</div>
      <div class="col-text">
        <div class="eyebrow">Công nghệ sản xuất tiên tiến</div>
        <h2>Máy hàn siêu âm &amp; hàn nhiệt hiện đại</h2>
        <p>Tạo đường hàn túi lọc chất lỏng kín khít, loại bỏ hoàn toàn nguy cơ rò rỉ qua chân kim dệt — thay thế phương pháp may chỉ truyền thống ở những ứng dụng đòi hỏi độ vô trùng cao.</p>
        <ul class="feature-list">
          <li><span class="fi">{icon('check-circle')}</span><div><strong>Đường hàn kín khít</strong><p>Không có lỗ kim, loại bỏ điểm rò rỉ và nguy cơ nhiễm vi sinh.</p></div></li>
          <li><span class="fi">{icon('layers')}</span><div><strong>Phù hợp đa vật liệu</strong><p>Ứng dụng cho PP, PE, Nylon và các vật liệu kỹ thuật chuyên dụng khác.</p></div></li>
        </ul>
      </div>
    </div>
  </div>
</section>

<section class="section-navy">
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Kiểm soát chất lượng</div>
      <h2>Phòng thí nghiệm kiểm soát chất lượng kỹ thuật cao</h2>
      <p>Mỗi lô sản phẩm được kiểm định qua hệ thống thiết bị đo lường chuyên dụng nhập khẩu trước khi xuất xưởng.</p>
    </div>
    <div class="grid grid-3">
      <div class="lab-card" style="background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.14)">
        <span class="lab-ic">{icon('wind')}</span>
        <div>
          <h4 style="color:#fff">Thiết bị đo độ thấm khí</h4>
          <p style="color:var(--gray-300)">Kiểm định lưu lượng dòng khí sấy tầng sôi, đảm bảo hiệu suất lọc đúng thiết kế.</p>
          <span class="origin">Xuất xứ Thụy Sĩ</span>
        </div>
      </div>
      <div class="lab-card" style="background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.14)">
        <span class="lab-ic">{icon('zap')}</span>
        <div>
          <h4 style="color:#fff">Thiết bị đo điện trở bề mặt</h4>
          <p style="color:var(--gray-300)">Cam kết độ an toàn tĩnh điện, phòng chống cháy nổ cho môi trường bụi mịn dễ cháy.</p>
          <span class="origin">Xuất xứ CHLB Đức</span>
        </div>
      </div>
      <div class="lab-card" style="background:rgba(255,255,255,.04);border-color:rgba(255,255,255,.14)">
        <span class="lab-ic">{icon('search')}</span>
        <div>
          <h4 style="color:#fff">Thiết bị kiểm tra cấu trúc vải</h4>
          <p style="color:var(--gray-300)">Kiểm tra chuyên dụng cấu trúc dệt, đảm bảo đồng nhất cấp lọc trên toàn bộ tấm vật liệu.</p>
          <span class="origin">Xuất xứ Nhật Bản</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="cta-band">
      <div>
        <h2>Có bản vẽ hoặc mẫu thiết bị cần tư vấn gia công?</h2>
        <p>Gửi file bản vẽ CAD hoặc mô tả biên dạng thiết bị — kỹ sư Betaratio phản hồi phương án thiết kế trong 24 giờ làm việc.</p>
      </div>
      <a href="contact.html" class="btn btn-primary">Gửi yêu cầu thiết kế riêng {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Gia công theo yêu cầu (Custom OEM/ODM)",
        "Năng lực thiết kế may đo, công nghệ cắt laser & hàn siêu âm, phòng thí nghiệm kiểm soát chất lượng kỹ thuật cao của Betaratio.",
        "custom-oem.html", depth, "oem", body,
    )


# =========================================================================
# RESOURCES PAGE
# =========================================================================
def resources_page():
    depth = 0
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Trang chủ</a><span class="sep">/</span><span>Tài nguyên kỹ thuật</span></div>
    <div class="eyebrow">Resources</div>
    <h1>Tài nguyên kỹ thuật</h1>
    <p class="lead">Thư viện catalogue &amp; datasheet, chứng nhận tiêu chuẩn và các case study thực tế — hỗ trợ đội ngũ kỹ thuật của bạn ra quyết định nhanh và chính xác.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">5.1</div>
      <h2>Thư viện Catalogue &amp; Datasheet</h2>
      <p>Tải tài liệu kỹ thuật chi tiết cho từng dòng sản phẩm. Đăng tệp PDF thật của bạn vào thư mục <code>/resources/</code> rồi cập nhật liên kết bên dưới.</p>
    </div>
    <div class="grid grid-3">
      <div class="card">
        <span class="ic-badge">{icon('file-text')}</span>
        <h3>Catalogue tổng hợp 2026</h3>
        <p>Toàn bộ dải sản phẩm lọc chất lỏng &amp; lọc khí, kèm bảng thông số kỹ thuật.</p>
        <a href="#" class="btn btn-ghost-navy btn-sm" style="margin-top:14px">{icon('download')} Tải PDF</a>
      </div>
      <div class="card">
        <span class="ic-badge">{icon('file-text')}</span>
        <h3>Datasheet Lọc Chất lỏng</h3>
        <p>Thông số lõi lọc, túi lọc EF/FF/MF, vải lọc máy và bình lọc áp suất.</p>
        <a href="products/liquid-filtration.html" class="btn btn-ghost-navy btn-sm" style="margin-top:14px">Xem trực tuyến {icon('arrow-right')}</a>
      </div>
      <div class="card">
        <span class="ic-badge">{icon('file-text')}</span>
        <h3>Datasheet Lọc Khí &amp; Sàng lọc</h3>
        <p>Thông số túi sấy tầng sôi, túi thông áp và khớp nối mềm kỹ thuật.</p>
        <a href="products/gas-separation.html" class="btn btn-ghost-navy btn-sm" style="margin-top:14px">Xem trực tuyến {icon('arrow-right')}</a>
      </div>
    </div>
  </div>
</section>

<section class="section-alt" id="certifications">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">5.2</div>
      <h2>Chứng nhận tiêu chuẩn</h2>
      <p>Betaratio tuân thủ các tiêu chuẩn quốc tế và trong nước để đảm bảo sản phẩm phù hợp với môi trường sản xuất khắt khe nhất.</p>
    </div>
    <div class="cert-strip">
      <div class="cert-badge">
        <span class="badge-ic">{icon('shield-check')}</span>
        <div><strong>ISO 9001:2015</strong><span>Hệ thống quản lý chất lượng</span></div>
      </div>
      <div class="cert-badge">
        <span class="badge-ic">{icon('award')}</span>
        <div><strong>SGS FDA 21 CFR</strong><span>Chuẩn tiếp xúc thực phẩm trực tiếp</span></div>
      </div>
      <div class="cert-badge">
        <span class="badge-ic">{icon('check-circle')}</span>
        <div><strong>QCVN 12-1:2011/BYT</strong><span>An toàn vệ sinh thực phẩm Việt Nam</span></div>
      </div>
    </div>
    <p class="field-note" style="margin-top:16px">Bản sao chứng chỉ gốc được cung cấp theo yêu cầu khi ký kết hợp đồng cung ứng — liên hệ đội ngũ kinh doanh để nhận bộ hồ sơ đầy đủ.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">5.3</div>
      <h2>Case Studies — Dự án thực tế</h2>
      <p>Một số bài toán vận hành tiêu biểu Betaratio đã đồng hành cùng đối tác.</p>
    </div>
    <div class="grid grid-3">
      <div class="case-card">
        {case_media('wind', 'case-studies/case-1-pharma-fluidbed', depth)}
        <div class="cc-body">
          <span class="cc-tag">Dược phẩm</span>
          <h3>Kéo dài tuổi thọ túi sấy tầng sôi</h3>
          <p>Tối ưu cấu trúc sợi và cấp lọc giúp giảm tần suất thay thế túi sấy tầng sôi cho dây chuyền sấy bột dược phẩm.</p>
        </div>
      </div>
      <div class="case-card">
        {case_media('zap', 'case-studies/case-2-hightech-esd', depth)}
        <div class="cc-body">
          <span class="cc-tag">Công nghệ cao</span>
          <h3>Triệt tiêu tĩnh điện, chống cháy nổ</h3>
          <p>Tích hợp sợi dẫn điện Carbon/SS316L, đưa điện trở bề mặt về ngưỡng an toàn cho khu vực bụi mịn dễ cháy nổ.</p>
        </div>
      </div>
      <div class="case-card">
        {case_media('droplet', 'case-studies/case-3-food-welded-seam', depth)}
        <div class="cc-body">
          <span class="cc-tag">Thực phẩm &amp; Đồ uống</span>
          <h3>Loại bỏ xơ sợi rơi vào sản phẩm</h3>
          <p>Chuyển đổi từ túi may chỉ sang túi hàn nhiệt siêu âm (welded seam) cho dây chuyền lọc siro.</p>
        </div>
      </div>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Tài nguyên kỹ thuật",
        "Thư viện catalogue & datasheet, chứng nhận tiêu chuẩn ISO 9001:2015, SGS FDA 21 CFR, QCVN 12-1:2011/BYT và case study thực tế của Betaratio.",
        "resources.html", depth, "resources", body,
    )


# =========================================================================
# ABOUT PAGE
# =========================================================================
def about_page():
    depth = 0
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Trang chủ</a><span class="sep">/</span><span>Về Betaratio</span></div>
    <div class="eyebrow">About Betaratio</div>
    <h1>Đội ngũ kỹ thuật chuyên sâu, đồng hành cùng nhà máy của bạn</h1>
    <p class="lead">Betaratio là công ty công nghệ lọc và phân tách công nghiệp, quy tụ đội ngũ kỹ sư chuyên môn hóa cao, tập trung vào giải pháp gia công theo yêu cầu (Custom OEM/ODM) thay vì chỉ phân phối sản phẩm có sẵn.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="grid grid-2">
      <div class="card" style="padding:32px">
        <span class="ic-badge">{icon('target')}</span>
        <h3>Sứ mệnh</h3>
        <p>Mang đến giải pháp lọc &amp; phân tách vừa vặn tuyệt đối cho từng thiết bị nhà máy — giúp khách hàng nâng tầm chất lượng sản phẩm và tối ưu chi phí vận hành dài hạn.</p>
      </div>
      <div class="card" style="padding:32px">
        <span class="ic-badge">{icon('eye')}</span>
        <h3>Tầm nhìn</h3>
        <p>Trở thành đối tác kỹ thuật lọc &amp; phân tách được tin cậy hàng đầu cho các ngành công nghiệp yêu cầu khắt khe về vệ sinh, an toàn và hiệu suất tại Việt Nam.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-alt">
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Triết lý hoạt động</div>
      <h2>Điều làm nên khác biệt của Betaratio</h2>
    </div>
    <div class="grid grid-4">
      <div class="card">
        <span class="ic-badge">{icon('layers')}</span>
        <h3>Lấy giải pháp ngành làm trung tâm</h3>
        <p>Ưu tiên thấu hiểu bài toán vận hành của từng ngành trước khi đề xuất sản phẩm cụ thể.</p>
      </div>
      <div class="card">
        <span class="ic-badge">{icon('grid')}</span>
        <h3>Cấu trúc sản phẩm đa chiều</h3>
        <p>Tìm kiếm theo nhóm kỹ thuật hoặc theo chức năng lọc — tách rắn–lỏng hay tách rắn–khí.</p>
      </div>
      <div class="card">
        <span class="ic-badge">{icon('settings')}</span>
        <h3>Kỹ thuật &amp; Tùy biến (OEM)</h3>
        <p>Thế mạnh gia công may đo theo yêu cầu, khác biệt so với nhà phân phối thương mại thông thường.</p>
      </div>
      <div class="card">
        <span class="ic-badge">{icon('shield-check')}</span>
        <h3>Bảo chứng niềm tin kỹ thuật</h3>
        <p>Chứng nhận FDA, ISO, QCVN và phòng lab kiểm tra chất lượng nội bộ trước khi xuất xưởng.</p>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="section-head center">
      <div class="eyebrow">Đội ngũ</div>
      <h2>Đội ngũ sáng lập chuyên môn hóa cao</h2>
      <p>Betaratio được vận hành bởi đội ngũ kỹ sư có nền tảng chuyên sâu trong lĩnh vực vật liệu lọc, cơ khí chính xác và kiểm soát chất lượng công nghiệp — trực tiếp tham gia từ khâu tư vấn thiết kế đến giám sát sản xuất cho từng đơn hàng.</p>
    </div>
    <div class="grid grid-3">
      <div class="card text-center">
        <span class="ic-badge" style="margin:0 auto 16px">{icon('settings')}</span>
        <h3>Kỹ thuật &amp; Thiết kế</h3>
        <p>Chịu trách nhiệm dựng bản vẽ CAD 2D/3D và tư vấn cấu trúc vật liệu phù hợp với từng bài toán vận hành.</p>
      </div>
      <div class="card text-center">
        <span class="ic-badge" style="margin:0 auto 16px">{icon('flask')}</span>
        <h3>Kiểm soát chất lượng</h3>
        <p>Vận hành phòng thí nghiệm kiểm định độ thấm khí, điện trở bề mặt và cấu trúc vải trước khi xuất xưởng.</p>
      </div>
      <div class="card text-center">
        <span class="ic-badge" style="margin:0 auto 16px">{icon('users')}</span>
        <h3>Kinh doanh &amp; Tư vấn kỹ thuật</h3>
        <p>Đồng hành cùng khách hàng từ khảo sát hiện trạng thiết bị đến đề xuất giải pháp và hậu mãi.</p>
      </div>
    </div>
  </div>
</section>

<section class="section-navy">
  <div class="container">
    <div class="cta-band" style="background:transparent;padding:0">
      <div>
        <h2>Muốn tìm hiểu thêm về năng lực sản xuất của Betaratio?</h2>
        <p>Liên hệ đội ngũ kinh doanh để nhận hồ sơ năng lực, chứng chỉ và tham quan (thực tế hoặc trực tuyến) dây chuyền sản xuất.</p>
      </div>
      <a href="contact.html" class="btn btn-primary">Liên hệ Betaratio {icon('arrow-right')}</a>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Về Betaratio",
        "Betaratio — công ty công nghệ lọc và phân tách công nghiệp với đội ngũ kỹ sư chuyên môn hóa cao, tập trung vào giải pháp gia công theo yêu cầu (Custom OEM/ODM).",
        "about.html", depth, "about", body,
    )


# =========================================================================
# CONTACT / RFQ PAGE
# =========================================================================
def contact_page():
    depth = 0
    industry_options = "".join(f'<option value="{ind["slug"]}">{ind["name"]}</option>' for ind in INDUSTRIES)
    body = f"""
<section class="page-hero">
  <div class="container">
    <div class="breadcrumb"><a href="index.html">Trang chủ</a><span class="sep">/</span><span>Liên hệ &amp; Yêu cầu báo giá</span></div>
    <div class="eyebrow">Contact &amp; RFQ</div>
    <h1>Liên hệ &amp; Yêu cầu báo giá kỹ thuật</h1>
    <p class="lead">Gửi thông tin dây chuyền, bản vẽ hoặc mẫu thiết bị thực tế — đội ngũ kỹ thuật Betaratio phản hồi phương án phù hợp trong 24 giờ làm việc.</p>
  </div>
</section>

<section>
  <div class="container">
    <div class="grid grid-2" style="align-items:start; gap:40px">
      <div class="form-card">
        <h3 style="margin-bottom:6px">Gửi yêu cầu báo giá (RFQ)</h3>
        <p class="field-note" style="margin-bottom:22px">Điền càng chi tiết, đội ngũ kỹ thuật càng phản hồi nhanh và chính xác.</p>
        <form data-rfq-form action="https://formspree.io/f/maeyjzpg" method="POST">
          <input type="hidden" name="_subject" value="Yêu cầu báo giá (RFQ) — Website Betaratio">
          <div class="form-row">
            <div class="field"><label>Họ và tên *</label><input type="text" name="name" required placeholder="Nguyễn Văn A"></div>
            <div class="field"><label>Tên công ty *</label><input type="text" name="company" required placeholder="Công ty TNHH ..."></div>
          </div>
          <div class="form-row">
            <div class="field"><label>Email *</label><input type="email" name="email" required placeholder="ban@congty.com"></div>
            <div class="field"><label>Số điện thoại *</label><input type="tel" name="phone" required placeholder="09xx xxx xxx"></div>
          </div>
          <div class="form-row">
            <div class="field">
              <label>Ngành công nghiệp</label>
              <select name="industry">
                <option value="">— Chọn ngành —</option>
                {industry_options}
                <option value="other">Khác</option>
              </select>
            </div>
            <div class="field">
              <label>Nhóm sản phẩm quan tâm</label>
              <select name="product_group">
                <option value="">— Chọn nhóm sản phẩm —</option>
                <option value="cartridge">Lõi lọc / Cột lọc</option>
                <option value="bag">Túi lọc dung dịch lỏng</option>
                <option value="cloth">Vải lọc máy công nghiệp</option>
                <option value="vessel">Bình lọc chất lỏng</option>
                <option value="fluidbed">Túi sấy tầng sôi</option>
                <option value="collector">Túi lọc bụi / thu hồi bột mịn</option>
                <option value="vent">Túi thông áp bồn chứa</option>
                <option value="connector">Khớp nối mềm bằng vải</option>
                <option value="oem">Gia công theo yêu cầu (Custom OEM)</option>
              </select>
            </div>
          </div>
          <div class="field">
            <label>Mô tả yêu cầu kỹ thuật</label>
            <textarea name="message" placeholder="Mô tả thiết bị, thông số kỹ thuật, sản lượng dự kiến..."></textarea>
          </div>
          <div class="field">
            <label>Đính kèm bản vẽ / mẫu (tùy chọn)</label>
            <input type="file" name="attachment">
            <p class="field-note">Tối đa 10MB/tệp — file gửi kèm sẽ đến trực tiếp email đội ngũ kỹ thuật cùng yêu cầu báo giá.</p>
          </div>
          <button type="submit" class="btn btn-primary btn-block" data-rfq-submit>Gửi yêu cầu báo giá {icon('arrow-right')}</button>
          <p data-form-note style="display:none;margin-top:14px;padding:12px 14px;border-radius:8px;font-size:13.5px;font-weight:600"></p>
        </form>
      </div>

      <div>
        <div class="contact-info">
          <div class="info-card">
            <span class="ic">{icon('map-pin')}</span>
            <div><strong>Địa chỉ</strong><span>{ADDRESS}</span></div>
          </div>
          <div class="info-card">
            <span class="ic">{icon('phone')}</span>
            <div><strong>Điện thoại</strong><span><a href="tel:{PHONE.replace(' ', '')}">{PHONE}</a></span></div>
          </div>
          <div class="info-card">
            <span class="ic">{icon('mail')}</span>
            <div><strong>Email</strong><span><a href="mailto:{EMAIL}">{EMAIL}</a></span></div>
          </div>
          <div class="info-card">
            <span class="ic">{icon('clock')}</span>
            <div><strong>Giờ làm việc</strong><span>Thứ 2 – Thứ 7, 8:00 – 17:30</span></div>
          </div>
        </div>
        <div class="img-frame dark" style="--ar:4/3;margin-top:20px">{icon('map-pin')}<span class="cap">Bản đồ vị trí nhà máy / văn phòng — nhúng Google Maps thực tế tại đây</span></div>
      </div>
    </div>
  </div>
</section>
"""
    return PAGE(
        "Liên hệ & Yêu cầu báo giá",
        "Liên hệ Betaratio để nhận tư vấn kỹ thuật và báo giá cho giải pháp lọc & phân tách công nghiệp — phản hồi trong 24 giờ làm việc.",
        "contact.html", depth, "contact", body,
    )

# =========================================================================
# MISC STATIC FILES
# =========================================================================
def favicon_svg():
    return """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64">
<rect width="64" height="64" rx="14" fill="#0a1e30"/>
<path d="M32 14l16 16a16 16 0 1 1-32 0z" fill="#10a9a3"/>
</svg>"""


def robots_txt(sitemap_url):
    return f"""User-agent: *
Allow: /

Sitemap: {sitemap_url}
"""


def sitemap_xml(paths):
    urls = "\n".join(
        f"  <url><loc>{SITE_DOMAIN_PLACEHOLDER}/{p}</loc></url>" for p in paths
    )
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
{urls}
</urlset>
"""


def not_found_page():
    depth = 0
    body = f"""
<section class="page-hero text-center">
  <div class="container">
    <div class="eyebrow">404</div>
    <h1>Không tìm thấy trang</h1>
    <p class="lead" style="margin:0 auto">Trang bạn tìm không tồn tại hoặc đã được di chuyển. Hãy quay lại trang chủ hoặc khám phá dải sản phẩm của Betaratio.</p>
    <div class="cta-row" style="justify-content:center;margin-top:24px">
      <a href="index.html" class="btn btn-primary">Về trang chủ</a>
      <a href="products/index.html" class="btn btn-outline">Xem sản phẩm</a>
    </div>
  </div>
</section>
"""
    return PAGE("Không tìm thấy trang", "Trang không tồn tại.", "404.html", depth, "", body)


# =========================================================================
# MAIN BUILD
# =========================================================================
def main():
    write_page("index.html", home_page())
    write_page("industries.html", industries_hub_page())
    for ind in INDUSTRIES:
        write_page(f"industries/{ind['slug']}.html", industry_page(ind))
    write_page("products/index.html", products_hub_page())
    write_page("products/liquid-filtration.html", liquid_filtration_page())
    write_page("products/gas-separation.html", gas_separation_page())
    write_page("custom-oem.html", custom_oem_page())
    write_page("resources.html", resources_page())
    write_page("about.html", about_page())
    write_page("contact.html", contact_page())
    write_page("404.html", not_found_page())

    os.makedirs(os.path.join(ROOT, "images"), exist_ok=True)
    with open(os.path.join(ROOT, "images", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(favicon_svg())

    # Keep the real-photo drop folders around even on a fresh build.
    for sub in ("hero", "industries", "process", "case-studies", "products"):
        os.makedirs(os.path.join(PHOTOS_DIR, sub), exist_ok=True)

    all_paths = ["index.html", "industries.html", "products/index.html",
                 "products/liquid-filtration.html", "products/gas-separation.html",
                 "custom-oem.html", "resources.html", "about.html", "contact.html"]
    all_paths += [f"industries/{ind['slug']}.html" for ind in INDUSTRIES]

    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write(robots_txt(f"{SITE_DOMAIN_PLACEHOLDER}/sitemap.xml"))
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write(sitemap_xml(all_paths))

    print(f"\nDone. {len(all_paths) + 1} HTML pages generated.")


if __name__ == "__main__":
    main()
