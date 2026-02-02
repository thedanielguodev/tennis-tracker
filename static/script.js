function updateUI(state) {
    document.getElementById("score").textContent = state.effectiveness;
    document.getElementById("utr").textContent = state.utr ?? "Not set";
    document.getElementById("predicted").textContent = state.predicted ?? "—";
}

document.getElementById("setUtrBtn").addEventListener("click", () => {
    const utr = parseFloat(document.getElementById("player_utr").value);
    fetch("/set_utr", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({utr})
    })
    .then(res => res.json())
    .then(updateUI);
});

document.getElementById("practiceBtn").addEventListener("click", () => {
    const minutes = parseFloat(document.getElementById("minutes").value);
    const intensity = parseFloat(document.getElementById("intensity").value);
    fetch("/practice", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({minutes, intensity})
    })
    .then(res => res.json())
    .then(updateUI);
});

document.getElementById("matchBtn").addEventListener("click", () => {
    const opponent = parseFloat(document.getElementById("opponent").value);
    const result = document.getElementById("result").value;
    fetch("/match", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({opponent, result})
    })
    .then(res => res.json())
    .then(updateUI);
});
