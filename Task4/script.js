document.addEventListener("DOMContentLoaded", function () {
  var menuButton = document.getElementById("hamburgerButton");
  var menuDropdown = document.getElementById("menuDropdown");
  var closeButton = document.getElementById("closeButton");

  menuButton.addEventListener("click", function () {
    menuDropdown.classList.toggle("show");
  });

  closeButton.addEventListener("click", function () {
    menuDropdown.classList.remove("show");
  });
});
