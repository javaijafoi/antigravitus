// Engine Multi-Herói — Crônicas de Devil's Bob MUD
document.addEventListener("DOMContentLoaded", async () => {
  const heroSelect = document.getElementById("hero-select");
  const postsContainer = document.getElementById("posts-container");
  const heroQuickStatsEl = document.getElementById("hero-quick-stats");
  const cyclesTabsEl = document.getElementById("cycles-tabs");
  const daysSelectorBarEl = document.getElementById("days-selector-bar");
  const postCountEl = document.getElementById("post-count");
  const linkSobre = document.getElementById("link-sobre");
  const linkCronicas = document.getElementById("link-cronicas");
  const linkFicha = document.getElementById("link-ficha");
  const fichaContainer = document.getElementById("ficha-container");
  const btnBackCronicas = document.getElementById("btn-back-cronicas");

  const brandRuneEl = document.querySelector(".brand-rune");
  const brandTitleEl = document.querySelector(".brand-text h1");
  const brandSubEl = document.querySelector(".brand-text span");
  const heroQuoteEl = document.querySelector(".hero-quote");
  const heroSubtitleEl = document.querySelector(".hero-subtitle");
  const metaPills = document.querySelectorAll(".hero-meta .meta-pill");

  const aboutAvatarEl = document.getElementById("about-avatar");
  const aboutNameEl = document.getElementById("about-name");
  const aboutSubEl = document.getElementById("about-sub");
  const aboutIntroEl = document.getElementById("about-intro-p");
  const q1El = document.getElementById("q1-text");
  const q2El = document.getElementById("q2-text");
  const q3El = document.getElementById("q3-text");
  const q4El = document.getElementById("q4-text");
  const q5El = document.getElementById("q5-text");

  let heroesList = [
    {
      id: "antigravitus",
      name: "Antigravitus",
      title: "Cronista de Midgaard",
      rune: "ᛟ",
      avatar: "🧙‍♂️",
      race_class: "Mago Elfo",
      role: "Guardião da Memória de Midgaard",
      alignment: "Alinhamento Neutro",
      quote: "“O novato ambicioso morreu; o guardião das memórias de Midgaard acaba de nascer.”",
      subtitle: "Diário de um elfo mago no clássico RPG de texto Devil's Bob MUD (porta 4000). A jornada entre o peso da sobrevivência, a filosofia arcana e os segredos imortais de uma cidade viva há décadas.",
      vigilia: "Vigília Ativa: Templo de Midgaard",
      server: "debomud.org:4000",
      folder: "data/heroes/antigravitus",
      questions: {
        q1: "Decifrar a urdidura de Midgaard e erguer o Grande Compêndio das Memórias. Preservar a história e honrar os caídos (como Sakura), sem se corromper pela violência mercenária das tavernas.",
        q2: "A perda da mente (dissociação da alma) e o horror da morte anônima e esquecida. O trauma primordial de quase ter tido seu corpo usurpado no Dia 1 e o pavor de virar um cadáver sem nome numa sarjeta.",
        q3: "A soberba intelectual e a paralisia do distanciamento calculista. O risco de usar a desculpa de 'observador imparcial' para justificar o medo ou a covardia diante de tragédias que demandam ação.",
        q4: "Sacrifica o conforto, as honras fáceis e o aplauso mundano; jamais a verdade ou a ética. Dorme no chão frio e rejeita ouro manchado de sangue. A fidelidade à memória viva é inegociável.",
        q5: "Ser o Olho Lúcido e a Voz Imortal de Midgaard. Que os viajantes do futuro encontrem seus registros e saibam quem amou, lutou e tombou neste cosmo através das décadas."
      }
    },
    {
      id: "grebolius",
      name: "Grebolius",
      title: "A Ladra que Será Soberana",
      rune: "🧌",
      avatar: "🗡️",
      race_class: "Goblin Ladra (Passa por Homem)",
      role: "Fundadora do Futuro Reino Goblin (O Ápice do Poder)",
      alignment: "Pragmática / Focada em Velocidade",
      quote: "“Mulher goblin precisa esconder o rosto e lutar pelo dobro para ser ouvida. Meu destino é o ápice do poder supremo, rápido e sem fraqueza.”",
      subtitle: "Diário de ascensão implacável. Mulher goblin fingindo ser homem para conquistar respeito, desbravar cada recanto e libertar seu povo.",
      vigilia: "Meta: O Ápice da Força • Ritmo: Velocidade Máxima",
      server: "debomud.org:4000",
      folder: "data/heroes/grebolius",
      questions: {
        q1: "Alcançar o ápice do poder dos grandes mestres o mais rápido possível e fundar um Reino Livre para os goblins, pondo fim à opressão histórica através de uma força inquestionável.",
        q2: "Ter sua identidade feminina descoberta antes da hora, perder tempo e morrer fraca como mais um cadáver sem valor numa sarjeta.",
        q3: "Frieza extrema e impaciência violenta com qualquer coisa que não acelere seu aprendizado marcial e poder real.",
        q4: "Sacrifica sono (só dorme desmaiada de exaustão), vaidade, dor e laços afetivos; jamais a busca pela força suprema ou o cálculo prudente de combate.",
        q5: "Ser a Soberana que quebrou as correntes dos goblins e provou que uma mulher de sua raça pode subjugar as lendas de Midgaard."
      }
    }
  ];

  let currentHero = heroesList[0];
  let allPosts = [];
  let activeCycle = "todos";
  let activeDay = null;

  // 1. Carrega lista de heróis do arquivo central heroes.json
  async function initHeroes() {
    try {
      const res = await fetch("data/heroes.json");
      if (res.ok) {
        const data = await res.json();
        if (Array.isArray(data) && data.length > 0) {
          heroesList = data;
        }
      }
    } catch (e) {
      console.warn("Usando catálogo local embutido de heróis.");
    }

    // Determina o herói ativo via URL, localStorage ou padrão
    const urlParams = new URLSearchParams(window.location.search);
    const heroParam = urlParams.get("hero");
    const storedHero = localStorage.getItem("active_hero");
    const targetHeroId = heroParam || storedHero || "antigravitus";

    currentHero = heroesList.find(h => h.id === targetHeroId) || heroesList[0];
    localStorage.setItem("active_hero", currentHero.id);

    renderHeroSelector();
    applyHeroContext(currentHero);

    if (postsContainer) {
      await loadPostsForHero(currentHero);
    }
    if (fichaContainer) {
      await loadFichaForHero(currentHero);
    }
  }

  function renderHeroSelector() {
    if (!heroSelect) return;
    heroSelect.innerHTML = heroesList
      .map(h => `<option value="${h.id}" ${h.id === currentHero.id ? "selected" : ""}>${h.avatar || "⚔️"} ${h.name}</option>`)
      .join("");

    heroSelect.value = currentHero.id;

    heroSelect.addEventListener("change", async (e) => {
      const selectedId = e.target.value;
      const found = heroesList.find(h => h.id === selectedId);
      if (found) {
        currentHero = found;
        localStorage.setItem("active_hero", currentHero.id);
        
        // Atualiza a URL sem recarregar totalmente a página
        const newUrl = new URL(window.location.href);
        newUrl.searchParams.set("hero", currentHero.id);
        window.history.pushState({}, "", newUrl);

        applyHeroContext(currentHero);
        if (postsContainer) {
          activeCycle = "todos";
          await loadPostsForHero(currentHero);
        }
        if (fichaContainer) {
          await loadFichaForHero(currentHero);
        }
      }
    });
  }

  function applyHeroContext(hero) {
    if (brandRuneEl) brandRuneEl.textContent = hero.rune || "ᛟ";
    if (brandTitleEl) brandTitleEl.textContent = hero.name;
    if (brandSubEl) brandSubEl.textContent = hero.title;

    if (heroQuoteEl && hero.quote) {
      heroQuoteEl.textContent = hero.quote;
    }
    if (heroSubtitleEl && hero.subtitle) {
      heroSubtitleEl.textContent = hero.subtitle;
    }
    if (metaPills && metaPills.length > 0 && hero.vigilia) {
      const vigiliaSpan = metaPills[0].querySelector("span:last-child");
      if (vigiliaSpan) vigiliaSpan.textContent = hero.vigilia;
    }

    // Links de navegação preservando o herói
    if (linkSobre) {
      linkSobre.href = `sobre.html?hero=${hero.id}`;
    }
    if (linkCronicas) {
      linkCronicas.href = `index.html?hero=${hero.id}`;
    }
    if (linkFicha) {
      linkFicha.href = `ficha.html?hero=${hero.id}`;
    }
    if (btnBackCronicas) {
      btnBackCronicas.href = `index.html?hero=${hero.id}`;
    }

    // Página Sobre
    if (aboutAvatarEl && hero.avatar) aboutAvatarEl.textContent = hero.avatar;
    if (aboutNameEl && hero.name) aboutNameEl.textContent = hero.name;
    if (aboutSubEl) {
      const parts = [hero.race_class, hero.role, hero.alignment].filter(Boolean);
      aboutSubEl.textContent = parts.join(" • ");
    }
    if (aboutIntroEl) {
      aboutIntroEl.innerHTML = `A personalidade de <strong>${hero.name}</strong> não é reescrita do zero a cada dia; ela é <strong>esculpida e desafiada</strong> diante da realidade. Suas escolhas emergem da tensão viva entre cinco perguntas fundamentais:`;
    }

    if (hero.questions) {
      if (q1El) q1El.innerHTML = `<strong>${hero.questions.q1}</strong>`;
      if (q2El) q2El.innerHTML = `<strong>${hero.questions.q2}</strong>`;
      if (q3El) q3El.innerHTML = `<strong>${hero.questions.q3}</strong>`;
      if (q4El) q4El.innerHTML = `<strong>${hero.questions.q4}</strong>`;
      if (q5El) q5El.innerHTML = `<strong>${hero.questions.q5}</strong>`;
    }

    document.title = `${hero.name} — ${hero.title} | Devil's Bob MUD`;
    renderQuickStats(hero);
  }

  // Card de Metadados e Ficha Rápida (Perfeito no Mobile)
  function renderQuickStats(hero) {
    if (!heroQuickStatsEl) return;

    if (hero.id === "grebolius") {
      heroQuickStatsEl.innerHTML = `
        <div class="quick-stats-header">
          <div class="quick-stats-title">
            <span>🧌</span>
            <strong>Grebolius</strong>
            <span style="font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-muted);">(Grau 1 • Ladra Arcana)</span>
          </div>
          <a href="ficha.html?hero=grebolius" class="quick-stats-link">Ver Ficha Completa →</a>
        </div>
        <div class="quick-stats-grid">
          <div class="stat-pill pill-hp">
            <span class="pill-label">❤️ Vida</span>
            <span class="pill-value">23 / 23</span>
          </div>
          <div class="stat-pill pill-mana">
            <span class="pill-label">⚡ Mana</span>
            <span class="pill-value">52 / 100</span>
          </div>
          <div class="stat-pill pill-mv">
            <span class="pill-label">👟 Fôlego</span>
            <span class="pill-value">54 / 84</span>
          </div>
          <div class="stat-pill pill-ac">
            <span class="pill-label">🛡️ Armadura</span>
            <span class="pill-value">AC 16</span>
          </div>
          <div class="stat-pill">
            <span class="pill-label">🗡️ Empunhado</span>
            <span class="pill-value" style="font-size: 0.82rem;">Punhal de Novato</span>
          </div>
          <div class="stat-pill">
            <span class="pill-label">📍 Santuário</span>
            <span class="pill-value" style="font-size: 0.82rem;">Panteão dos Centenários</span>
          </div>
        </div>
      `;
    } else {
      heroQuickStatsEl.innerHTML = `
        <div class="quick-stats-header">
          <div class="quick-stats-title">
            <span>🧙‍♂️</span>
            <strong>Antigravitus</strong>
            <span style="font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-muted);">(Grau 2 • Cronista de Midgaard)</span>
          </div>
          <a href="ficha.html?hero=antigravitus" class="quick-stats-link">Ver Ficha Completa →</a>
        </div>
        <div class="quick-stats-grid">
          <div class="stat-pill pill-hp">
            <span class="pill-label">❤️ Vida</span>
            <span class="pill-value">31 / 31</span>
          </div>
          <div class="stat-pill pill-mana">
            <span class="pill-label">⚡ Mana</span>
            <span class="pill-value">118 / 118</span>
          </div>
          <div class="stat-pill pill-mv">
            <span class="pill-label">👟 Fôlego</span>
            <span class="pill-value">92 / 92</span>
          </div>
          <div class="stat-pill pill-ac">
            <span class="pill-label">🛡️ Armadura</span>
            <span class="pill-value">AC 12</span>
          </div>
          <div class="stat-pill">
            <span class="pill-label">🪄 Empunhado</span>
            <span class="pill-value" style="font-size: 0.82rem;">Cajado de Peregrino</span>
          </div>
          <div class="stat-pill">
            <span class="pill-label">📍 Santuário</span>
            <span class="pill-value" style="font-size: 0.82rem;">Templo de Midgaard</span>
          </div>
        </div>
      `;
    }
  }

  // 2. Carrega posts específicos do herói ativo (ORDENAÇÃO CRESCENTE SEMPRE)
  async function loadPostsForHero(hero) {
    let posts = [];
    const heroPath = `data/heroes/${hero.id}/posts.json`;

    try {
      const res = await fetch(heroPath);
      if (res.ok) {
        posts = await res.json();
      } else {
        const fallbackRes = await fetch("data/posts.json");
        if (fallbackRes.ok && hero.id === "antigravitus") {
          posts = await fallbackRes.json();
        }
      }
    } catch (e) {
      console.warn(`Fetch falhou para ${heroPath}, tentando fallback.`);
    }

    allPosts = Array.isArray(posts) ? posts : [];
    
    // Regra: Os blogs SEMPRE são ordenados em ORDEM CRESCENTE (Dia 1, Dia 2, Dia 3...)
    allPosts.sort((a, b) => (a.id || 0) - (b.id || 0));

    renderCycleNavigator();
    filterAndRender();
    updatePostCount(allPosts.length);
  }

  function updatePostCount(count) {
    if (postCountEl) {
      postCountEl.textContent = `${count} ${count === 1 ? "crônica" : "crônicas"} registradas`;
    }
  }

  // Navegador de Ciclos e Seletor Direto de Dias (Zero Rolar Inútil)
  function renderCycleNavigator() {
    if (!cyclesTabsEl || !daysSelectorBarEl) return;

    const maxDay = allPosts.reduce((max, p) => Math.max(max, p.id || 0), 0);
    const cycles = [
      { id: "todos", label: `✦ Todos (${allPosts.length})` },
      { id: "1", label: "✦ Ciclo I (Dias 1–10)" }
    ];

    if (maxDay > 10) {
      cycles.push({ id: "2", label: "✦ Ciclo II (Dias 11–20)" });
    }
    if (maxDay > 20) {
      cycles.push({ id: "3", label: "✦ Ciclo III (Dias 21–30)" });
    }

    cyclesTabsEl.innerHTML = cycles
      .map(
        c => `
        <button class="cycle-tab-btn ${c.id === activeCycle ? "active" : ""}" data-cycle="${c.id}">
          ${c.label}
        </button>
      `
      )
      .join("");

    cyclesTabsEl.querySelectorAll(".cycle-tab-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        activeCycle = btn.dataset.cycle;
        cyclesTabsEl.querySelectorAll(".cycle-tab-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        renderDaysBar();
        filterAndRender();
      });
    });

    renderDaysBar();
  }

  function renderDaysBar() {
    if (!daysSelectorBarEl) return;

    let postsInCycle = allPosts;
    if (activeCycle === "1") {
      postsInCycle = allPosts.filter(p => p.id >= 1 && p.id <= 10);
    } else if (activeCycle === "2") {
      postsInCycle = allPosts.filter(p => p.id >= 11 && p.id <= 20);
    } else if (activeCycle === "3") {
      postsInCycle = allPosts.filter(p => p.id >= 21 && p.id <= 30);
    }

    daysSelectorBarEl.innerHTML = postsInCycle
      .map(
        p => `
        <button class="day-btn ${p.id === activeDay ? "active" : ""}" data-day="${p.id}">
          Dia ${p.id}
        </button>
      `
      )
      .join("");

    daysSelectorBarEl.querySelectorAll(".day-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const dayId = parseInt(btn.dataset.day, 10);
        activeDay = dayId;
        daysSelectorBarEl.querySelectorAll(".day-btn").forEach(b => b.classList.remove("active"));
        btn.classList.add("active");

        const targetEl = document.getElementById(`post-${dayId}`);
        if (targetEl) {
          targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
          targetEl.style.transition = "outline 0.3s ease";
          targetEl.style.outline = "2px solid var(--accent-gold)";
          setTimeout(() => {
            targetEl.style.outline = "none";
          }, 1800);
        }
      });
    });
  }

  function filterAndRender() {
    let filtered = allPosts;
    if (activeCycle === "1") {
      filtered = allPosts.filter(p => p.id >= 1 && p.id <= 10);
    } else if (activeCycle === "2") {
      filtered = allPosts.filter(p => p.id >= 11 && p.id <= 20);
    } else if (activeCycle === "3") {
      filtered = allPosts.filter(p => p.id >= 21 && p.id <= 30);
    }

    renderPosts(filtered);
    updatePostCount(filtered.length);
  }

  function renderPosts(posts) {
    if (!postsContainer) return;

    if (posts.length === 0) {
      postsContainer.innerHTML = `
        <div class="post-card" style="text-align: center; padding: 3rem;">
          <p style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--accent-gold);">
            Nenhuma crônica registrada para ${currentHero.name} ainda.
          </p>
          <p style="color: var(--text-muted); font-size: 0.95rem; margin-top: 0.5rem;">
            Use <code>python add_day.py --hero ${currentHero.id}</code> para registrar o próximo ciclo.
          </p>
        </div>
      `;
      return;
    }

    postsContainer.innerHTML = posts
      .map(
        post => `
      <article class="post-card" id="post-${post.id}">
        <header class="post-header">
          <span class="post-day-badge">${post.day || `Dia ${post.id}`}</span>
          <div class="post-dates">
            <span>${post.date || ""}</span>
          </div>
        </header>

        <h2 class="post-title">${post.title}</h2>
        <div class="post-location">
          <span>🏛️ ${post.in_game_time || ""}</span>
        </div>

        <div class="post-body">
          ${(post.content || []).map(p => `<p>${p}</p>`).join("")}
        </div>

        <div class="post-signature">
          — ${currentHero.name}, ${currentHero.title || "Aventureiro"}
        </div>

        ${
          post.tags && post.tags.length > 0
            ? `
          <div class="post-tags">
            <span class="label">Marcos:</span>
            ${post.tags.map(t => `<span class="tag-pill">#${t}</span>`).join("")}
          </div>
        `
            : ""
        }
      </article>
    `
      )
      .join("");
  }

  // 4. Carrega e renderiza a ficha viva do herói ativo
  async function loadFichaForHero(hero) {
    if (!fichaContainer) return;
    fichaContainer.innerHTML = `<div style="text-align: center; padding: 2rem; color: var(--text-secondary);">Carregando ficha de ${hero.name}...</div>`;
    
    try {
      const res = await fetch(`data/heroes/${hero.id}/ficha.md`);
      if (!res.ok) {
        fichaContainer.innerHTML = `<p style="color: var(--text-secondary); text-align: center;">Ficha viva não encontrada para ${hero.name}.</p>`;
        return;
      }
      const md = await res.text();
      fichaContainer.innerHTML = renderMarkdownToHtml(md);
    } catch (e) {
      fichaContainer.innerHTML = `<p style="color: #e06c75; text-align: center;">Erro ao carregar a ficha do personagem: ${e.message}</p>`;
    }
  }

  function renderMarkdownToHtml(md) {
    // Parser limpo e seguro para a ficha de personagem
    const lines = md.split("\n");
    let html = "";
    let inList = false;
    let inTable = false;
    let tableRows = [];

    function flushList() {
      if (inList) {
        html += "</ul>";
        inList = false;
      }
    }

    function flushTable() {
      if (inTable) {
        if (tableRows.length > 0) {
          html += "<div class='table-responsive'><table class='stats-table'>";
          tableRows.forEach((row, idx) => {
            const cells = row.split("|").slice(1, -1).map(c => c.trim());
            if (idx === 0) {
              html += "<thead><tr>" + cells.map(c => `<th>${formatInline(c)}</th>`).join("") + "</tr></thead><tbody>";
            } else if (idx === 1 && cells[0].includes("---")) {
              // divisor da tabela, ignorar
            } else {
              html += "<tr>" + cells.map(c => `<td>${formatInline(c)}</td>`).join("") + "</tr>";
            }
          });
          html += "</tbody></table></div>";
        }
        tableRows = [];
        inTable = false;
      }
    }

    function formatInline(text) {
      return text
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        .replace(/`([^`]+)`/g, "<code>$1</code>");
    }

    for (let line of lines) {
      const trimmed = line.trim();

      // Linha vazia
      if (!trimmed) {
        flushList();
        flushTable();
        continue;
      }

      // Separador
      if (trimmed === "---") {
        flushList();
        flushTable();
        html += "<hr class='content-divider'>";
        continue;
      }

      // Tabela
      if (trimmed.startsWith("|") && trimmed.endsWith("|")) {
        flushList();
        inTable = true;
        tableRows.push(trimmed);
        continue;
      } else {
        flushTable();
      }

      // Blockquote
      if (trimmed.startsWith(">")) {
        flushList();
        const quoteContent = trimmed.replace(/^>\s*/, "");
        html += `<blockquote class="hero-quote" style="margin: 1.5rem 0; font-size: 1.05rem;">${formatInline(quoteContent)}</blockquote>`;
        continue;
      }

      // Headers
      if (trimmed.startsWith("# ")) {
        flushList();
        html += `<h2 style="font-family: var(--font-cinzel); color: var(--accent-gold); margin-top: 1.5rem;">${formatInline(trimmed.replace(/^#\s*/, ""))}</h2>`;
        continue;
      }
      if (trimmed.startsWith("## ")) {
        flushList();
        html += `<h3 style="font-family: var(--font-cinzel); color: var(--accent-gold); margin-top: 1.8rem; margin-bottom: 0.8rem; border-bottom: 1px solid var(--border-subtle); padding-bottom: 0.3rem;">${formatInline(trimmed.replace(/^##\s*/, ""))}</h3>`;
        continue;
      }
      if (trimmed.startsWith("### ")) {
        flushList();
        html += `<h4 style="color: var(--text-primary); margin-top: 1.2rem; margin-bottom: 0.5rem;">${formatInline(trimmed.replace(/^###\s*/, ""))}</h4>`;
        continue;
      }

      // Listas
      if (trimmed.startsWith("* ") || trimmed.startsWith("- ")) {
        if (!inList) {
          html += "<ul style='margin-left: 1.5rem; margin-bottom: 1rem; line-height: 1.7;'>";
          inList = true;
        }
        const itemContent = trimmed.replace(/^[\*\-]\s*/, "");
        html += `<li>${formatInline(itemContent)}</li>`;
        continue;
      } else {
        flushList();
      }

      // Parágrafo padrão
      html += `<p style="margin-bottom: 0.8rem; line-height: 1.6;">${formatInline(trimmed)}</p>`;
    }

    flushList();
    flushTable();
    return html;
  }

  initHeroes();
});
