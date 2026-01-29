document.addEventListener("DOMContentLoaded", () => {
    const score = document.getElementById("score");

    document.getElementById("practiceBtn").onclick = async () => {
        const minutes = document.getElementById("minutes").value;
        const intensity = document.getElementById("intensity").value;

        const res = await fetch("/practice", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ minutes, intensity })
        });

        const data = await res.json();
        score.textContent = data.score;
    };

    document.getElementById("matchBtn").onclick = async () => {
        const opponent = document.getElementById("opponent").value;
        const result = document.getElementById("result").value;

        const res = await fetch("/match", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({ opponent, result })
        });

        const data = await res.json();
        score.textContent = data.score;
    };
});
