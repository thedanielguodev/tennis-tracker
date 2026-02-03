let effectiveness = {{ effectiveness }};
let labelText = "{{ label }}";
let playerUTR = {{ utr ?? 0 }};
let predictedUTR = {{ predicted ?? 0 }};
let practiceHistory = [];
let matchHistory = [];

const effectivenessEl = document.getElementById("effectiveness");
const effectLabelEl = document.getElementById("effect-label");
const practiceList = document.getElementById("practiceHistory");
const matchList = document.getElementById("matchHistory");

function updateDisplay() {
    effectivenessEl.textContent = Math.round(effectiveness);
    effectLabelEl.textContent = labelText;

    practiceList.innerHTML = "";
    practiceHistory.forEach(p => {
        const li = document.createElement("li");
        li.textContent = `${p.date}: ${p.minutes} min @ ${p.intensity}/5`;
        practiceList.appendChild(li);
    });

    matchList.innerHTML = "";
    matchHistory.forEach(m => {
        const li = document.createElement("li");
        li.textContent = `${m.date}: vs UTR ${m.opponent} - ${m.result}`;
        matchList.appendChild(li);
    });

    effectChart.data.labels.push(new Date().toLocaleDateString());
    effectChart.data.datasets[0].data.push(effectiveness);
    effectChart.update();

    winChart.data.labels.push(new Date().toLocaleDateString());
    let wins = matchHistory.filter(m => m.result === "win").length;
    winChart.data.datasets[0].data.push(wins);
    winChart.update();
}

document.getElementById("practiceBtn").addEventListener("click", () => {
    const minutes = Number(document.getElementById("minutes").value);
    const intensity = Number(document.getElementById("intensity").value);
    if (!minutes || !intensity) return alert("Fill all fields");
    const date = new Date().toLocaleDateString();
    practiceHistory.push({minutes, intensity, date});
    effectiveness += Math.min((minutes * intensity) / 40, 12);
    effectiveness = Math.min(effectiveness, 100);
    labelText = getLabel(effectiveness);
    updateDisplay();
});

document.getElementById("matchBtn").addEventListener("click", () => {
    const opponent = Number(document.getElementById("opponentUTR").value);
    const result = document.getElementById("result").value;
    if (!opponent) return alert("Enter opponent UTR");
    const date = new Date().toLocaleDateString();
    matchHistory.push({opponent, result, date});
    effectiveness += (result === "win" ? 6 : -6);
    effectiveness = Math.min(Math.max(effectiveness, 0), 100);
    labelText = getLabel(effectiveness);
    updateDisplay();
});

document.getElementById("resetBtn").addEventListener("click", () => {
    effectiveness = 50;
    labelText = getLabel(effectiveness);
    practiceHistory = [];
    matchHistory = [];
    updateDisplay();
});

document.getElementById("setUTRBtn").addEventListener("click", () => {
    const utr = Number(document.getElementById("playerUTR").value);
    if (!utr || utr < 0 || utr > 16.5) return alert("UTR must be 0–16.5");
    playerUTR = utr;
    predictedUTR = utr;
    alert(`UTR set to ${utr}`);
});

/* EFFECTIVENESS LABELS */
function getLabel(e) {
    if (e < 30) return "Cold";
    if (e < 50) return "Average";
    if (e < 70) return "Sharp";
    if (e < 85) return "On Fire";
    return "Peak Form";
}

/* CHARTS */
const effectChartCtx = document.getElementById("effectivenessChart").getContext("2d");
const effectChart = new Chart(effectChartCtx, {
    type: "line",
    data: { labels: [], datasets: [{ label: "Effectiveness", data: [], borderColor: "#38bdf8", backgroundColor: "rgba(56, 189, 248,0.2)", tension: 0.3 }] },
    options: { responsive: true, scales: { y: { min: 0, max: 100 } } }
});

const winChartCtx = document.getElementById("winsChart").getContext("2d");
const winChart = new Chart(winChartCtx, {
    type: "bar",
    data: { labels: [], datasets: [{ label: "Cumulative Wins", data: [], backgroundColor: "#facc15" }] },
    options: { responsive: true, scales: { y: { beginAtZero: true } } }
});

updateDisplay();
