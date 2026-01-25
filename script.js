let practices = JSON.parse(localStorage.getItem("practices")) || []
let matches = JSON.parse(localStorage.getItem("matches")) || []

const save = () => {
  localStorage.setItem("practices", JSON.stringify(practices))
  localStorage.setItem("matches", JSON.stringify(matches))
}

const updateStats = () => {
  const totalMinutes = practices.reduce((sum, p) => sum + p.minutes, 0)
  document.getElementById("total-minutes").textContent =
    "Total Minutes: " + totalMinutes

  const wins = matches.filter(m => m.result === "Win").length
  const winRate = matches.length
    ? Math.round((wins / matches.length) * 100)
    : 0

  document.getElementById("win-rate").textContent =
    "Win Rate: " + winRate + "%"
}

document.getElementById("add-practice").onclick = () => {
  if (!p-date.value || !p-minutes.value) return

  practices.push({
    date: p-date.value,
    minutes: Number(p-minutes.value),
    type: p-type.value
  })

  save()
  updateStats()
}

document.getElementById("add-match").onclick = () => {
  if (!m-date.value || !m-score.value) return

  matches.push({
    date: m-date.value,
    score: m-score.value,
    result: m-result.value
  })

  save()
  updateStats()
}

updateStats()
