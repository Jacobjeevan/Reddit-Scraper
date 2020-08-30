function setProgressBar() {
  let progressbar = document.getElementById("progress-bar");
  progressbar.setAttribute("aria-valuenow", 0);
  progressbar.setAttribute("style", `width: 0%`);
  progressbar.textContent = 0 + "%";
}
