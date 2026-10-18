import json
from datetime import datetime

import pandas as pd


#NACIMINETOS



def _preparar_nacimiento(df: pd.DataFrame, vaca_por_finca: bool = False) -> list:
    COLUMNAS = ["FINCA", "TORO", "VACA", "FECHA_NACIMIENTO", "RAZA", "SEXO", "TC_GG_O"]
    faltantes = [c for c in COLUMNAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el dataframe: {faltantes}")

    d = df[COLUMNAS].copy()

    for c in ["FINCA", "TORO", "VACA", "RAZA", "SEXO"]:
        d[c] = d[c].astype("string").str.strip().str.lower().fillna("sin dato")
        d[c] = d[c].replace("", "sin dato")

    d["TC_GG_O"] = d["TC_GG_O"].astype("string").str.strip().str.upper().fillna("SIN DATO")
    d["TC_GG_O"] = d["TC_GG_O"].replace("", "SIN DATO")

    fecha = pd.to_datetime(d["FECHA_NACIMIENTO"], errors="coerce")
    d["fecha"] = fecha.dt.strftime("%Y-%m-%d").fillna("")
    d["anio"] = fecha.dt.year.astype("Int64").astype("string").fillna("sin fecha")
    d["mes"] = fecha.dt.month.astype("Int64").astype("string").fillna("")

    # Intervalo entre partos: días desde el parto anterior de la misma vaca.
    # Se calcula con todo el historial de cada vaca; las crías con la misma fecha
    # (mellizos) cuentan como un solo parto.
    clave = d["FINCA"] + "|" + d["VACA"] if vaca_por_finca else d["VACA"]
    base = pd.DataFrame({"clave": clave.astype(object), "fecha": fecha})
    valido = fecha.notna() & (d["VACA"] != "sin dato")
    eventos = base[valido].drop_duplicates().sort_values(["clave", "fecha"]).copy()
    eventos["intervalo"] = eventos.groupby("clave")["fecha"].diff().dt.days
    con_intervalo = base.merge(eventos, on=["clave", "fecha"], how="left")["intervalo"]
    es_evento = valido & ~base.duplicated(["clave", "fecha"])

    registros = pd.DataFrame({
        "fecha": d["fecha"],
        "anio": d["anio"],
        "mes": d["mes"],
        "finca": d["FINCA"],
        "toro": d["TORO"],
        "vaca": d["VACA"],
        "raza": d["RAZA"],
        "sexo": d["SEXO"],
        "tc_gg_o": d["TC_GG_O"],
    })
    lista = registros.astype(object).to_dict(orient="records")
    for fila, iv, ev in zip(lista, con_intervalo.tolist(), es_evento.tolist()):
        fila["intervalo"] = None if pd.isna(iv) else int(iv)
        fila["evento"] = bool(ev)
    return lista


def generar_reporte_nacimiento_html(df: pd.DataFrame, titulo: str = "REPORTE CRÍAS", vaca_por_finca: bool = False,tipo_reporte: str = "") -> str:
    """Devuelve el HTML completo del reporte como string.

    vaca_por_finca=True si un mismo código de vaca puede repetirse en fincas distintas
    (en ese caso cada finca se trata como un hato separado para medir los intervalos).
    """
    datos_json = json.dumps(_preparar_nacimiento(df, vaca_por_finca), ensure_ascii=False).replace("</", "<\\/")
    return (
        _NACIMIENTO.replace("__DATA__", datos_json)
        .replace("__TITULO__", titulo)
        .replace("__GENERADO__", datetime.now().strftime("%Y-%m-%d %H:%M"))
    )


_NACIMIENTO = r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITULO__</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{
--txt:#e8f5ee; --muted:#8fb3a1; --line:rgba(190,255,220,.12); --edge:rgba(210,255,230,.30);
--g1:#34d399; --g2:#10b981; --glow:rgba(52,211,153,.38);
}
*{box-sizing:border-box}
html{background:#000;color-scheme:dark}
body{margin:0;color:var(--txt);min-height:100vh;
font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:14px;
background:
  radial-gradient(1100px 520px at 12% -12%, rgba(16,185,129,.18), transparent 60%),
  radial-gradient(900px 480px at 100% 0%, rgba(52,211,153,.08), transparent 55%),
  #000;}
header{padding:24px 24px 6px}
h1{margin:0;font-size:20px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;text-shadow:0 0 18px var(--glow)}
.section-title{text-align:center;margin:24px 0 14px;font-size:15px;letter-spacing:.32em;color:#d6f5e4}
.sub{color:var(--muted);margin-top:4px}
main{padding:16px 24px 44px;max-width:1400px;margin:0 auto}

.card{position:relative;border:1px solid var(--edge);border-radius:16px;padding:14px 18px;
background:linear-gradient(90deg, rgba(52,211,153,.30) 0, rgba(16,70,48,.28) 5%, rgba(8,24,18,.62) 40%, rgba(5,12,9,.78) 100%);
-webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
box-shadow:0 0 28px rgba(52,211,153,.07), inset 0 1px 0 rgba(255,255,255,.10);
transition:box-shadow .25s ease, border-color .25s ease}
.card:hover{border-color:rgba(210,255,230,.5);box-shadow:0 0 36px rgba(52,211,153,.18), inset 0 1px 0 rgba(255,255,255,.16)}
.card h3{font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#d6f5e4}

.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-bottom:14px}
.filters h3{margin:0 0 10px;font-size:11px;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:6px;max-height:132px;overflow:auto;padding:2px}
.chip{border:1px solid rgba(210,255,230,.25);color:var(--txt);border-radius:999px;padding:4px 12px;cursor:pointer;font-size:13px;
background:linear-gradient(135deg, rgba(52,211,153,.16), rgba(8,24,18,.5));
transition:all .18s ease}
.chip:hover{border-color:rgba(110,255,190,.7);box-shadow:0 0 12px rgba(52,211,153,.35)}
.chip.on{color:#03150c;font-weight:600;border-color:rgba(190,255,220,.9);
background:linear-gradient(135deg, rgba(110,255,190,.95), rgba(16,185,129,.8));
box-shadow:0 0 16px rgba(52,211,153,.6), inset 0 1px 0 rgba(255,255,255,.5)}
.vacio{color:var(--muted);font-size:12px;padding:4px}

.toolbar{display:flex;gap:10px;align-items:center;margin-bottom:14px;flex-wrap:wrap}
button.act,button.sec{border-radius:12px;padding:8px 18px;cursor:pointer;font-size:12px;letter-spacing:.12em;text-transform:uppercase;transition:all .2s ease}
button.act{color:#03150c;font-weight:600;border:1px solid rgba(190,255,220,.8);
background:linear-gradient(135deg, rgba(110,255,190,.95), rgba(16,185,129,.8));box-shadow:0 0 18px rgba(52,211,153,.45)}
button.act:hover{box-shadow:0 0 28px rgba(52,211,153,.8)}
button.sec{color:var(--txt);border:1px solid var(--edge);background:rgba(52,211,153,.08)}
button.sec:hover{box-shadow:0 0 16px rgba(52,211,153,.35)}

.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:14px}
.kpi .v{font-size:28px;font-weight:300;color:#eafff3;text-shadow:0 0 16px rgba(52,211,153,.55)}
.kpi .l{color:var(--muted);font-size:12px;margin-top:3px}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(400px,100%),1fr));gap:14px;margin-bottom:14px}
.grid h3,.card>h3{margin:0 0 10px;font-size:12px}
.box{position:relative;height:290px}
.box.tall{height:360px}
.full{margin-bottom:14px}

.tablewrap{overflow-x:auto}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
th{color:#9fd4b8;font-weight:600;user-select:none;text-transform:uppercase;letter-spacing:.06em;font-size:12px}
tr:hover td{background:rgba(52,211,153,.07)}
td.n,th.n{text-align:right}

input[type=number],select{color:var(--txt);border:1px solid var(--edge);border-radius:12px;padding:7px 12px;
background:rgba(5,14,10,.65);outline:none}
input[type=number]:focus,select:focus{border-color:rgba(110,255,190,.8);box-shadow:0 0 14px rgba(52,211,153,.35)}
input[type=number]{width:80px}

.note{color:var(--muted);font-size:12px;margin-top:8px}

::-webkit-scrollbar{height:8px;width:8px}
::-webkit-scrollbar-thumb{background:rgba(110,255,190,.28);border-radius:8px}
::-webkit-scrollbar-track{background:transparent}

@media(max-width:600px){
header{padding:16px 14px 4px}
main{padding:12px 12px 28px}
.grid{grid-template-columns:minmax(0,1fr)}
.box{height:250px}
}
</style>
</head>
<body>
<header>
<h1>__TITULO__</h1>
<div class="sub">Generado el __GENERADO__. Selecciona uno o varios valores en cada filtro; los filtros se ajustan entre sí.</div>
</header>

<main>
<h1 class="section-title">FILTROS</h1>
<div class="filters" id="filters"></div>

<div class="toolbar">
<button class="sec" id="reset">Limpiar filtros</button>
<button class="act" id="csv">Descargar CSV filtrado</button>
<span class="sub" id="status"></span>
</div>

<h1 class="section-title">DATOS TOTALIZADOS</h1>
<div class="kpis" id="kpis"></div>

<h1 class="section-title">GRÁFICOS</h1>
<div class="grid">
<div class="card"><h3>CRÍAS NACIDAS POR AÑO Y SEXO</h3><div class="box"><canvas id="c_anio_sexo"></canvas></div></div>
<div class="card"><h3>CRÍAS POR AÑO Y TIPO DE CONCEPCIÓN</h3><div class="box"><canvas id="c_anio_tc_gg_o"></canvas></div></div>
<div class="card"><h3>CRÍAS POR RAZA</h3><div class="box"><canvas id="c_raza"></canvas></div></div>
<div class="card"><h3>CRÍAS POR MES</h3><div class="box"><canvas id="c_mes"></canvas></div></div>
<div class="card"><h3>TOROS CON MÁS CRÍAS (TOP 10)</h3><div class="box"><canvas id="c_toro"></canvas></div></div>
<div class="card"><h3>CRÍAS POR FINCA</h3><div class="box"><canvas id="c_finca"></canvas></div></div>
</div>

<div class="card full">
<h3 style="margin:0 0 10px">RESUMEN POR AÑO</h3>
<div class="tablewrap"><table id="pivot"></table></div>
</div>

<div class="card full">
<div class="toolbar" style="margin-bottom:10px">
  <h3 style="margin:0">TOP 10 VACAS</h3>
  <select id="topord">
    <option value="intervalo">Menor tiempo entre partos</option>
    <option value="crias">Mayor cantidad de crías</option>
  </select>
  <label class="sub">Mínimo de intervalos medidos (solo al ordenar por tiempo entre partos):</label>
  <input type="number" id="topmin" min="1" value="1">
</div>
<div class="box tall"><canvas id="c_vacas"></canvas></div>
<div class="note" id="topnote"></div>
<div class="tablewrap" style="margin-top:10px"><table id="t_vacas"></table></div>
</div>
</main>

<script>
const DATA = __DATA__;
const TC_GG_O_LABEL = {
CN: 'Monta natural',
IA: 'Inseminación artificial',
TE: 'Transferencia de embriones',
'SIN DATO': 'Sin dato'
};
const MESES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
const PALETA = ['#34d399','#fbbf24','#2dd4bf','#f87171','#60a5fa','#a3e635','#86efac','#94a3b8'];
const DIMS = {anio:'Año', raza:'Raza', finca:'Finca', sexo:'Sexo', tc_gg_o:'Tipo de concepción'};
const FILTROS = Object.keys(DIMS);
const sel = {}; FILTROS.forEach(k => sel[k] = new Set());
const FW = {};
const charts = {};

const tcCode = v => {
const value = String(v ?? '').trim().toUpperCase();
if (!value || value === 'SIN DATO') return 'SIN DATO';
return value.substring(0, 2);
};
const cap = s => s ? String(s).charAt(0).toUpperCase() + String(s).slice(1) : s;
const cmp = (a,b) => {
const na = Number(a), nb = Number(b);
return a !== '' && b !== '' && Number.isFinite(na) && Number.isFinite(nb)
? na - nb : String(a).localeCompare(String(b), 'es');
};
const dimValue = (dim, row) => dim === 'tc_gg_o' ? tcCode(row.tc_gg_o) : String(row[dim] ?? 'sin dato');
const chipLabel = (dim, v) => cap(dim === 'tc_gg_o' ? (TC_GG_O_LABEL[v] || v) : v);
function countBy(rows, fn){
const m = new Map();
rows.forEach(r => { const k = fn(r); m.set(k, (m.get(k) || 0) + 1); });
return m;
}
function pct(a,b){ return b ? (100*a/b).toFixed(1)+'%' : '-'; }

// ---------- Filtros dependientes ----------
function passes(r, skip){
return FILTROS.every(k => k === skip || sel[k].size === 0 || sel[k].has(dimValue(k, r)));
}
function filtered(){ return DATA.filter(r => passes(r, null)); }
function optionsFor(dim){
return [...new Set(DATA.filter(r => passes(r, dim)).map(r => dimValue(dim, r)))].sort(cmp);
}
function pruneSelections(){
for (let i = 0; i < 6; i++){
let changed = false;
FILTROS.forEach(dim => {
  if (!sel[dim].size) return;
  const ok = new Set(optionsFor(dim));
  [...sel[dim]].forEach(v => { if (!ok.has(v)){ sel[dim].delete(v); changed = true; } });
});
if (!changed) break;
}
}
function buildFilters(){
const root = document.getElementById('filters'); root.innerHTML = '';
FILTROS.forEach(dim => {
const card = document.createElement('div'); card.className = 'card';
card.innerHTML = '<h3>' + DIMS[dim] + '</h3>';
const wrap = document.createElement('div'); wrap.className = 'chips';
card.appendChild(wrap); root.appendChild(card);
FW[dim] = wrap;
});
}
function updateFilters(){
FILTROS.forEach(dim => {
const wrap = FW[dim], pos = wrap.scrollTop;
wrap.innerHTML = '';
const vals = optionsFor(dim);
if (!vals.length){ wrap.innerHTML = '<span class="vacio">Sin opciones con los filtros actuales</span>'; return; }
vals.forEach(v => {
  const b = document.createElement('button'); b.className = 'chip' + (sel[dim].has(v) ? ' on' : '');
  b.textContent = chipLabel(dim, v);
  b.onclick = () => { sel[dim].has(v) ? sel[dim].delete(v) : sel[dim].add(v); render(); };
  wrap.appendChild(b);
});
wrap.scrollTop = pos;
});
}

// ---------- Gráficos ----------
function glassify(config){
const alpha = c => (typeof c === 'string' && /^#[0-9a-f]{6}$/i.test(c)) ? c + 'b0' : c;
(config.data.datasets || []).forEach(ds => {
const solid = ds.backgroundColor;
ds.borderColor = solid;
ds.backgroundColor = Array.isArray(solid) ? solid.map(alpha) : alpha(solid);
ds.borderWidth = 1;
ds.borderRadius = 6;
});
return config;
}
function draw(id, config){
if (charts[id]) charts[id].destroy();
charts[id] = new Chart(document.getElementById(id), glassify(config));
}
const avgLine = {id:'avgLine', afterDatasetsDraw(chart, args, opts){
if (!opts || opts.value == null) return;
const ctx = chart.ctx, area = chart.chartArea, x = chart.scales.x.getPixelForValue(opts.value);
ctx.save();
ctx.strokeStyle = '#fbbf24'; ctx.fillStyle = '#fbbf24'; ctx.lineWidth = 1.5; ctx.setLineDash([6,4]);
ctx.beginPath(); ctx.moveTo(x, area.top); ctx.lineTo(x, area.bottom); ctx.stroke();
ctx.setLineDash([]); ctx.font = '11px system-ui'; ctx.textAlign = 'left';
ctx.fillText(opts.text, x + 4, area.top + 12);
ctx.restore();
}};
function stacked(id, rows, xs, groupFn, groups, groupLabel, horizontal, xKey){
const datasets = groups.map((g,i) => ({
label: groupLabel(g),
data: xs.map(x => rows.filter(r => String(r[xKey]) === x && groupFn(r) === g).length),
backgroundColor: PALETA[i % PALETA.length]
}));
draw(id, {
type:'bar',
data:{labels:xs.map(cap), datasets},
options:{
  indexAxis:horizontal ? 'y' : 'x',
  responsive:true, maintainAspectRatio:false,
  scales:{x:{stacked:true}, y:{stacked:true, beginAtZero:true, ticks:{precision:0}}}
}
});
}

// ---------- Render ----------
function render(){
pruneSelections();
updateFilters();
const rows = filtered();
document.getElementById('status').textContent =
rows.length + ' de ' + DATA.length + ' crías con los filtros actuales';

const m = rows.filter(r => r.sexo === 'macho').length;
const h = rows.filter(r => r.sexo === 'hembra').length;
const cn = rows.filter(r => tcCode(r.tc_gg_o) === 'CN').length;
const ia = rows.filter(r => tcCode(r.tc_gg_o) === 'IA').length;
const te = rows.filter(r => tcCode(r.tc_gg_o) === 'TE').length;

const kp = [
[rows.length,'Total de crías'],
[m,'Machos ('+pct(m,rows.length)+')'],
[h,'Hembras ('+pct(h,rows.length)+')'],
[cn,'Monta natural ('+pct(cn,rows.length)+')'],
[ia,'Inseminación ('+pct(ia,rows.length)+')'],
[te,'Transferencia de embriones ('+pct(te,rows.length)+')'],
[new Set(rows.map(r => r.vaca)).size,'Vacas distintas'],
[new Set(rows.map(r => r.toro)).size,'Toros distintos']
];
document.getElementById('kpis').innerHTML = kp.map(k =>
'<div class="card kpi"><div class="v">'+k[0]+'</div><div class="l">'+k[1]+'</div></div>'
).join('');

const anios = [...new Set(rows.map(r => String(r.anio)))].sort(cmp);
const sexos = [...new Set(rows.map(r => r.sexo))].sort();
const tipos = [...new Set(rows.map(r => tcCode(r.tc_gg_o)))].sort();
const razas = [...new Set(rows.map(r => r.raza))].sort();
const fincas = [...new Set(rows.map(r => r.finca))].sort();

stacked('c_anio_sexo', rows, anios, r => r.sexo, sexos, cap, false, 'anio');
stacked('c_anio_tc_gg_o', rows, anios, r => tcCode(r.tc_gg_o), tipos,
k => TC_GG_O_LABEL[k] || k, false, 'anio');
stacked('c_raza', rows, razas, r => r.sexo, sexos, cap, true, 'raza');
stacked('c_finca', rows, fincas, r => r.finca, fincas, cap, true, 'finca');

const mesCnt = MESES.map((_,i) => rows.filter(r => r.mes === String(i+1)).length);
draw('c_mes', {
type:'bar',
data:{labels:MESES, datasets:[{label:'Crías',data:mesCnt,backgroundColor:PALETA[0]}]},
options:{
  responsive:true, maintainAspectRatio:false,
  plugins:{legend:{display:false}},
  scales:{y:{beginAtZero:true,ticks:{precision:0}}}
}
});

const top = [...countBy(rows, r => r.toro).entries()].sort((a,b) => b[1]-a[1]).slice(0,10);
draw('c_toro', {
type:'bar',
data:{labels:top.map(t => cap(t[0])),datasets:[{label:'Crías',data:top.map(t => t[1]),backgroundColor:PALETA[1]}]},
options:{
  indexAxis:'y', responsive:true, maintainAspectRatio:false,
  plugins:{legend:{display:false}},
  scales:{x:{beginAtZero:true,ticks:{precision:0}}}
}
});

let ph = '<tr><th>Año</th><th class="n">Total</th><th class="n">Machos</th><th class="n">Hembras</th><th class="n">% hembras</th><th class="n">Monta natural</th><th class="n">Inseminación</th><th class="n">Transferencia embriones</th></tr>';
anios.forEach(a => {
const rr = rows.filter(r => String(r.anio) === a);
const mm = rr.filter(r => r.sexo === 'macho').length;
const hh = rr.filter(r => r.sexo === 'hembra').length;
ph += '<tr><td>'+a+'</td><td class="n">'+rr.length+'</td><td class="n">'+mm+'</td><td class="n">'+hh+'</td><td class="n">'+pct(hh,rr.length)+
  '</td><td class="n">'+rr.filter(r => tcCode(r.tc_gg_o) === 'CN').length+
  '</td><td class="n">'+rr.filter(r => tcCode(r.tc_gg_o) === 'IA').length+
  '</td><td class="n">'+rr.filter(r => tcCode(r.tc_gg_o) === 'TE').length+'</td></tr>';
});
document.getElementById('pivot').innerHTML = ph;

renderVacas(rows);
}

// ---------- Top 10 vacas ----------
function renderVacas(rows){
const ord = document.getElementById('topord').value;
const minn = Math.max(1, Number(document.getElementById('topmin').value) || 1);
const num = (v, d) => v == null ? '-' : v.toFixed(d);

const g = new Map();
rows.filter(r => r.vaca !== 'sin dato').forEach(r => {
if (!g.has(r.vaca)) g.set(r.vaca, []);
g.get(r.vaca).push(r);
});
const vacas = [...g.entries()].map(([k, rs]) => {
const iv = rs.filter(r => r.evento && r.intervalo != null).map(r => r.intervalo);
return {k, crias: rs.length, partos: new Set(rs.filter(r => r.fecha).map(r => r.fecha)).size,
  n: iv.length, prom: iv.length ? iv.reduce((a,b) => a+b, 0) / iv.length : null,
  min: iv.length ? Math.min(...iv) : null};
});

const todosIv = rows.filter(r => r.evento && r.intervalo != null).map(r => r.intervalo);
const promGeneral = todosIv.length ? todosIv.reduce((a,b) => a+b, 0) / todosIv.length : null;

let list;
if (ord === 'intervalo'){
list = vacas.filter(x => x.n >= minn).sort((a,b) => a.prom - b.prom || b.crias - a.crias);
} else {
list = [...vacas].sort((a,b) => b.crias - a.crias || (a.prom ?? Infinity) - (b.prom ?? Infinity));
}
const topv = list.slice(0, 10);

const porIntervalo = ord === 'intervalo';
draw('c_vacas', {type:'bar', plugins:[avgLine],
data:{
  labels: topv.map(x => cap(x.k) + (porIntervalo ? ' (' + x.n + ' intervalos)' : ' (promedio ' + num(x.prom, 0) + ' d)')),
  datasets:[{label: porIntervalo ? 'Días promedio entre partos' : 'Crías',
    data: topv.map(x => porIntervalo ? Math.round(x.prom * 10) / 10 : x.crias),
    backgroundColor: porIntervalo ? PALETA[0] : PALETA[1]}]
},
options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
  plugins:{legend:{display:false},
    avgLine: porIntervalo && promGeneral != null ? {value: promGeneral, text: 'Promedio general ' + promGeneral.toFixed(0) + ' d'} : {}},
  scales:{x:{beginAtZero:true, ticks:{precision:0},
    suggestedMax: porIntervalo && promGeneral != null ? Math.ceil(promGeneral * 1.08) : undefined,
    title:{display:true, text: porIntervalo ? 'Días promedio entre partos' : 'Cantidad de crías'}}}}});

document.getElementById('topnote').textContent =
'Intervalo: días entre un parto y el siguiente de la misma vaca. Las crías con la misma fecha (mellizos) cuentan como un solo parto. ' +
'El intervalo se mide con todo el historial de la vaca y se asigna al parto en el que termina, por lo que respeta los filtros. ' +
'Una vaca con un solo parto no tiene intervalo. ' +
(porIntervalo ? 'Se muestran las que tienen al menos ' + minn + ' intervalos medidos; la línea punteada es el promedio general con los filtros actuales.'
              : 'Ordenado por cantidad de crías; en empate, por menor intervalo promedio.');

document.getElementById('t_vacas').innerHTML =
'<tr><th>Vaca</th><th class="n">Crías</th><th class="n">Partos</th><th class="n">Intervalos medidos</th>' +
'<th class="n">Intervalo promedio (días)</th><th class="n">Intervalo mínimo (días)</th></tr>' +
topv.map(x => '<tr><td>'+cap(x.k)+'</td><td class="n">'+x.crias+'</td><td class="n">'+x.partos+'</td><td class="n">'+x.n+
  '</td><td class="n">'+num(x.prom, 1)+'</td><td class="n">'+num(x.min, 0)+'</td></tr>').join('') +
'<tr><td><b>Promedio general</b></td><td class="n">'+rows.length+'</td><td class="n"></td><td class="n">'+todosIv.length+
  '</td><td class="n">'+num(promGeneral, 1)+'</td><td class="n"></td></tr>';
}

// ---------- Eventos ----------
document.getElementById('topord').addEventListener('change', () => renderVacas(filtered()));
document.getElementById('topmin').addEventListener('input', () => renderVacas(filtered()));
document.getElementById('reset').onclick = () => {
Object.values(sel).forEach(s => s.clear());
render();
};
document.getElementById('csv').onclick = () => {
const rows = filtered();
const esc = v => '"' + String(v ?? '').replace(/"/g,'""') + '"';
const csv = ['FECHA_NACIMIENTO,FINCA,TORO,VACA,RAZA,SEXO,TC_GG_O'].concat(
rows.map(r => [r.fecha,r.finca,r.toro,r.vaca,r.raza,r.sexo,r.tc_gg_o].map(esc).join(','))
).join('\n');
const a = document.createElement('a');
a.href = URL.createObjectURL(new Blob(['\ufeff'+csv], {type:'text/csv;charset=utf-8'}));
a.download = 'crias_filtradas.csv';
a.click();
URL.revokeObjectURL(a.href);
};

Chart.defaults.color = '#bfe3cf';
Chart.defaults.borderColor = 'rgba(190,255,220,.10)';
Chart.defaults.font.family = 'system-ui,-apple-system,"Segoe UI",Roboto,sans-serif';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
buildFilters();
render();
</script>
</body>
</html>
"""




# Columnas donde se escribe "RP" cuando la vaca rechazó el protocolo (no hubo transferencia)
RP_COLS = ["DONADORA", "REPRODUCTOR", "RAZA", "TIPO_EMBRION"]
# Una fila es rechazo si cualquiera de estas columnas vale "RP" (X1 y X3 también pueden traerlo)
RP_DETECT = RP_COLS + ["X1", "X3"]


def _texto(serie: pd.Series) -> pd.Series:
    s = serie.astype("string").str.strip().str.lower().fillna("sin dato")
    return s.replace("", "sin dato")


def _resultado(serie: pd.Series) -> pd.Series:
    """Normaliza X1/X3 a 'P', 'V', 'RP' o 'SIN DATO' (pendiente)."""
    x = serie.astype("string").str.strip().str.upper()
    es_rp = (x == "RP").fillna(False).astype(bool)
    es_p = x.str.startswith("P", na=False) | x.str.startswith("+", na=False)
    es_v = x.str.startswith("V", na=False)
    out = pd.Series("SIN DATO", index=serie.index, dtype="object")
    out[es_p] = "P"
    out[es_v & ~es_p] = "V"
    out[es_rp] = "RP"
    return out


def _preparar_embriones(df: pd.DataFrame, dia_primero: bool) -> list:
    COLUMNAS = [
    "PROVEEDOR", "FINCA", "FECHA_SINCRONIZACION", "FECHA_TRANSFERENCIA",
    "RECEPTORA", "DONADORA", "REPRODUCTOR", "RAZA", "TIPO_EMBRION", "X1", "X3",
]
    faltantes = [c for c in COLUMNAS if c not in df.columns]
    if faltantes:
        raise ValueError(f"Faltan columnas en el dataframe: {faltantes}")

    d = df[COLUMNAS].copy()

    fsync = pd.to_datetime(d["FECHA_SINCRONIZACION"], errors="coerce", dayfirst=dia_primero)
    ftrans = pd.to_datetime(d["FECHA_TRANSFERENCIA"], errors="coerce", dayfirst=dia_primero)
    fref = ftrans.fillna(fsync)  # fecha de referencia para año y mes

    dias = (ftrans - fsync).dt.days
    dias = dias.where(dias >= 0)

    out = pd.DataFrame(index=d.index)
    out["fsync"] = fsync.dt.strftime("%Y-%m-%d").fillna("")
    out["ftrans"] = ftrans.dt.strftime("%Y-%m-%d").fillna("")
    out["anio"] = fref.dt.year.astype("Int64").astype("string").fillna("sin fecha")
    out["mes"] = fref.dt.month.astype("Int64").astype("string").fillna("sin dato")
    out["aniomes"] = fref.dt.strftime("%Y-%m").fillna("")
    out["finca"] = _texto(d["FINCA"])
    out["proveedor"] = _texto(d["PROVEEDOR"])
    out["receptora"] = _texto(d["RECEPTORA"])
    out["donadora"] = _texto(d["DONADORA"])
    out["reproductor"] = _texto(d["REPRODUCTOR"])
    out["raza"] = _texto(d["RAZA"])
    out["tipo"] = _texto(d["TIPO_EMBRION"])
    out["x1"] = _resultado(d["X1"])
    out["x3"] = _resultado(d["X3"])

    # Rechazó el protocolo: alguna de las columnas de RP_DETECT vale "RP"
    rechazo = pd.Series(False, index=d.index)
    for c in RP_DETECT:
        es_rp = (d[c].astype("string").str.strip().str.upper() == "RP").fillna(False)
        rechazo = rechazo | es_rp.astype(bool)
    out["transferida"] = ~rechazo
    out["estado"] = out["transferida"].map({True: "transferida", False: "rechazó protocolo"})
    out.loc[rechazo, ["donadora", "reproductor", "raza", "tipo"]] = "RP"
    out.loc[rechazo, ["x1", "x3"]] = "RP"

    # Si X1 es V, X3 toma por defecto el mismo valor (no se preña sola)
    out.loc[(out["x1"] == "V") & (out["x3"] == "SIN DATO"), "x3"] = "V"

    registros = []
    for fila, dia in zip(out.astype(object).to_dict(orient="records"), dias.tolist()):
        fila["transferida"] = bool(fila["transferida"])
        fila["dias"] = None if (pd.isna(dia) or not fila["transferida"]) else int(dia)
        registros.append(fila)
    return registros


def generar_reporte_embriones_html(
    df: pd.DataFrame,
    titulo: str = "Reporte de procesos de embriones",
    dia_primero: bool = False,
) -> str:
    """Devuelve el HTML completo del reporte como string.

    dia_primero=True si tus fechas vienen como texto día/mes/año (03/05/2024 = 3 de mayo).
    """
    datos = _preparar_embriones(df, dia_primero)
    datos_json = json.dumps(datos, ensure_ascii=False).replace("</", "<\\/")
    generado = datetime.now().strftime("%Y-%m-%d %H:%M")
    return (
        _EMBRIONES.replace("__DATA__", datos_json)
        .replace("__TITULO__", titulo)
        .replace("__GENERADO__", generado)
    )


_EMBRIONES= r"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>__TITULO__</title>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<style>
:root{
  --txt:#e8f5ee; --muted:#8fb3a1; --line:rgba(190,255,220,.12); --edge:rgba(210,255,230,.30);
  --g1:#34d399; --g2:#10b981; --glow:rgba(52,211,153,.38);
}
*{box-sizing:border-box}
html{background:#000;color-scheme:dark}
body{margin:0;color:var(--txt);min-height:100vh;
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;font-size:14px;
  background:
    radial-gradient(1100px 520px at 12% -12%, rgba(16,185,129,.18), transparent 60%),
    radial-gradient(900px 480px at 100% 0%, rgba(52,211,153,.08), transparent 55%),
    #000;}
header{padding:24px 24px 6px}
h1{margin:0;font-size:20px;font-weight:400;letter-spacing:.22em;text-transform:uppercase;text-shadow:0 0 18px var(--glow)}
.sub{color:var(--muted);margin-top:4px}
main{padding:16px 24px 44px;max-width:1400px;margin:0 auto}

.card{position:relative;border:1px solid var(--edge);border-radius:16px;padding:14px 18px;
  background:linear-gradient(90deg, rgba(52,211,153,.30) 0, rgba(16,70,48,.28) 5%, rgba(8,24,18,.62) 40%, rgba(5,12,9,.78) 100%);
  -webkit-backdrop-filter:blur(12px);backdrop-filter:blur(12px);
  box-shadow:0 0 28px rgba(52,211,153,.07), inset 0 1px 0 rgba(255,255,255,.10);
  transition:box-shadow .25s ease, border-color .25s ease}
.card:hover{border-color:rgba(210,255,230,.5);box-shadow:0 0 36px rgba(52,211,153,.18), inset 0 1px 0 rgba(255,255,255,.16)}
.card h3{font-weight:400;letter-spacing:.14em;text-transform:uppercase;color:#d6f5e4}

.filters{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:12px;margin-bottom:14px}
.filters h3{margin:0 0 10px;font-size:11px;color:var(--muted)}
.chips{display:flex;flex-wrap:wrap;gap:6px;max-height:132px;overflow:auto;padding:2px}
.chip{border:1px solid rgba(210,255,230,.25);color:var(--txt);border-radius:999px;padding:4px 12px;cursor:pointer;font-size:13px;
  background:linear-gradient(135deg, rgba(52,211,153,.16), rgba(8,24,18,.5));
  transition:all .18s ease}
.chip:hover{border-color:rgba(110,255,190,.7);box-shadow:0 0 12px rgba(52,211,153,.35)}
.chip.on{color:#03150c;font-weight:600;border-color:rgba(190,255,220,.9);
  background:linear-gradient(135deg, rgba(110,255,190,.95), rgba(16,185,129,.8));
  box-shadow:0 0 16px rgba(52,211,153,.6), inset 0 1px 0 rgba(255,255,255,.5)}
.fsearch{width:100%;margin-bottom:8px;padding:5px 10px;font-size:12px}
.vacio{color:var(--muted);font-size:12px;padding:4px}

.toolbar{display:flex;gap:10px;align-items:center;margin-bottom:14px;flex-wrap:wrap}
button.act,button.sec{border-radius:12px;padding:8px 18px;cursor:pointer;font-size:12px;letter-spacing:.12em;text-transform:uppercase;transition:all .2s ease}
button.act{color:#03150c;font-weight:600;border:1px solid rgba(190,255,220,.8);
  background:linear-gradient(135deg, rgba(110,255,190,.95), rgba(16,185,129,.8));box-shadow:0 0 18px rgba(52,211,153,.45)}
button.act:hover{box-shadow:0 0 28px rgba(52,211,153,.8)}
button.sec{color:var(--txt);border:1px solid var(--edge);background:rgba(52,211,153,.08)}
button.sec:hover{box-shadow:0 0 16px rgba(52,211,153,.35)}

.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin-bottom:14px}
.kpi .v{font-size:28px;font-weight:300;color:#eafff3;text-shadow:0 0 16px rgba(52,211,153,.55)}
.kpi .l{color:var(--muted);font-size:12px;margin-top:3px}

.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));gap:14px;margin-bottom:14px}
.grid h3,.card>h3{margin:0 0 10px;font-size:12px}
.box{position:relative;height:290px}
.box.tall{height:360px}
.full{margin-bottom:14px}

.tablewrap{overflow-x:auto}
table{width:100%;border-collapse:collapse}
th,td{text-align:left;padding:7px 10px;border-bottom:1px solid var(--line);white-space:nowrap}
th{color:#9fd4b8;font-weight:600;user-select:none;text-transform:uppercase;letter-spacing:.06em;font-size:12px}
tr:hover td{background:rgba(52,211,153,.07)}
td.n,th.n{text-align:right}

input[type=search],input[type=number],select{color:var(--txt);border:1px solid var(--edge);border-radius:12px;padding:7px 12px;
  background:rgba(5,14,10,.65);outline:none}
input[type=search]:focus,input[type=number]:focus,select:focus{border-color:rgba(110,255,190,.8);box-shadow:0 0 14px rgba(52,211,153,.35)}
input[type=search]{min-width:220px}
input[type=number]{width:80px}

.note{color:var(--muted);font-size:12px;margin-top:8px}
.warn{border:1px solid var(--edge);border-left:3px solid var(--g1);border-radius:12px;padding:9px 14px;margin-bottom:14px;
  color:var(--muted);font-size:13px;background:rgba(52,211,153,.06)}

::-webkit-scrollbar{height:8px;width:8px}
::-webkit-scrollbar-thumb{background:rgba(110,255,190,.28);border-radius:8px}
::-webkit-scrollbar-track{background:transparent}
</style>
</head>
<body>
<header>
<h1>__TITULO__</h1>
<div class="sub">Generado el __GENERADO__. Selecciona uno o varios valores en cada filtro; los filtros se ajustan entre sí.</div>
</header>
<main>
<div class="warn" id="supuestos"></div>
<div class="filters" id="filters"></div>
<div class="toolbar">
  <button class="sec" id="reset">Limpiar filtros</button>
  <button class="act" id="csv">Descargar CSV filtrado</button>
  <span class="sub" id="status"></span>
</div>

<div class="kpis" id="kpis"></div>

<div class="card full">
  <div class="toolbar" style="margin-bottom:10px">
    <h3 style="margin:0">Transferencias, preñadas en X1 y abortos por</h3>
    <select id="catdim"></select>
    <label class="sub">Mínimo de transferencias:</label>
    <input type="number" id="minn" min="1" value="1">
  </div>
  <div class="box tall"><canvas id="c_cat"></canvas></div>
  <div class="note" id="catnote"></div>
  <div class="tablewrap" style="margin-top:10px"><table id="t_cat"></table></div>
</div>

<div class="grid">
  <div class="card"><h3>Transferencias y preñeces X1 por mes</h3><div class="box"><canvas id="c_tiempo"></canvas></div></div>
  <div class="card"><h3>Preñez X1 según días entre sincronización y transferencia</h3><div class="box"><canvas id="c_dias"></canvas></div>
    <div class="note">Entre paréntesis, el número de casos con X1 confirmado.</div></div>
</div>

<div class="card full">
  <div class="toolbar" style="margin-bottom:10px">
    <h3 style="margin:0">Top 10</h3>
    <select id="topcrit">
      <option value="mejores">Mejores</option>
      <option value="peores">Peores</option>
    </select>
    <select id="topent">
      <option value="reproductor">Reproductores</option>
      <option value="donadora">Donadoras</option>
      <option value="receptora">Receptoras</option>
    </select>
    <label class="sub">Ordenar por:</label>
    <select id="toporden">
      <option value="porcentaje">Porcentaje</option>
      <option value="ajustado">Ajustado por n.º de casos</option>
      <option value="cantidad">Cantidad</option>
      
    </select>
    <label class="sub">Mínimo de casos (solo al ordenar por porcentaje):</label>
    <input type="number" id="topmin" min="1" value="3">
  </div>
  <div class="box tall"><canvas id="c_top"></canvas></div>
  <div class="note" id="topnote"></div>
  <div class="tablewrap" style="margin-top:10px"><table id="t_top"></table></div>
</div>
<div class="card full">
  <div class="toolbar" style="margin-bottom:10px">
    <h3 style="margin:0">Receptoras con rechazos repetidos (RP)</h3>
    <label class="sub">Mostrar las que rechazaron al menos</label>
    <input type="number" id="rpmin" min="1" value="2">
    <label class="sub">veces</label>
  </div>
  <div class="tablewrap"><table id="t_rp"></table></div>
  <div class="note" id="rpnote"></div>
</div>
</main>

<script>
const DATA = __DATA__;
const MESES = ['Ene','Feb','Mar','Abr','May','Jun','Jul','Ago','Sep','Oct','Nov','Dic'];
const PALETA = ['#34d399','#fbbf24','#2dd4bf','#f87171','#60a5fa','#a3e635','#86efac','#94a3b8'];
const LABELS = {anio:'Año', mes:'Mes', finca:'Finca', proveedor:'Proveedor', raza:'Raza', tipo:'Tipo de embrión',
reproductor:'Reproductor', donadora:'Donadora', receptora:'Receptora', estado:'Estado'};
const FILTROS = ['anio','mes','finca','proveedor','raza','reproductor','donadora','estado'];
const CATDIMS = ['proveedor','reproductor','donadora','raza','tipo','finca','anio','mes'];
const SOLO_TRANSFERIDAS = ['raza','tipo','reproductor','donadora'];
const sel = {}; FILTROS.forEach(k => sel[k] = new Set());
const FW = {};
const charts = {};
const HAS_REJECT = DATA.some(r => !r.transferida);

const cap = s => s ? s.charAt(0).toUpperCase() + s.slice(1) : s;
function lab(dim, v){
if (dim === 'mes' && !isNaN(v)) return MESES[Number(v)-1] || v;
return cap(String(v));
}
const cmp = (a,b) => (isNaN(a)||isNaN(b)) ? String(a).localeCompare(String(b),'es') : Number(a)-Number(b);
const res = v => v === 'P' ? 'P+' : v === 'V' ? 'V' : v === 'RP' ? 'RP' : 'PENDIENTE';
const rate = (a,b) => b ? 100*a/b : null;
const fmt = v => v == null ? '-' : v.toFixed(1) + '%';

// ---------- Filtros dependientes ----------
function passes(r, skip){
return FILTROS.every(k => k === skip || sel[k].size === 0 || sel[k].has(String(r[k])));
}
function filtered(){ return DATA.filter(r => passes(r, null)); }
function optionsFor(dim){
let src = DATA.filter(r => passes(r, dim));
if (SOLO_TRANSFERIDAS.includes(dim)) src = src.filter(r => r.transferida);
return [...new Set(src.map(r => String(r[dim])))].sort(cmp);
}
function pruneSelections(){
for (let i = 0; i < 6; i++){
  let changed = false;
  FILTROS.forEach(dim => {
    if (!sel[dim].size) return;
    const ok = new Set(optionsFor(dim));
    [...sel[dim]].forEach(v => { if (!ok.has(v)){ sel[dim].delete(v); changed = true; } });
  });
  if (!changed) break;
}
}
function buildFilters(){
const root = document.getElementById('filters'); root.innerHTML = '';
FILTROS.forEach(dim => {
  const card = document.createElement('div'); card.className = 'card';
  card.innerHTML = '<h3>'+LABELS[dim]+'</h3>';
  let inp = null;
  if (new Set(DATA.map(r => String(r[dim]))).size > 12){
    inp = document.createElement('input'); inp.type = 'search'; inp.className = 'fsearch'; inp.placeholder = 'Buscar...';
    inp.oninput = () => applySearch(dim);
    card.appendChild(inp);
  }
  const wrap = document.createElement('div'); wrap.className = 'chips';
  card.appendChild(wrap); root.appendChild(card);
  FW[dim] = {wrap, inp};
});
const s = document.getElementById('catdim');
CATDIMS.forEach(d => { const o = document.createElement('option'); o.value = d; o.textContent = LABELS[d]; s.appendChild(o); });
}
function applySearch(dim){
const {wrap, inp} = FW[dim];
const t = inp ? inp.value.toLowerCase() : '';
wrap.querySelectorAll('.chip').forEach(c => c.style.display = c.textContent.toLowerCase().includes(t) ? '' : 'none');
}
function updateFilters(){
FILTROS.forEach(dim => {
  const wrap = FW[dim].wrap, pos = wrap.scrollTop;
  wrap.innerHTML = '';
  const vals = optionsFor(dim);
  if (!vals.length){ wrap.innerHTML = '<span class="vacio">Sin opciones con los filtros actuales</span>'; return; }
  vals.forEach(v => {
    const b = document.createElement('button'); b.className = 'chip' + (sel[dim].has(v) ? ' on' : '');
    b.textContent = lab(dim, v);
    b.onclick = () => { sel[dim].has(v) ? sel[dim].delete(v) : sel[dim].add(v); render(); };
    wrap.appendChild(b);
  });
  applySearch(dim);
  wrap.scrollTop = pos;
});
}

// ---------- Cálculos ----------
function stats(rows){
const tr = rows.filter(r => r.transferida);
const x1p = tr.filter(r => r.x1 === 'P').length;
const x1v = tr.filter(r => r.x1 === 'V').length;
const x1pend = tr.filter(r => r.x1 === 'SIN DATO').length;
const pp = tr.filter(r => r.x1 === 'P' && r.x3 === 'P').length;   // siguen preñadas
const pv = tr.filter(r => r.x1 === 'P' && r.x3 === 'V').length;   // abortos
const x3pend = tr.filter(r => r.x1 === 'P' && r.x3 === 'SIN DATO').length;
const dd = tr.filter(r => r.dias != null).map(r => r.dias);
return {sync: rows.length, tr: tr.length, n1: x1p + x1v, x1p, x1v, x1pend, pp, pv, x3pend,
  dias: dd.length ? dd.reduce((a,b) => a+b, 0) / dd.length : null};
}

function glassify(config){
const alpha = c => (typeof c === 'string' && /^#[0-9a-f]{6}$/i.test(c)) ? c + 'b0' : c;
(config.data.datasets || []).forEach(ds => {
  const solid = ds.backgroundColor;
  ds.borderColor = solid;
  ds.backgroundColor = Array.isArray(solid) ? solid.map(alpha) : alpha(solid);
  ds.borderWidth = 1;
  ds.borderRadius = 6;
});
return config;
}
function draw(id, config){
if (charts[id]) charts[id].destroy();
charts[id] = new Chart(document.getElementById(id), glassify(config));
}

// ---------- Render ----------
function render(){
pruneSelections();
updateFilters();
const rows = filtered();
const s = stats(rows);
document.getElementById('status').textContent = rows.length + ' de ' + DATA.length + ' animales con los filtros actuales';

const perd = rate(s.pv, s.pp + s.pv);
const kp = [
  [s.sync, 'Animales sincronizados'],
  [s.tr, 'Transferencias'],
  [s.sync - s.tr, 'Rechazaron el protocolo (RP)'],
  [HAS_REJECT ? fmt(rate(s.tr, s.sync)) : 'Sin dato', 'Aceptación del protocolo'],
  [fmt(rate(s.x1p, s.n1)), 'Preñez X1 (' + s.x1p + ' de ' + s.n1 + ')'],
  [fmt(perd), 'Abortos X1 a X3 (' + s.pv + ' de ' + (s.pp + s.pv) + ')'],
  [new Set(rows.filter(r => r.transferida).map(r => r.donadora)).size, 'Donadoras distintas'],
  [new Set(rows.map(r => r.receptora)).size, 'Receptoras distintas'],
  [new Set(rows.filter(r => r.transferida).map(r => r.reproductor)).size, 'Reproductores distintos']
];
document.getElementById('kpis').innerHTML = kp.map(k =>
  '<div class="card kpi"><div class="v">'+k[0]+'</div><div class="l">'+k[1]+'</div></div>').join('');

renderCat(rows, s);

// Transferencias y preñeces por mes
const tr = rows.filter(r => r.transferida && r.aniomes);
const meses = [...new Set(tr.map(r => r.aniomes))].sort();
draw('c_tiempo', {type:'bar', data:{labels: meses, datasets:[
  {label:'Transferencias', data: meses.map(m => tr.filter(r => r.aniomes === m).length), backgroundColor: PALETA[0]},
  {label:'Preñadas en X1', data: meses.map(m => tr.filter(r => r.aniomes === m && r.x1 === 'P').length), backgroundColor: PALETA[1]}]},
  options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, ticks:{precision:0}}}}});

// Preñez X1 según días entre sincronización y transferencia
const conDias = rows.filter(r => r.transferida && r.dias != null);
const dvals = [...new Set(conDias.map(r => r.dias))].sort((a,b) => a-b);
const dstat = dvals.map(d => {
  const rr = conDias.filter(r => r.dias === d);
  const p = rr.filter(r => r.x1 === 'P').length, v = rr.filter(r => r.x1 === 'V').length;
  return {d, n: p+v, rt: rate(p, p+v)};
});
draw('c_dias', {type:'bar', data:{labels: dstat.map(x => x.d + ' d (' + x.n + ')'),
  datasets:[{label:'Preñez X1 (%)', data: dstat.map(x => x.rt), backgroundColor: PALETA[2]}]},
  options:{responsive:true, maintainAspectRatio:false, plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true, max:100}}}});

renderTop(rows);
renderRP(rows);
}

function renderCat(rows, total){
const dim = document.getElementById('catdim').value || CATDIMS[0];
const minn = Math.max(1, Number(document.getElementById('minn').value) || 1);
const g = new Map();
rows.filter(r => r.transferida).forEach(r => { const k = String(r[dim]); if (!g.has(k)) g.set(k, []); g.get(k).push(r); });
let list = [...g.entries()].map(([k, rs]) => ({k, ...stats(rs)})).filter(x => x.tr >= minn);
if (dim === 'anio' || dim === 'mes') list.sort((a,b) => cmp(a.k, b.k));
else list.sort((a,b) => b.tr - a.tr || String(a.k).localeCompare(String(b.k),'es'));
const MAXC = 25, shown = list.slice(0, MAXC);

draw('c_cat', {type:'bar', data:{labels: shown.map(x => lab(dim, x.k)), datasets:[
  {label:'Transferencias', data: shown.map(x => x.tr), backgroundColor: PALETA[2]},
  {label:'Preñadas en X1', data: shown.map(x => x.x1p), backgroundColor: PALETA[0]},
  {label:'Abortos (P+ en X1 y V en X3)', data: shown.map(x => x.pv), backgroundColor: PALETA[3]}]},
  options:{responsive:true, maintainAspectRatio:false, scales:{y:{beginAtZero:true, ticks:{precision:0}}}}});

document.getElementById('catnote').textContent =
  'Pendientes con los filtros actuales: ' + total.x1pend + ' sin X1 confirmado y ' + total.x3pend + ' preñadas en X1 sin X3 confirmado. ' +
  '% preñez X1: sobre transferencias con X1 confirmado. % abortos: sobre preñadas en X1 con X3 confirmado. ' +
  (list.length > MAXC ? 'El gráfico muestra los primeros ' + MAXC + ' de ' + list.length + '; la tabla muestra todos.' : '');

document.getElementById('t_cat').innerHTML =
  '<tr><th>'+LABELS[dim]+'</th><th class="n">Transferencias</th><th class="n">X1 pendiente</th><th class="n">Preñadas X1</th><th class="n">% preñez X1</th>' +
  '<th class="n">Abortos</th><th class="n">% abortos</th><th class="n">X3 pendiente</th></tr>' +
  list.map(x => '<tr><td>'+lab(dim, x.k)+'</td><td class="n">'+x.tr+'</td><td class="n">'+x.x1pend+'</td><td class="n">'+x.x1p+
    '</td><td class="n">'+fmt(rate(x.x1p, x.n1))+'</td><td class="n">'+x.pv+'</td><td class="n">'+fmt(rate(x.pv, x.pp + x.pv))+
    '</td><td class="n">'+x.x3pend+'</td></tr>').join('');
}

// ---------- Top 10 por % de preñez ----------
function wilson(k, n){
if (!n) return 0;
const z = 1.96, p = k / n, d = 1 + z*z/n, c = p + z*z/(2*n);
const m = z * Math.sqrt(p*(1-p)/n + z*z/(4*n*n));
return (c - m) / d;
}
const avgLine = {id:'avgLine', afterDatasetsDraw(chart, args, opts){
if (!opts || opts.value == null) return;
const ctx = chart.ctx, area = chart.chartArea, x = chart.scales.x.getPixelForValue(opts.value);
ctx.save();
ctx.strokeStyle = '#fbbf24'; ctx.fillStyle = '#fbbf24'; ctx.lineWidth = 1.5; ctx.setLineDash([6,4]);
ctx.beginPath(); ctx.moveTo(x, area.top); ctx.lineTo(x, area.bottom); ctx.stroke();
ctx.setLineDash([]); ctx.font = '11px system-ui'; ctx.textAlign = 'left';
ctx.fillText('Promedio ' + opts.value.toFixed(1) + '%', x + 4, area.top + 12);
ctx.restore();
}};

function renderTop(rows){
const ent = document.getElementById('topent').value;
const crit = document.getElementById('topcrit').value;
const ord = document.getElementById('toporden').value;
const minn = Math.max(1, Number(document.getElementById('topmin').value) || 1);

// Solo animales transferidos con X1 confirmado; RP no entra en el cálculo
const g = new Map();
rows.filter(r => r.transferida).forEach(r => { const k = String(r[ent]); if (!g.has(k)) g.set(k, []); g.get(k).push(r); });
const todos = [...g.entries()].map(([k, rs]) => {
  const p = rs.filter(r => r.x1 === 'P').length, v = rs.filter(r => r.x1 === 'V').length;
  return {k, p, v, n: p + v};
}).filter(x => x.n > 0);

const clave = x => crit === 'mejores' ? x.p : x.v;
const totN = todos.reduce((a,x) => a + x.n, 0), totP = todos.reduce((a,x) => a + x.p, 0), totV = todos.reduce((a,x) => a + x.v, 0);
const prom = rate(crit === 'mejores' ? totP : totV, totN);

let list = todos.filter(x => clave(x) > 0);
if (ord === 'porcentaje'){
  list = list.filter(x => x.n >= minn);
  list.sort((a,b) => rate(clave(b), b.n) - rate(clave(a), a.n) || b.n - a.n);
} else if (ord === 'ajustado'){
  list.sort((a,b) => wilson(clave(b), b.n) - wilson(clave(a), a.n) || b.n - a.n);
} else {
  list.sort((a,b) => clave(b) - clave(a) || rate(clave(b), b.n) - rate(clave(a), a.n));
}
const top = list.slice(0, 10);

draw('c_top', {type:'bar', plugins:[avgLine],
  data:{labels: top.map(x => lab(ent, x.k) + ' (' + clave(x) + ' de ' + x.n + ')'),
    datasets:[{label: crit === 'mejores' ? 'Preñez X1 (%)' : 'Vacías en X1 (%)',
      data: top.map(x => rate(clave(x), x.n)), backgroundColor: crit === 'mejores' ? PALETA[0] : PALETA[3]}]},
  options:{indexAxis:'y', responsive:true, maintainAspectRatio:false,
    plugins:{legend:{display:false}, avgLine:{value: prom}},
    scales:{x:{beginAtZero:true, max:100, ticks:{callback: v => v + '%'}}}}});

document.getElementById('topnote').textContent =
  (crit === 'mejores' ? 'Mejores: mayor % de preñez en X1. ' : 'Peores: mayor % de vacías (V) en X1. ') +
  'Entre paréntesis: casos preñados (o vacíos) de los casos con X1 confirmado. La línea punteada es el promedio general con los filtros actuales. ' +
  (ord === 'porcentaje' ? 'Solo se muestran los que tienen al menos ' + minn + ' casos. '
    : ord === 'ajustado' ? 'El orden ajustado tiene en cuenta el número de casos: con pocos casos, el porcentaje pesa menos. '
    : 'Ordenado por cantidad. ') +
  'Los casos con X1 pendiente no se cuentan y RP no entra en el cálculo.';

document.getElementById('t_top').innerHTML =
  '<tr><th>'+LABELS[ent]+'</th><th class="n">Casos con X1</th><th class="n">P+</th><th class="n">V</th><th class="n">% preñez</th><th class="n">% V</th></tr>' +
  top.map(x => '<tr><td>'+lab(ent, x.k)+'</td><td class="n">'+x.n+'</td><td class="n">'+x.p+'</td><td class="n">'+x.v+
    '</td><td class="n">'+fmt(rate(x.p, x.n))+'</td><td class="n">'+fmt(rate(x.v, x.n))+'</td></tr>').join('') +
  '<tr><td><b>Promedio general</b></td><td class="n">'+totN+'</td><td class="n">'+totP+'</td><td class="n">'+totV+
    '</td><td class="n">'+fmt(rate(totP, totN))+'</td><td class="n">'+fmt(rate(totV, totN))+'</td></tr>';
}

// ---------- Receptoras con rechazos repetidos ----------
function renderRP(rows){
const minr = Math.max(1, Number(document.getElementById('rpmin').value) || 1);
const g = new Map();
rows.forEach(r => { const k = String(r.receptora); if (!g.has(k)) g.set(k, []); g.get(k).push(r); });
const list = [...g.entries()].map(([k, rs]) => {
  const rp = rs.filter(r => !r.transferida).length;
  const tr = rs.filter(r => r.transferida);
  const p = tr.filter(r => r.x1 === 'P').length, v = tr.filter(r => r.x1 === 'V').length;
  return {k, sync: rs.length, rp, tr: tr.length, p, n1: p + v};
}).filter(x => x.rp >= minr)
  .sort((a,b) => b.rp - a.rp || rate(b.rp, b.sync) - rate(a.rp, a.sync));
const MAXR = 50;

document.getElementById('t_rp').innerHTML =
  '<tr><th>Receptora</th><th class="n">Veces sincronizada</th><th class="n">Rechazos (RP)</th><th class="n">% rechazo</th>' +
  '<th class="n">Transferencias</th><th class="n">Preñadas X1</th><th class="n">% preñez X1</th></tr>' +
  (list.length ? list.slice(0, MAXR).map(x => '<tr><td>'+lab('receptora', x.k)+'</td><td class="n">'+x.sync+'</td><td class="n">'+x.rp+
    '</td><td class="n">'+fmt(rate(x.rp, x.sync))+'</td><td class="n">'+x.tr+'</td><td class="n">'+x.p+
    '</td><td class="n">'+fmt(rate(x.p, x.n1))+'</td></tr>').join('')
  : '<tr><td colspan="7">Ninguna receptora con al menos ' + minr + ' rechazos con los filtros actuales.</td></tr>');

document.getElementById('rpnote').textContent =
  list.length + ' receptoras con al menos ' + minr + ' rechazos. ' +
  (list.length > MAXR ? 'Se muestran las primeras ' + MAXR + '. ' : '') +
  'Una receptora sin transferencias no tiene dato de preñez. ' +
  'Si hay filtros de raza, reproductor o donadora activos, las filas RP no se incluyen, porque en un rechazo esos campos valen RP.';
}

// ---------- CSV ----------
const COLS = [['fsync','Sincronización'],['ftrans','Transferencia'],['finca','Finca'],['proveedor','Proveedor'],['receptora','Receptora'],
['donadora','Donadora'],['reproductor','Reproductor'],['raza','Raza'],['tipo','Tipo embrión'],['x1','X1'],['x3','X3'],['estado','Estado']];
const cell = (k,r) => (k === 'x1' || k === 'x3') ? res(r[k]) : r[k];

document.getElementById('supuestos').textContent =
'Cada fila se toma como una vaca sincronizada. ' +
(HAS_REJECT ? 'Las filas marcadas como RP (en donadora, reproductor, raza, tipo de embrión, X1 o X3) se cuentan como rechazo del protocolo y no como transferidas. '
            : 'Ninguna fila está marcada como RP, por lo que la aceptación del protocolo no se puede medir con estos datos. ') +
'X1 y X3 son confirmaciones de preñez (P+ o V). Si X1 es V, X3 toma el mismo valor; un valor vacío se toma como pendiente. Aborto: P+ en X1 y V en X3.';

document.getElementById('catdim').addEventListener('change', () => renderCat(filtered(), stats(filtered())));
document.getElementById('minn').addEventListener('input', () => renderCat(filtered(), stats(filtered())));
['topent','topcrit','toporden','topmin'].forEach(id => {
const el = document.getElementById(id);
el.addEventListener(id === 'topmin' ? 'input' : 'change', () => renderTop(filtered()));
});
document.getElementById('rpmin').addEventListener('input', () => renderRP(filtered()));
document.getElementById('reset').onclick = () => { Object.values(sel).forEach(s => s.clear()); render(); };
document.getElementById('csv').onclick = () => {
const rows = filtered();
const esc = v => '"' + String(v).replace(/"/g,'""') + '"';
const head = COLS.map(c => c[1].toUpperCase()).join(',');
const csv = [head].concat(rows.map(r => COLS.map(c => esc(cell(c[0], r))).join(','))).join('\n');
const a = document.createElement('a');
a.href = URL.createObjectURL(new Blob(['\ufeff'+csv], {type:'text/csv;charset=utf-8'}));
a.download = 'embriones_filtrados.csv'; a.click();
};

Chart.defaults.color = '#bfe3cf';
Chart.defaults.borderColor = 'rgba(190,255,220,.10)';
Chart.defaults.font.family = 'system-ui,-apple-system,"Segoe UI",Roboto,sans-serif';
Chart.defaults.plugins.legend.labels.usePointStyle = true;
buildFilters();
render();
</script>
</body>
</html>
"""

