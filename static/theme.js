const toggle = document.querySelector("[data-theme-toggle]");
const bioDetails = document.querySelectorAll(".bio-detail-card");
const bioCards = document.querySelectorAll(".bio-card");
const navLinks = document.querySelectorAll(".site-nav a");

if (toggle) {
  syncThemeIcons();

  toggle.addEventListener("click", () => {
    const current = document.documentElement.dataset.theme === "dark" ? "dark" : "light";
    const next = current === "dark" ? "light" : "dark";
    document.documentElement.dataset.theme = next;
    localStorage.setItem("theme", next);
    syncThemeIcons();
  });
}

syncBioPanels();
syncBioCardHeights();
syncActiveNavLink();

function syncThemeIcons() {
  const dark = document.documentElement.dataset.theme === "dark";
  document.documentElement.classList.toggle("theme-dark", dark);
}

function syncBioPanels() {
  const collapseForMobile = window.matchMedia("(max-width: 1200px)").matches;

  bioDetails.forEach((detail) => {
    if (collapseForMobile) {
      detail.removeAttribute("open");
    } else {
      detail.setAttribute("open", "");
    }
  });
}

function syncBioCardHeights() {
  if (!bioCards.length) {
    return;
  }

  // Keep About page profile cards equal-height on desktop so the paired
  // headshot/card blocks stay aligned even when one bio metadata column grows.
  const stackForMobile = window.matchMedia("(max-width: 1200px)").matches;

  bioCards.forEach((card) => {
    card.style.minHeight = "";
  });

  if (stackForMobile) {
    return;
  }

  let maxHeight = 0;

  bioCards.forEach((card) => {
    maxHeight = Math.max(maxHeight, card.getBoundingClientRect().height);
  });

  bioCards.forEach((card) => {
    card.style.minHeight = `${Math.ceil(maxHeight)}px`;
  });
}

function syncActiveNavLink() {
  if (!navLinks.length) {
    return;
  }

  const path = window.location.pathname.endsWith("/") ? window.location.pathname : `${window.location.pathname}/`;

  navLinks.forEach((link) => {
    const href = link.getAttribute("href");
    const normalizedHref = href.endsWith("/") ? href : `${href}/`;
    const isActive = normalizedHref === path;

    if (isActive) {
      link.setAttribute("aria-current", "page");
    } else {
      link.removeAttribute("aria-current");
    }
  });
}

window.addEventListener("resize", syncBioPanels);
window.addEventListener("resize", syncBioCardHeights);
