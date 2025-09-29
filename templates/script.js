// Sidebar toggle
const sidebar = document.getElementById("sidebar");
document.getElementById("toggleSidebar").addEventListener("click", () => {
  sidebar.classList.toggle("collapsed");
});

// Dark/light toggle
const themeToggle = document.getElementById("themeToggle");
themeToggle.addEventListener("click", () => {
  document.body.classList.toggle("dark");
});

// Insert options toggle
const insertButton = document.getElementById("insert-button");
const optionsMenu = document.getElementById("insert-options-menu");
insertButton.addEventListener("click", () => {
  optionsMenu.classList.toggle("hidden");
});
document.addEventListener("click", (e) => {
  if (!e.target.closest(".insert-options-wrapper")) {
    optionsMenu.classList.add("hidden");
  }
});

// Typing indicator demo
const typingIndicator = document.getElementById("typingIndicator");
typingIndicator.style.display = "flex"; // Show typing animation
setTimeout(() => {
  typingIndicator.style.display = "none"; // Hide after few seconds
}, 4000);
