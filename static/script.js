document.addEventListener("DOMContentLoaded", () => {
    const utrInput = document.getElementById("utr");
    const utrBtn = document.getElementById("utrBtn");
    const minutesInput = document.getElementById("minutes");
    const intensityInput = document.getElementById("intensity");
    const practiceBtn = document.getElementById("practiceBtn");
    const opponentInput = document.getElementById("opponent");
    const resultSelect = document.getElementById("result");
    const matchBtn = document.getElementById("matchBtn");
    const resetBtn = document.getElementById("resetBtn");

    const scoreEl = document.getElementById("score");
    const labelEl = document.getElementById("label");
    const predictedEl = document.getElementById("predicted");
    const practiceLogEl = document.getElementById("practiceLog");
    const matchLogEl = document.getElementById("matchLog");

    let effectivenessChart, winsChart;

    async function updateState() {
        const res = await fetch("/state");
        const data = await res.json();

        scoreEl.textContent = data.effectiveness;
        labelEl.textContent = data.label;
        predictedEl.textContent = data.predicted ? `Predicted UTR: ${data.predicted}` : "-";

        // Practice log
        practiceLogEl.innerHTML = "";
        data.practice_log.forEach(p => {
            const li = document.createElement("li");
            li.textContent = `${p.date} - ${p.minutes} min, Intensity ${p.intensity}`;
            practiceLogEl.appendChild(li);
        });

        // Match log
        matchLogEl.innerHTML = "";
        data.match_log.forEach(m => {
            const li = document.createElement("li");
            li.textContent = `${m.date} - Opponent ${m.opponent}, Result: ${m.result}`;
            matchLogEl.appendChild(li);
        });

        // Charts
        const effData = data.practice_log.map(p => p.intensity * p.minutes);
        const effLabels = data.practice_log.map(p => p.date);

        if (effectivenessChart) effectivenessChart.destroy();
        effectivenessChart = new Chart(document.getElementById("effectivenessChart"), {
            type: 'line',
            data: { labels: effLabels, datasets: [{ label: 'Practice Impact', data: effData, borderColor: '#38bdf8', backgroundColor: 'rgba(56, 189, 248,0.2)', fill:true }]},
            options: { responsive: true, plugins: { legend: { display: false }}}
        });

        const winsData = data.match_log.map(m => m.result === "win" ? 1 : 0);
        const winsLabels = data.match_log.map(m => m.date);

        if (winsChart) winsChart.destroy();
        winsChart = new Chart(document.getElementById("winsChart"), {
            type: 'bar',
            data: { labels: winsLabels, datasets: [{ label: 'Wins', data: winsData, backgroundColor: '#0ea5e9' }]},
            options: { responsive: true, scales: { y: { beginAtZero: true, max: 1, ticks: { stepSize: 1 }}}}
        });
    }

    utrBtn.addEventListener("click", async () => {
        await fetch("/set_utr", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ utr: utrInput.value })});
        updateState();
    });

    practiceBtn.addEventListener("click", async () => {
        await fetch("/practice", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ minutes: minutesInput.value, intensity: intensityInput.value })});
        updateState();
    });

    matchBtn.addEventListener("click", async () => {
        await fetch("/match", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ opponent: opponentInput.value, result: resultSelect.value })});
        updateState();
    });

    resetBtn.addEventListener("click", async () => {
        await fetch("/reset", { method: "POST" });
        updateState();
    });

    updateState();
});
