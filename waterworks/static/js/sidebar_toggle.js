/**
 * waterworks Admin Panel UI interactions:
 * - Sidebar collapse/expand
 * - Profile dropdown
 * - Theme toggle (persisted in localStorage)
 * - Sidebar submenu toggle
 */

const menuToggle = document.getElementById("menu-toggle");
const sidebar = document.querySelector(".sidebar");

if (menuToggle && sidebar) {
  menuToggle.addEventListener("click", () => {
    const isMobile = window.innerWidth <= 992;

    if (isMobile) {
      sidebar.classList.toggle("open");
      document.body.classList.toggle("mobile-sidebar-active");

      // handle close on outside click
      if (sidebar.classList.contains("open")) {
        const closeOnOutside = (e) => {
          if (!sidebar.contains(e.target) && e.target !== menuToggle) {
            sidebar.classList.remove("open");
            document.body.classList.remove("mobile-sidebar-active");
            document.removeEventListener("click", closeOnOutside);
          }
        };
        document.addEventListener("click", closeOnOutside);
      }
    } else {
      sidebar.classList.toggle("collapsed");
    }
  });
}

const profileBtn = document.getElementById("profile-btn");
const dropdown = document.getElementById("profile-dropdown");

if (profileBtn && dropdown) {
  profileBtn.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdown.classList.toggle("show");
  });

  dropdown.addEventListener("click", (e) => {
    e.stopPropagation();
  });

  document.addEventListener("click", () => {
    dropdown.classList.remove("show");
  });
}

const themeBtn = document.getElementById("theme-toggle");

if (themeBtn) {
  if (localStorage.getItem("theme") === "dark") {
    document.body.classList.add("dark");
    themeBtn.textContent = "☀️";
  }

  themeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");

    if (document.body.classList.contains("dark")) {
      localStorage.setItem("theme", "dark");
      themeBtn.textContent = "☀️";
    } else {
      localStorage.setItem("theme", "light");
      themeBtn.textContent = "🌙";
    }
  });
}

// Submenu toggle
document.querySelectorAll(".has-submenu").forEach((item) => {
  const link = item.querySelector(".menu-link");
  if (!link) return;

  link.addEventListener("click", (e) => {
    e.preventDefault();
    item.classList.toggle("open");
  });
});

// Filters toggle button dropdown
const filterToggle = document.querySelector(".filter-toggle");
const installationFilterBox = document.querySelector(".installation-filters");
const replacementFilterBox = document.querySelector(".replacement-filters");

if (filterToggle) {
  filterToggle.addEventListener("click", () => {
    installationFilterBox.classList.toggle("open");
  });
}

if (filterToggle) {
  filterToggle.addEventListener("click", () => {
    replacementFilterBox.classList.toggle("open");
  });
}
