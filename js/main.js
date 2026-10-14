// Engine Multi-Herói — Crônicas de Devil's Bob MUD
document.addEventListener("DOMContentLoaded", async () => {
  const heroSelect = document.getElementById("hero-select");
  const postsContainer = document.getElementById("posts-container");
  const heroQuickStatsEl = document.getElementById("hero-quick-stats");
  const gridPageIndicator = document.getElementById("grid-page-indicator");
  const gridCyclesBar = document.getElementById("grid-cycles-bar");
  const gridDaysMatrix = document.getElementById("grid-days-matrix");
  const postsPaginationEl = document.getElementById("posts-pagination");
  const floatingDockEl = document.getElementById("floating-reading-dock");
  const dockBtnPrev = document.getElementById("dock-btn-prev");
  const dockBtnNext = document.getElementById("dock-btn-next");
  const dockIndicator = document.getElementById("dock-indicator");
  const btnToggleOrder = document.getElementById("btn-toggle-order");
  const orderLabelText = document.getElementById("order-label-text");
  const btnJumpLatest = document.getElementById("btn-jump-latest");
  const latestBadgeText = document.getElementById("latest-badge-text");
  const postCountEl = document.getElementById("post-count");
  const linkSobre = document.getElementById("link-sobre");
  const linkCronicas = document.getElementById("link-cronicas");
  const linkFicha = document.getElementById("link-ficha");
  const linkMapa = document.getElementById("link-mapa");
  const fichaContainer = document.getElementById("ficha-container");
  const mapCanvasWrap = document.getElementById("map-canvas-wrap");
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
      },
      quick_stats: {
        level_badge: "(Grau 2 • Cronista de Midgaard)",
        hp: "31 / 31",
        mana: "118 / 118",
        mv: "92 / 92",
        ac: "AC 12",
        weapon: "Cajado de Peregrino",
        weapon_icon: "🪄",
        sanctuary: "Templo de Midgaard"
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
      },
      quick_stats: {
        level_badge: "(Grau 4 • Mago / Ladra)",
        hp: "33 / 33",
        mana: "111 / 111",
        mv: "89 / 89",
        ac: "AC 17",
        weapon: "Punhal de Novato (+ Escudo)",
        weapon_icon: "🗡️",
        sanctuary: "Panteão dos Centenários"
      }
    }
  ];

  let currentHero = heroesList[0];
  let allPosts = [];
  let activeCycle = 1; // Número do Ciclo ativo (cada ciclo = 1 página de 10 dias)
  let activeDay = null;
  let latestPostId = 0;
  // Cache de preferências do usuário (localStorage)
  let sortOrder = localStorage.getItem("antigravitus_sort_order") || "desc"; // "desc" (mais novo 1º) ou "asc" (mais antigo 1º)

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
    if (mapCanvasWrap) {
      await loadMapForHero(currentHero);
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
        if (mapCanvasWrap) {
          await loadMapForHero(currentHero);
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
    if (linkMapa) {
      linkMapa.href = `mapa.html?hero=${hero.id}`;
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

  // Card de Metadados e Ficha Rápida (100% Dinâmico para qualquer Herói)
  function renderQuickStats(hero) {
    if (!heroQuickStatsEl) return;

    const qs = hero.quick_stats || {
      level_badge: `(${hero.race_class || "Aventureiro"})`,
      hp: "—",
      mana: "—",
      mv: "—",
      ac: "—",
      weapon: "Desarmado",
      weapon_icon: "🗡️",
      sanctuary: hero.vigilia || "Midgaard"
    };

    heroQuickStatsEl.innerHTML = `
      <div class="quick-stats-header">
        <div class="quick-stats-title">
          <span>${hero.avatar || "⚔️"}</span>
          <strong>${hero.name}</strong>
          <span style="font-family: var(--font-sans); font-size: 0.8rem; color: var(--text-muted);">${qs.level_badge || ""}</span>
        </div>
        <a href="ficha.html?hero=${hero.id}" class="quick-stats-link">Ver Ficha Completa →</a>
      </div>
      <div class="quick-stats-grid">
        <div class="stat-pill pill-hp">
          <span class="pill-label">❤️ Vida</span>
          <span class="pill-value">${qs.hp || "—"}</span>
        </div>
        <div class="stat-pill pill-mana">
          <span class="pill-label">⚡ Mana</span>
          <span class="pill-value">${qs.mana || "—"}</span>
        </div>
        <div class="stat-pill pill-mv">
          <span class="pill-label">👟 Fôlego</span>
          <span class="pill-value">${qs.mv || "—"}</span>
        </div>
        <div class="stat-pill pill-ac">
          <span class="pill-label">🛡️ Armadura</span>
          <span class="pill-value">${qs.ac || "—"}</span>
        </div>
        <div class="stat-pill">
          <span class="pill-label">${qs.weapon_icon || "🗡️"} Empunhado</span>
          <span class="pill-value" style="font-size: 0.82rem;">${qs.weapon || "—"}</span>
        </div>
        <div class="stat-pill">
          <span class="pill-label">📍 Santuário</span>
          <span class="pill-value" style="font-size: 0.82rem;">${qs.sanctuary || "Midgaard"}</span>
        </div>
      </div>
    `;
  }

  // 2. Carrega posts específicos do herói ativo
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
    
    // Identifica o último dia publicado dinamicamente
    latestPostId = allPosts.reduce((max, p) => Math.max(max, p.id || 0), 0);
    const totalCycles = Math.max(1, Math.ceil(latestPostId / 10));

    // Se a ordenação for "mais novo primeiro", abre no ciclo mais recente por padrão
    if (sortOrder === "desc") {
      activeCycle = totalCycles;
      activeDay = latestPostId;
    } else {
      activeCycle = 1;
      activeDay = 1;
    }

    setupGlobalNavControls();
    renderAllViews();
    updatePostCount(allPosts.length);
  }

  function updatePostCount(count) {
    if (postCountEl) {
      postCountEl.textContent = `${count} ${count === 1 ? "crônica" : "crônicas"} registradas`;
    }
  }

  function toRoman(num) {
    const lookup = { M: 1000, CM: 900, D: 500, CD: 400, C: 100, XC: 90, L: 50, XL: 40, X: 10, IX: 9, V: 5, IV: 4, I: 1 };
    let roman = "";
    let n = num;
    for (let key in lookup) {
      while (n >= lookup[key]) {
        roman += key;
        n -= lookup[key];
      }
    }
    return roman || String(num);
  }

  function escapeHtml(text) {
    return (text || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;");
  }

  // --- CONFIGURAÇÃO GLOBAL DOS CONTROLES DO NAVEGADOR ---
  let navControlsInitialized = false;
  function setupGlobalNavControls() {
    // Atualiza texto e estado do botão do Último Publicado
    if (latestBadgeText) {
      latestBadgeText.textContent = `★ Último: Dia ${latestPostId}`;
    }

    // Atualiza texto da ordenação com base no cache
    if (orderLabelText) {
      orderLabelText.textContent = sortOrder === "desc" ? "Mais Novo 1º" : "Mais Antigo 1º";
    }

    if (navControlsInitialized) return;
    navControlsInitialized = true;

    // Alternar ordenação (Mais Novo vs Mais Antigo - Persistido em Cache)
    if (btnToggleOrder) {
      btnToggleOrder.addEventListener("click", () => {
        sortOrder = sortOrder === "desc" ? "asc" : "desc";
        localStorage.setItem("antigravitus_sort_order", sortOrder);
        if (orderLabelText) {
          orderLabelText.textContent = sortOrder === "desc" ? "Mais Novo 1º" : "Mais Antigo 1º";
        }
        renderAllViews();
      });
    }

    // Saltar para o último publicado em 1 clique
    if (btnJumpLatest) {
      btnJumpLatest.addEventListener("click", () => {
        jumpToPost(latestPostId);
      });
    }

    // Botões da barra flutuante de leitura rápida
    if (dockBtnPrev) {
      dockBtnPrev.addEventListener("click", () => {
        const curr = activeDay || (sortOrder === "desc" ? latestPostId : 1);
        if (curr > 1) jumpToPost(curr - 1);
      });
    }
    if (dockBtnNext) {
      dockBtnNext.addEventListener("click", () => {
        const curr = activeDay || (sortOrder === "desc" ? latestPostId : 1);
        if (curr < latestPostId) jumpToPost(curr + 1);
      });
    }

    // Atalhos de teclado globais (← / → / J / K)
    setupKeyboardShortcuts();
  }

  // Renderiza toda a interface com base no ciclo e ordenação ativos
  function renderAllViews() {
    renderGridNavigation();
    renderFeed();
    renderPagination();
    updateFloatingDock();
  }

  // Define um ciclo ativo e recarrega views
  function setCycle(cycleNum, scrollToTop = true) {
    activeCycle = cycleNum;
    renderAllViews();
    if (scrollToTop && postsContainer) {
      postsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // Salta suavemente para uma crônica específica (trocando de página se necessário)
  function jumpToPost(dayId) {
    if (!dayId || dayId < 1 || dayId > latestPostId) return;
    activeDay = dayId;

    const targetCycle = Math.ceil(dayId / 10);
    const needPageChange = (activeCycle !== targetCycle);

    if (needPageChange) {
      activeCycle = targetCycle;
      renderAllViews();
    } else {
      renderGridNavigation();
      updateFloatingDock();
    }

    setTimeout(() => {
      const targetEl = document.getElementById(`post-${dayId}`);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
        targetEl.classList.add("highlight-target-pulse");
        setTimeout(() => {
          targetEl.classList.remove("highlight-target-pulse");
        }, 1800);
      }
    }, needPageChange ? 120 : 40);
  }

  // ============================================================
  // GRADE RPG DE CICLOS E DIAS (NAVEGADOR PRINCIPAL)
  // ============================================================
  function renderGridNavigation() {
    if (!gridCyclesBar || !gridDaysMatrix) return;

    const totalCycles = Math.max(1, Math.ceil(latestPostId / 10));
    
    // Indicador da página/ciclo ativo
    const startDay = (activeCycle - 1) * 10 + 1;
    const endDay = Math.min(activeCycle * 10, latestPostId);
    if (gridPageIndicator) {
      gridPageIndicator.textContent = `Ciclo ${toRoman(activeCycle)} (Dias ${startDay} a ${endDay}) • 10 crônicas nesta página`;
    }

    // Abas de Ciclos
    let cycleList = [];
    for (let c = 1; c <= totalCycles; c++) {
      cycleList.push(c);
    }
    // Ordena as abas conforme a preferência de ordenação
    if (sortOrder === "desc") {
      cycleList.reverse();
    }

    gridCyclesBar.innerHTML = cycleList.map(c => {
      const cStart = (c - 1) * 10 + 1;
      const cEnd = Math.min(c * 10, latestPostId);
      const isActive = (c === activeCycle);
      const hasLatest = (latestPostId >= cStart && latestPostId <= cEnd);
      return `
        <button class="cycle-page-btn ${isActive ? "active" : ""} ${hasLatest ? "has-latest" : ""}" data-cycle="${c}" title="Abrir Ciclo ${toRoman(c)}">
          <span>✦ Ciclo ${toRoman(c)} (${cStart}–${cEnd})</span>
          ${hasLatest ? `<span style="color: #3fb950; font-size: 0.75rem;">★</span>` : ""}
        </button>
      `;
    }).join("");

    // Eventos nas abas de ciclo
    gridCyclesBar.querySelectorAll(".cycle-page-btn").forEach(btn => {
      btn.addEventListener("click", () => {
        const c = parseInt(btn.dataset.cycle, 10);
        setCycle(c, false);
      });
    });

    // Grade dos 10 Dias do Ciclo Ativo
    let daysInCycle = allPosts.filter(p => p.id >= startDay && p.id <= endDay);
    daysInCycle.sort((a, b) => {
      return sortOrder === "desc" ? (b.id - a.id) : (a.id - b.id);
    });

    gridDaysMatrix.innerHTML = daysInCycle.map(p => {
      const isActive = (p.id === activeDay);
      const isLatest = (p.id === latestPostId);
      const shortDate = p.date ? p.date.split(" de ")[0] : "";
      return `
        <button class="grid-day-cell ${isActive ? "active" : ""} ${isLatest ? "is-latest" : ""}" data-day="${p.id}" title="${p.day}: ${p.title} (${p.date})">
          ${isLatest ? `<span class="cell-latest-badge">★ ÚLTIMO</span>` : ""}
          <span class="cell-day-num">Dia ${p.id}</span>
          <span class="cell-date-hint">${shortDate}</span>
        </button>
      `;
    }).join("");

    // Eventos nas células de dia
    gridDaysMatrix.querySelectorAll(".grid-day-cell").forEach(cell => {
      cell.addEventListener("click", () => {
        const day = parseInt(cell.dataset.day, 10);
        jumpToPost(day);
      });
    });
  }

  // ============================================================
  // FEED DE CRÔNICAS: 10 POSTS POR PÁGINA + NAVEGADOR DE FIM DE DIA
  // ============================================================
  function renderFeed() {
    if (!postsContainer) return;

    const startDay = (activeCycle - 1) * 10 + 1;
    const endDay = activeCycle * 10;
    let cyclePosts = allPosts.filter(p => p.id >= startDay && p.id <= endDay);

    if (cyclePosts.length === 0) {
      postsContainer.innerHTML = `
        <div class="post-card" style="text-align: center; padding: 3rem;">
          <p style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--accent-gold);">
            Nenhuma crônica registrada para este ciclo ainda.
          </p>
        </div>
      `;
      return;
    }

    // Ordenação dos 10 posts dentro do ciclo
    cyclePosts.sort((a, b) => {
      return sortOrder === "desc" ? (b.id - a.id) : (a.id - b.id);
    });

    postsContainer.innerHTML = cyclePosts.map(post => {
      const isLatest = (post.id === latestPostId);

      // Encontra posts anterior e próximo em todo o compêndio
      const prevPost = allPosts.find(p => p.id === post.id - 1);
      const nextPost = allPosts.find(p => p.id === post.id + 1);

      return `
        <article class="post-card ${isLatest ? "post-card-latest" : ""}" id="post-${post.id}">
          <header class="post-header">
            ${isLatest ? `<div class="latest-feed-ribbon">★ ÚLTIMO PUBLICADO</div>` : ""}
            <span class="post-day-badge">${post.day || `Dia ${post.id}`}</span>
            <div class="post-dates">
              <span>${post.date || ""}</span>
            </div>
          </header>

          <h2 class="post-title">${post.title}</h2>
          <div class="post-location">
            <span>🏛️ ${post.in_game_time || ""}</span>
          </div>

          <div class="post-narration-bar" id="narration-bar-${post.id}">
            <span class="narration-badge">🎙️ Ouvir Capítulo</span>
            <audio controls preload="none" src="audio/${currentHero.id}/dia_${String(post.id).padStart(2, '0')}.mp3" onerror="this.closest('.post-narration-bar').style.display='none';"></audio>
          </div>

          <div class="post-body">
            ${(post.content || []).map(p => `<p>${p}</p>`).join("")}
          </div>

          <div class="post-signature">
            — ${currentHero.name}, ${currentHero.title || "Aventureiro"}
          </div>

          ${post.tags && post.tags.length > 0 ? `
            <div class="post-tags">
              <span class="label">Marcos:</span>
              ${post.tags.map(t => `<span class="tag-pill">#${t}</span>`).join("")}
            </div>
          ` : ""}

          <!-- Navegador Fácil ao Finalizar o Dia -->
          <footer class="post-end-navigator">
            <div class="end-nav-status">✦ Fim da Crônica do Dia ${post.id} ✦</div>
            ${prevPost ? `
              <button class="btn-end-step btn-end-prev" data-jump="${prevPost.id}">
                <span>◀</span>
                <div>
                  <span class="end-step-sub">Crônica Anterior</span>
                  <span class="end-step-title">Dia ${prevPost.id}: ${escapeHtml(prevPost.title)}</span>
                </div>
              </button>
            ` : `<div style="flex: 1 1 200px;"></div>`}

            ${nextPost ? `
              <button class="btn-end-step btn-end-next" data-jump="${nextPost.id}">
                <div>
                  <span class="end-step-sub">Próxima Crônica ➔</span>
                  <span class="end-step-title">Dia ${nextPost.id}: ${escapeHtml(nextPost.title)}</span>
                </div>
                <span>▶</span>
              </button>
            ` : `
              <div class="end-step-concluded">
                ★ Você concluiu a leitura até o Dia ${post.id} (Última Publicada)!
              </div>
            `}
          </footer>
        </article>
      `;
    }).join("");

    // Conecta cliques no navegador de fim de dia
    postsContainer.querySelectorAll(".btn-end-step").forEach(btn => {
      btn.addEventListener("click", () => {
        const targetDay = parseInt(btn.dataset.jump, 10);
        jumpToPost(targetDay);
      });
    });
  }

  // ============================================================
  // BARRA DE PAGINAÇÃO (10 EM 10 DIAS)
  // ============================================================
  function renderPagination() {
    if (!postsPaginationEl) return;

    const totalCycles = Math.max(1, Math.ceil(latestPostId / 10));

    // Determina próximo e anterior respeitando a ordem visual
    const hasPrev = sortOrder === "desc" ? (activeCycle < totalCycles) : (activeCycle > 1);
    const hasNext = sortOrder === "desc" ? (activeCycle > 1) : (activeCycle < totalCycles);
    const prevCycleTarget = sortOrder === "desc" ? (activeCycle + 1) : (activeCycle - 1);
    const nextCycleTarget = sortOrder === "desc" ? (activeCycle - 1) : (activeCycle + 1);

    let pagesOrder = [];
    for (let c = 1; c <= totalCycles; c++) {
      pagesOrder.push(c);
    }
    if (sortOrder === "desc") {
      pagesOrder.reverse();
    }

    postsPaginationEl.innerHTML = `
      <div class="pagination-controls">
        <button class="pagination-btn" id="pag-btn-prev" ${!hasPrev ? "disabled" : ""}>
          ◀ Ciclo Anterior
        </button>

        ${pagesOrder.map(c => `
          <button class="pagination-btn ${c === activeCycle ? "active" : ""}" data-cycle="${c}">
            Ciclo ${toRoman(c)}
          </button>
        `).join("")}

        <button class="pagination-btn" id="pag-btn-next" ${!hasNext ? "disabled" : ""}>
          Próximo Ciclo ▶
        </button>
      </div>
      <div class="pagination-info-text">
        Exibindo 10 de ${allPosts.length} crônicas registradas • Ciclo ${toRoman(activeCycle)} (${(activeCycle - 1) * 10 + 1} a ${Math.min(activeCycle * 10, latestPostId)})
      </div>
    `;

    // Conecta botões de paginação
    const pagBtnPrev = postsPaginationEl.querySelector("#pag-btn-prev");
    const pagBtnNext = postsPaginationEl.querySelector("#pag-btn-next");

    if (pagBtnPrev && hasPrev) {
      pagBtnPrev.addEventListener("click", () => setCycle(prevCycleTarget, true));
    }
    if (pagBtnNext && hasNext) {
      pagBtnNext.addEventListener("click", () => setCycle(nextCycleTarget, true));
    }

    postsPaginationEl.querySelectorAll(".pagination-btn[data-cycle]").forEach(btn => {
      btn.addEventListener("click", () => {
        const c = parseInt(btn.dataset.cycle, 10);
        setCycle(c, true);
      });
    });
  }

  // ============================================================
  // BARRA FLUTUANTE DE LEITURA (FLOATING DOCK)
  // ============================================================
  function updateFloatingDock() {
    if (!floatingDockEl) return;
    const curr = activeDay || (sortOrder === "desc" ? latestPostId : 1);

    if (dockIndicator) {
      dockIndicator.textContent = `Dia ${curr} de ${latestPostId}`;
    }
    if (dockBtnPrev) {
      dockBtnPrev.disabled = (curr <= 1);
    }
    if (dockBtnNext) {
      dockBtnNext.disabled = (curr >= latestPostId);
    }
  }

  // Atalhos de teclado globais
  let keyboardInitialized = false;
  function setupKeyboardShortcuts() {
    if (keyboardInitialized) return;
    keyboardInitialized = true;

    window.addEventListener("keydown", (e) => {
      const tag = document.activeElement ? document.activeElement.tagName.toLowerCase() : "";
      if (tag === "input" || tag === "textarea" || tag === "select") return;

      const curr = activeDay || (sortOrder === "desc" ? latestPostId : 1);
      if (e.key === "ArrowLeft" || e.key === "j" || e.key === "J") {
        if (curr > 1) {
          e.preventDefault();
          jumpToPost(curr - 1);
        }
      } else if (e.key === "ArrowRight" || e.key === "k" || e.key === "K") {
        if (curr < latestPostId) {
          e.preventDefault();
          jumpToPost(curr + 1);
        }
      }
    });
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

    function escapeHtml(text) {
      return (text || "")
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;");
    }

    function formatInline(text) {
      const safe = escapeHtml(text);
      return safe
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
          html += "<ul class='ficha-ul'>";
          inList = true;
        }
        const itemContent = trimmed.replace(/^[\*\-]\s*/, "");
        html += `<li class='ficha-li'>${formatInline(itemContent)}</li>`;
        continue;
      } else {
        flushList();
      }

      // Parágrafo padrão
      html += `<p class="ficha-p">${formatInline(trimmed)}</p>`;
    }

    flushList();
    flushTable();
    return html;
  }

  // ============================================================
  // MAPA INTERATIVO SIMPLIFICADO POR AVENTUREIRO (COM CAMADAS)
  // ============================================================
  let currentMapData = null;
  let currentActiveLayer = "superficie";
  let mapScale = 1.0;
  let mapPanX = 0;
  let mapPanY = 0;
  let isMapDragging = false;
  let dragStartX = 0;
  let dragStartY = 0;
  let activeSelectedRoomId = null;

  async function loadMapForHero(hero) {
    if (!mapCanvasWrap) return;

    const mapHeroTitle = document.getElementById("map-hero-title");
    const mapHeroSub = document.getElementById("map-hero-sub");
    const mapCycleText = document.getElementById("map-cycle-text");
    const statRooms = document.getElementById("stat-rooms-count");
    const statZones = document.getElementById("stat-zones-count");
    const statSafe = document.getElementById("stat-safe-count");
    const statDanger = document.getElementById("stat-danger-count");
    const layersTabsEl = document.getElementById("map-layers-tabs");
    const zoneFilter = document.getElementById("map-filter-zone");
    const riskFilter = document.getElementById("map-filter-risk");
    const searchInput = document.getElementById("map-search");
    const edgesLayer = document.getElementById("map-edges-layer");
    const nodesLayer = document.getElementById("map-nodes-layer");
    const viewportGroup = document.getElementById("map-viewport-group");
    const inspectorEl = document.getElementById("map-room-inspector");
    const tableContainer = document.getElementById("map-table-container");

    if (mapHeroTitle) {
      mapHeroTitle.textContent = `🗺️ Mapa Topológico de ${hero.name}`;
    }
    if (mapHeroSub) {
      mapHeroSub.textContent = `Território explorado, rotas e santuários de ${hero.name} (${hero.title}).`;
    }

    try {
      const res = await fetch(`data/heroes/${hero.id}/mapa.json`);
      if (!res.ok) {
        throw new Error(`Arquivo mapa.json não encontrado para ${hero.name}`);
      }
      currentMapData = await res.json();
    } catch (e) {
      console.warn("Erro ao carregar mapa.json:", e);
      if (edgesLayer) edgesLayer.innerHTML = "";
      if (nodesLayer) {
        nodesLayer.innerHTML = `<text x="500" y="350" text-anchor="middle" fill="var(--text-muted)">Nenhum mapa catalogado ainda para ${hero.name}.</text>`;
      }
      return;
    }

    const { rooms = [], zones = [], layers = [], sanctuary_id = "", last_updated_cycle = "A cada 10 ciclos" } = currentMapData;

    // Atualiza indicadores
    if (mapCycleText) mapCycleText.textContent = `Consolidado: ${last_updated_cycle}`;
    if (statRooms) statRooms.textContent = rooms.length;
    if (statZones) statZones.textContent = zones.length || new Set(rooms.map(r => r.zone)).size;
    
    const safeCount = rooms.filter(r => r.risk_code === "safe").length;
    const dangerCount = rooms.filter(r => r.risk_code === "danger" || r.risk_code === "fatal").length;
    if (statSafe) statSafe.textContent = safeCount;
    if (statDanger) statDanger.textContent = dangerCount;

    // Mapa de busca rápida por ID
    const roomMap = new Map();
    rooms.forEach(r => roomMap.set(r.id, r));

    // Determina camada inicial (a do santuário do herói ou a primeira disponível)
    const sanctuaryRoom = roomMap.get(sanctuary_id);
    if (sanctuaryRoom && sanctuaryRoom.layer) {
      currentActiveLayer = sanctuaryRoom.layer;
    } else if (layers.length > 0) {
      currentActiveLayer = layers[0].id;
    } else {
      currentActiveLayer = "all";
    }

    // Renderiza a barra de abas de camadas
    function renderLayersTabs() {
      if (!layersTabsEl) return;
      layersTabsEl.innerHTML = "";

      const defaultLayers = layers.length > 0 ? layers : [
        { id: "superficie", name: "🏛️ Superfície Urbana" }
      ];

      defaultLayers.forEach(l => {
        const count = rooms.filter(r => r.layer === l.id).length;
        const btn = document.createElement("button");
        btn.className = `layer-tab-btn ${currentActiveLayer === l.id ? "active" : ""}`;
        btn.setAttribute("data-layer", l.id);
        btn.innerHTML = `<span>${l.name}</span><span class="layer-room-count">${count}</span>`;
        btn.addEventListener("click", () => {
          switchLayer(l.id);
        });
        layersTabsEl.appendChild(btn);
      });

      // Aba "Ver Todas as Camadas"
      const allBtn = document.createElement("button");
      allBtn.className = `layer-tab-btn ${currentActiveLayer === "all" ? "active" : ""}`;
      allBtn.setAttribute("data-layer", "all");
      allBtn.innerHTML = `<span>🌐 Ver Todas</span><span class="layer-room-count">${rooms.length}</span>`;
      allBtn.addEventListener("click", () => {
        switchLayer("all");
      });
      layersTabsEl.appendChild(allBtn);
    }

    function switchLayer(layerId) {
      currentActiveLayer = layerId;

      // Atualiza botões de aba
      if (layersTabsEl) {
        layersTabsEl.querySelectorAll(".layer-tab-btn").forEach(btn => {
          if (btn.getAttribute("data-layer") === layerId) {
            btn.classList.add("active");
          } else {
            btn.classList.remove("active");
          }
        });
      }

      renderMapForCurrentLayer();

      // Centraliza na camada ativa
      const activeRooms = currentActiveLayer === "all" ? rooms : rooms.filter(r => r.layer === currentActiveLayer);
      if (activeRooms.length > 0) {
        const hasSanctuary = activeRooms.find(r => r.id === sanctuary_id);
        if (hasSanctuary) {
          centerOnCoords(hasSanctuary.coords.x, hasSanctuary.coords.y, 0.95);
          inspectRoom(hasSanctuary);
        } else {
          // Centroide da camada
          const avgX = activeRooms.reduce((acc, r) => acc + (r.coords ? r.coords.x : 0), 0) / activeRooms.length;
          const avgY = activeRooms.reduce((acc, r) => acc + (r.coords ? r.coords.y : 0), 0) / activeRooms.length;
          centerOnCoords(avgX, avgY, 0.9);
          inspectRoom(activeRooms[0]);
        }
      }
    }

    // Popula o seletor de zonas
    if (zoneFilter) {
      zoneFilter.innerHTML = '<option value="all">Todas as Zonas</option>';
      const uniqueZones = zones.length > 0 ? zones : [...new Set(rooms.map(r => r.zone))];
      uniqueZones.forEach(z => {
        const opt = document.createElement("option");
        opt.value = z;
        opt.textContent = z;
        zoneFilter.appendChild(opt);
      });
      zoneFilter.value = "all";
    }

    if (riskFilter) riskFilter.value = "all";
    if (searchInput) searchInput.value = "";

    // Renderiza Edges (Conexões)
    function renderEdges(visibleRooms) {
      if (!edgesLayer) return;
      edgesLayer.innerHTML = "";
      const drawnConnections = new Set();
      const visibleSet = new Set(visibleRooms.map(r => r.id));

      visibleRooms.forEach(room => {
        if (!room.coords || !room.exits) return;
        Object.entries(room.exits).forEach(([dir, targetId]) => {
          // Só desenha aresta se o nó de destino estiver visível nesta camada
          if (!visibleSet.has(targetId)) return;
          const target = roomMap.get(targetId);
          if (!target || !target.coords) return;

          const connKey = [room.id, targetId].sort().join("<->");
          if (drawnConnections.has(connKey)) return;
          drawnConnections.add(connKey);

          const line = document.createElementNS("http://www.w3.org/2000/svg", "line");
          line.setAttribute("x1", room.coords.x);
          line.setAttribute("y1", room.coords.y);
          line.setAttribute("x2", target.coords.x);
          line.setAttribute("y2", target.coords.y);
          line.setAttribute("class", "map-edge-line");
          line.setAttribute("data-from", room.id);
          line.setAttribute("data-to", targetId);
          edgesLayer.appendChild(line);
        });
      });
    }

    // Formata o rótulo da sala em até 2 linhas e fundo pill
    function appendRoomLabel(g, room) {
      const name = room.name || room.id;
      const words = name.split(" ");
      let lines = [name];

      if (name.length > 15 && words.length > 1) {
        const mid = Math.ceil(words.length / 2);
        lines = [words.slice(0, mid).join(" "), words.slice(mid).join(" ")];
      }

      const lineHeight = 13;
      const totalHeight = lines.length * lineHeight + 6;
      const maxLen = Math.max(...lines.map(l => l.length));
      const pillWidth = Math.max(50, Math.min(maxLen * 7.2 + 14, 200));

      // Fundo Pill para contraste impecável e sem overlap de texto
      const bgRect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
      bgRect.setAttribute("class", "map-label-bg");
      bgRect.setAttribute("x", room.coords.x - pillWidth / 2);
      bgRect.setAttribute("y", room.coords.y + 24);
      bgRect.setAttribute("width", pillWidth);
      bgRect.setAttribute("height", totalHeight);
      bgRect.setAttribute("rx", "5");
      bgRect.setAttribute("ry", "5");
      g.appendChild(bgRect);

      // Texto com tspans
      const text = document.createElementNS("http://www.w3.org/2000/svg", "text");
      text.setAttribute("class", "map-node-label");
      text.setAttribute("x", room.coords.x);
      text.setAttribute("y", room.coords.y + 36);

      lines.forEach((line, idx) => {
        const tspan = document.createElementNS("http://www.w3.org/2000/svg", "tspan");
        tspan.setAttribute("x", room.coords.x);
        if (idx > 0) tspan.setAttribute("dy", `${lineHeight}px`);
        tspan.textContent = line;
        text.appendChild(tspan);
      });
      g.appendChild(text);
    }

    // Renderiza Nodes (Salas)
    function renderNodes(visibleRooms) {
      if (!nodesLayer) return;
      nodesLayer.innerHTML = "";

      visibleRooms.forEach(room => {
        if (!room.coords) return;
        const g = document.createElementNS("http://www.w3.org/2000/svg", "g");
        g.setAttribute("class", `map-room-node ${room.id === activeSelectedRoomId ? "selected" : ""}`);
        g.setAttribute("id", `node-${room.id}`);
        g.setAttribute("data-id", room.id);
        g.setAttribute("data-zone", room.zone);
        g.setAttribute("data-risk", room.risk_code || "low");
        g.setAttribute("data-layer", room.layer || "superficie");

        // Pulso se for santuário
        if (room.id === sanctuary_id) {
          const pulse = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          pulse.setAttribute("class", "sanctuary-pulse-ring");
          pulse.setAttribute("cx", room.coords.x);
          pulse.setAttribute("cy", room.coords.y);
          pulse.setAttribute("r", "28");
          g.appendChild(pulse);
        }

        // Fundo do nó
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("class", `map-node-bg risk-${room.risk_code || "low"} ${room.id === sanctuary_id ? "is-sanctuary" : ""}`);
        rect.setAttribute("x", room.coords.x - 22);
        rect.setAttribute("y", room.coords.y - 22);
        rect.setAttribute("width", "44");
        rect.setAttribute("height", "44");
        rect.setAttribute("rx", "10");
        rect.setAttribute("ry", "10");
        g.appendChild(rect);

        // Ícone
        const icon = document.createElementNS("http://www.w3.org/2000/svg", "text");
        icon.setAttribute("class", "map-node-icon");
        icon.setAttribute("x", room.coords.x);
        icon.setAttribute("y", room.coords.y);
        icon.textContent = room.icon || "📍";
        g.appendChild(icon);

        // Transição de Camada (Portal / Escadas) se a sala levar a outra camada
        if (room.exits) {
          const crossExit = Object.values(room.exits).find(targetId => {
            const tgt = roomMap.get(targetId);
            return tgt && tgt.layer && tgt.layer !== room.layer;
          });

          if (crossExit) {
            const target = roomMap.get(crossExit);
            const portalG = document.createElementNS("http://www.w3.org/2000/svg", "g");
            portalG.setAttribute("class", "map-portal-badge");
            portalG.setAttribute("transform", `translate(${room.coords.x + 16}, ${room.coords.y - 18})`);
            
            const pCirc = document.createElementNS("http://www.w3.org/2000/svg", "circle");
            pCirc.setAttribute("r", "10");
            pCirc.setAttribute("fill", "#0a0d14");
            pCirc.setAttribute("stroke", "#5ec4d6");
            pCirc.setAttribute("stroke-width", "1.5");
            portalG.appendChild(pCirc);

            const pTxt = document.createElementNS("http://www.w3.org/2000/svg", "text");
            pTxt.setAttribute("text-anchor", "middle");
            pTxt.setAttribute("dominant-baseline", "central");
            pTxt.setAttribute("font-size", "11");
            pTxt.textContent = "🪜";
            portalG.appendChild(pTxt);

            portalG.addEventListener("click", (e) => {
              e.stopPropagation();
              if (target && target.layer) {
                switchLayer(target.layer);
                centerOnRoom(target);
                inspectRoom(target);
              }
            });

            g.appendChild(portalG);
          }
        }

        // Rótulo protegido em pill
        appendRoomLabel(g, room);

        // Evento de clique
        g.addEventListener("click", (evt) => {
          evt.stopPropagation();
          inspectRoom(room);
        });

        nodesLayer.appendChild(g);
      });
    }

    function renderMapForCurrentLayer() {
      const visibleRooms = currentActiveLayer === "all"
        ? rooms
        : rooms.filter(r => r.layer === currentActiveLayer);

      renderEdges(visibleRooms);
      renderNodes(visibleRooms);
      renderTable(visibleRooms);
      applyFilters();
    }

    // Renderiza a Tabela Tática alternativa
    function renderTable(visibleRooms = rooms) {
      if (!tableContainer) return;
      tableContainer.innerHTML = visibleRooms.map(r => {
        const exitsList = r.exits
          ? Object.entries(r.exits).map(([dir, tid]) => {
              const tgt = roomMap.get(tid);
              const crossBadge = tgt && tgt.layer !== r.layer ? ` <small style="color: var(--accent-cyan);">(🪜 ${tgt.layer})</small>` : "";
              return `<button class="exit-btn" data-target="${tid}"><span>🧭 ${dir.toUpperCase()}</span>: ${tgt ? tgt.name : tid}${crossBadge}</button>`;
            }).join(" ")
          : "<span style='color: var(--text-muted); font-size: 0.85rem;'>Nenhuma</span>";

        const npcsList = r.npcs && r.npcs.length > 0
          ? r.npcs.map(n => `<span class="npc-pill">${n}</span>`).join(" ")
          : "<span style='color: var(--text-muted); font-size: 0.85rem;'>Nenhum catalogado</span>";

        return `
          <div class="tactical-room-card" id="card-${r.id}" data-id="${r.id}" data-zone="${r.zone}" data-risk="${r.risk_code || 'low'}" data-layer="${r.layer || 'superficie'}">
            <div class="tactical-card-header">
              <div class="tactical-card-title">
                <span>${r.icon || "📍"}</span>
                <span>${r.name}</span>
                <span style="font-size: 0.78rem; color: var(--text-muted); font-family: var(--font-sans);">(${r.zone} • Camada: ${r.layer || 'superfície'})</span>
              </div>
              <span class="inspector-badge ${r.risk_code || 'low'}">${r.risk || 'Normal'}</span>
            </div>
            <div style="margin: 0.4rem 0;">
              <strong style="color: var(--accent-gold); font-size: 0.85rem; font-family: var(--font-sans);">Saídas:</strong>
              <div style="display: inline-flex; flex-wrap: wrap; gap: 0.35rem; margin-left: 0.5rem;">${exitsList}</div>
            </div>
            <div style="margin: 0.4rem 0;">
              <strong style="color: var(--accent-cyan); font-size: 0.85rem; font-family: var(--font-sans);">Presença / NPCs:</strong>
              <span style="margin-left: 0.5rem;">${npcsList}</span>
            </div>
            <p style="font-size: 0.95rem; color: var(--text-primary); margin-top: 0.4rem;">${r.notes || ""}</p>
          </div>
        `;
      }).join("");

      tableContainer.onclick = (e) => {
        const btn = e.target.closest(".exit-btn");
        if (btn) {
          const tid = btn.getAttribute("data-target");
          const targetRoom = roomMap.get(tid);
          if (targetRoom) {
            if (targetRoom.layer && targetRoom.layer !== currentActiveLayer && currentActiveLayer !== "all") {
              switchLayer(targetRoom.layer);
            }
            centerOnRoom(targetRoom);
            inspectRoom(targetRoom);
            const btnVisual = document.getElementById("btn-view-visual");
            if (btnVisual) btnVisual.click();
          }
        }
      };
    }

    // Inspetor de Sala
    function inspectRoom(room) {
      if (!room) return;
      activeSelectedRoomId = room.id;

      // Destaca nó no SVG
      if (nodesLayer) {
        const allNodes = nodesLayer.querySelectorAll(".map-room-node");
        allNodes.forEach(n => {
          if (n.getAttribute("data-id") === room.id) {
            n.classList.add("selected");
          } else {
            n.classList.remove("selected");
          }
        });
      }

      // Destaca conexões adjacentes
      if (edgesLayer) {
        const allEdges = edgesLayer.querySelectorAll(".map-edge-line");
        allEdges.forEach(e => {
          const from = e.getAttribute("data-from");
          const to = e.getAttribute("data-to");
          if (from === room.id || to === room.id) {
            e.classList.add("highlight");
          } else {
            e.classList.remove("highlight");
          }
        });
      }

      if (!inspectorEl) return;
      const inspectIcon = document.getElementById("inspect-icon");
      const inspectName = document.getElementById("inspect-name");
      const inspectZone = document.getElementById("inspect-zone");
      const inspectBadge = document.getElementById("inspect-risk-badge");
      const inspectExits = document.getElementById("inspect-exits");
      const inspectNpcs = document.getElementById("inspect-npcs");
      const inspectNotes = document.getElementById("inspect-notes");
      const inspectDiscovered = document.getElementById("inspect-discovered");

      if (inspectIcon) inspectIcon.textContent = room.icon || "📍";
      if (inspectName) inspectName.textContent = room.name;
      if (inspectZone) inspectZone.textContent = `${room.zone} • Camada: ${room.layer || 'superfície'}`;
      if (inspectBadge) {
        inspectBadge.className = `inspector-badge ${room.risk_code || "low"}`;
        inspectBadge.textContent = room.risk || "Normal";
      }
      if (inspectNotes) inspectNotes.textContent = room.notes || "Sem anotações de campo registradas.";
      if (inspectDiscovered) inspectDiscovered.textContent = room.discovered_in || "Ciclo I";

      // Saídas clicáveis
      if (inspectExits) {
        inspectExits.innerHTML = "";
        const dirNames = { n: "Norte", s: "Sul", l: "Leste", o: "Oeste", u: "Cima (Up)", d: "Baixo (Down)" };
        if (room.exits && Object.keys(room.exits).length > 0) {
          Object.entries(room.exits).forEach(([dir, targetId]) => {
            const targetRoom = roomMap.get(targetId);
            const btn = document.createElement("button");
            btn.className = "exit-btn";
            const layerNotice = targetRoom && targetRoom.layer !== room.layer ? ` <small style="color: var(--accent-cyan);">(🪜 ${targetRoom.layer})</small>` : "";
            btn.innerHTML = `<span>🧭 ${dirNames[dir] || dir.toUpperCase()}</span> → <strong>${targetRoom ? targetRoom.name : targetId}</strong>${layerNotice}`;
            btn.addEventListener("click", () => {
              if (targetRoom) {
                // Se a sala estiver em outra camada, muda de camada automaticamente
                if (targetRoom.layer && targetRoom.layer !== currentActiveLayer && currentActiveLayer !== "all") {
                  switchLayer(targetRoom.layer);
                }
                centerOnRoom(targetRoom);
                inspectRoom(targetRoom);
              }
            });
            inspectExits.appendChild(btn);
          });
        } else {
          inspectExits.innerHTML = "<span style='color: var(--text-muted); font-size: 0.85rem;'>Sem saídas catalogadas.</span>";
        }
      }

      // NPCs
      if (inspectNpcs) {
        inspectNpcs.innerHTML = "";
        if (room.npcs && room.npcs.length > 0) {
          room.npcs.forEach(npc => {
            const span = document.createElement("span");
            span.className = "npc-pill";
            span.textContent = npc;
            inspectNpcs.appendChild(span);
          });
        } else {
          inspectNpcs.innerHTML = "<span style='color: var(--text-muted); font-size: 0.85rem;'>Nenhum NPC hostil ou habitante catalogado nesta sala.</span>";
        }
      }

      inspectorEl.classList.add("active");
    }

    // Fechar inspetor
    const btnCloseInspector = document.getElementById("btn-close-inspector");
    if (btnCloseInspector) {
      btnCloseInspector.onclick = () => {
        if (inspectorEl) inspectorEl.classList.remove("active");
        if (edgesLayer) {
          edgesLayer.querySelectorAll(".map-edge-line").forEach(e => e.classList.remove("highlight"));
        }
        if (nodesLayer) {
          nodesLayer.querySelectorAll(".map-room-node").forEach(n => n.classList.remove("selected"));
        }
      };
    }

    // Aplica matriz de transformação ao viewport
    function applyTransform() {
      if (viewportGroup) {
        viewportGroup.setAttribute("transform", `translate(${mapPanX}, ${mapPanY}) scale(${mapScale})`);
      }
    }

    function centerOnCoords(x, y, targetScale = 1.0) {
      mapScale = targetScale;
      // Centraliza na caixa de visualização do SVG (com base na resolução de 1000x700)
      mapPanX = 500 - x * mapScale;
      mapPanY = 320 - y * mapScale;
      applyTransform();
    }

    function centerOnRoom(room) {
      if (!room || !room.coords) return;
      centerOnCoords(room.coords.x, room.coords.y, Math.max(mapScale, 0.95));
    }

    // Filtros e busca em tempo real
    function applyFilters() {
      const q = (searchInput ? searchInput.value : "").trim().toLowerCase();
      const selectedZone = zoneFilter ? zoneFilter.value : "all";
      const selectedRisk = riskFilter ? riskFilter.value : "all";

      rooms.forEach(room => {
        const nodeEl = document.getElementById(`node-${room.id}`);
        const cardEl = document.getElementById(`card-${room.id}`);

        const matchSearch = !q ||
          room.name.toLowerCase().includes(q) ||
          room.id.toLowerCase().includes(q) ||
          (room.notes && room.notes.toLowerCase().includes(q)) ||
          (room.npcs && room.npcs.some(n => n.toLowerCase().includes(q)));

        const matchZone = selectedZone === "all" || room.zone === selectedZone;
        const matchRisk = selectedRisk === "all" ||
          (selectedRisk === "safe" && room.risk_code === "safe") ||
          (selectedRisk === "medium" && room.risk_code === "medium") ||
          (selectedRisk === "danger" && (room.risk_code === "danger" || room.risk_code === "fatal"));

        const isMatch = matchSearch && matchZone && matchRisk;

        if (nodeEl) {
          if (isMatch) {
            nodeEl.style.opacity = "1";
            nodeEl.style.pointerEvents = "auto";
          } else {
            nodeEl.style.opacity = "0.15";
            nodeEl.style.pointerEvents = "none";
          }
        }

        if (cardEl) {
          cardEl.style.display = isMatch ? "block" : "none";
        }
      });
    }

    if (searchInput) searchInput.addEventListener("input", applyFilters);
    if (zoneFilter) zoneFilter.addEventListener("change", applyFilters);
    if (riskFilter) riskFilter.addEventListener("change", applyFilters);

    // Controles de Modo de Visão
    const btnViewVisual = document.getElementById("btn-view-visual");
    const btnViewTable = document.getElementById("btn-view-table");

    if (btnViewVisual && btnViewTable) {
      btnViewVisual.onclick = () => {
        btnViewVisual.classList.add("active");
        btnViewTable.classList.remove("active");
        if (mapCanvasWrap) mapCanvasWrap.style.display = "block";
        if (tableContainer) tableContainer.classList.remove("active");
      };

      btnViewTable.onclick = () => {
        btnViewTable.classList.add("active");
        btnViewVisual.classList.remove("active");
        if (mapCanvasWrap) mapCanvasWrap.style.display = "none";
        if (tableContainer) tableContainer.classList.add("active");
      };
    }

    // Zoom Controls
    const btnZoomIn = document.getElementById("ctrl-zoom-in");
    const btnZoomOut = document.getElementById("ctrl-zoom-out");
    const btnZoomReset = document.getElementById("ctrl-zoom-reset");
    const btnCenterSanctuary = document.getElementById("btn-center-sanctuary");

    if (btnZoomIn) {
      btnZoomIn.onclick = () => {
        mapScale = Math.min(mapScale * 1.25, 3.5);
        applyTransform();
      };
    }
    if (btnZoomOut) {
      btnZoomOut.onclick = () => {
        mapScale = Math.max(mapScale / 1.25, 0.3);
        applyTransform();
      };
    }
    if (btnZoomReset) {
      btnZoomReset.onclick = () => {
        const sanctuary = roomMap.get(sanctuary_id) || rooms[0];
        if (sanctuary) centerOnCoords(sanctuary.coords.x, sanctuary.coords.y, 0.95);
      };
    }
    if (btnCenterSanctuary) {
      btnCenterSanctuary.onclick = () => {
        const sanctuary = roomMap.get(sanctuary_id) || rooms[0];
        if (sanctuary) {
          if (sanctuary.layer && sanctuary.layer !== currentActiveLayer && currentActiveLayer !== "all") {
            switchLayer(sanctuary.layer);
          }
          centerOnCoords(sanctuary.coords.x, sanctuary.coords.y, 1.15);
          inspectRoom(sanctuary);
        }
      };
    }

    // Pan & Drag Handlers
    mapCanvasWrap.onmousedown = (e) => {
      if (e.target.closest(".map-room-node") || e.target.closest(".map-floating-controls") || e.target.closest(".map-legend-box") || e.target.closest(".map-portal-badge")) return;
      isMapDragging = true;
      dragStartX = e.clientX - mapPanX;
      dragStartY = e.clientY - mapPanY;
      mapCanvasWrap.classList.add("is-dragging");
    };

    window.addEventListener("mousemove", (e) => {
      if (!isMapDragging) return;
      mapPanX = e.clientX - dragStartX;
      mapPanY = e.clientY - dragStartY;
      applyTransform();
    });

    window.addEventListener("mouseup", () => {
      if (isMapDragging) {
        isMapDragging = false;
        mapCanvasWrap.classList.remove("is-dragging");
      }
    });

    // Zoom via Roda do Mouse
    mapCanvasWrap.onwheel = (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.85;
      const newScale = Math.max(0.25, Math.min(mapScale * zoomFactor, 3.5));

      const rect = mapCanvasWrap.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      mapPanX = mouseX - (mouseX - mapPanX) * (newScale / mapScale);
      mapPanY = mouseY - (mouseY - mapPanY) * (newScale / mapScale);
      mapScale = newScale;
      applyTransform();
    };

    // Suporte a Touch para Mobile
    let touchStartDist = 0;
    mapCanvasWrap.ontouchstart = (e) => {
      if (e.touches.length === 1) {
        isMapDragging = true;
        dragStartX = e.touches[0].clientX - mapPanX;
        dragStartY = e.touches[0].clientY - mapPanY;
      } else if (e.touches.length === 2) {
        touchStartDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
      }
    };

    mapCanvasWrap.ontouchmove = (e) => {
      if (e.touches.length === 1 && isMapDragging) {
        mapPanX = e.touches[0].clientX - dragStartX;
        mapPanY = e.touches[0].clientY - dragStartY;
        applyTransform();
      } else if (e.touches.length === 2) {
        const currentDist = Math.hypot(
          e.touches[0].clientX - e.touches[1].clientX,
          e.touches[0].clientY - e.touches[1].clientY
        );
        if (touchStartDist > 0) {
          const factor = currentDist / touchStartDist;
          mapScale = Math.max(0.25, Math.min(mapScale * factor, 3.5));
          touchStartDist = currentDist;
          applyTransform();
        }
      }
    };

    mapCanvasWrap.ontouchend = () => {
      isMapDragging = false;
      touchStartDist = 0;
    };

    // Inicialização da barra de camadas e renderização
    renderLayersTabs();
    switchLayer(currentActiveLayer);
  }

  initHeroes();
});
