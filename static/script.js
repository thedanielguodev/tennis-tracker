document.addEventListener("DOMContentLoaded", () => {
    const logButton = document.getElementById("logButton");
    const minutesInput = document.getElementById("minutesInput");
    const weeklyMinutes = document.getElementById("weeklyMinutes");

    logButton.addEventListener("click", async () => {
        const minutes = parseInt(minutesInput.value);
        if (!minutes || minutes <= 0) return;

        const response = await fetch("/log_practice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ duration: minutes })
        });

        const data = await response.json();
        weeklyMinutes.textContent = data.weekly_total;
        minutesInput.value = "";
    });
});
