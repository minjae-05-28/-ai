"""Page for the random-law Mars experiment: what a present-day Mars microbe would look like.

    python scripts/build_mars_page.py [--out results/mars.html]

Reads results/mars_random/metrics.json. Traits in the cell portrait come from the
simulation (median genome of surviving lineages); cell size, growth rate and habitat
come from Earth analogues and are marked as such.
"""

import argparse
import json
from pathlib import Path

KO = {
    "replication": "DNA 복제", "transcription": "전사", "translation": "번역", "membrane": "막 지질",
    "cell_division": "세포 분열", "chaperones": "샤페론", "regulation": "조절", "unknown": "기능 미상",
    "fermentation": "발효", "aerobic_respiration": "산소 호흡", "h2_oxidation": "수소 산화",
    "carbon_fixation": "탄소 고정", "photosynthesis": "광합성", "perchlorate_reduction": "과염소산염 환원",
    "transporters": "수송체", "amino_acid_synthesis": "아미노산 합성", "nucleotide_synthesis": "뉴클레오타이드 합성",
    "cofactor_synthesis": "보조인자 합성", "cold_adaptation": "저온 적응", "osmoprotection": "삼투 보호",
    "dna_repair": "DNA 수선", "oxidative_stress": "산화 스트레스 방어", "pigments_uv": "UV 색소",
    "dormancy": "휴면·포자", "motility": "운동(편모)",
}
SCEN_KO = {
    "gradual": "서서히 변화", "abrupt": "급변", "earth": "지구 대조군",
    "isolated_gradual": "고립 · 서서히", "isolated_abrupt": "고립 · 급변",
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--metrics", default="results/mars_random/metrics.json")
    ap.add_argument("--out", default="results/mars.html")
    args = ap.parse_args()
    m = json.loads(Path(args.metrics).read_text())
    from organelle_evo.mars import MODULES

    req = {k: v[1] for k, v in MODULES.items()}
    # Portrait from the most realistic scenario that still has survivors.
    portrait = next(sc for sc in ("isolated_gradual", "gradual") if sc in m["summary"] and m["summary"][sc]["survived"])
    data = {"m": m, "req": req, "ko": KO, "scen_ko": SCEN_KO, "portrait": portrait}
    Path(args.out).write_text(TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False)))
    print(f"wrote {args.out} (portrait from {portrait})")


TEMPLATE = r"""<title>화성 소금물 세포</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Gowun+Batang:wght@400;700&family=IBM+Plex+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: field report — one reading column; the cell portrait is the hero, with its key beside it */
:root {
  --bg: #eef1f1; --panel: #f9fafa; --fg: #17212a; --muted: #56636c; --line: #d3d9db;
  --dust: #a8571c; --dust-soft: #f1dfcf; --brine: #2f6f86; --brine-soft: #d6e7ec; --earth: #7d8a91;
  --display: "Gowun Batang", "Nanum Myeongjo", "AppleMyungjo", serif;
  --sans: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0f1519; --panel: #162026; --fg: #e3e9ec; --muted: #94a3ab; --line: #27343b;
  --dust: #e3955a; --dust-soft: #3d281a; --brine: #74b8cf; --brine-soft: #18323b; --earth: #7f8d95; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #0f1519; --panel: #162026; --fg: #e3e9ec; --muted: #94a3ab; --line: #27343b;
  --dust: #e3955a; --dust-soft: #3d281a; --brine: #74b8cf; --brine-soft: #18323b; --earth: #7f8d95; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font-family: var(--sans); font-size: 16px; line-height: 1.7; }
.page { max-width: 1000px; margin: 0 auto; padding-inline: 16px; padding-block: 36px 72px; display: grid; gap: 52px; }
.col { max-width: 720px; display: grid; gap: 14px; }
h1 { font-family: var(--display); font-weight: 700; font-size: clamp(36px, 7vw, 58px); line-height: 1.1; margin: 0; text-wrap: balance; }
h2 { font-family: var(--display); font-weight: 700; font-size: 24px; line-height: 1.3; margin: 0; text-wrap: balance; }
h3 { font-size: 15px; margin: 0; }
p { margin: 0; max-width: 66ch; }
.muted { color: var(--muted); }
.eyebrow { font-family: var(--mono); font-size: 12px; letter-spacing: 0.1em; text-transform: uppercase; color: var(--dust); }
.lede { font-size: 18px; }
.note { font-size: 14px; color: var(--muted); }
section { display: grid; gap: 16px; }
.key { display: grid; gap: 12px; padding: 0; margin: 0; list-style: none; }
.viewer { display: grid; grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 16px; }
@media (max-width: 680px) { .viewer { grid-template-columns: 1fr; } }
.pane { margin: 0; display: grid; gap: 10px; min-width: 0; }
.stage { position: relative; aspect-ratio: 1 / 0.82; max-width: 100%; background: radial-gradient(circle at 50% 45%, var(--panel), var(--bg) 75%); border: 1px solid var(--line); border-radius: 14px; overflow: hidden; touch-action: none; }
.stage canvas { width: 100%; height: 100%; display: block; cursor: grab; }
.stage .fallback { position: absolute; inset: 0; display: grid; place-items: center; color: var(--muted); font-size: 14px; }
figcaption { display: grid; gap: 6px; font-size: 15px; }
.chips { display: flex; flex-wrap: wrap; gap: 6px; }
.chip { font-size: 12px; padding: 2px 9px; border-radius: 99px; border: 1px solid var(--line); color: var(--muted); }
.chip.on { border-color: var(--dust); color: var(--fg); }
.controls { display: flex; flex-wrap: wrap; gap: 10px 18px; align-items: center; }
.seg { display: inline-flex; border: 1px solid var(--line); border-radius: 8px; overflow: hidden; }
.seg button { font: 500 14px var(--sans); padding: 7px 14px; border: 0; background: var(--panel); color: var(--muted); cursor: pointer; }
.seg button[aria-pressed="true"] { background: var(--fg); color: var(--bg); }
.parts { display: flex; flex-wrap: wrap; gap: 6px 16px; font-size: 13px; color: var(--muted); }
.parts span { display: inline-flex; align-items: center; gap: 6px; }
.parts i { width: 12px; height: 12px; border-radius: 3px; display: inline-block; }
.key { grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); column-gap: 28px; }

.key li { display: grid; grid-template-columns: 18px 1fr; gap: 10px; align-items: start; }
.key .n { width: 14px; height: 14px; margin-top: 6px; border-radius: 50%; background: var(--dust); color: var(--panel); font: 500 12px/22px var(--mono); text-align: center; }
.key .n.inf { background: transparent; color: var(--brine); border: 1.5px solid var(--brine); line-height: 19px; }
.key b { font-weight: 700; }
.key .ev { font-family: var(--mono); font-size: 12px; color: var(--muted); }
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 13px; color: var(--muted); align-items: center; }
.dot { display: inline-block; width: 12px; height: 12px; border-radius: 50%; vertical-align: -1px; margin-right: 6px; }
.frame { overflow-x: auto; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: left; padding: 8px 10px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-weight: 500; color: var(--muted); font-size: 12px; }
td.v { font-family: var(--mono); font-variant-numeric: tabular-nums; white-space: nowrap; }
td.mars { color: var(--dust); }
.scen { display: grid; gap: 10px; }
.srow { display: grid; grid-template-columns: 130px 1fr 64px; gap: 12px; align-items: center; font-size: 14px; }
.track { height: 14px; background: var(--brine-soft); border-radius: 3px; overflow: hidden; }
.fill { height: 100%; background: var(--brine); }
.fill.dead { background: var(--dust); }
.srow .pct { font-family: var(--mono); font-variant-numeric: tabular-nums; text-align: right; }
.mods { display: grid; gap: 4px; }
.mrow { display: grid; grid-template-columns: 128px 1fr 1fr; gap: 10px; align-items: center; font-size: 13px; }
.mrow.head { font-size: 12px; color: var(--muted); }
.bar { position: relative; height: 16px; }
.bar::before { content: ""; position: absolute; left: 50%; top: -2px; bottom: -2px; width: 1px; background: var(--line); }
.bar span { position: absolute; top: 2px; height: 12px; border-radius: 2px; }
.bar.mars span { background: var(--dust); }
.bar.earth span { background: var(--earth); }
@media (max-width: 520px) { .mrow, .srow { grid-template-columns: 96px 1fr 1fr; } .srow { grid-template-columns: 96px 1fr 52px; } }
.analog { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 12px; }
.analog > div { border-top: 2px solid var(--brine); padding-top: 10px; display: grid; gap: 4px; min-width: 0; }
.analog .val { font-family: var(--mono); font-size: 15px; }
.drivers { display: grid; gap: 8px; padding: 0; margin: 0; list-style: none; font-size: 14px; }
.drivers li { display: grid; grid-template-columns: 56px 1fr; gap: 10px; }
.drivers .r { font-family: var(--mono); font-variant-numeric: tabular-nums; }
.limits { display: grid; gap: 8px; padding-left: 18px; margin: 0; font-size: 15px; }
:focus-visible { outline: 2px solid var(--dust); outline-offset: 2px; }
[hidden] { display: none !important; }
</style>

<div class="page">
  <header class="col" style="gap:18px">
    <div class="eyebrow">organelle-evo · 화성 실험 · 학습한 법칙을 쓰지 않음</div>
    <h1>화성 소금물 세포</h1>
    <p class="lede">지금 화성 지하에 생명이 산다면 어떤 모습일까. 가장 단순한 세포 하나를 화성의 환경 변수 속에 두고, 진화 법칙은 무작위로 수백 번 바꿔 가며 진화시켰습니다. 어떤 법칙에서도 되풀이해 나타난 모습만 모았습니다.</p>
    <p class="note" id="scope"></p>
  </header>

  <section>
    <div class="eyebrow">예측한 모습</div>
    <h2>현재 화성에 산다면, 이런 세포</h2>
    <div class="viewer">
      <figure class="pane">
        <div class="stage"><canvas id="c-mars" aria-label="예측한 화성 세포 3D"></canvas><span class="fallback" hidden>이 브라우저에서는 3D를 표시할 수 없습니다.</span></div>
        <figcaption><b>화성 지하 소금물</b> <span class="note" id="cap-mars"></span><div class="chips" id="chips-mars"></div></figcaption>
      </figure>
      <figure class="pane">
        <div class="stage"><canvas id="c-earth" aria-label="지구 대조군 세포 3D"></canvas><span class="fallback" hidden>이 브라우저에서는 3D를 표시할 수 없습니다.</span></div>
        <figcaption><b>지구 토양 (대조군)</b> <span class="note" id="cap-earth"></span><div class="chips" id="chips-earth"></div></figcaption>
      </figure>
    </div>
    <div class="controls">
      <div class="seg" role="group" aria-label="크기 비교">
        <button type="button" id="b-same" aria-pressed="true">같은 크기로</button>
        <button type="button" id="b-real" aria-pressed="false">실제 크기 비율</button>
      </div>
      <span class="note">끌어서 돌려 보세요. 두 세포는 같은 무작위 법칙들로 같은 출발 세포에서 진화했습니다.</span>
    </div>
    <div class="parts" id="parts"></div>
    <ol class="key" id="key"></ol>
    <div class="legend"><span><span class="dot" style="background:var(--dust)"></span>시뮬레이션이 정한 특징</span><span><span class="dot" style="border:1.5px solid var(--brine)"></span>지구의 비슷한 생물에서 추론한 특징</span></div>
  </section>

  <section>
    <div class="eyebrow">지구 유사 생물에서 추론</div>
    <h2>얼마나 크고, 얼마나 느리고, 어디에 사나</h2>
    <p class="note">시뮬레이션은 유전자 구성만 정합니다. 아래는 비슷한 조건에 사는 지구 미생물에서 가져온 추정입니다.</p>
    <div class="analog" id="analog"></div>
  </section>

  <section>
    <div class="eyebrow">환경 변수</div>
    <h2>세포가 겪은 세 환경</h2>
    <div class="frame"><table id="env"></table></div>
  </section>

  <section>
    <div class="eyebrow">실험</div>
    <h2>무작위 법칙에서 얼마나 살아남았나</h2>
    <p class="note" id="method"></p>
    <div class="scen" id="scen"></div>
  </section>

  <section>
    <div class="eyebrow">유전체 변화</div>
    <h2>어떤 법칙에서도 같은 쪽으로 움직인 모듈</h2>
    <p class="note">막대는 살아남은 계통 중 그 모듈이 늘어난 비율에서 줄어든 비율을 뺀 값입니다. 오른쪽은 늘어남, 왼쪽은 줄어듦. 같은 무작위 법칙을 지구 환경에서 돌린 결과와 나란히 놓았습니다.</p>
    <div class="mods" id="mods"></div>
  </section>

  <section id="drv-sec" hidden>
    <div class="eyebrow">생존을 가른 것</div>
    <h2>어떤 법칙이 살아남았나</h2>
    <p class="note" id="drvnote"></p>
    <ul class="drivers" id="drivers"></ul>
  </section>

  <section class="col">
    <div class="eyebrow">한계</div>
    <h2>이 예측이 말하지 않는 것</h2>
    <ul class="limits">
      <li>지구 생명이 화성에 적응한 모습입니다. 화성에서 따로 생겨난 생명의 생화학은 전혀 다를 수 있습니다.</li>
      <li>환경마다 어떤 능력이 필요한지는 미리 정한 가정입니다. 실험이 보여 주는 것은 진화 법칙이 무엇이든 그 해법에 도달하는가입니다.</li>
      <li>유전자는 기능 모듈 25개로 묶은 단순화입니다. 세포 크기와 성장 속도는 모델 밖의 추론입니다.</li>
      <li>데이터로 학습한 환경 법칙(극한 미생물 36종)의 화성 예측은 수집이 끝나면 따로 비교합니다.</li>
    </ul>
  </section>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script>
const D = __DATA__;
const M = D.m, S = M.summary, P = S[D.portrait], start = M.start_genome, req = D.req, ko = D.ko;
const $ = (id) => document.getElementById(id);
const med = (mod) => P.modules[mod].median;
const has = (mod) => med(mod) >= 0.75 * req[mod];
const pct = (x) => Math.round(x * 100) + "%";

$("scope").textContent = `초상은 '${D.scen_ko[D.portrait]}' 시나리오에서 살아남은 계통 ${P.survived}개의 유전체 중앙값으로 그렸습니다.`;

// Traits: simulation-derived (filled marker) and analogue-derived (outlined marker).
const g = (mod) => P.modules[mod];
const traits = [];
if (has("h2_oxidation") && has("perchlorate_reduction"))
  traits.push(["sim", "수소를 먹고 과염소산염으로 숨쉰다", `수소 산화 ${med("h2_oxidation").toFixed(0)}개, 과염소산염 환원 ${med("perchlorate_reduction").toFixed(0)}개 유전자. 처음엔 없던 과염소산염 환원을 살아남은 계통의 ${pct(g("perchlorate_reduction").share_grew)}가 새로 얻었습니다. 화성 흙에 흔한 과염소산염(ClO₄⁻)이 독이자 산소 대신 쓰는 숨이 됩니다.`, "perc"]);
if (has("carbon_fixation"))
  traits.push(["sim", "CO₂를 고정해 스스로 몸을 만든다", `탄소 고정 ${med("carbon_fixation").toFixed(0)}개, 아미노산 합성 ${med("amino_acid_synthesis").toFixed(0)}개. 유기물이 거의 없으니 먹이를 흡수하는 대신 대기의 CO₂로 직접 만듭니다.`, "cfix"]);
traits.push(["sim", "추위와 소금에 맞춘 막과 세포질", `저온 적응 ${start.cold_adaptation} → ${med("cold_adaptation").toFixed(0)}개, 삼투 보호 ${start.osmoprotection} → ${med("osmoprotection").toFixed(0)}개 (각각 계통의 ${pct(g("cold_adaptation").share_grew)}, ${pct(g("osmoprotection").share_grew)}에서 증가). 영하에서도 굳지 않는 막과, 소금물에 쪼그라들지 않게 하는 용질을 만듭니다.`, "mem"]);
traits.push(["sim", "DNA 수선 장치가 두 배", `DNA 수선 ${start.dna_repair} → ${med("dna_repair").toFixed(0)}개 (계통의 ${pct(g("dna_repair").share_grew)}에서 증가). 지표 방사선은 지구의 수십 배이고, 얼어 있는 동안 쌓인 손상을 깨어날 때 고칩니다.`, "dna"]);
if (has("dormancy"))
  traits.push(["sim", "대부분의 시간을 휴면으로", `휴면·포자 0 → ${med("dormancy").toFixed(0)}개 (계통의 ${pct(g("dormancy").share_grew)}). 소금물이 잠깐 녹는 시기에만 활동합니다.`, "spore"]);
if (has("pigments_uv"))
  traits.push(["sim", "색소를 띤다", `UV 색소 0 → ${med("pigments_uv").toFixed(0)}개 (계통의 ${pct(g("pigments_uv").share_grew)}). 지구의 방사선 내성 세균처럼 카로티노이드 계열 색소로 활성 산소를 줄였을 것입니다.`, "pig"]);
traits.push(["sim", "편모와 쓸모없는 유전자는 버린다", `운동(편모) ${start.motility} → ${med("motility").toFixed(0)}개, 기능 미상 ${start.unknown} → ${med("unknown").toFixed(0)}개. 광합성(${med("photosynthesis").toFixed(0)})과 산소 호흡(${med("aerobic_respiration").toFixed(0)})은 생기지 않았습니다. 지하에는 빛도 산소도 없습니다.`, "flag"]);
traits.push(["inf", "아주 작은 세포", "지름 약 0.2–0.5 µm. 영구동토·심부 지하의 영양 부족 미생물이 이 크기입니다.", "size"]);
$("key").innerHTML = traits.map(([kind, t, d], i) => `<li><span class="n ${kind === "inf" ? "inf" : ""}"></span><div><b>${t}</b><br><span class="note">${d}</span></div></li>`).join("");

// 3D cells built from the median genome of surviving lineages in each scenario.
const PART_COLORS = {membrane: "#9db4bf", spore: "#c8a874", h2: "#d1a531", perc: "#b9531d", transport: "#5f87a8",
  dna: null, repair: "#d9662b", osmo: "#4fa3c4", pigment: "#e0812f", ribo: "#8f9aa3", flag: null, brine: "#5aa8c8"};
const partsKo = [["membrane", "세포막"], ["h2", "수소 산화 효소"], ["perc", "과염소산염 환원 효소"], ["transport", "영양 수송체"],
  ["repair", "DNA 수선 효소"], ["osmo", "삼투 보호 용질"], ["pigment", "색소 알갱이"], ["spore", "포자 외피"], ["ribo", "리보솜"]];
$("parts").innerHTML = partsKo.map(([k, n]) => `<span><i style="background:${PART_COLORS[k]}"></i>${n}</span>`).join("");

function cellSpec(sc) {
  const mods = S[sc].modules, v = (k) => mods[k].median || 0, ok = (k) => v(k) >= 0.75 * req[k];
  return {
    rod: sc === "earth", brine: sc !== "earth",
    h2: ok("h2_oxidation") ? Math.round(v("h2_oxidation") / 2) : 0,
    perc: ok("perchlorate_reduction") ? Math.round(v("perchlorate_reduction") * 1.5) : 0,
    transport: Math.round(v("transporters") / 2),
    repair: Math.round(v("dna_repair") / 2),
    osmo: Math.round(v("osmoprotection") * 25),
    pigment: ok("pigments_uv") ? Math.round(v("pigments_uv") * 3) : 0,
    spore: ok("dormancy"), flag: ok("motility"), ribo: Math.round(v("translation") / 2),
    chips: [["편모", ok("motility")], ["포자·휴면", ok("dormancy")], ["색소", ok("pigments_uv")], ["과염소산염 호흡", ok("perchlorate_reduction")],
      ["수소 산화", ok("h2_oxidation")], ["발효", ok("fermentation")], ["저온 적응", ok("cold_adaptation")], ["삼투 보호", ok("osmoprotection")]],
    genes: Math.round(Object.values(mods).reduce((a, m) => a + (m.median || 0), 0)),
  };
}

function rng(seed) { let s = seed >>> 0; return () => ((s = (s * 1664525 + 1013904223) >>> 0) / 4294967296); }

function buildCell(spec, fg) {
  const T = THREE, g = new T.Group(), r = rng(spec.rod ? 7 : 3);
  const R = 1, L = spec.rod ? 1.8 : 0;  // rod: cylinder length L between two hemispheres
  const mat = (c, o = {}) => new T.MeshStandardMaterial(Object.assign({color: c, roughness: 0.55, metalness: 0.05}, o));
  // envelope
  const shell = (rad, m) => {
    if (!L) return [new T.Mesh(new T.SphereGeometry(rad, 48, 32), m)];
    const cyl = new T.Mesh(new T.CylinderGeometry(rad, rad, L, 48, 1, true), m); cyl.rotation.z = Math.PI / 2;
    const a = new T.Mesh(new T.SphereGeometry(rad, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), m); a.rotation.z = -Math.PI / 2; a.position.x = L / 2;
    const b = new T.Mesh(new T.SphereGeometry(rad, 48, 24, 0, Math.PI * 2, 0, Math.PI / 2), m); b.rotation.z = Math.PI / 2; b.position.x = -L / 2;
    return [cyl, a, b];
  };
  const memM = mat(PART_COLORS.membrane, {transparent: true, opacity: 0.3, side: T.DoubleSide, depthWrite: false});
  shell(R, memM).forEach((m) => g.add(m));
  shell(R * 0.93, mat(PART_COLORS.membrane, {transparent: true, opacity: 0.12, side: T.DoubleSide, depthWrite: false})).forEach((m) => g.add(m));
  if (spec.spore) {
    const coat = new T.Mesh(new T.IcosahedronGeometry(R * 1.2, 2), mat(PART_COLORS.spore, {transparent: true, opacity: 0.22, flatShading: true, depthWrite: false}));
    g.add(coat);
    g.add(new T.Mesh(new T.IcosahedronGeometry(R * 1.2, 2), new T.MeshBasicMaterial({color: PART_COLORS.spore, wireframe: true, transparent: true, opacity: 0.35})));
  }
  if (spec.brine) g.add(new T.Mesh(new T.SphereGeometry(R * 1.75, 40, 24), mat(PART_COLORS.brine, {transparent: true, opacity: 0.07, depthWrite: false})));
  // a point on the envelope and its outward normal
  const surface = () => {
    const u = r() * 2 - 1, th = r() * Math.PI * 2, d = new T.Vector3(Math.sqrt(1 - u * u) * Math.cos(th), u, Math.sqrt(1 - u * u) * Math.sin(th));
    if (!L) return [d.clone().multiplyScalar(R), d];
    const x = (r() - 0.5) * (L + R), n = new T.Vector3(0, Math.cos(th), Math.sin(th));
    if (Math.abs(x) > L / 2) { const s = Math.sign(x), dd = d.clone(); dd.x = Math.abs(dd.x) * s; return [dd.clone().multiplyScalar(R).add(new T.Vector3(s * L / 2, 0, 0)), dd]; }
    return [n.clone().multiplyScalar(R).add(new T.Vector3(x, 0, 0)), n];
  };
  const inside = (scale = 0.8) => {
    for (;;) {
      const p = new T.Vector3((r() * 2 - 1) * (R + L / 2), (r() * 2 - 1) * R, (r() * 2 - 1) * R).multiplyScalar(scale);
      const ax = Math.max(Math.abs(p.x) - L / 2 * scale, 0);
      if (ax * ax + p.y * p.y + p.z * p.z < (R * scale) ** 2) return p;
    }
  };
  const protein = (n, color, h, w) => {
    const geo = new T.CylinderGeometry(w, w * 1.15, h, 10), m = mat(color, {roughness: 0.4});
    for (let i = 0; i < n; i++) {
      const [p, nrm] = surface(), mesh = new T.Mesh(geo, m);
      mesh.position.copy(p); mesh.quaternion.setFromUnitVectors(new T.Vector3(0, 1, 0), nrm); g.add(mesh);
    }
  };
  protein(spec.h2, PART_COLORS.h2, 0.2, 0.05);
  protein(spec.perc, PART_COLORS.perc, 0.24, 0.06);
  protein(spec.transport, PART_COLORS.transport, 0.16, 0.035);
  // nucleoid with repair enzymes on it
  const pts = []; for (let i = 0; i < 14; i++) pts.push(inside(0.5));
  const curve = new T.CatmullRomCurve3(pts, true);
  g.add(new T.Mesh(new T.TubeGeometry(curve, 240, 0.025, 8, true), mat(fg, {roughness: 0.7})));
  const rep = new T.OctahedronGeometry(0.055), repM = mat(PART_COLORS.repair, {roughness: 0.35});
  for (let i = 0; i < spec.repair; i++) { const m = new T.Mesh(rep, repM); m.position.copy(curve.getPointAt(i / spec.repair)); g.add(m); }
  // ribosomes, osmolytes, pigment granules
  const ribo = new T.SphereGeometry(0.035, 8, 6), riboM = mat(PART_COLORS.ribo);
  for (let i = 0; i < spec.ribo; i++) { const m = new T.Mesh(ribo, riboM); m.position.copy(inside(0.85)); g.add(m); }
  if (spec.osmo) {
    const pos = new Float32Array(spec.osmo * 3);
    for (let i = 0; i < spec.osmo; i++) { const p = inside(0.88); pos.set([p.x, p.y, p.z], i * 3); }
    const geo = new T.BufferGeometry(); geo.setAttribute("position", new T.BufferAttribute(pos, 3));
    g.add(new T.Points(geo, new T.PointsMaterial({color: PART_COLORS.osmo, size: 0.035, transparent: true, opacity: 0.8})));
  }
  const pig = new T.SphereGeometry(0.06, 10, 8), pigM = mat(PART_COLORS.pigment, {roughness: 0.3, emissive: PART_COLORS.pigment, emissiveIntensity: 0.15});
  for (let i = 0; i < spec.pigment; i++) { const [p] = surface(), m = new T.Mesh(pig, pigM); m.position.copy(p.multiplyScalar(0.88)); g.add(m); }
  // flagellum: a helix from one pole
  let flag = null;
  if (spec.flag) {
    const hp = []; for (let i = 0; i <= 120; i++) { const t = i / 120; hp.push(new T.Vector3(L / 2 + R + t * 3.2, 0.16 * Math.sin(t * 22), 0.16 * Math.cos(t * 22))); }
    flag = new T.Mesh(new T.TubeGeometry(new T.CatmullRomCurve3(hp), 200, 0.022, 6), mat(fg, {roughness: 0.6}));
    g.add(flag);
  }
  return {group: g, flag, span: L / 2 + R + (spec.flag ? 3.2 : 0), radius: spec.brine ? R * 1.8 : spec.spore ? R * 1.25 : R};
}

const views = [];
function makeView(canvasId, sc) {
  const canvas = $(canvasId), spec = cellSpec(sc);
  $(`chips-${sc === "earth" ? "earth" : "mars"}`).innerHTML = spec.chips.map(([n, on]) => `<span class="chip ${on ? "on" : ""}">${on ? "" : "없음 · "}${n}</span>`).join("");
  $(`cap-${sc === "earth" ? "earth" : "mars"}`).textContent = `유전자 약 ${spec.genes}개 · ${sc === "earth" ? "막대 모양, 지름 약 1 µm(지구 토양 세균 기준)" : "공 모양, 지름 약 0.3 µm(추론)"}`;
  let renderer;
  try { renderer = new THREE.WebGLRenderer({canvas, antialias: true, alpha: true, preserveDrawingBuffer: true}); }
  catch (e) { canvas.hidden = true; canvas.parentNode.querySelector(".fallback").hidden = false; return; }
  const scene = new THREE.Scene(), camera = new THREE.PerspectiveCamera(32, 1, 0.1, 100);
  scene.add(new THREE.HemisphereLight(0xffffff, 0x445566, 0.85));
  const key = new THREE.DirectionalLight(0xffffff, 0.75); key.position.set(3, 4, 5); scene.add(key);
  const v = {sc, spec, scene, camera, renderer, canvas, cell: null, scale: 1};
  v.controls = new THREE.OrbitControls(camera, canvas);
  v.controls.enablePan = false; v.controls.enableDamping = true; v.controls.minDistance = 3; v.controls.maxDistance = 16;
  v.rebuild = () => {
    if (v.cell) scene.remove(v.cell.group);
    v.cell = buildCell(spec, getComputedStyle(document.documentElement).getPropertyValue("--fg").trim());
    v.cell.group.rotation.set(0.35, 0.6, 0.15);
    scene.add(v.cell.group);
    applyScale(v);
  };
  views.push(v); v.rebuild();
  const resize = () => { const w = canvas.clientWidth, h = canvas.clientHeight; if (!w || !h) return;
    renderer.setPixelRatio(Math.min(devicePixelRatio, 2)); renderer.setSize(w, h, false); camera.aspect = w / h; camera.updateProjectionMatrix(); };
  new ResizeObserver(resize).observe(canvas); resize();
}

let realSize = false;
const EARTH_UM = 1.0, MARS_UM = 0.3;  // cell diameters (inferred from Earth analogues)
function applyScale(v) {
  // Same size: each cell fills its pane. Real ratio: both at the Earth cell's framing.
  const earthSpan = cellSpec("earth").flag ? 0.9 + 1 + 3.2 : 2;
  const fit = v.cell.span;
  const s = realSize ? (v.sc === "earth" ? 1 : MARS_UM / EARTH_UM) : 1;
  v.cell.group.scale.setScalar(s);
  const dist = realSize ? earthSpan * 2.1 : Math.max(fit * 2.4, v.cell.radius / 0.27);
  v.camera.position.set(0, dist * 0.18, dist); v.controls.target.set(0, 0, 0); v.controls.update();
}
const setReal = (on) => { realSize = on; $("b-real").setAttribute("aria-pressed", on); $("b-same").setAttribute("aria-pressed", !on); views.forEach(applyScale); };
$("b-real").addEventListener("click", () => setReal(true));
$("b-same").addEventListener("click", () => setReal(false));

const still = matchMedia("(prefers-reduced-motion: reduce)").matches;
if (window.THREE && THREE.OrbitControls) {
  makeView("c-mars", D.portrait);
  makeView("c-earth", "earth");
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => views.forEach((v) => v.rebuild()));
  new MutationObserver(() => views.forEach((v) => v.rebuild())).observe(document.documentElement, {attributes: true, attributeFilter: ["data-theme"]});
  let t = 0;
  (function loop() {
    t += 1;
    for (const v of views) {
      if (!still) v.cell.group.rotation.y += 0.0035;
      if (v.cell.flag && !still) v.cell.flag.rotation.x = t * 0.12;
      v.controls.update(); v.renderer.render(v.scene, v.camera);
    }
    requestAnimationFrame(loop);
  })();
} else {
  document.querySelectorAll(".stage canvas").forEach((c) => { c.hidden = true; c.parentNode.querySelector(".fallback").hidden = false; });
}


$("analog").innerHTML = [
  ["세포 크기", "0.2–0.5 µm", "영구동토·심부 지하 미생물, 초소형 세균(CPR)"],
  ["한 번 분열하는 데", "수백~수천 년", "에너지가 극도로 부족한 해저 퇴적층 미생물의 추정치"],
  ["사는 곳", "지하 수 m, 소금물 막", "지표는 방사선과 UV로 살균되고, 과염소산염 소금물은 −70 °C까지 얼지 않음"],
  ["가장 닮은 지구 생물", "Planococcus halocryophilus 등", "−15 °C 소금물에서 자라는 영구동토 세균, 과염소산염 호흡 세균 Dechloromonas, 방사선 내성 Deinococcus"],
].map(([k, v, d]) => `<div><span class="note">${k}</span><span class="val">${v}</span><span class="note">${d}</span></div>`).join("");

const envs = Object.entries(M.environments);
const rows = [["temp_c", "온도", (v) => `${v} °C`], ["salt_pct", "염분", (v) => `${v}%`], ["o2_pal", "산소 (지구 대기 = 1)", (v) => v], ["radiation_x", "방사선 (지구 지표 = 1)", (v) => `${v}×`],
  ["organics", "유기물 (0–1)", (v) => v], ["h2", "수소 (0–1)", (v) => v], ["perchlorate", "과염소산염 (0–1)", (v) => v], ["light", "빛 (0–1)", (v) => v]];
const envKo = {"Earth soil": "지구 토양", "early Mars lake (~3.8 Gya)": "초기 화성 호수 (38억 년 전)", "present Mars subsurface brine": "현재 화성 지하 소금물"};
$("env").innerHTML = `<tr><th>환경 변수</th>${envs.map(([n]) => `<th>${envKo[n] || n}</th>`).join("")}</tr>` +
  rows.map(([k, label, f]) => `<tr><td>${label}</td>${envs.map(([n, e], i) => `<td class="v ${i === 2 ? "mars" : ""}">${f(e[k])}</td>`).join("")}</tr>`).join("");

const nLaws = S.gradual.n_laws;
$("method").textContent = `출발점은 LUCA를 닮은 최소 세포(유전자 ${Object.values(start).reduce((a, b) => a + b, 0)}개, 모듈 25개)입니다. 무작위 법칙은 모듈마다 유전자가 사라지고, 복제되고, 새로 들어오는 속도가 환경 변수에 어떻게 반응할지를 정합니다. 법칙 하나에 계수 600개, 시나리오마다 ${nLaws}개를 뽑아 세포 300개 집단을 6,000세대 진화시켰습니다. '고립'은 화성에 유전자를 받아 올 다른 생물이 없다고 보고 새 유전자 획득을 2%로 줄인 조건입니다.`;
const order = ["earth", "gradual", "abrupt", "isolated_gradual", "isolated_abrupt"].filter((k) => S[k]);
$("scen").innerHTML = order.map((k) => `<div class="srow"><span>${D.scen_ko[k]}</span><div class="track"><div class="fill ${S[k].survival_rate < 0.5 ? "dead" : ""}" style="width:${S[k].survival_rate * 100}%"></div></div><span class="pct">${pct(S[k].survival_rate)}</span></div>`).join("") +
  `<p class="note">생존한 법칙의 비율. 각 막대 ${nLaws}개 법칙(지구 대조군 ${S.earth.n_laws}개).</p>`;

const net = (sc, mod) => S[sc].modules[mod].share_grew - S[sc].modules[mod].share_shrank;
const mods = Object.keys(start).sort((a, b) => Math.abs(net(D.portrait, b) - net("earth", b)) - Math.abs(net(D.portrait, a) - net("earth", a)));
const bar = (v, cls) => `<div class="bar ${cls}"><span style="${v >= 0 ? `left:50%;width:${v * 50}%` : `left:${50 + v * 50}%;width:${-v * 50}%`}"></span></div>`;
$("mods").innerHTML = `<div class="mrow head"><span>모듈</span><span>화성 (${D.scen_ko[D.portrait]})</span><span>지구 대조군</span></div>` +
  mods.map((k) => `<div class="mrow" title="화성 ${net(D.portrait, k).toFixed(2)} · 지구 ${net("earth", k).toFixed(2)}"><span>${ko[k]}</span>${bar(net(D.portrait, k), "mars")}${bar(net("earth", k), "earth")}</div>`).join("");

if (M.survival_drivers && M.survival_drivers.length) {
  $("drv-sec").hidden = false;
  const kindKo = {loss: "소실", dup: "복제", gain: "획득"}, stKo = {cold: "추위", salt: "염분", o2: "산소", radiation: "방사선", organics: "유기물", h2: "수소", perchlorate: "과염소산염", light: "빛"};
  $("drvnote").textContent = `'${D.scen_ko[M.driver_scenario] || M.driver_scenario}' 시나리오에서 살아남은 법칙과 멸종한 법칙을 가른 계수입니다. r은 그 계수와 생존의 상관입니다. 양수면 그 반응이 클수록 살아남았습니다.`;
  $("drivers").innerHTML = M.survival_drivers.slice(0, 8).map((d) => `<li><span class="r">${d.corr_with_survival >= 0 ? "+" : "−"}${Math.abs(d.corr_with_survival).toFixed(2)}</span><span>${stKo[d.stress]}에 따라 <b>${ko[d.module]}</b> 유전자의 ${kindKo[d.kind]} 속도가 ${d.corr_with_survival >= 0 ? "빨라지는" : "느려지는"} 법칙일수록 생존</span></li>`).join("");
}
</script>
"""

if __name__ == "__main__":
    main()
