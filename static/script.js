let state = {
    utr: null,
    predicted: null,
    effectiveness: 50,
    matches: [],
    effectivenessHistory: []
};

// Update UI
function updateUI() {
    document.getElementById("score").textContent = state.effectiveness;
    document.getElementById("utr").textContent = state.utr ?? "-";
    document.getElementById("predicted").textContent = state.predicted ?? "-";

    // Update charts
    updateWinLossChart();
    updateEffectivenessChart();
}

// Set player UTR
document.getElementById("setUTRBtn").onclick = () => {
    let utr = parseFloat(document.getElementById("setUTR").value);
    if (isNaN(utr)) return;
    fetch("/set_utr", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ utr })
    }).then(res => res.json()).then(data => {
        state = data;
        updateUI();
    });
};

// Log practice
document.getElementById("practiceBtn").onclick = () => {
    let minutes = parseFloat(document.getElementById("minutes").value);
    let intensity = parseFloat(document.getElementById("intensity").value);
    fetch("/practice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ minutes, intensity })
    }).then(res => res.json()).then(data => {
        state = data;
        state.effectivenessHistory.push(state.effectiveness);
        updateUI();
    });
};

// Log match
document.getElementById("matchBtn").onclick = () => {
    let opponent = parseFloat(document.getElementById("opponent").value);
    let result = document.getElementById("result").value;
    let date = document.getElementById("matchDate").value || new Date().toISOString().split("T")[0];
    fetch("/match", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ opponent, result })
    }).then(res => res.json()).then(data => {
        state = data;
        state.matches.push({ date, result });
        state.effectivenessHistory.push(state.effectiveness);
        updateUI();
    });
};

// Reset all
document.getElementById("resetBtn").onclick = () => {
    state = { utr: null, predicted: null, effectiveness: 50, matches: [], effectivenessHistory: [] };
    updateUI();
};

// Charts
let winLossChart, effectivenessChart;
function updateWinLossChart() {
    const ctx = document.getElementById("winLossChart").getContext("2d");
    const labels = state.matches.map(m => m.date);
    const wins = state.matches.map(m => m.result === "win" ? 1 : 0);
    const losses = state.matches.map(m => m.result === "loss" ? 1 : 0);
    if (winLossChart) winLossChart.destroy();
    winLossChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels,
            datasets: [
                { label: "Wins", data: wins, backgroundColor: "#22c55e" },
                { label: "Losses", data: losses, backgroundColor: "#ef4444" }
            ]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true } } }
    });
}

function updateEffectivenessChart() {
    const ctx = document.getElementById("effectivenessChart").getContext("2d");
    const labels = state.effectivenessHistory.map((_, i) => `Session ${i+1}`);
    if (effectivenessChart) effectivenessChart.destroy();
    effectivenessChart = new Chart(ctx, {
        type: "line",
        data: {
            labels,
            datasets: [{ label: "Effectiveness", data: state.effectivenessHistory, borderColor: "#38bdf8", fill: false }]
        },
        options: { responsive: true, scales: { y: { beginAtZero: true, max: 100 } } }
    });
}

// Initial UI
updateUI();
