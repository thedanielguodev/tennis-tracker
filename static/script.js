document.addEventListener("DOMContentLoaded", () => {
    const score = document.getElementById("score");

    document.getElementById("logPractice").onclick = async () => {
        const minutes = parseInt(document.getElementById("practiceMinutes").value);
        const intensity = parseInt(document.getElementById("practiceIntensity").value);

        if (!minutes || !intensity) return;

        const res = await fetch("/log_practice", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ minutes, intensity })
        });

        const data = await res.json();
        score.textContent = data.effectiveness;
    };

    document.getElementById("logMatch").onclick = async () => {
        const opponent = parseInt(document.getElementById("opponentLevel").value);
        const result = document.getElementById("matchResult").value;

        if (!opponent) return;

        const res = await fetch("/log_match", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ opponent, result })
        });

        const data = await res.json();
        score.textContent = data.effectiveness;
    };
});
