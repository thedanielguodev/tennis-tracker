document.addEventListener("DOMContentLoaded", () => {
    const scoreEl = document.getElementById("score");

    document.getElementById("practiceBtn").addEventListener("click", () => {
        fetch("/practice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                minutes: document.getElementById("minutes").value,
                intensity: document.getElementById("intensity").value
            })
        })
        .then(res => res.json())
        .then(data => {
            scoreEl.textContent = data.score;
        });
    });

    document.getElementById("matchBtn").addEventListener("click", () => {
        fetch("/match", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                opponent: document.getElementById("opponent").value,
                result: document.getElementById("result").value
            })
        })
        .then(res => res.json())
        .then(data => {
            scoreEl.textContent = data.score;
        });
    });
});
