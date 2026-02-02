let state = {
    effectivenessHistory: [],
    matchHistory: []
};

function updateState(data) {
    document.getElementById("score").textContent = data.effectiveness;
    document.getElementById("effectivenessLabel").textContent = data.label;
    document.getElementById("utrDisplay").textContent = data.utr !== null ? data.utr : "-";
    document.getElementById("predicted").textContent = data.predicted !== null ? data.predicted : "-";

    // Add to history
    state.effectivenessHistory.push({date: new Date().toLocaleDateString(), value: data.effectiveness});
    renderCharts();
}

function postJSON(url, body) {
    return fetch(url, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(body)
    }).then(res => res.json());
}

// Set UTR
document.getElementById("setUtrBtn").addEventListener("click", () => {
    const utr = parseFloat(document.getElementById("utrInput").value);
    postJSON("/set_utr", {utr}).then(updateState);
});

// Log practice
document.getElementById("practiceBtn").addEventListener("click", () => {
    const minutes = parseFloat(document.getElementById("minutes").value);
    const intensity = parseFloat(document.getElementById("intensity").value);
    postJSON("/practice", {minutes, intensity}).then(updateState);
});

// Log match
document.getElementById("matchBtn").addEventListener("click", () => {
    const opponent = parseFloat(document.getElementById("opponent").value);
    const result = document.getElementById("result").value;
    postJSON("/match", {opponent, result}).then(data => {
        state.matchHistory.push({date: new Date().toLocaleDateString(), win: result === "win" ? 1 : 0});
        updateState(data);
    });
});

// Reset
document.getElementById("resetBtn").addEventListener("click", () => {
    location.reload();
});

// Charts
let effChart, matchChart;

function renderCharts() {
    const dates = state.effectivenessHistory.map(e => e.date);
    const effValues = state.effectivenessHistory.map(e => e.value);

    const wins = state.matchHistory.map((m,i) => m.win);
    const matchDates = state.matchHistory.map(m => m.date);

    if (!effChart) {
        const ctx = document.getElementById("effectivenessChart").getContext("2d");
        effChart = new Chart(ctx, {
            type: "line",
            data: {labels: dates, datasets: [{label: "Effectiveness", data: effValues, borderColor: "#38bdf8", fill: false}]},
            options: {responsive:true, scales:{y:{min:0, max:100}}}
        });
    } else {
        effChart.data.labels = dates;
        effChart.data.datasets[0].data = effValues;
        effChart.update();
    }

    if (!matchChart) {
        const ctx2 = document.getElementById("matchChart").getContext("2d");
        matchChart = new Chart(ctx2, {
            type: "bar",
            data: {labels: matchDates, datasets: [{label:"Wins", data:wins, backgroundColor:"#0ea5e9"}]},
            options:{responsive:true, scales:{y:{min:0,max:1}}}
        });
    } else {
        matchChart.data.labels = matchDates;
        matchChart.data.datasets[0].data = wins;
        matchChart.update();
    }
}
