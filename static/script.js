async function logPractice(player_id){
    const minutes = document.getElementById(`minutes-${player_id}`).value;
    const intensity = document.getElementById(`intensity-${player_id}`).value;
    const res = await fetch('/practice', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({player_id, minutes, intensity})
    });
    const data = await res.json();
    alert(`Effectiveness: ${data.effectiveness}% (${data.label})`);
}

async function logMatch(player_id){
    const opponent_utr = document.getElementById(`opp-${player_id}`).value;
    const result = document.getElementById(`result-${player_id}`).value;
    const res = await fetch('/match', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({player_id, opponent_utr, result})
    });
    const data = await res.json();
    alert(`UTR: ${data.utr}, Effectiveness: ${data.effectiveness}% (${data.label})`);
}

async function resetEffectiveness(player_id){
    const res = await fetch('/reset', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({player_id})
    });
    const data = await res.json();
    alert(`Effectiveness reset to ${data.effectiveness}% (${data.label})`);
}
