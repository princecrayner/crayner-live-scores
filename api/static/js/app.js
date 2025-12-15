async function loadMatches() {
  const container = document.getElementById('matches');
  container.innerHTML = '<div class="loading">Loading live matches…</div>';
  try {
    const resp = await fetch('/api/matches/');
    if (!resp.ok) throw new Error('Network error');
    const data = await resp.json();
    const list = data || [];
    if (!list.length) {
      container.innerHTML = '<div class="no-data">No live matches right now.</div>';
      return;
    }
    container.innerHTML = '';
    list.forEach(m => {
      const league = (m.league && m.league.name) || 'Unknown League';
      const home = m.home?.name || 'Home';
      const away = m.away?.name || 'Away';
      const homeLogo = m.home?.logo || '';
      const awayLogo = m.away?.logo || '';
      const score = `${m.home_score ?? 0} - ${m.away_score ?? 0}`;
      const status = m.status || '';

      const card = document.createElement('div');
      card.className = 'match-card';
      card.innerHTML = `
        <div style="flex:1">
          <div style="font-size:13px;color:#9aa">${league}</div>
          <div style="display:flex;gap:12px;align-items:center;margin-top:8px">
            <div class="team"><img src="${homeLogo}" onerror="this.style.display='none'"/><div>${home}</div></div>
            <div class="score">${score}<div style="font-size:12px;color:#9aa">${status}</div></div>
            <div class="team"><img src="${awayLogo}" onerror="this.style.display='none'"/><div>${away}</div></div>
          </div>
        </div>
      `;
      container.appendChild(card);
    });
  } catch (e) {
    container.innerHTML = '<div class="error">Could not load matches.</div>';
    console.warn(e);
  }
}

loadMatches();
setInterval(loadMatches, 30000); // refresh 30s
