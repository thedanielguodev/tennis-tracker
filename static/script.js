async function postData(url = '', data = {}) {
    const res = await fetch(url, {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    return res.json();
}

function updateUI(state){
    document.getElementById('score').innerText = state.effectiveness;
    document.querySelector('.score-box .label').innerText = state.label;
    renderCharts(state);
}

document.getElementById('practiceBtn').onclick = async () => {
    const minutes = parseFloat(document.getElementById('minutes').value);
    const intensity = parseFloat(document.getElementById('intensity').value);
    const state = await postData('/practice', {minutes, intensity});
    updateUI(state);
};

document.getElementById('matchBtn').onclick = async () => {
    const opponent = parseFloat(document.getElementById('opponent').value);
    const result = document.getElementById('result').value;
    const state = await postData('/match', {opponent, result});
    updateUI(state);
};

document.getElementById('resetBtn').onclick = async () => {
    const state = await postData('/reset', {});
    updateUI(state);
};

function renderCharts(state){
    const effCtx = document.getElementById('effChart').getContext('2d');
    const wlCtx = document.getElementById('wlChart').getContext('2d');

    const labels = Object.keys(state.daily_effectiveness).sort();
    const effData = labels.map(d => state.daily_effectiveness[d]);

    new Chart(effCtx, {
        type: 'line',
        data: { labels, datasets: [{label: 'Effectiveness', data: effData, borderColor:'#38bdf8', fill:false}] },
        options: { responsive:true }
    });

    const winCount = state.match_log.filter(m => m[2]=='win').length;
    const lossCount = state.match_log.filter(m => m[2]=='loss').length;

    new Chart(wlCtx, {
        type:'bar',
        data: { labels:['Wins','Losses'], datasets:[{label:'Matches', data:[winCount, lossCount], backgroundColor:['#22c55e','#ef4444']}] },
        options:{responsive:true}
    });
}
