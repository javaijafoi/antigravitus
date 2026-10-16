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
  const cycleSummaryContainer = document.getElementById("cycle-summary-container");
  const seasonSelect = document.getElementById("season-select");
  const seasonSelectorWrap = document.getElementById("season-selector-wrap");
  const gridTitleEl = document.querySelector(".grid-title");
  const gridIconEl = document.querySelector(".grid-icon");
  const gridActionsGroup = document.querySelector(".grid-actions-group");

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

  // O catálogo central é a única fonte de perfis; não há ficha histórica de reserva.
  let heroesList = [];
  let currentHero = null;
  let currentState = null;
  let heroLoadVersion = 0;
  let audioManifest = { heroes: {} };
  let postsLoadError = false;
  let mapListenersController = null;
  let allPosts = [];
  let allCycles = []; // Resumos dos ciclos do herói ativo (com spoilers)
  let activeCycle = 1; // Número do Ciclo ativo (cada ciclo = 1 página de 10 dias)
  let activeDay = null;
  let latestPostId = 0;
  // Cache de preferências do usuário (localStorage)
  let sortOrder = localStorage.getItem("antigravitus_sort_order") || "desc"; // "desc" (mais novo 1º) ou "asc" (mais antigo 1º)

  // Temporadas e capítulos (Season 02+). A Season 01 continua no modelo por dias.
  let seasonsCatalog = null;
  let activeSeason = null;
  let chaptersData = null;
  let activeTomoNumber = 1;
  let activeChapterId = null;
  let seasonSelectorReady = false;

  // 1. Carrega lista de heróis do arquivo central heroes.json
  async function initHeroes() {
    try {
      const res = await fetch("data/heroes.json");
      if (!res.ok) throw new Error("Catálogo indisponível");
      const data = await res.json();
      if (!Array.isArray(data) || !data.length || data.some(h => !h.id || !h.name)) throw new Error("Catálogo inválido");
      heroesList = data;
    } catch (e) {
      showLoadStatus("Não foi possível carregar o catálogo de aventureiros. Abra o projeto por um servidor local e recarregue a página.");
      if (heroSelect) heroSelect.disabled = true;
      if (postsContainer) postsContainer.textContent = "Crônicas indisponíveis enquanto o catálogo não carregar.";
      if (fichaContainer) fichaContainer.textContent = "Não foi possível carregar a ficha.";
      return;
    }

    // O manifesto contém apenas gravações presentes no projeto. Sua ausência não impede a leitura.
    try {
      const res = await fetch("audio/manifest.json");
      if (!res.ok) throw new Error("Manifesto indisponível");
      audioManifest = await res.json();
    } catch (e) {
      audioManifest = { heroes: {} };
      showLoadStatus("O catálogo de áudio não carregou. As crônicas continuam disponíveis em texto.");
    }

    // Determina o herói ativo via URL, localStorage ou padrão
    const urlParams = new URLSearchParams(window.location.search);
    const heroParam = urlParams.get("hero");
    const storedHero = localStorage.getItem("active_hero");
    const targetHeroId = heroParam || storedHero || "antigravitus";

    currentHero = heroesList.find(h => h.id === targetHeroId) || heroesList[0];
    renderHeroSelector();
    await activateHero(currentHero);
  }

  function showLoadStatus(message) {
    const el = document.getElementById("load-status");
    if (el) { el.textContent = message; el.hidden = !message; }
  }

  async function activateHero(hero) {
    const version = ++heroLoadVersion;
    currentHero = hero;
    currentState = null;
    // A troca de herói recarrega a temporada escolhida para ele.
    seasonsCatalog = null;
    activeSeason = null;
    chaptersData = null;
    activeTomoNumber = 1;
    activeChapterId = null;
    if (seasonSelectorWrap) seasonSelectorWrap.hidden = true;
    if (postsContainer) {
      allPosts = [];
      allCycles = [];
      latestPostId = 0;
      activeDay = null;
      postsLoadError = false;
      renderAllViews();
    }
    localStorage.setItem("active_hero", hero.id);
    applyHeroContext(hero);
    const tasks = [loadStateForHero(hero, version)];
    if (postsContainer) tasks.push(loadPostsForHero(hero, version));
    if (postsContainer) tasks.push(loadSeasonsForHero(hero, version));
    if (fichaContainer) tasks.push(loadFichaForHero(hero, version));
    if (mapCanvasWrap) tasks.push(loadMapForHero(hero, version));
    await Promise.all(tasks);
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
        // Atualiza a URL sem recarregar totalmente a página
        const newUrl = new URL(window.location.href);
        newUrl.searchParams.set("hero", found.id);
        window.history.pushState({}, "", newUrl);
        await activateHero(found);
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
    const alignmentEl = document.getElementById("hero-alignment");
    if (alignmentEl) alignmentEl.textContent = hero.alignment || "Orientação não registrada";
    const serverEl = document.getElementById("hero-server");
    if (serverEl) serverEl.textContent = `Servidor: ${hero.server || "não registrado"}`;

    // Marca e links do rodapé também preservam a seleção do aventureiro.
    document.querySelectorAll('a.brand, .footer-links a[href], a.post-day-badge[href]').forEach(link => {
      const href = link.getAttribute("href");
      if (/^(index|mapa|ficha|sobre)\.html(?:\?|$)/.test(href || "")) {
        link.href = `${href.split("?")[0]}?hero=${encodeURIComponent(hero.id)}`;
      }
    });

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
    document.querySelectorAll("[data-hero-document]").forEach(el => {
      el.textContent = `data/heroes/${hero.id}/${el.dataset.heroDocument}`;
    });

    document.title = `${hero.name} — ${hero.title} | Devil's Bob MUD`;
    renderQuickStats(hero);
  }

  // Card de Metadados e Ficha Rápida (100% Dinâmico para qualquer Herói)
  function renderQuickStats(hero) {
    if (!heroQuickStatsEl) return;

    const qs = { ...(hero.quick_stats || {
      level_badge: `(${hero.race_class || "Aventureiro"})`,
      hp: "—",
      mana: "—",
      mv: "—",
      ac: "—",
      weapon: "—",
      weapon_icon: "🗡️",
      sanctuary: "—"
    }) };
    const state = currentState;
    if (state) {
      qs.level_badge = `(Nível ${state.level ?? "—"} • ${state.mechanical_class || hero.race_class || "Classe não registrada"})`;
      ["hp", "mana", "mv"].forEach(key => {
        const value = state.vitals && state.vitals[key];
        if (value) qs[key] = `${value.current ?? "—"} / ${value.max ?? "—"}`;
      });
    }
    const registeredLocation = state?.location?.name || qs.location;
    const registeredCamp = state?.camp?.name || qs.camp;
    const locationLabel = registeredLocation ? "Posição registrada" : registeredCamp ? "Acampamento registrado" : "Santuário de referência";
    const locationName = registeredLocation || registeredCamp || state?.sanctuary?.name || qs.sanctuary || "—";

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
          <span class="pill-label">📍 ${locationLabel}</span>
          <span class="pill-value" style="font-size: 0.82rem;">${escapeHtml(locationName)}</span>
        </div>
      </div>
      <p class="document-status">${state ? `Registro documental até o Dia ${state.as_of.day}; conferir mudanças no jogo.` : "Dados do catálogo documental; sem consulta ao servidor nesta página."}</p>
    `;
  }

  async function loadStateForHero(hero, version) {
    try {
      const res = await fetch(`data/heroes/${hero.id}/state.json`);
      if (version !== heroLoadVersion) return;
      if (!res.ok) return;
      const state = await res.json();
      if (version !== heroLoadVersion) return;
      if (state.hero_id !== hero.id || !state.as_of) return;
      currentState = state;
      renderQuickStats(hero);
    } catch (e) {
      // Estado opcional
    }
  }

  // 2. Carrega posts específicos do herói ativo
  async function loadPostsForHero(hero, version) {
    let posts = [];
    let cycles = [];
    let failed = false;
    const heroPath = `data/heroes/${hero.id}/posts.json`;
    postsContainer.textContent = `Carregando crônicas de ${hero.name}…`;

    try {
      const res = await fetch(heroPath);
      if (res.ok) {
        posts = await res.json();
      } else throw new Error("Crônicas indisponíveis");
      if (!Array.isArray(posts)) throw new Error("Formato inválido");
    } catch (e) {
      failed = true;
    }
    
    // Carrega resumos dos ciclos (com spoilers) do herói
    const ciclosPath = `data/heroes/${hero.id}/ciclos.json`;
    try {
      const ciclosRes = await fetch(ciclosPath);
      if (ciclosRes.ok) {
        cycles = await ciclosRes.json();
      }
    } catch (e) {
      console.warn(`Fetch falhou para ${ciclosPath}`);
    }
    if (version !== heroLoadVersion) return;
    allPosts = failed ? [] : posts;
    allCycles = Array.isArray(cycles) ? cycles : [];
    postsLoadError = failed;
    
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
    if (failed && postCountEl) postCountEl.textContent = "Crônicas indisponíveis";
  }

  function updatePostCount(count) {
    if (isChapterSeason()) return; // a contagem de capítulos é atualizada em renderChapterContent
    if (postCountEl) {
      postCountEl.textContent = `${count} ${count === 1 ? "crônica" : "crônicas"} registradas`;
    }
  }

  // ============================================================
  // TEMPORADAS — Season 01 por dias • Season 02+ por capítulos
  // ============================================================
  function isChapterSeason() {
    return !!(activeSeason && activeSeason.model === "capitulos");
  }

  function seasonTitleShort(season) {
    const title = String(season.title || ("Season " + season.number));
    const parts = title.split("\u2014").length > 1 ? title.split("\u2014") : title.split("-");
    const short = parts.length > 1 ? parts.slice(1).join(" ").trim() : title;
    return "T" + season.number + " · " + short;
  }

  // Esconde os controles exclusivos do modelo por dias durante a temporada de capítulos.
  function toggleSeason01Chrome(show) {
    const display = show ? "" : "none";
    if (gridActionsGroup) gridActionsGroup.style.display = display;
    if (floatingDockEl) floatingDockEl.style.display = display;
    if (postsPaginationEl) postsPaginationEl.style.display = display;
    if (show) {
      if (gridTitleEl) gridTitleEl.textContent = "Grade de Ciclos e Dias";
      if (gridIconEl) gridIconEl.textContent = "📅";
    } else if (cycleSummaryContainer) {
      cycleSummaryContainer.style.display = "none";
    }
  }

  async function loadSeasonsForHero(hero, version) {
    // Somente a página de crônicas usa temporadas; ficha, mapa e sobre seguem no modelo por dias.
    if (!postsContainer || !seasonSelect) return;
    try {
      const res = await fetch("data/heroes/" + hero.id + "/temporadas.json");
      if (version !== heroLoadVersion) return;
      if (!res.ok) throw new Error("Catálogo de temporadas indisponível");
      const data = await res.json();
      if (version !== heroLoadVersion) return;
      if (!data || !Array.isArray(data.seasons) || data.seasons.length === 0) throw new Error("Catálogo de temporadas inválido");
      seasonsCatalog = data;
      const urlSeason = new URLSearchParams(window.location.search).get("season");
      const stored = localStorage.getItem("active_season");
      const seasons = data.seasons;
      const resolved = seasons.find(s => s.id === urlSeason)
        || seasons.find(s => s.id === stored)
        || seasons.find(s => s.id === data.current)
        || seasons[0];
      await activateSeason(resolved.id, version);
    } catch (e) {
      seasonsCatalog = null;
      activeSeason = null;
      if (seasonSelectorWrap) seasonSelectorWrap.hidden = true;
      renderAllViews();
    }
  }

  function renderSeasonSelector() {
    if (!seasonSelect) return;
    const seasons = (seasonsCatalog && seasonsCatalog.seasons) || [];
    if (!seasons.length) {
      if (seasonSelectorWrap) seasonSelectorWrap.hidden = true;
      return;
    }
    if (seasonSelectorWrap) seasonSelectorWrap.hidden = false;
    seasonSelect.innerHTML = seasons.map(s => {
      const selected = (activeSeason && s.id === activeSeason.id) ? " selected" : "";
      return '<option value="' + escapeHtml(s.id) + '"' + selected + ">" + escapeHtml(seasonTitleShort(s)) + "</option>";
    }).join("");
    if (activeSeason) seasonSelect.value = activeSeason.id;
    if (!seasonSelectorReady) {
      seasonSelectorReady = true;
      seasonSelect.addEventListener("change", (e) => { activateSeason(e.target.value); });
    }
  }

  async function activateSeason(seasonId, version) {
    const seasons = (seasonsCatalog && seasonsCatalog.seasons) || [];
    const season = seasons.find(s => s.id === seasonId) || seasons[0];
    if (!season) return;
    activeSeason = season;
    activeTomoNumber = 1;
    activeChapterId = null;
    if (season.model === "capitulos") {
      await loadChaptersForHero(currentHero, season, version);
      activeChapterId = defaultChapterId();
    } else {
      chaptersData = null;
    }
    localStorage.setItem("active_season", season.id);
    if (seasonSelect) seasonSelect.value = season.id;
    if (currentHero) {
      const newUrl = new URL(window.location.href);
      newUrl.searchParams.set("hero", currentHero.id);
      newUrl.searchParams.set("season", season.id);
      window.history.replaceState({}, "", newUrl);
    }
    renderSeasonSelector();
    renderAllViews();
  }

  async function loadChaptersForHero(hero, season, version) {
    if (!hero || !season) return;
    if (chaptersData && chaptersData.hero_id === hero.id && chaptersData.season === season.id) return;
    try {
      const source = season.source || "capitulos.json";
      const res = await fetch("data/heroes/" + hero.id + "/" + source);
      if (version !== undefined && version !== heroLoadVersion) return;
      if (!res.ok) throw new Error("Capítulos indisponíveis");
      const data = await res.json();
      if (version !== undefined && version !== heroLoadVersion) return;
      chaptersData = (data && Array.isArray(data.chapters)) ? data : null;
    } catch (e) {
      chaptersData = null;
    }
  }

  function defaultChapterId() {
    const chapters = (chaptersData && chaptersData.chapters) || [];
    if (!chapters.length) return null;
    const concluded = chapters.filter(c => c.status === "concluido").map(c => c.id).sort((a, b) => a - b);
    if (concluded.length) return concluded[0];
    return chapters.map(c => c.id).sort((a, b) => a - b)[0];
  }

  function chapterStatusText(status) {
    if (status === "concluido") return "✔ Concluído";
    return "✎ Em produção";
  }

  function seasonPlaceholder(message) {
    return '<div class="post-card" style="text-align: center; padding: 3rem;">'
      + '<p style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--accent-gold);">'
      + escapeHtml(message) + "</p></div>";
  }

  function renderChapterParts(chapter) {
    if (!Array.isArray(chapter.parts) || chapter.parts.length === 0) return "";
    let html = '<section class="chapter-parts"><h3 class="chapter-parts-title">Partes registradas</h3>';
    chapter.parts.forEach(part => {
      html += '<div class="chapter-part">';
      html += '<div class="chapter-part-head"><span class="chapter-part-day">Dia ' + escapeHtml(String(part.day)) + "</span>";
      if (part.date) html += '<span class="chapter-part-date">' + escapeHtml(part.date) + "</span>";
      html += "</div>";
      if (part.summary) html += '<p class="chapter-part-summary">' + escapeHtml(part.summary) + "</p>";
      html += "</div>";
    });
    return html + "</section>";
  }

  function renderChapterContent() {
    if (!postsContainer) return;
    const chapters = (chaptersData && chaptersData.chapters) || [];
    let html = "";
    if (activeChapterId === null || activeChapterId === undefined) {
      html = seasonPlaceholder("Selecione um capítulo na grade acima.");
    } else {
      const chapter = chapters.find(c => c.id === activeChapterId);
      const badge = "Capítulo " + activeChapterId + (chapter && chapter.kind === "prologo" ? " • Prólogo" : "");
      if (!chapter) {
        html = '<article class="post-card chapter-view">'
          + '<header class="post-header"><span class="post-day-badge">' + escapeHtml(badge) + "</span></header>"
          + '<h2 class="post-title">Capítulo ' + escapeHtml(String(activeChapterId)) + "</h2>"
          + '<div class="chapter-production-warning">⏳ Em produção — este capítulo ainda não foi publicado.</div>'
          + "</article>";
      } else if (chapter.status === "concluido" && Array.isArray(chapter.content) && chapter.content.length) {
        html = '<article class="post-card chapter-view" id="chapter-' + chapter.id + '">'
          + '<header class="post-header">'
          + '<span class="post-day-badge">' + escapeHtml(badge) + "</span>"
          + '<div class="post-dates"><span>' + escapeHtml(chapter.date || "") + "</span></div>"
          + "</header>"
          + '<h2 class="post-title">' + escapeHtml(chapter.title || ("Capítulo " + chapter.id)) + "</h2>"
          + (chapter.in_game_time ? '<div class="post-location"><span>🏛️ ' + escapeHtml(chapter.in_game_time) + "</span></div>" : "")
          + (chapter.excerpt ? '<p class="chapter-excerpt">' + escapeHtml(chapter.excerpt) + "</p>" : "")
          + '<div class="post-body">' + chapter.content.map(p => "<p>" + p + "</p>").join("") + "</div>"
          + '<div class="post-signature">— ' + escapeHtml(currentHero ? currentHero.name : "") + ", " + escapeHtml(currentHero ? (currentHero.title || "Aventureiro") : "Aventureiro") + "</div>"
          + (chapter.tags && chapter.tags.length ? '<div class="post-tags"><span class="label">Marcos:</span>' + chapter.tags.map(t => '<span class="tag-pill">#' + escapeHtml(t) + "</span>").join("") + "</div>" : "")
          + renderChapterParts(chapter)
          + "</article>";
      } else {
        html = '<article class="post-card chapter-view" id="chapter-' + chapter.id + '">'
          + '<header class="post-header"><span class="post-day-badge">' + escapeHtml(badge) + "</span></header>"
          + '<h2 class="post-title">' + escapeHtml(chapter.title || ("Capítulo " + chapter.id)) + "</h2>"
          + (chapter.excerpt ? '<p class="chapter-excerpt">' + escapeHtml(chapter.excerpt) + "</p>" : "")
          + '<div class="chapter-goal"><strong>Objetivo:</strong> ' + escapeHtml(chapter.goal || "não registrado") + "</div>"
          + '<div class="chapter-production-warning">⏳ Em produção — este capítulo ainda não foi fechado.</div>'
          + "</article>";
      }
    }
    postsContainer.innerHTML = html;
    if (postCountEl) {
      const total = chapters.length;
      postCountEl.textContent = total + (total === 1 ? " capítulo registrado" : " capítulos registrados");
    }
  }

  function renderChapterView() {
    const tomos = (chaptersData && chaptersData.tomos) || [];
    const chapters = (chaptersData && chaptersData.chapters) || [];
    if (gridTitleEl) gridTitleEl.textContent = "Tomos e Capítulos";
    if (gridIconEl) gridIconEl.textContent = "📖";
    toggleSeason01Chrome(false);

    if (!tomos.length) {
      if (gridPageIndicator) gridPageIndicator.textContent = "Nenhum tomo publicado nesta temporada.";
      if (gridCyclesBar) gridCyclesBar.innerHTML = "";
      if (gridDaysMatrix) gridDaysMatrix.innerHTML = "";
      if (cycleSummaryContainer) { cycleSummaryContainer.innerHTML = ""; cycleSummaryContainer.style.display = "none"; }
      renderChapterContent();
      return;
    }

    if (!tomos.some(t => t.number === activeTomoNumber)) activeTomoNumber = tomos[0].number;
    const tomo = tomos.find(t => t.number === activeTomoNumber) || tomos[0];

    if (gridPageIndicator) {
      gridPageIndicator.textContent = (tomo.title || ("Tomo " + (tomo.roman || tomo.number)))
        + " • Capítulos " + tomo.chapter_start + " a " + tomo.chapter_end;
    }

    if (gridCyclesBar) {
      gridCyclesBar.innerHTML = tomos.map(t => {
        const active = t.number === activeTomoNumber ? " active" : "";
        return '<button class="cycle-page-btn' + active + '" data-tomo="' + t.number + '" title="' + escapeHtml(t.subtitle || t.title || "") + '">'
          + "<span>✦ Tomo " + escapeHtml(String(t.roman || t.number)) + " (" + t.chapter_start + "–" + t.chapter_end + ")</span></button>";
      }).join("");
      gridCyclesBar.querySelectorAll(".cycle-page-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          activeTomoNumber = parseInt(btn.dataset.tomo, 10);
          renderChapterView();
        });
      });
    }

    if (cycleSummaryContainer) {
      if (tomo.subtitle || tomo.title) {
        cycleSummaryContainer.style.display = "block";
        cycleSummaryContainer.innerHTML = '<div class="cycle-spoiler-card"><div class="cycle-spoiler-quote-banner">'
          + '<div class="cycle-spoiler-badge">✦ ' + escapeHtml(tomo.title || ("Tomo " + (tomo.roman || tomo.number))) + "</div>"
          + (tomo.subtitle ? '<p class="cycle-spoiler-text">' + escapeHtml(tomo.subtitle) + "</p>" : "")
          + "</div></div>";
      } else {
        cycleSummaryContainer.innerHTML = "";
        cycleSummaryContainer.style.display = "none";
      }
    }

    const ids = [];
    for (let id = tomo.chapter_start; id <= tomo.chapter_end; id++) ids.push(id);
    if (gridDaysMatrix) {
      gridDaysMatrix.innerHTML = ids.map(id => {
        const chapter = chapters.find(c => c.id === id);
        const concluded = !!(chapter && chapter.status === "concluido");
        const title = chapter ? chapter.title : ("Capítulo " + id);
        return '<button class="grid-day-cell chapter-cell' + (id === activeChapterId ? " active" : "") + (concluded ? " chapter-concluido" : " chapter-producao")
          + '" data-chapter="' + id + '" title="Cap. ' + id + ": " + escapeHtml(title) + '">'
          + '<span class="cell-day-num">Cap. ' + id + "</span>"
          + '<span class="chapter-cell-title">' + escapeHtml(title) + "</span>"
          + '<span class="chapter-status ' + (concluded ? "concluido" : "producao") + '">' + chapterStatusText(chapter ? chapter.status : "ausente") + "</span>"
          + "</button>";
      }).join("");
      gridDaysMatrix.querySelectorAll(".chapter-cell").forEach(cell => {
        cell.addEventListener("click", () => {
          activeChapterId = parseInt(cell.dataset.chapter, 10);
          renderChapterView();
        });
      });
    }

    renderChapterContent();
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
    return String(text ?? "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;");
  }

  // --- CONFIGURAÇÃO GLOBAL DOS CONTROLES DO NAVEGADOR ---
  let navControlsInitialized = false;
  function setupGlobalNavControls() {
    // Atualiza texto e estado do botão do Último Publicado
    if (latestBadgeText) {
      latestBadgeText.textContent = latestPostId ? `★ Último: Dia ${latestPostId}` : "Nenhuma crônica carregada";
    }
    if (btnJumpLatest) btnJumpLatest.disabled = !latestPostId;

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
    // Season 02+ usa tomos e capítulos; a Season 01 mantém a grade de dias.
    if (isChapterSeason()) {
      renderChapterView();
      return;
    }
    toggleSeason01Chrome(true);
    renderGridNavigation();
    renderCycleSummary();
    renderFeed();
    renderPagination();
    updateFloatingDock();
  }

  // Define um ciclo ativo e recarrega views
  function setCycle(cycleNum, scrollToTop = true) {
    if (isChapterSeason()) return;
    activeCycle = cycleNum;
    renderAllViews();
    if (scrollToTop && postsContainer) {
      postsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // Salta suavemente para uma crônica específica (trocando de página se necessário)
  function jumpToPost(dayId) {
    if (isChapterSeason()) return;
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
  // BLOCO RETRÁTIL: RESUMO DO CICLO COM AVISO DE SPOILER
  // ============================================================
  function renderCycleSummary() {
    if (!cycleSummaryContainer) return;

    if (!Array.isArray(allCycles) || allCycles.length === 0) {
      cycleSummaryContainer.innerHTML = "";
      cycleSummaryContainer.style.display = "none";
      return;
    }

    const cycleData = allCycles.find(c => c.cycle === activeCycle);
    if (!cycleData || !cycleData.summary) {
      cycleSummaryContainer.innerHTML = "";
      cycleSummaryContainer.style.display = "none";
      return;
    }

    cycleSummaryContainer.style.display = "block";
    const startDay = cycleData.start_day || ((activeCycle - 1) * 10 + 1);
    const endDay = cycleData.end_day || Math.min(activeCycle * 10, latestPostId);

    cycleSummaryContainer.innerHTML = `
      <div class="cycle-spoiler-card">
        <details class="cycle-spoiler-details" id="cycle-spoiler-${activeCycle}">
          <summary class="cycle-spoiler-summary">
            <div class="cycle-spoiler-header-left">
              <span class="spoiler-shield-icon" aria-hidden="true">⚠️</span>
              <div class="spoiler-texts">
                <span class="spoiler-tag">RESUMO DO CICLO ${toRoman(activeCycle)} • CONTÉM SPOILERS</span>
                <span class="spoiler-prompt">Quer pular este bloco ou relembrar os feitos do ciclo? Clique para ver o resumo</span>
              </div>
            </div>
            <div class="spoiler-action-badge">
              <span class="spoiler-toggle-text">👁️ Revelar Resumo</span>
              <span class="spoiler-arrow">▾</span>
            </div>
          </summary>
          <div class="cycle-spoiler-content">
            <div class="cycle-spoiler-quote-banner">
              <div class="cycle-spoiler-badge">✦ O Legado do Ciclo ${toRoman(activeCycle)} (Dias ${startDay} a ${endDay})</div>
              ${cycleData.title ? `<h4 class="cycle-spoiler-title">${escapeHtml(cycleData.title)}</h4>` : ""}
              <p class="cycle-spoiler-text">${escapeHtml(cycleData.summary)}</p>
            </div>
          </div>
        </details>
      </div>
    `;

    const detailsEl = cycleSummaryContainer.querySelector(".cycle-spoiler-details");
    if (detailsEl) {
      detailsEl.addEventListener("toggle", () => {
        const textEl = detailsEl.querySelector(".spoiler-toggle-text");
        const arrowEl = detailsEl.querySelector(".spoiler-arrow");
        if (detailsEl.open) {
          if (textEl) textEl.textContent = "🙈 Ocultar Resumo";
          if (arrowEl) arrowEl.textContent = "▴";
        } else {
          if (textEl) textEl.textContent = "👁️ Revelar Resumo";
          if (arrowEl) arrowEl.textContent = "▾";
        }
      });
    }
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
            ${postsLoadError ? "Não foi possível carregar as crônicas. Recarregue a página para tentar novamente." : "Nenhuma crônica registrada para este ciclo ainda."}
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
      const audioSrc = audioManifest.heroes?.[currentHero.id]?.[String(post.id)];

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

          ${audioSrc ? `<div class="post-narration-bar" id="narration-bar-${post.id}">
            <span class="narration-badge">🎙️ Ouvir Capítulo</span>
            <audio controls preload="none" src="${escapeHtml(audioSrc)}"></audio>
            <span class="audio-error" hidden>Gravação indisponível; o capítulo pode ser lido abaixo.</span>
          </div>` : ""}

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
    postsContainer.querySelectorAll("audio").forEach(player => {
      player.addEventListener("error", () => {
        player.hidden = true;
        const message = player.parentElement.querySelector(".audio-error");
        if (message) message.hidden = false;
      });
    });
  }

  // ============================================================
  // BARRA DE PAGINAÇÃO (10 EM 10 DIAS)
  // ============================================================
  function renderPagination() {
    if (!postsPaginationEl) return;
    if (!allPosts.length) { postsPaginationEl.innerHTML = ""; return; }

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
        Exibindo ${allPosts.filter(post => post.id >= (activeCycle - 1) * 10 + 1 && post.id <= activeCycle * 10).length} de ${allPosts.length} crônicas registradas • Ciclo ${toRoman(activeCycle)} (${(activeCycle - 1) * 10 + 1} a ${Math.min(activeCycle * 10, latestPostId)})
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
  async function loadFichaForHero(hero, version) {
    if (!fichaContainer) return;
    fichaContainer.innerHTML = `<div style="text-align: center; padding: 2rem; color: var(--text-secondary);">Carregando ficha de ${hero.name}...</div>`;
    
    try {
      const res = await fetch(`data/heroes/${hero.id}/ficha.md`);
      if (version !== heroLoadVersion) return;
      if (!res.ok) {
        fichaContainer.innerHTML = `<p style="color: var(--text-secondary); text-align: center;">Ficha viva não encontrada para ${hero.name}.</p>`;
        return;
      }
      const md = await res.text();
      if (version !== heroLoadVersion) return;
      fichaContainer.innerHTML = renderMarkdownToHtml(md);
    } catch (e) {
      if (version !== heroLoadVersion) return;
      fichaContainer.textContent = "Não foi possível carregar a ficha documental do personagem. Recarregue a página para tentar novamente.";
    }
  }

  function renderMarkdownToHtml(md) {
    // Parser limpo e seguro para a ficha de personagem
    const lines = md.split("\n");
    let html = "";
    let listStack = []; // pilha de níveis de lista
    let inTable = false;
    let tableRows = [];
    let inCodeBlock = false;
    let codeBlockContent = [];

    function flushList() {
      while (listStack.length > 0) {
        html += "</ul>";
        listStack.pop();
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
        .replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" target="_blank" rel="noopener noreferrer">$1</a>')
        .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")
        .replace(/\*(.*?)\*/g, "<em>$1</em>")
        .replace(/`([^`]+)`/g, "<code>$1</code>");
    }

    for (let line of lines) {
      const trimmed = line.trim();

      // Bloco de código com cerca tripla (```)
      if (trimmed.startsWith("```")) {
        flushList();
        flushTable();
        if (inCodeBlock) {
          html += `<pre class="ficha-pre"><code>${escapeHtml(codeBlockContent.join("\n"))}</code></pre>`;
          codeBlockContent = [];
          inCodeBlock = false;
        } else {
          inCodeBlock = true;
          codeBlockContent = [];
        }
        continue;
      }

      if (inCodeBlock) {
        codeBlockContent.push(line);
        continue;
      }

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

      // Listas com suporte a indentação (aninhamento)
      const listMatch = line.match(/^(\s*)([\*\-])\s+(.*)$/);
      if (listMatch) {
        const indentLength = listMatch[1].length;
        const level = Math.floor(indentLength / 2) + 1;
        const itemContent = listMatch[3];

        if (listStack.length < level) {
          while (listStack.length < level) {
            html += "<ul class='ficha-ul'>";
            listStack.push(true);
          }
        } else if (listStack.length > level) {
          while (listStack.length > level) {
            html += "</ul>";
            listStack.pop();
          }
        }

        html += `<li class='ficha-li'>${formatInline(itemContent)}</li>`;
        continue;
      } else {
        flushList();
      }

      // Parágrafo padrão
      html += `<p class="ficha-p">${formatInline(trimmed)}</p>`;
    }

    if (inCodeBlock) {
      html += `<pre class="ficha-pre"><code>${escapeHtml(codeBlockContent.join("\n"))}</code></pre>`;
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

  async function loadMapForHero(hero, version) {
    if (!mapCanvasWrap) return;
    if (mapListenersController) mapListenersController.abort();
    mapListenersController = new AbortController();
    const mapSignal = mapListenersController.signal;
    activeSelectedRoomId = null;
    isMapDragging = false;

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
    // Descarta ações ligadas ao herói anterior mesmo se o próximo carregamento falhar.
    mapCanvasWrap.classList.remove("is-dragging");
    ["onmousedown", "onwheel", "ontouchstart", "ontouchmove", "ontouchend"].forEach(key => { mapCanvasWrap[key] = null; });
    ["ctrl-zoom-in", "ctrl-zoom-out", "ctrl-zoom-reset", "btn-center-location", "btn-center-sanctuary"].forEach(id => {
      const button = document.getElementById(id);
      if (button) button.onclick = null;
    });
    if (searchInput) searchInput.oninput = null;
    if (zoneFilter) zoneFilter.onchange = null;
    if (riskFilter) riskFilter.onchange = null;
    if (tableContainer) tableContainer.onclick = null;
    if (inspectorEl) inspectorEl.classList.remove("active");
    if (edgesLayer) edgesLayer.innerHTML = "";
    if (nodesLayer) nodesLayer.innerHTML = "";
    if (tableContainer) tableContainer.textContent = "Carregando mapa documental…";
    if (layersTabsEl) layersTabsEl.innerHTML = "";
    [statRooms, statZones, statSafe, statDanger].forEach(el => { if (el) el.textContent = "—"; });
    if (mapCycleText) mapCycleText.textContent = "Carregando registro…";

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
      const data = await res.json();
      if (version !== heroLoadVersion) return;
      if (!Array.isArray(data.rooms)) throw new Error("Formato de mapa inválido");
      currentMapData = data;
    } catch (e) {
      if (version !== heroLoadVersion) return;
      console.warn("Erro ao carregar mapa.json:", e);
      if (edgesLayer) edgesLayer.innerHTML = "";
      if (nodesLayer) {
        nodesLayer.innerHTML = `<text x="500" y="350" text-anchor="middle" fill="var(--text-muted)">Não foi possível carregar o mapa de ${escapeHtml(hero.name)}.</text>`;
      }
      if (tableContainer) tableContainer.textContent = "Mapa indisponível. Recarregue a página para tentar novamente.";
      if (mapCycleText) mapCycleText.textContent = "Registro indisponível";
      return;
    }

    const { rooms = [], zones = [], layers = [], sanctuary_id = "", current_location_id = "", camp_id = "", last_updated_cycle = "data não informada", last_updated_day } = currentMapData;
    const dirNames = { n: "Norte", s: "Sul", l: "Leste", o: "Oeste", e: "Leste", w: "Oeste", u: "Cima", d: "Baixo" };
    const serverCommands = { l: "e", o: "w" };
    function exitLabel(room, dir) {
      const meta = room.exit_metadata?.[dir];
      const direction = `${dirNames[dir] || dir.toUpperCase()} · comando ${serverCommands[dir] || dir}`;
      const warning = meta?.one_way ? " · sentido único registrado" : "";
      const door = meta?.command ? ` · ${meta.command}` : "";
      return `${direction}${warning}${door}`;
    }
    function roomRole(room) {
      return [room.id === current_location_id ? "Posição registrada" : "", room.id === camp_id ? "Acampamento" : "", room.id === sanctuary_id ? "Santuário de referência" : ""].filter(Boolean).join(" · ");
    }

    // Atualiza indicadores
    if (mapCycleText) mapCycleText.textContent = `Documental: ${last_updated_day ? `Dia ${last_updated_day} · ` : ""}${last_updated_cycle}`;
    if (statRooms) statRooms.textContent = rooms.length;
    if (statZones) statZones.textContent = zones.length || new Set(rooms.map(r => r.zone)).size;
    
    const safeCount = rooms.filter(r => r.risk_code === "safe").length;
    const dangerCount = rooms.filter(r => r.risk_code === "danger" || r.risk_code === "fatal").length;
    if (statSafe) statSafe.textContent = safeCount;
    if (statDanger) statDanger.textContent = dangerCount;

    // Mapa de busca rápida por ID
    const roomMap = new Map();
    rooms.forEach(r => roomMap.set(r.id, r));

    // A posição registrada guia a abertura; santuário não implica presença atual.
    const sanctuaryRoom = roomMap.get(current_location_id) || roomMap.get(camp_id) || roomMap.get(sanctuary_id);
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
        const hasSanctuary = activeRooms.find(r => r.id === current_location_id) || activeRooms.find(r => r.id === camp_id) || activeRooms.find(r => r.id === sanctuary_id);
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

          const isOneWay = Boolean(room.exit_metadata?.[dir]?.one_way);
          const connKey = isOneWay ? `${room.id}->${targetId}` : [room.id, targetId].sort().join("<->");
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
          if (isOneWay) {
            line.classList.add("is-one-way");
            line.setAttribute("marker-end", "url(#arrow)");
            const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
            title.textContent = `${room.name} → ${target.name}: ${exitLabel(room, dir)}`;
            line.appendChild(title);
          }
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
        const title = document.createElementNS("http://www.w3.org/2000/svg", "title");
        title.textContent = `${room.name}${roomRole(room) ? ` · ${roomRole(room)}` : ""}`;
        g.appendChild(title);

        // O pulso identifica a posição documental, não uma consulta ao jogo.
        if (room.id === current_location_id) {
          const pulse = document.createElementNS("http://www.w3.org/2000/svg", "circle");
          pulse.setAttribute("class", "sanctuary-pulse-ring current-location-ring");
          pulse.setAttribute("cx", room.coords.x);
          pulse.setAttribute("cy", room.coords.y);
          pulse.setAttribute("r", "28");
          g.appendChild(pulse);
        }

        // Fundo do nó
        const rect = document.createElementNS("http://www.w3.org/2000/svg", "rect");
        rect.setAttribute("class", `map-node-bg risk-${room.risk_code || "low"} ${room.id === sanctuary_id ? "is-sanctuary" : ""} ${room.id === camp_id ? "is-camp" : ""} ${room.id === current_location_id ? "is-current-location" : ""}`);
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
              return `<button class="exit-btn" data-target="${tid}"><span>🧭 ${escapeHtml(exitLabel(r, dir))}</span>: ${tgt ? tgt.name : tid}${crossBadge}</button>`;
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
                ${roomRole(r) ? `<span class="map-room-role">${roomRole(r)}</span>` : ""}
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
      if (inspectZone) inspectZone.textContent = `${room.zone} • Camada: ${room.layer || 'superfície'}${roomRole(room) ? ` • ${roomRole(room)}` : ""}`;
      if (inspectBadge) {
        inspectBadge.className = `inspector-badge ${room.risk_code || "low"}`;
        inspectBadge.textContent = room.risk || "Normal";
      }
      if (inspectNotes) inspectNotes.textContent = room.notes || "Sem anotações de campo registradas.";
      if (inspectDiscovered) inspectDiscovered.textContent = room.discovered_in || "Ciclo I";

      // Saídas clicáveis
      if (inspectExits) {
        inspectExits.innerHTML = "";
        if (room.exits && Object.keys(room.exits).length > 0) {
          Object.entries(room.exits).forEach(([dir, targetId]) => {
            const targetRoom = roomMap.get(targetId);
            const btn = document.createElement("button");
            btn.className = "exit-btn";
            const layerNotice = targetRoom && targetRoom.layer !== room.layer ? ` <small style="color: var(--accent-cyan);">(🪜 ${targetRoom.layer})</small>` : "";
            btn.innerHTML = `<span>🧭 ${escapeHtml(exitLabel(room, dir))}</span> → <strong>${targetRoom ? targetRoom.name : targetId}</strong>${layerNotice}`;
            if (room.exit_metadata?.[dir]?.note) btn.title = room.exit_metadata[dir].note;
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
          inspectExits.innerHTML = "<span style='color: var(--text-muted); font-size: 0.85rem;'>Sem destinos de saída confirmados nos registros.</span>";
        }
        Object.entries(room.unresolved_exits || {}).forEach(([dir, pending]) => {
          const label = document.createElement("span");
          label.className = "exit-pending";
          label.textContent = `${dirNames[dir] || dir.toUpperCase()} · comando ${serverCommands[dir] || dir} → Destino pendente: ${pending.description || "saída ainda sem destino confirmado"}`;
          inspectExits.appendChild(label);
        });
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

    if (searchInput) searchInput.oninput = applyFilters;
    if (zoneFilter) zoneFilter.onchange = applyFilters;
    if (riskFilter) riskFilter.onchange = applyFilters;

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
    const btnCenterLocation = document.getElementById("btn-center-location");
    if (btnCenterLocation) {
      btnCenterLocation.disabled = !roomMap.has(current_location_id);
      btnCenterLocation.onclick = () => {
        const room = roomMap.get(current_location_id);
        if (!room) return;
        if (room.layer && room.layer !== currentActiveLayer && currentActiveLayer !== "all") switchLayer(room.layer);
        centerOnCoords(room.coords.x, room.coords.y, 1.15);
        inspectRoom(room);
      };
    }

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
        switchLayer(currentActiveLayer);
      };
    }
    if (btnCenterSanctuary) {
      btnCenterSanctuary.disabled = !roomMap.has(sanctuary_id);
      btnCenterSanctuary.onclick = () => {
        const sanctuary = roomMap.get(sanctuary_id);
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
    }, { signal: mapSignal });

    window.addEventListener("mouseup", () => {
      if (isMapDragging) {
        isMapDragging = false;
        mapCanvasWrap.classList.remove("is-dragging");
      }
    }, { signal: mapSignal });

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

  window.addEventListener("popstate", () => {
    const heroId = new URLSearchParams(window.location.search).get("hero");
    const hero = heroesList.find(item => item.id === heroId) || heroesList[0];
    if (!hero) return;
    if (heroSelect) heroSelect.value = hero.id;
    activateHero(hero);
  });
  initHeroes();
});
