document.addEventListener("DOMContentLoaded", () => {
  const logButton = document.getElementById("logButton");
  const minutesInput = document.getElementById("minutesInput");
  const totalMinutes = document.getElementById("totalMinutes");

  logButton.addEventListener("click", async () => {
    const minutes = parseInt(minutesInput.value);

    if (isNaN(minutes) || minutes <= 0) return;

    const response = await fetch("/log", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ minutes })
    });

    const data = await response.json();
    totalMinutes.textContent = data.total_minutes;
    minutesInput.value = "";
  });
});
