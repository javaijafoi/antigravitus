/* mapa_grade.js — o mapa do herói em grade, como mapa de masmorra.
 *
 * Os dados vêm de data/heroes/<id>/mapa_grade.json, derivado do mapa.json pelo
 * scripts/gerar_mapa_grade.py (via sync_hero.py): cada sala já traz número e casa (x, y).
 * Este arquivo só desenha e reage a clique, busca, zoom e arraste.
 *
 * Uso:
 *   - no site (mapa.html): ouve o evento "hero:activated" do main.js e carrega o herói;
 *   - avulso: MapaGrade.montar(elemento, dados).
 */
(function () {
  "use strict";
  const P = 76, S = 52, M = (P - S) / 2, CW = 14;
  const DIR = { n: [0, -1], s: [0, 1], e: [1, 0], w: [-1, 0] };
  const NOME_DIR = { n: "norte", s: "sul", e: "leste", w: "oeste", u: "cima", d: "baixo" };
  const RISCO = {
    safe: ["#4ade80", "seguro"], low: ["#5ec4d6", "baixo"], medium: ["#e5b364", "médio"], high: ["#f08a3c", "alto"],
    danger: ["#f87171", "perigo"], critical: ["#d9468f", "crítico"], fatal: ["#a855f7", "fatal"], unknown: ["#6b778d", "desconhecido"]
  };
  const PERIGOSOS = ["high", "danger", "critical", "fatal"];
  const TIPOS_AVISO = {
    colisao: "Desenhadas fora do lugar", nao_reciproca: "Saídas sem volta", destino_inexistente: "Destino que não existe",
    saida_pendente: "Saídas pendentes", duplicata: "Duplicatas"
  };
  const NS = "http://www.w3.org/2000/svg";

  function esc(t) { return String(t == null ? "" : t).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c])); }
  function el(tag, attrs, pai) { const e = document.createElementNS(NS, tag); for (const k in attrs) e.setAttribute(k, attrs[k]); if (pai) pai.appendChild(e); return e; }
  const cx = s => s.x * P + P / 2, cy = s => s.y * P + P / 2;

  let atual = null;   // a instância montada (uma por página)

  function montar(raiz, D) {
    if (atual) atual.destruir();
    const abortar = new AbortController(), sinal = { signal: abortar.signal };
    raiz.innerHTML =
      '<div class="mg">' +
      '  <div class="mg-abas layers-tabs-wrap" role="tablist" aria-label="Zonas"></div>' +
      '  <div class="mg-barra">' +
      '    <div class="map-search-box mg-busca"><span class="map-search-icon">🔍</span>' +
      '      <input type="search" class="map-search-input" placeholder="Buscar sala por nome ou id…" autocomplete="off" aria-label="Buscar sala">' +
      '      <div class="mg-resultados" hidden></div></div>' +
      '    <button type="button" class="map-btn-tool mg-bt-avisos" title="Lista para validar o mapa"></button>' +
      '  </div>' +
      '  <div class="mg-corpo">' +
      '    <div class="mg-palco">' +
      '      <svg class="mg-svg" xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid meet" aria-label="Mapa da zona">' +
      '        <defs><pattern id="mg-papel" width="8.67" height="8.67" patternUnits="userSpaceOnUse">' +
      '          <rect width="8.67" height="8.67" fill="#efe6d2"/><path d="M8.67 0H0V8.67" fill="none" stroke="#c9b48a" stroke-opacity=".45" stroke-width=".6"/></pattern>' +
      '          <filter id="mg-brilho" x="-30%" y="-30%" width="160%" height="160%"><feDropShadow dx="0" dy="0" stdDeviation="4" flood-color="#e5b364" flood-opacity=".85"/></filter></defs>' +
      '        <g class="mg-corr"></g><g class="mg-salas"></g></svg>' +
      '      <div class="mg-dica" hidden></div>' +
      '      <div class="mg-legenda-risco"></div>' +
      '      <div class="map-floating-controls mg-controles">' +
      '        <button type="button" class="map-ctrl-btn" data-z="in" title="Aproximar">+</button>' +
      '        <button type="button" class="map-ctrl-btn" data-z="out" title="Afastar">−</button>' +
      '        <button type="button" class="map-ctrl-btn" data-z="fit" title="Centralizar a zona">⤢</button></div>' +
      '    </div>' +
      '    <aside class="mg-lado">' +
      '      <section class="mg-detalhe vazio">Clique numa sala para ver o que sabemos dela.</section>' +
      '      <section class="mg-lista"><div class="mg-lista-topo"><strong class="mg-titulo-lista">Legenda</strong>' +
      '        <input type="search" class="map-search-input mg-filtro" placeholder="filtrar" aria-label="Filtrar legenda"></div>' +
      '        <ol class="mg-legenda"></ol></section>' +
      '    </aside>' +
      '  </div>' +
      '</div>';
    const q = s => raiz.querySelector(s);
    const svg = q(".mg-svg"), gCorr = q(".mg-corr"), gSalas = q(".mg-salas"), abas = q(".mg-abas");
    const detalhe = q(".mg-detalhe"), legenda = q(".mg-legenda"), filtro = q(".mg-filtro"), tituloLista = q(".mg-titulo-lista");
    const busca = q(".mg-busca input"), res = q(".mg-resultados"), dica = q(".mg-dica"), btAv = q(".mg-bt-avisos");

    // índices
    const porId = {}, avisosPorSala = {};
    D.zonas.forEach((z, zi) => {
      const conta = {};
      z.salas.forEach(s => { porId[s.id] = { z: zi, s: s }; conta[s.name] = (conta[s.name] || 0) + 1; });
      z.salas.forEach(s => { s.rotulo = conta[s.name] > 1 ? s.name + " (" + s.id + ")" : s.name; });
    });
    D.avisos.forEach(a => { (avisosPorSala[a.sala] = avisosPorSala[a.sala] || []).push(a); });

    let zonaAtual = -1, salaAtual = null, vb = { x: 0, y: 0, w: 100, h: 100 }, modoAvisos = false;
    const nodos = {};

    // abas
    D.zonas.forEach((z, zi) => {
      const b = document.createElement("button");
      b.type = "button"; b.className = "layer-tab-btn"; b.setAttribute("role", "tab"); b.dataset.z = zi;
      b.innerHTML = esc(z.nome) + ' <span class="layer-room-count">' + z.n + "</span>";
      b.onclick = () => abrirZona(zi);
      abas.appendChild(b);
    });
    btAv.innerHTML = "⚠ Avisos <span class=\"layer-room-count\">" + D.avisos.length + "</span>";
    btAv.onclick = () => (modoAvisos ? preencherLegenda(D.zonas[zonaAtual]) : mostrarAvisos());
    q(".mg-legenda-risco").innerHTML = Object.keys(RISCO).map(k => '<span><i style="background:' + RISCO[k][0] + '"></i>' + RISCO[k][1] + "</span>").join("") +
      '<span class="mg-l-torta">┄ corredor torto</span><span>▲▼ escada</span><span class="mg-l-zona">▸ outra zona</span>';

    function marcarAba(i) { [...abas.children].forEach(b => { const s = b.dataset.z == i; b.classList.toggle("active", s); b.setAttribute("aria-selected", String(s)); }); }

    function abrirZona(zi, semAjuste) {
      if (zi === zonaAtual) { if (modoAvisos) preencherLegenda(D.zonas[zi]); if (!semAjuste) ajustar(); return; }
      zonaAtual = zi; marcarAba(zi);
      gCorr.textContent = ""; gSalas.textContent = "";
      for (const k in nodos) delete nodos[k];
      const z = D.zonas[zi], aqui = {};
      z.salas.forEach(s => { aqui[s.id] = s; });
      z.arestas.forEach(e => {
        const a = aqui[e.a], b = aqui[e.b];
        if (e.torta) {
          el("path", { class: "mg-c torta", d: "M" + cx(a) + " " + cy(a) + "L" + cx(b) + " " + cy(a) + "L" + cx(b) + " " + cy(b) }, gCorr);
        } else {
          el("line", { class: "mg-c", "stroke-width": CW, x1: cx(a), y1: cy(a), x2: cx(b), y2: cy(b) }, gCorr);
          const mx = (cx(a) + cx(b)) / 2, my = (cy(a) + cy(b)) / 2, hz = a.y === b.y;
          [-1, 1].forEach(sg => {
            const px = hz ? mx + sg * (P / 2 - M) : mx, py = hz ? my : my + sg * (P / 2 - M);
            el("rect", { class: "mg-porta", x: px - 3.5, y: py - 3.5, width: 7, height: 7 }, gCorr);
          });
        }
      });
      z.salas.forEach(s => {
        const x = s.x * P + M, y = s.y * P + M, ex = s.exits || {};
        const g = el("g", { class: "mg-sala", "data-id": s.id, tabindex: 0, role: "button", "aria-label": s.num + " " + s.rotulo }, gSalas);
        el("rect", { class: "mg-chao", x: x, y: y, width: S, height: S, rx: 2.5, fill: "url(#mg-papel)" }, g);
        el("text", { class: "mg-num", x: x + 5, y: y + 18 }, g).textContent = s.num;
        const r = RISCO[s.risk_code] || RISCO.unknown;
        el("circle", { cx: x + S - 7, cy: y + 7, r: 4.2, fill: r[0], stroke: "#0a0d14", "stroke-width": 1 }, g);
        if (s.icon) el("text", { class: "mg-ico", x: x + S - 16, y: y + S - 5 }, g).textContent = s.icon;
        const escada = (ex.u ? "▲" : "") + (ex.d ? "▼" : "");
        if (escada) el("text", { class: "mg-esc", x: x + 5, y: y + S - 6 }, g).textContent = escada;
        if (avisosPorSala[s.id]) el("text", { class: "mg-alerta", x: x + S - 12, y: y + 25 }, g).textContent = "!";
        if (s.id === D.santuario) el("rect", { class: "mg-santuario", x: x - 4, y: y - 4, width: S + 8, height: S + 8, rx: 5 }, g);
        if (s.id === D.atual) el("circle", { class: "mg-aqui", cx: x + S / 2, cy: y + S / 2 + 6, r: 5 }, g);
        if (ex.u && aqui[ex.u]) el("line", { class: "mg-escada", x1: cx(s), y1: cy(s), x2: cx(aqui[ex.u]), y2: cy(aqui[ex.u]) }, gCorr);
        if (ex.d && aqui[ex.d] && (aqui[ex.d].exits || {}).u !== s.id) el("line", { class: "mg-escada", x1: cx(s), y1: cy(s), x2: cx(aqui[ex.d]), y2: cy(aqui[ex.d]) }, gCorr);
        Object.keys(ex).forEach(d => {
          if (!DIR[d]) return;
          const alvo = porId[ex[d]];
          if (!alvo || alvo.z === zi) return;
          const [dx, dy] = DIR[d], ox = cx(s) + dx * S / 2, oy = cy(s) + dy * S / 2;
          el("line", { class: "mg-toco", x1: ox, y1: oy, x2: ox + dx * 13, y2: oy + dy * 13 }, gCorr);
          const ax = ox + dx * 16, ay = oy + dy * 16;
          el("path", { class: "mg-seta", d: "M" + (ax + dx * 6) + " " + (ay + dy * 6) + "L" + (ax - dy * 5) + " " + (ay + dx * 5) + "L" + (ax + dy * 5) + " " + (ay - dx * 5) + "Z" }, gCorr);
        });
        g.addEventListener("click", ev => { if (!arrastou) selecionar(s.id); ev.stopPropagation(); });
        g.addEventListener("keydown", ev => { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); selecionar(s.id); } });
        g.addEventListener("pointerenter", () => mostrarDica(s));
        g.addEventListener("pointerleave", () => { dica.hidden = true; });
        nodos[s.id] = g;
      });
      preencherLegenda(z);
      if (salaAtual && porId[salaAtual] && porId[salaAtual].z === zi) nodos[salaAtual].classList.add("sel");
      if (!semAjuste) ajustar();
    }

    function preencherLegenda(z) {
      modoAvisos = false; btAv.classList.remove("active");
      tituloLista.textContent = "Legenda · " + z.nome;
      filtro.hidden = false;
      const f = filtro.value.trim().toLowerCase();
      legenda.textContent = "";
      z.salas.forEach(s => {
        if (f && !(s.name.toLowerCase().includes(f) || s.id.toLowerCase().includes(f) || String(s.num) === f)) return;
        const li = document.createElement("li"), b = document.createElement("button");
        b.type = "button"; b.dataset.id = s.id; if (s.id === salaAtual) b.className = "sel";
        b.innerHTML = '<span class="n">' + s.num + "</span><span>" + esc(s.rotulo) + "</span>" + (avisosPorSala[s.id] ? '<span class="t">⚠</span>' : "");
        b.onclick = () => selecionar(s.id, true);
        li.appendChild(b); legenda.appendChild(li);
      });
    }
    filtro.addEventListener("input", () => { if (zonaAtual >= 0) preencherLegenda(D.zonas[zonaAtual]); });

    function mostrarAvisos() {
      modoAvisos = true; btAv.classList.add("active");
      tituloLista.textContent = "Avisos de validação (" + D.avisos.length + ")";
      filtro.hidden = true;
      legenda.textContent = "";
      Object.keys(TIPOS_AVISO).forEach(tipo => {
        const lista = D.avisos.filter(a => a.tipo === tipo);
        if (!lista.length) return;
        const h = document.createElement("li"); h.className = "mg-grupo"; h.textContent = TIPOS_AVISO[tipo] + " · " + lista.length; legenda.appendChild(h);
        lista.forEach(a => {
          const info = porId[a.sala], li = document.createElement("li"), b = document.createElement("button");
          b.type = "button";
          b.innerHTML = '<span class="n">' + (info ? info.s.num : "?") + "</span><span>" + esc(info ? info.s.rotulo : a.sala) + " — <small>" + esc(a.texto) + "</small></span>" +
            '<span class="t">' + esc(info ? D.zonas[info.z].nome : "") + "</span>";
          b.onclick = () => selecionar(a.sala, true);
          li.appendChild(b); legenda.appendChild(li);
        });
      });
    }

    function selecionar(id, centrar) {
      const info = porId[id];
      if (!info) return;
      if (info.z !== zonaAtual) abrirZona(info.z, true);
      if (salaAtual && nodos[salaAtual]) nodos[salaAtual].classList.remove("sel");
      salaAtual = id;
      nodos[id].classList.add("sel");
      legenda.querySelectorAll("button.sel").forEach(b => b.classList.remove("sel"));
      const lb = legenda.querySelector('button[data-id="' + CSS.escape(id) + '"]');
      if (lb) { lb.classList.add("sel"); lb.scrollIntoView({ block: "nearest" }); }
      painel(info);
      if (centrar) centrarEm(info.s);
      try { const u = new URL(location.href); u.hash = "sala=" + encodeURIComponent(id); history.replaceState(null, "", u); } catch (e) { /* file:// sem history */ }
    }

    function chips(v) { return (v && v.length) ? v.map(x => '<span class="mg-chip">' + esc(x) + "</span>").join("") : "—"; }

    function painel(info) {
      const s = info.s, z = D.zonas[info.z], r = RISCO[s.risk_code] || RISCO.unknown, ex = s.exits || {};
      const ordem = ["n", "e", "s", "w", "u", "d"].filter(d => d in ex).concat(Object.keys(ex).filter(d => !NOME_DIR[d]));
      const saidas = ordem.map(d => {
        const alvo = porId[ex[d]];
        if (!alvo) return '<div class="mg-saida morta"><b>' + esc(NOME_DIR[d] || d) + "</b><span>" + esc(ex[d]) + " <small>(não está no mapa)</small></span></div>";
        const outra = alvo.z !== info.z ? " <small>· " + esc(D.zonas[alvo.z].nome) + "</small>" : "";
        return '<button type="button" class="mg-saida" data-ir="' + esc(ex[d]) + '"><b>' + esc(NOME_DIR[d] || d) + "</b><span>" + alvo.s.num + " · " + esc(alvo.s.rotulo) + outra + "</span></button>";
      }).join("") || "—";
      const fontes = [].concat(s.fontes || [], s.source ? [s.source] : []);
      const linhas = [["Zona", esc(z.nome)], ["Camada", esc(s.layer)],
        ["Risco", '<span class="mg-chip" style="background:' + r[0] + ';color:#0a0d14">' + esc(r[1]) + "</span> " + esc(s.risk || "")],
        ["Saídas", saidas], ["NPCs", chips(s.npcs)]];
      if (s.npcs_confirmados) linhas.push(["Confirmados", chips(s.npcs_confirmados)]);
      linhas.push(["Notas", esc(s.notes) || "—"], ["Descoberta", esc(s.discovered_in) || "—"],
        ["Visitas", s.visitas_registradas != null ? s.visitas_registradas : "—"], ["Fontes", chips(fontes)]);
      if (s.aliases) linhas.push(["Também", chips(s.aliases)]);
      if (s.unresolved_exits) linhas.push(["Pendentes", chips(s.unresolved_exits)]);
      if (s.duplicata_de) linhas.push(["Duplicata de", esc(s.duplicata_de)]);
      linhas.push(["id", "<code>" + esc(s.id) + "</code>"]);
      const av = (avisosPorSala[s.id] || []).map(a => "<div>⚠ " + esc(a.texto) + "</div>").join("");
      detalhe.classList.remove("vazio");
      detalhe.innerHTML = '<h3><span class="mg-n">' + s.num + "</span>" + esc(s.icon || "") + " " + esc(s.name) + "</h3>" +
        (s.id === D.santuario ? '<span class="mg-chip mg-ouro">santuário</span>' : "") + (s.id === D.atual ? '<span class="mg-chip mg-ouro">última posição registrada</span>' : "") +
        "<dl>" + linhas.map(l => "<dt>" + l[0] + "</dt><dd>" + l[1] + "</dd>").join("") + "</dl>" + (av ? '<div class="mg-aviso-sala">' + av + "</div>" : "");
      detalhe.querySelectorAll("[data-ir]").forEach(b => { b.onclick = () => selecionar(b.dataset.ir, true); });
    }

    function mostrarDica(s) {
      const r = svg.getBoundingClientRect(), m = svg.getScreenCTM();
      dica.textContent = s.num + " · " + s.rotulo;
      dica.style.left = (m.a * cx(s) + m.e - r.left) + "px";
      dica.style.top = (m.d * (s.y * P + M) + m.f - r.top) + "px";
      dica.hidden = false;
    }

    // pan e zoom pelo viewBox
    function aplicar() { svg.setAttribute("viewBox", vb.x + " " + vb.y + " " + vb.w + " " + vb.h); }
    function paraMapa(px, py) { const m = svg.getScreenCTM().inverse(); return { x: m.a * px + m.e, y: m.d * py + m.f }; }
    function proporcao() { const r = svg.getBoundingClientRect(); return r.width / Math.max(r.height, 1) || 1.6; }
    function ajustar() {
      const z = D.zonas[zonaAtual], pad = P * .6, ar = proporcao();
      vb = { x: -pad, y: -pad, w: z.largura * P + 2 * pad, h: z.altura * P + 2 * pad };
      if (vb.w / vb.h < ar) { const w = vb.h * ar; vb.x -= (w - vb.w) / 2; vb.w = w; } else { const h = vb.w / ar; vb.y -= (h - vb.h) / 2; vb.h = h; }
      aplicar();
    }
    function zoom(f, px, py) {
      const r = svg.getBoundingClientRect();
      const c = (px == null) ? paraMapa(r.left + r.width / 2, r.top + r.height / 2) : paraMapa(px, py);
      const nw = Math.min(Math.max(vb.w * f, P * 3), P * 400), k = nw / vb.w;
      vb = { x: c.x - (c.x - vb.x) * k, y: c.y - (c.y - vb.y) * k, w: nw, h: vb.h * k };
      aplicar();
    }
    function centrarEm(s) {
      const w = Math.min(vb.w, P * 14), h = w / proporcao();
      vb = { x: cx(s) - w / 2, y: cy(s) - h / 2, w: w, h: h };
      aplicar();
    }
    svg.addEventListener("wheel", ev => { ev.preventDefault(); zoom(ev.deltaY > 0 ? 1.15 : 1 / 1.15, ev.clientX, ev.clientY); }, { passive: false });
    let arrasto = null, arrastou = false;
    svg.addEventListener("pointerdown", ev => { arrasto = { x: ev.clientX, y: ev.clientY, vx: vb.x, vy: vb.y }; arrastou = false; });
    window.addEventListener("pointermove", ev => {
      if (!arrasto) return;
      const dx = ev.clientX - arrasto.x, dy = ev.clientY - arrasto.y;
      if (!arrastou && Math.hypot(dx, dy) < 4) return;
      if (!arrastou) { arrastou = true; svg.classList.add("arrastando"); }
      const k = vb.w / svg.getBoundingClientRect().width;
      vb.x = arrasto.vx - dx * k; vb.y = arrasto.vy - dy * k; aplicar();
    }, sinal);
    window.addEventListener("pointerup", () => { arrasto = null; svg.classList.remove("arrastando"); setTimeout(() => { arrastou = false; }, 0); }, sinal);
    window.addEventListener("resize", () => { if (zonaAtual >= 0) ajustar(); }, sinal);
    raiz.querySelectorAll(".mg-controles [data-z]").forEach(b => {
      b.onclick = () => (b.dataset.z === "in" ? zoom(1 / 1.3) : b.dataset.z === "out" ? zoom(1.3) : ajustar());
    });

    // busca em todas as zonas
    busca.addEventListener("input", () => {
      const t = busca.value.trim().toLowerCase();
      res.textContent = "";
      if (!t) { res.hidden = true; return; }
      const achados = [];
      D.zonas.forEach(z => z.salas.forEach(s => { if (s.name.toLowerCase().includes(t) || s.id.toLowerCase().includes(t)) achados.push([z, s]); }));
      achados.slice(0, 40).forEach(([z, s]) => {
        const b = document.createElement("button"); b.type = "button";
        b.innerHTML = "<b>" + s.num + "</b> · " + esc(s.rotulo) + " <small>· " + esc(z.nome) + "</small>";
        b.onclick = () => { res.hidden = true; busca.value = ""; selecionar(s.id, true); };
        res.appendChild(b);
      });
      if (!achados.length) res.innerHTML = '<button type="button" disabled>nenhuma sala</button>';
      res.hidden = false;
    });
    document.addEventListener("click", ev => { if (!ev.target.closest || !ev.target.closest(".mg-busca")) res.hidden = true; }, sinal);

    // início: #sala=<id>, ou a zona do santuário
    const m = location.hash.match(/sala=([^&]+)/), inicio = m && porId[decodeURIComponent(m[1])];
    if (inicio) { abrirZona(inicio.z); selecionar(inicio.s.id, true); }
    else abrirZona(porId[D.santuario] ? porId[D.santuario].z : 0);

    atual = { destruir() { abortar.abort(); raiz.textContent = ""; atual = null; }, selecionar, abrirZona };
    return atual;
  }

  function resumo(D) {
    let seguras = 0, perigosas = 0;
    D.zonas.forEach(z => z.salas.forEach(s => {
      if (s.risk_code === "safe") seguras++;
      if (PERIGOSOS.includes(s.risk_code)) perigosas++;
    }));
    return { salas: D.total, zonas: D.zonas.length, seguras, perigosas };
  }

  // no site: o main.js avisa qual herói está ativo
  let versao = 0;
  document.addEventListener("hero:activated", async ev => {
    const raiz = document.getElementById("mapa-grade");
    if (!raiz) return;
    const hero = ev.detail && ev.detail.hero;
    if (!hero) return;
    const minha = ++versao;
    const titulo = document.getElementById("map-hero-title"), ciclo = document.getElementById("map-cycle-text");
    const sub = document.getElementById("map-hero-sub");
    if (titulo) titulo.textContent = "🗺️ Mapa de " + hero.name;
    if (sub) sub.textContent = "Salas, corredores e perigos registrados por " + hero.name + ", zona por zona. Clique numa sala para ver o que sabemos dela.";
    raiz.innerHTML = '<p class="mg-carregando">Carregando o mapa de ' + esc(hero.name) + "…</p>";
    try {
      const r = await fetch("data/heroes/" + encodeURIComponent(hero.id) + "/mapa_grade.json");
      if (!r.ok) throw new Error("HTTP " + r.status);
      const D = await r.json();
      if (minha !== versao) return;
      montar(raiz, D);
      const n = resumo(D), set = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v; };
      set("stat-rooms-count", n.salas); set("stat-zones-count", n.zonas); set("stat-safe-count", n.seguras); set("stat-danger-count", n.perigosas);
      if (ciclo) ciclo.textContent = D.dia ? "Registro do Dia " + D.dia : "Registro sem data";
    } catch (e) {
      if (minha !== versao) return;
      if (atual) atual.destruir();
      raiz.innerHTML = '<p class="mg-carregando">Ainda não há mapa em grade para ' + esc(hero.name) + ".</p>";
      if (ciclo) ciclo.textContent = "Registro indisponível";
    }
  });

  window.MapaGrade = { montar, resumo };
})();
