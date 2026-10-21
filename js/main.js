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
  let seasonLoadVersion = 0;
  let chaptersLoadError = false;

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
      document.getElementById("feature-read")?.setAttribute("disabled","");
      document.getElementById("feature-start")?.setAttribute("disabled","");
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
    const targetHeroId = heroParam || storedHero || "grebolius";

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
    // O mapa em grade (js/mapa_grade.js) ouve este evento para carregar o herói ativo.
    document.dispatchEvent(new CustomEvent("hero:activated", { detail: { hero } }));
    if (seasonSelect) await loadSeasonsForHero(hero, version);
    const tasks = [loadStateForHero(hero, version)];
    if (postsContainer) tasks.push(loadPostsForHero(hero, version));

    if (fichaContainer) tasks.push(loadFichaForHero(hero, version));
    await Promise.all(tasks);
  }

  function renderHeroSelector() {
    if (!heroSelect) return;
    heroSelect.innerHTML = heroesList
      .map(h => `<option value="${h.id}" ${h.id === currentHero.id ? "selected" : ""}>${escapeHtml(h.name)}</option>`)
      .join("");

    heroSelect.value = currentHero.id;

    heroSelect.addEventListener("change", async (e) => {
      const selectedId = e.target.value;
      const found = heroesList.find(h => h.id === selectedId);
      if (found) {
        // Atualiza a URL sem recarregar totalmente a página
        const newUrl = new URL(window.location.href);
        newUrl.searchParams.set("hero", found.id);
        ["season", "day", "chapter"].forEach(key => newUrl.searchParams.delete(key));
        newUrl.hash = "";
        window.history.pushState({}, "", newUrl);
        await activateHero(found);
      }
    });
  }

  function applyHeroContext(hero) {
    if (brandRuneEl) brandRuneEl.textContent = document.body.classList.contains("chronicle-shell") ? "✧" : (hero.rune || "ᛟ");
    if (brandTitleEl) brandTitleEl.textContent = document.body.classList.contains("chronicle-shell") ? "Crônicas de Midgaard" : hero.name;
    if (brandSubEl) brandSubEl.textContent = document.body.classList.contains("chronicle-shell") ? "Um mundo. Muitas jornadas." : hero.title;

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
      const parts = [hero.race_class, hero.role].filter(Boolean);
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
    updateProfileSummary();
    updateJourneyPresentation();
    preserveContextLinks();
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
      updateProfileSummary();
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

    const requestedDay = Number(new URLSearchParams(location.search).get("day"));
    if (allPosts.some(p => p.id === requestedDay)) { activeDay = requestedDay; activeCycle = Math.ceil(requestedDay / 10); }
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
    if (!seasonSelect) return;
    try {
      const res = await fetch("data/heroes/" + hero.id + "/temporadas.json");
      if (version !== heroLoadVersion) return;
      if (!res.ok) throw new Error("Catálogo opcional ausente");
      const data = await res.json();
      if (version !== heroLoadVersion) return;
      if (!data || !Array.isArray(data.seasons) || !data.seasons.length) throw new Error("Catálogo inválido");
      seasonsCatalog = data;
    } catch (e) {
      if (version !== heroLoadVersion) return;
      seasonsCatalog = {current:"s01", seasons:[{id:"s01",number:1,title:"Temporada 1 — A jornada de "+hero.name,model:"dias",status:"arquivo",summary:"Todos os registros da jornada, do primeiro dia à crônica mais recente."}]};
    }
    const seasons = seasonsCatalog.seasons;
    const params = new URLSearchParams(location.search);
    const stored = localStorage.getItem("active_season:"+hero.id);
    let resolved = seasons.find(s => s.id === params.get("season")) || seasons.find(s => s.id === stored) || seasons.find(s => s.id === seasonsCatalog.current) || seasons[0];
    // Link antigo de dia (?season=s01&day=N): a Season 01 virou tomo, e os dias vivem na versão Legacy.
    if (params.get("day") && resolved.model === "capitulos") resolved = seasons.find(s => s.model === "dias" && s.number === resolved.number) || resolved;
    await activateSeason(resolved.id, version);
  }

  function renderSeasonSelector() {
    if (!seasonSelect) return;
    const seasons = (seasonsCatalog && seasonsCatalog.seasons) || [];
    if (!seasons.length) {
      if (seasonSelectorWrap) seasonSelectorWrap.hidden = true;
      return;
    }
    if (seasonSelectorWrap) seasonSelectorWrap.hidden = false;
    seasonSelect.disabled = seasons.length < 2;
    seasonSelect.innerHTML = seasons.map(s => {
      const selected = (activeSeason && s.id === activeSeason.id) ? " selected" : "";
      return '<option value="' + escapeHtml(s.id) + '"' + selected + ">" + escapeHtml(seasonTitleShort(s)) + "</option>";
    }).join("");
    if (activeSeason) seasonSelect.value = activeSeason.id;
    if (!seasonSelectorReady) {
      seasonSelectorReady = true;
      seasonSelect.addEventListener("change", (e) => { activateSeason(e.target.value, undefined, true); });
    }
  }

  async function activateSeason(seasonId, version, userNavigation = false) {
    const heroVersion = version ?? heroLoadVersion;
    const requestVersion = ++seasonLoadVersion;
    const seasons = seasonsCatalog?.seasons || [];
    const season = seasons.find(s => s.id === seasonId) || seasons[0];
    if (!season || !currentHero) return;
    const hero = currentHero;
    let loaded = null;
    if (season.model === "capitulos") loaded = await loadChaptersForHero(hero, season, heroVersion);
    if (heroVersion !== heroLoadVersion || requestVersion !== seasonLoadVersion) return;
    activeSeason = season;
    chaptersData = loaded;
    activeTomoNumber = loaded?.tomos?.[0]?.number || 1;
    const params = new URLSearchParams(location.search);
    const requested = userNavigation ? null : params.get("chapter");
    activeChapterId = requested !== null && loaded?.chapters?.some(c => c.id === Number(requested)) ? Number(requested) : defaultChapterId();
    if (userNavigation && season.model !== "capitulos") { activeDay = latestPostId; activeCycle = Math.max(1,Math.ceil(latestPostId/10)); }
    localStorage.setItem("active_season:"+hero.id, season.id);
    const next = new URL(location.href);
    next.searchParams.set("hero",hero.id); next.searchParams.set("season",season.id);
    if (userNavigation) {next.searchParams.delete("day"); next.searchParams.delete("chapter");next.hash="";}
    window.history[userNavigation ? "pushState" : "replaceState"]({},"",next);
    renderSeasonSelector();
    renderAllViews();
    preserveContextLinks();
  }

  async function loadChaptersForHero(hero, season, version) {
    chaptersLoadError = false;
    try {
      const res = await fetch("data/heroes/"+hero.id+"/"+(season.source || "capitulos.json"));
      if (version !== heroLoadVersion) return null;
      if (!res.ok) throw new Error("Capítulos indisponíveis");
      const data = await res.json();
      if (!data || !Array.isArray(data.chapters)) throw new Error("Formato inválido");
      return data;
    } catch (e) {if (version === heroLoadVersion) chaptersLoadError = true; return null;}
  }

  function defaultChapterId() {
    const chapters = (chaptersData && chaptersData.chapters) || [];
    if (!chapters.length) return null;
    const concluded = chapters.filter(c => c.status === "concluido").map(c => c.id).sort((a, b) => a - b);
    if (concluded.length) return concluded[0];
    return chapters.map(c => c.id).sort((a, b) => a - b)[0];
  }

  function chapterStatusText(status) {
    if (status === "concluido") return "Publicado";
    return "Em andamento";
  }

  function seasonPlaceholder(message) {
    return '<div class="post-card" style="text-align: center; padding: 3rem;">'
      + '<p style="font-family: var(--font-serif); font-size: 1.3rem; color: var(--accent-gold);">'
      + escapeHtml(message) + "</p></div>";
  }

  function renderChapterParts(chapter) {
    if (!Array.isArray(chapter.parts) || chapter.parts.length === 0) return "";
    const heading = activeSeason && activeSeason.rewrite_of ? "Resumo dos dias" : "Partes registradas";
    let html = '<section class="chapter-parts"><h3 class="chapter-parts-title">' + heading + "</h3>";
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
      html = seasonPlaceholder(chaptersLoadError ? "Não foi possível carregar os capítulos. Recarregue a página para tentar novamente." : "Nenhum capítulo publicado nesta temporada.");
    } else {
      const chapter = chapters.find(c => c.id === activeChapterId);
      const badge = chapter?.kind === "prologo" ? "Prólogo" : "Capítulo " + activeChapterId;
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
    const ordered = [...chapters].sort((a,b)=>a.id-b.id);
    const index = ordered.findIndex(c=>c.id===activeChapterId);
    const previous = ordered[index-1], following = ordered[index+1];
    const followingSeason = !following && index >= 0 ? seasonsCatalog?.seasons?.filter(s=>s.number>(activeSeason?.number || 1)).sort((a,b)=>a.number-b.number)[0] : null;
    if (index >= 0 && (previous || following || followingSeason)) html += '<nav class="chapter-reader-nav" aria-label="Seguir a leitura">'
      + (previous ? '<button data-nav-chapter="'+previous.id+'">← '+escapeHtml(previous.kind === "prologo" ? "Voltar ao prólogo" : "Capítulo "+previous.id)+'</button>' : '<span></span>')
      + (following ? '<button data-nav-chapter="'+following.id+'">'+escapeHtml(following.status === "concluido" ? "Próximo capítulo" : "Próximo capítulo · Em andamento")+' →</button>' : '')
      + (followingSeason ? '<button data-next-season="'+escapeHtml(followingSeason.id)+'">Continuar na Temporada '+followingSeason.number+' →</button>' : '') + '</nav>';
    postsContainer.innerHTML = html;
    postsContainer.querySelectorAll('[data-nav-chapter]').forEach(button=>button.addEventListener('click',()=>{
      activeChapterId=Number(button.dataset.navChapter); syncReadingUrl(); renderChapterView();updateJourneyPresentation();focusReader();
    }));
    postsContainer.querySelectorAll('[data-next-season]').forEach(button=>button.addEventListener('click',async()=>{await activateSeason(button.dataset.nextSeason,undefined,true);focusReader();}));
    if (postCountEl) {
      const published = chapters.filter(c => c.status === "concluido").length;
      const ongoing = chapters.length - published;
      postCountEl.textContent = published + " publicado" + (published === 1 ? "" : "s") + (ongoing ? " · " + ongoing + " em andamento" : "");
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
      const published = chapters.filter(c=>c.tomo===tomo.number && c.status==="concluido").length;
      gridPageIndicator.textContent = (tomo.title || ("Tomo " + (tomo.roman || tomo.number)))
        + " · " + published + (published === 1 ? " texto publicado" : " textos publicados");
    }

    if (gridCyclesBar) {
      gridCyclesBar.innerHTML = tomos.map(t => {
        const active = t.number === activeTomoNumber ? " active" : "";
        return '<button class="cycle-page-btn' + active + '" data-tomo="' + t.number + '" title="' + escapeHtml(t.subtitle || t.title || "") + '">'
          + "<span>Tomo " + escapeHtml(String(t.roman || t.number)) + "</span></button>";
      }).join("");
      gridCyclesBar.querySelectorAll(".cycle-page-btn").forEach(btn => {
        btn.addEventListener("click", () => {
          activeTomoNumber = parseInt(btn.dataset.tomo, 10);
          syncReadingUrl();
          renderChapterView();
          updateJourneyPresentation();
          focusReader();
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

    const ids = chapters.filter(c => c.tomo === tomo.number).map(c => c.id).sort((a,b) => a-b);
    if (gridDaysMatrix) {
      gridDaysMatrix.innerHTML = ids.map(id => {
        const chapter = chapters.find(c => c.id === id);
        const concluded = !!(chapter && chapter.status === "concluido");
        const title = chapter ? chapter.title : ("Capítulo " + id);
        return '<button class="grid-day-cell chapter-cell' + (id === activeChapterId ? " active" : "") + (concluded ? " chapter-concluido" : " chapter-producao")
          + '" data-chapter="' + id + '" aria-current="' + (id === activeChapterId ? "page" : "false") + '" title="Cap. ' + id + ": " + escapeHtml(title) + '">'
          + '<span class="cell-day-num">' + (chapter?.kind === "prologo" ? "Prólogo" : "Cap. " + id) + "</span>"
          + '<span class="chapter-cell-title">' + escapeHtml(title) + "</span>"
          + '<span class="chapter-status ' + (concluded ? "concluido" : "producao") + '">' + chapterStatusText(chapter ? chapter.status : "ausente") + "</span>"
          + "</button>";
      }).join("");
      gridDaysMatrix.querySelectorAll(".chapter-cell").forEach(cell => {
        cell.addEventListener("click", () => {
          activeChapterId = parseInt(cell.dataset.chapter, 10);
          syncReadingUrl();
          renderChapterView();
          updateJourneyPresentation();
          focusReader();
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
      orderLabelText.textContent = sortOrder === "desc" ? "Recentes primeiro" : "Antigos primeiro";
    }

    if (navControlsInitialized) return;
    navControlsInitialized = true;

    // Alternar ordenação (Mais Novo vs Mais Antigo - Persistido em Cache)
    if (btnToggleOrder) {
      btnToggleOrder.addEventListener("click", () => {
        sortOrder = sortOrder === "desc" ? "asc" : "desc";
        localStorage.setItem("antigravitus_sort_order", sortOrder);
        if (orderLabelText) {
          orderLabelText.textContent = sortOrder === "desc" ? "Recentes primeiro" : "Antigos primeiro";
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
    updateJourneyPresentation();
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
    const cycleDays = allPosts.filter(p => Math.ceil(p.id / 10) === cycleNum).sort((a,b)=>a.id-b.id);
    activeDay = (sortOrder === "desc" ? cycleDays.at(-1) : cycleDays[0])?.id || null;
    syncReadingUrl();
    renderAllViews();
    if (scrollToTop && postsContainer) {
      postsContainer.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  }

  // Salta suavemente para uma crônica específica (trocando de página se necessário)
  function jumpToPost(dayId) {
    if (isChapterSeason()) return;
    if (!allPosts.some(p => p.id === dayId)) return;
    activeDay = dayId;
    syncReadingUrl();

    const targetCycle = Math.ceil(dayId / 10);
    const needPageChange = (activeCycle !== targetCycle);

    if (needPageChange) {
      activeCycle = targetCycle;
      renderAllViews();
    } else {
      renderGridNavigation();
      renderFeed();
      updateJourneyPresentation();
      updateFloatingDock();
    }

    setTimeout(() => {
      const targetEl = document.getElementById(`post-${dayId}`);
      if (targetEl) {
        targetEl.scrollIntoView({ behavior: "smooth", block: "start" });
        focusReader(false);
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
      gridPageIndicator.textContent = `Ciclo ${toRoman(activeCycle)} · Dias ${startDay}–${endDay}`;
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
        <button class="cycle-page-btn ${isActive ? "active" : ""} ${hasLatest ? "has-latest" : ""}" data-cycle="${c}" aria-current="${isActive ? "page" : "false"}" title="Abrir Ciclo ${toRoman(c)}">
          <span>${toRoman(c)} · ${cStart}–${cEnd}</span>

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
        <button class="grid-day-cell ${isActive ? "active" : ""} ${isLatest ? "is-latest" : ""}" data-day="${p.id}" aria-current="${isActive ? "page" : "false"}" title="${p.day}: ${p.title} (${p.date})">
          ${isLatest ? `<span class="cell-latest-badge">★ ÚLTIMO</span>` : ""}
          <span class="cell-day-num">Dia ${p.id}</span>
          <span class="cell-entry-title">${escapeHtml(p.title)}</span>
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

    if (document.body.classList.contains("chronicles-home")) {
      const selected = cyclePosts.find(p => p.id === activeDay) || cyclePosts[0];
      cyclePosts = [selected];
    }
    postsContainer.innerHTML = cyclePosts.map(post => {
      const isLatest = (post.id === latestPostId);

      // Encontra posts anterior e próximo em todo o compêndio
      const prevPost = allPosts.find(p => p.id === post.id - 1);
      const nextPost = allPosts.find(p => p.id === post.id + 1);
      const audioSrc = audioManifest.heroes?.[currentHero.id]?.[String(post.id)];
      const followingSeason = seasonsCatalog?.seasons?.filter(s=>s.number>(activeSeason?.number || 1)).sort((a,b)=>a.number-b.number)[0];

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
              ${followingSeason ? `<button class="read-button next-season-button" data-next-season="${escapeHtml(followingSeason.id)}">Continuar na Temporada ${followingSeason.number} <span aria-hidden="true">→</span></button>` : `<div class="end-step-concluded">Você chegou à crônica mais recente.</div>`}
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
    postsContainer.querySelectorAll('[data-next-season]').forEach(button=>button.addEventListener('click',async()=>{await activateSeason(button.dataset.nextSeason,undefined,true);focusReader();}));
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
      if (tag === "input" || tag === "textarea" || tag === "select" || tag === "button" || document.activeElement?.isContentEditable) return;

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

  function updateProfileSummary() {
    if (!fichaContainer || !aboutSubEl) return;
    aboutSubEl.textContent = currentState ? "Ficha · Estado registrado no Dia "+currentState.as_of.day : "Ficha · Último estado registrado";
  }
  function preserveContextLinks() {
    if (!currentHero) return;
    const season = activeSeason?.id || new URLSearchParams(location.search).get("season") || localStorage.getItem("active_season:"+currentHero.id);
    document.querySelectorAll('a[href]').forEach(link => {
      const href = link.getAttribute("href");
      if (!/^(index|mapa|ficha|sobre)\.html(?:[?#]|$)/.test(href || "")) return;
      const url = new URL(href,location.href); url.searchParams.set("hero",currentHero.id);
      if (season) url.searchParams.set("season",season);
      const reading = new URLSearchParams(location.search);
      ["day","chapter"].forEach(key => {if (reading.has(key)) url.searchParams.set(key,reading.get(key)); else url.searchParams.delete(key);});
      link.setAttribute("href",url.pathname.split("/").at(-1)+url.search+url.hash);
    });
  }
  function syncReadingUrl() {
    const url = new URL(location.href);
    if (currentHero) url.searchParams.set("hero",currentHero.id);
    if (activeSeason) url.searchParams.set("season",activeSeason.id);
    url.searchParams.delete(isChapterSeason() ? "day" : "chapter");
    const value = isChapterSeason() ? activeChapterId : activeDay;
    if (value !== null) url.searchParams.set(isChapterSeason() ? "chapter" : "day",value);
    history.replaceState({},"",url);
    preserveContextLinks();
  }
  function focusReader(scroll = true) {
    const reader = document.getElementById("leitura");
    if (!reader) return;
    if (matchMedia("(max-width:800px)").matches) document.getElementById("archive-index").open = false;
    reader.focus({preventScroll:true});
    if (scroll) reader.scrollIntoView({behavior:matchMedia("(prefers-reduced-motion:reduce)").matches ? "auto" : "smooth",block:"start"});
  }
  function updateJourneyPresentation() {
    const name = document.getElementById("feature-name");
    if (!name || !currentHero) return;
    name.textContent = currentHero.name;
    name.classList.toggle("is-long",currentHero.name.length>10);
    const seasonName = activeSeason ? seasonTitleShort(activeSeason) : "Arquivo de jornadas";
    document.getElementById("feature-eyebrow").textContent = seasonName;
    document.getElementById("feature-description").textContent = activeSeason?.summary || "Acompanhe as escolhas, os encontros e as marcas de uma jornada em Midgaard.";
    document.getElementById("library-title").textContent = isChapterSeason() ? (activeSeason?.rewrite_of ? "O tomo da primeira temporada" : "Uma nova temporada") : "O diário da jornada";
    const selected = isChapterSeason() ? chaptersData?.chapters?.find(c=>c.id===activeChapterId) : allPosts.find(p=>p.id===activeDay);
    document.getElementById("reader-breadcrumb").textContent = currentHero.name + " / " + (activeSeason ? "Temporada "+activeSeason.number : "Arquivo") + " / " + (selected ? (isChapterSeason() ? (selected.kind === "prologo" ? "Prólogo" : "Capítulo "+selected.id) : "Dia "+selected.id) : "Leitura");
    document.getElementById("feature-read").disabled = isChapterSeason() ? (chaptersLoadError || !chaptersData) : (postsLoadError || !allPosts.length);
    document.getElementById("feature-start").disabled = !allPosts.length;
  }
  document.getElementById("feature-read")?.addEventListener("click",()=>focusReader());
  document.getElementById("feature-start")?.addEventListener("click",async()=>{
    const first = seasonsCatalog?.seasons?.find(s=>s.id==="s01");
    if (first && activeSeason?.id!=="s01") await activateSeason("s01",undefined,true);
    if (first?.model === "capitulos") {
      // A Season 01 agora é um tomo: começa pelo primeiro capítulo, não pelo Dia 1.
      const ids = (chaptersData?.chapters || []).map(c=>c.id);
      if (ids.length) { activeChapterId = Math.min(...ids); syncReadingUrl(); renderChapterView(); updateJourneyPresentation(); focusReader(); }
      return;
    }
    if (allPosts.length) jumpToPost(Math.min(...allPosts.map(p=>p.id)));
  });
  if (matchMedia("(max-width:800px)").matches && document.getElementById("archive-index")) document.getElementById("archive-index").open=false;

  window.addEventListener("popstate", () => {
    const heroId = new URLSearchParams(window.location.search).get("hero");
    const hero = heroesList.find(item => item.id === heroId) || heroesList[0];
    if (!hero) return;
    if (heroSelect) heroSelect.value = hero.id;
    activateHero(hero);
  });
  initHeroes();
});
