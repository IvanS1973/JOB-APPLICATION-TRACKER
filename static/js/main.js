// Confirm before any delete form is submitted
document.querySelectorAll("form[data-confirm]").forEach(function (form) {
  form.addEventListener("submit", function (event) {
    if (!window.confirm(form.dataset.confirm)) event.preventDefault();
  });
});

// Dismiss notifications (and auto-hide success messages)
document.querySelectorAll(".flash").forEach(function (flash) {
  flash.querySelector(".flash-close").addEventListener("click", function () { flash.remove(); });
  if (flash.classList.contains("flash-success")) setTimeout(function () { flash.remove(); }, 5000);
});

// Mobile menu toggle
var menuBtn = document.getElementById("menu-btn");
var sidebar = document.getElementById("sidebar");
if (menuBtn) menuBtn.addEventListener("click", function () { sidebar.classList.toggle("open"); });

// Client-side helper: warn if min salary > max salary (server validates too)
var minInput = document.getElementById("salary_min");
var maxInput = document.getElementById("salary_max");
function checkSalary() {
  if (!minInput || !maxInput) return;
  var bad = minInput.value && maxInput.value && Number(minInput.value) > Number(maxInput.value);
  maxInput.setCustomValidity(bad ? "Maximum salary must be at least the minimum salary." : "");
}
if (minInput && maxInput) { minInput.addEventListener("input", checkSalary); maxInput.addEventListener("input", checkSalary); }
