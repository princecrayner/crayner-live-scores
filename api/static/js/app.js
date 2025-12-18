async function loadMatches() {
  const container = document.getElementById("matches");
  container.innerHTML = '<div class="loading">Loading live matches…</div>';

  try {
    const resp = await fetch("/api/matches/");
    if (!resp.ok) throw new Error("Network error");

    const data = await resp.json();
    const list = data || [];

    if (!list.length) {
      container.innerHTML =
        '<div class="no-data">No live matches right now.</div>';
      return;
    }

    container.innerHTML = "";

    list.forEach(m => {
      const league = m.league || "Unknown League";
      const home = m.home_team || "Home";
      const away = m.away_team || "Away";
      const score = `${m.home_score ?? 0} - ${m.away_score ?? 0}`;
      const status = m.status || "";

      const card = document.createElement("div");
      card.className = "match-card";
      card.innerHTML = `
        <div class="league">${league}</div>
        <div class="teams">
          <span>${home}</span>
          <strong>${score}</strong>
          <span>${away}</span>
        </div>
        <div class="status">${status}</div>
      `;

      container.appendChild(card);
    });

  } catch (e) {
    container.innerHTML =
      '<div class="error">Could not load matches.</div>';
    console.warn(e);
  }
}

loadMatches();
setInterval(loadMatches, 30000);
