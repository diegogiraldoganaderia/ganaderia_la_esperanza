"""
reporte_crias.py
Genera un reporte HTML interactivo (un solo archivo) a partir del dataframe de crías.

Columnas esperadas: FINCA, TORO, VACA, FECHA_NACIMIENTO, RAZA, SEXO, T_C
T_C: CN = natural, IA = inseminación artificial, TE = transferencia de embriones

Uso en Streamlit:

    import streamlit as st
    import streamlit.components.v1 as components
    from reporte_crias import generar_reporte_html

    if st.button("Generar reporte de crías"):
        st.session_state["reporte_html"] = generar_reporte_html(df)

    if "reporte_html" in st.session_state:
        st.download_button(
            "Descargar reporte HTML",
            data=st.session_state["reporte_html"],
            file_name="reporte_crias.html",
            mime="text/html",
        )
        components.html(st.session_state["reporte_html"], height=1500, scrolling=True)
"""

import json
from datetime import datetime

import pandas as pd

COLUMNAS = ["FINCA", "TORO", "VACA", "FECHA_NACIMIENTO", "RAZA", "SEXO", "T_C"]


def _preparar(df: pd.DataFrame) -> list:
    faltantes = [c for c in COLUMNAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el dataframe: {faltantes}")

    d = df[COLUMNAS].copy()

    # Texto limpio
    for c in ["FINCA", "TORO", "VACA", "RAZA", "SEXO"]:
        d[c] = d[c].astype("string").str.strip().str.lower().fillna("sin dato")
        d[c] = d[c].replace("", "sin dato")
    d["T_C"] = d["T_C"].astype("string").str.strip().str.upper().fillna("SIN DATO")
    d["T_C"] = d["T_C"].replace("", "SIN DATO")

    # Fechas
    fecha = pd.to_datetime(d["FECHA_NACIMIENTO"], errors="coerce")
    d["fecha"] = fecha.dt.strftime("%Y-%m-%d").fillna("")
    d["anio"] = fecha.dt.year.astype("Int64").astype("string").fillna("sin fecha")
    d["mes"] = fecha.dt.month.astype("Int64").astype("string").fillna("")

    registros = pd.DataFrame(
        {
            "fecha": d["fecha"],
            "anio": d["anio"],
            "mes": d["mes"],
            "finca": d["FINCA"],
            "toro": d["TORO"],
            "vaca": d["VACA"],
            "raza": d["RAZA"],
            "sexo": d["SEXO"],
            "tc": d["T_C"],
        }
    )
    return registros.astype(object).to_dict(orient="records")


def generar_reporte_html(df: pd.DataFrame, titulo: str = "REPORTE CRÍAS") -> str:
    """Devuelve el HTML completo del reporte como string."""
    datos = _preparar(df)
    datos_json = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    generado = datetime.now().strftime("%Y-%m-%d %H:%M")
    return (
        _PLANTILLA.replace("__DATA__", datos_json)
        .replace("__TITULO__", titulo)
        .replace("__GENERADO__", generado)
    )


_PLANTILLA = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITULO__</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
  :root{
    --bg:#f6f7f4; --card:#ffffff; --txt:#1d2a1f; --muted:#6b786d; --line:#dfe4dc;
    --accent:#2f6b3a; --chip:#eef2ec; --chip-on:#2f6b3a; --chip-on-txt:#ffffff;
  }
  @media (prefers-color-scheme: dark){
    :root{
      --bg:#0f1511; --card:#18211b; --txt:#e6ece6; --muted:#97a69a; --line:#2a362d;
      --accent:#6fbf7d; --chip:#223027; --chip-on:#6fbf7d; --chip-on-txt:#0f1511;
    }
  }
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--txt);font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:14px}
  header{padding:20px 24px 4px}
  h1{margin:0;font-size:22px}
  .sub{color:var(--muted);margin-top:4px}
  main{padding:16px 24px 40px;max-width:1400px;margin:0 auto}
  .card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
  .filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:12px;margin-bottom:14px}
  .filters h3{margin:0 0 8px;font-size:12px;text-transform:uppercase;letter-spacing:.05em;color:var(--muted)}
  .chips{display:flex;flex-wrap:wrap;gap:6px}
  .chip{border:1px solid var(--line);background:var(--chip);color:var(--txt);border-radius:999px;padding:4px 11px;cursor:pointer;font-size:13px}
  .chip.on{background:var(--chip-on);color:var(--chip-on-txt);border-color:var(--chip-on)}
  .toolbar{display:flex;gap:10px;align-items:center;margin-bottom:14px;flex-wrap:wrap}
  button.act{background:var(--accent);color:var(--chip-on-txt);border:0;border-radius:8px;padding:7px 14px;cursor:pointer;font-size:13px}
  button.sec{background:transparent;color:var(--txt);border:1px solid var(--line);border-radius:8px;padding:7px 14px;cursor:pointer;font-size:13px}
  .kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px;margin-bottom:14px}
  .kpi .v{font-size:26px;font-weight:600}
  .kpi .l{color:var(--muted);font-size:12px;margin-top:2px}
  .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(380px,1fr));gap:14px;margin-bottom:14px}
  .grid h3{margin:0 0 10px;font-size:14px}
  .box{position:relative;height:280px}
  .tablewrap{overflow-x:auto}
  table{width:100%;border-collapse:collapse}
  th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
  th{cursor:pointer;color:var(--muted);font-weight:600;user-select:none}
  input[type=search]{background:var(--card);color:var(--txt);border:1px solid var(--line);border-radius:8px;padding:7px 10px;min-width:220px}
  .note{color:var(--muted);font-size:12px;margin-top:8px}
  .pivot td.n,.pivot th.n{text-align:right}
</style>
</head>
<body>
<header>
  <h1>__TITULO__</h1>
  <div class="sub">GENERADO EL __GENERADO__</div>
</header>
<main>
<header style="display: flex; justify-content: center;">
  <h1>FILTROS</h1>
</header>

  <div class="filters" id="filters"></div>
  <div class="toolbar">
    <button class="sec" id="reset">LIMPIAR FILTROS</button>
    <button class="act" id="csv">Descargar CSV filtrado</button>
    <span class="sub" id="status"></span>
  </div>

<!-- SE MUESTRAN LOS TOTALES CN LA FUNCION KPI -->

  <header style="display: flex; justify-content: center;">
  <h1>DATOS TOTALIZADOS</h1>
  </header>
  <div class="kpis" id="kpis"></div>

  <header style="display: flex; justify-content: center;">
  <h1>GRÁFICOS</h1>
  </header>
  <div class="grid">
    <div class="card"><h3>CRÍAS NACIDAS POR AÑO</h3><div class="box"><canvas id="c_anio_sexo"></canvas></div></div>
    <div class="card"><h3>NÚMERO DE CRÍAS POR TIPO DE CONCEPCIÓN</h3><div class="box"><canvas id="c_anio_tc"></canvas></div></div>
    <div class="card"><h3>CRÍAZ POR RAZA</h3><div class="box"><canvas id="c_raza"></canvas></div></div>
    <div class="card"><h3>DISTRIBUCIÓN POR TIPO DE CONCEPCIÓN</h3><div class="box"><canvas id="c_tc"></canvas></div></div>
    <div class="card"><h3>DISTRIBUCIÓN POR SEXO</h3><div class="box"><canvas id="c_sexo"></canvas></div></div>
    <div class="card"><h3>CRÍAS POR MES</h3><div class="box"><canvas id="c_mes"></canvas></div></div>
    <div class="card"><h3>TOROS CON MÁS CRÍAS (top 10)</h3><div class="box"><canvas id="c_toro"></canvas></div></div>
    <div class="card"><h3>CRÍAS POR FINCA</h3><div class="box"><canvas id="c_finca"></canvas></div></div>
  </div>

  <div class="card" style="margin-bottom:14px">
    <h3 style="margin:0 0 10px;font-size:14px">RESUMEN POR AÑO</h3>
    <div class="tablewrap"><table class="pivot" id="pivot"></table></div>
  </div>

  <div class="card">
    <div class="toolbar">
      <h3 style="margin:0;font-size:14px">DETALLE DE CRÍAS</h3>
      <input type="search" id="q" placeholder="Buscar toro, vaca, raza...">
    </div>
    <div class="tablewrap"><table id="tabla"></table></div>
    <div class="note" id="tnote"></div>
  </div>
</main>

<script>
const DATA = __DATA__;
const TC_LABEL = {CN:'Natural', IA:'Inseminación artificial', TE:'Transferencia de embriones'};
const MESES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
const PALETA = ['#2f6b3a','#d98c2b','#3b7ea1','#b5523b','#7a5c99','#6b9e8a','#c2a33a','#8a8f98','#a14d73','#4c6f9b'];
const DIMS = {anio:'Año', raza:'Raza', finca:'Finca', sexo:'Sexo', tc:'Concepción'};
const sel = {}; Object.keys(DIMS).forEach(k => sel[k] = new Set());
const charts = {};
let sortKey = 'fecha', sortDir = -1;

const tcName = v => TC_LABEL[v] || v;
const lab = (dim, v) => dim === 'tc' ? tcName(v) : v;
const cap = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
const cmp = (a,b) => (isNaN(a)||isNaN(b)) ? String(a).localeCompare(String(b),'es') : Number(a)-Number(b);

function uniq(dim){ return [...new Set(DATA.map(r => String(r[dim])))].sort(cmp); }

function filtered(){
  return DATA.filter(r => Object.keys(sel).every(k => sel[k].size === 0 || sel[k].has(String(r[k]))));
}
function countBy(rows, fn){
  const m = new Map();
  rows.forEach(r => { const k = fn(r); m.set(k, (m.get(k)||0)+1); });
  return m;
}
function pct(a,b){ return b ? (100*a/b).toFixed(1)+'%' : '-'; }

function buildFilters(){
  const root = document.getElementById('filters');
  root.innerHTML = '';
  Object.keys(DIMS).forEach(dim => {
    const card = document.createElement('div'); card.className = 'card';
    card.innerHTML = '<h3>'+DIMS[dim]+'</h3>';
    const wrap = document.createElement('div'); wrap.className = 'chips';
    uniq(dim).forEach(v => {
      const b = document.createElement('button'); b.className = 'chip';
      b.textContent = cap(lab(dim, v)); b.dataset.dim = dim; b.dataset.val = v;
      b.onclick = () => { sel[dim].has(v) ? sel[dim].delete(v) : sel[dim].add(v); render(); };
      wrap.appendChild(b);
    });
    card.appendChild(wrap); root.appendChild(card);
  });
}
function syncChips(){
  document.querySelectorAll('.chip').forEach(b => b.classList.toggle('on', sel[b.dataset.dim].has(b.dataset.val)));
}

function draw(id, config){
  if (charts[id]) charts[id].destroy();
  charts[id] = new Chart(document.getElementById(id), config);
}
function stacked(id, rows, xs, groupFn, groups, groupLabel, horizontal, xKey){
  const datasets = groups.map((g,i) => ({
    label: groupLabel(g),
    data: xs.map(x => rows.filter(r => String(r[xKey]) === x && groupFn(r) === g).length),
    backgroundColor: PALETA[i % PALETA.length]
  }));
  draw(id, {type:'bar', data:{labels: xs.map(cap), datasets},
    options:{indexAxis: horizontal ? 'y' : 'x', responsive:true, maintainAspectRatio:false,
      scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{precision:0}}}}});
}
function pie(id, map, labelFn){
  const keys = [...map.keys()];
  draw(id, {type:'doughnut', data:{labels: keys.map(k => cap(labelFn(k))),
    datasets:[{data: keys.map(k => map.get(k)), backgroundColor: keys.map((k,i) => PALETA[i % PALETA.length])}]},
    options:{responsive:true, maintainAspectRatio:false}});
}

function render(){
  syncChips();
  const rows = filtered();
  document.getElementById('status').textContent = rows.length + ' de ' + DATA.length + ' crías con los filtros actuales';

  // KPIs
  const m = rows.filter(r => r.sexo === 'macho').length;
  const h = rows.filter(r => r.sexo === 'hembra').length;
  const cn = rows.filter(r => r.tc === 'CN').length;
  const ia = rows.filter(r => r.tc === 'IA').length;
  const te = rows.filter(r => r.tc === 'TE').length;
  const kp = [
    [rows.length,'Total de crías'], [m,'Machos ('+pct(m,rows.length)+')'], [h,'Hembras ('+pct(h,rows.length)+')'],
    [cn,'Natural ('+pct(cn,rows.length)+')'], [ia,'Inseminación ('+pct(ia,rows.length)+')'], [te,'Embriones ('+pct(te,rows.length)+')'],
    [new Set(rows.map(r=>r.vaca)).size,'Vacas distintas'], [new Set(rows.map(r=>r.toro)).size,'Toros distintos']
  ];
  document.getElementById('kpis').innerHTML = kp.map(k =>
    '<div class="card kpi"><div class="v">'+k[0]+'</div><div class="l">'+k[1]+'</div></div>').join('');

  const anios = [...new Set(rows.map(r => String(r.anio)))].sort(cmp);
  const sexos = [...new Set(rows.map(r => r.sexo))].sort();
  const tcs = [...new Set(rows.map(r => r.tc))].sort();
  const razas = [...new Set(rows.map(r => r.raza))].sort();
  const fincas = [...new Set(rows.map(r => r.finca))].sort();

  stacked('c_anio_sexo', rows, anios, r => r.sexo, sexos, cap, false, 'anio');
  stacked('c_anio_tc', rows, anios, r => r.tc, tcs, tcName, false, 'anio');
  stacked('c_raza', rows, razas, r => r.sexo, sexos, cap, true, 'raza');
  stacked('c_finca', rows, anios, r => r.finca, fincas, cap, false, 'anio');
  pie('c_tc', countBy(rows, r => r.tc), tcName);
  pie('c_sexo', countBy(rows, r => r.sexo), x => x);

  const mesCnt = MESES.map((_,i) => rows.filter(r => r.mes === String(i+1)).length);
  draw('c_mes', {type:'bar', data:{labels:MESES, datasets:[{label:'Crías', data:mesCnt, backgroundColor:PALETA[0]}]},
    options:{responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true, ticks:{precision:0}}}}});

  const top = [...countBy(rows, r => r.toro).entries()].sort((a,b) => b[1]-a[1]).slice(0,10);
  draw('c_toro', {type:'bar', data:{labels: top.map(t => cap(t[0])), datasets:[{label:'Crías', data: top.map(t => t[1]), backgroundColor:PALETA[1]}]},
    options:{indexAxis:'y', responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{x:{beginAtZero:true, ticks:{precision:0}}}}});

  // Tabla resumen por año
  let ph = '<tr><th>Año</th><th class="n">Total</th><th class="n">Machos</th><th class="n">Hembras</th><th class="n">% hembras</th><th class="n">CN</th><th class="n">IA</th><th class="n">TE</th></tr>';
  anios.forEach(a => {
    const rr = rows.filter(r => String(r.anio) === a);
    const mm = rr.filter(r => r.sexo==='macho').length, hh = rr.filter(r => r.sexo==='hembra').length;
    ph += '<tr><td>'+a+'</td><td class="n">'+rr.length+'</td><td class="n">'+mm+'</td><td class="n">'+hh+'</td><td class="n">'+pct(hh,rr.length)+
      '</td><td class="n">'+rr.filter(r=>r.tc==='CN').length+'</td><td class="n">'+rr.filter(r=>r.tc==='IA').length+
      '</td><td class="n">'+rr.filter(r=>r.tc==='TE').length+'</td></tr>';
  });
  document.getElementById('pivot').innerHTML = ph;

  renderTable(rows);
}

const COLS = [['fecha','Fecha'],['finca','Finca'],['toro','Toro'],['vaca','Vaca'],['raza','Raza'],['sexo','Sexo'],['tc','Concepción']];
function renderTable(rows){
  const q = document.getElementById('q').value.trim().toLowerCase();
  let rr = rows;
  if (q) rr = rr.filter(r => [r.toro,r.vaca,r.raza,r.finca,r.sexo,r.tc].join(' ').toLowerCase().includes(q));
  rr = [...rr].sort((a,b) => sortDir * String(a[sortKey]).localeCompare(String(b[sortKey]),'es'));
  const MAX = 300;
  let html = '<tr>' + COLS.map(c => '<th data-k="'+c[0]+'">'+c[1]+(sortKey===c[0] ? (sortDir>0?' ▲':' ▼') : '')+'</th>').join('') + '</tr>';
  rr.slice(0, MAX).forEach(r => {
    html += '<tr><td>'+r.fecha+'</td><td>'+r.finca+'</td><td>'+r.toro+'</td><td>'+r.vaca+'</td><td>'+r.raza+'</td><td>'+r.sexo+'</td><td>'+tcName(r.tc)+'</td></tr>';
  });
  document.getElementById('tabla').innerHTML = html;
  document.getElementById('tnote').textContent = rr.length > MAX
    ? 'Se muestran las primeras '+MAX+' de '+rr.length+' filas. Usa los filtros o descarga el CSV para ver todas.'
    : rr.length + ' filas.';
  document.querySelectorAll('#tabla th').forEach(th => th.onclick = () => {
    const k = th.dataset.k; sortDir = (sortKey === k) ? -sortDir : 1; sortKey = k; renderTable(filtered());
  });
}

document.getElementById('q').addEventListener('input', () => renderTable(filtered()));
document.getElementById('reset').onclick = () => { Object.values(sel).forEach(s => s.clear()); document.getElementById('q').value=''; render(); };
document.getElementById('csv').onclick = () => {
  const rows = filtered();
  const esc = v => '"' + String(v).replace(/"/g,'""') + '"';
  const csv = ['FECHA_NACIMIENTO,FINCA,TORO,VACA,RAZA,SEXO,T_C'].concat(
    rows.map(r => [r.fecha,r.finca,r.toro,r.vaca,r.raza,r.sexo,r.tc].map(esc).join(','))).join('\n');
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob(['\ufeff'+csv], {type:'text/csv;charset=utf-8'}));
  a.download = 'crias_filtradas.csv'; a.click();
};

Chart.defaults.color = getComputedStyle(document.body).color;
Chart.defaults.borderColor = getComputedStyle(document.documentElement).getPropertyValue('--line');
buildFilters();
render();
</script>
</body>
</html>
"""
