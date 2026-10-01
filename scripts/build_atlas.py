"""Build the one-page visual summary (results/atlas.html) from laws/ and results/.

    python scripts/build_atlas.py [--out results/atlas.html]
"""

import argparse
import json
from pathlib import Path

FEATURES_KO = {
    "hydrophobicity_gravy": "소수성",
    "tm_helices": "막관통 나선",
    "protein_length": "단백질 길이",
    "redox_core": "전자전달 핵심",
    "atp_synthase": "ATP 합성효소",
    "translation": "번역 장치",
    "transcription": "전사(RNA 중합효소)",
    "protein_targeting": "단백질 수송",
}


def load(path):
    p = Path(path)
    return json.loads(p.read_text()) if p.exists() else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="results/atlas.html")
    args = ap.parse_args()

    endo = load("laws/endosymbiosis_v1.json")
    life = load("laws/eukaryote_lifestyle_v1.json")
    axes = load("laws/eukaryote_axes_v1.json")
    euk = load("results/eukaryotes/metrics.json")
    plas = load("results/plasmodium_ancestor/metrics.json")
    axes_m = load("results/eukaryote_axes/metrics.json")
    real = load("results/real/metrics.json")

    rows = []
    for ctx, label in [("mitochondrion", "미토콘드리아"), ("plastid", "엽록체·색소체"),
                       ("insect_endosymbiont", "곤충 공생세균")]:
        rows.append({"group": "공생 소기관·공생체 (endosymbiosis_v1)", "label": label,
                     "cells": endo["contexts"][ctx]})
    for ctx, label in [("loss_free_living", "자유생활"), ("loss_parasite", "기생")]:
        rows.append({"group": "진핵생물 유전자군 소실 (eukaryote_lifestyle_v1)", "label": label,
                     "cells": life["contexts"][ctx]})
    if axes:
        for ctx, label in [("loss_base", "기본"), ("loss_parasite", "+ 기생"),
                           ("loss_intracellular", "+ 세포 안"), ("loss_reduced_mitochondria", "+ 미토콘드리아 퇴화")]:
            rows.append({"group": "축별 소실 효과 (eukaryote_axes_v1)", "label": label,
                         "cells": axes["contexts"][ctx]})

    data = {
        "features": [[k, v] for k, v in FEATURES_KO.items()],
        "rows": rows,
        "stats": {
            "symbiont_genomes": sum(v["n_genomes"] for k, v in real.items() if k != "universality"),
            "eukaryotes": 32,
            "euk_pairs": len(euk["pairs"]),
            "delta_aic_endo": real["universality"]["delta_aic_shared_minus_separate"],
            "delta_aic_life": euk["delta_aic_lifestyle_vs_shared"],
        },
        "heldout": [
            {"name": r["pair"].split(" -> ")[1], "copies": r["copies_only"], "law": r["learned_law"],
             "ref": r["reference_plastid"], "memo": r["loss_frequency_elsewhere"]}
            for r in euk["heldout_parasites"]
        ],
        "similarity": euk["comparison_with_endosymbiosis_v1"],
        "scenario": euk["scenario_dictyostelium"],
        "plasmodium": plas,
        "axes_done": axes is not None,
        "axes_metrics": axes_m,
        "n_laws": len(list(Path("laws").glob("*.json"))),
        "n_species": len([f for f in Path("data/eukaryotes").glob("*.json")
                          if f.name not in ("pfam_meta.json", "family_annotations.json")]),
        "enrich": load("results/features/metrics.json"),
        "severity": load("results/severity/metrics.json"),
        "order": load("results/loss_order/metrics.json"),
        "modules": load("results/modules/metrics.json"),
        "expansion": load("results/expansion/metrics.json"),
        "transfer": load("results/transfer/metrics.json"),
        "nested": load("results/nestedness/metrics.json"),
        "sequence": load("results/sequence/metrics.json"),
        "family_seq": load("results/family_sequence/metrics.json"),
        "phylo": load("results/phylo/metrics.json"),
        "gc": load("results/gc_confound/metrics.json"),
        "n_literature": len(json.loads(Path("laws/literature/laws.json").read_text())["laws"]),
    }
    if data["sequence"]:
        q = data["sequence"]
        data["sequence"] = {"temperature": q["temperature"],
                            "salt": {k: q["salt"][k] for k in ("spearman_acidic_excess", "spearman_median_pi")},
                            "pairs_r2": {k: v.get("loo_r2_environment") for k, v in q["environment_pairs"]["by_statistic"].items()},
                            "n_pairs": q["environment_pairs"]["n_pairs"],
                            "oligo": q["oligotrophy"], "symb": {k: q["endosymbionts"][k] for k in ("spearman_size_fymink", "spearman_size_pi")}}
    if data["family_seq"]:
        data["family_seq"] = {k: {kk: v[kk] for kk in ("families_tested", "share_positive")}
                              for k, v in data["family_seq"].items() if isinstance(v, dict)}
    if data["enrich"]:
        data["enrich"] = {k: data["enrich"][k] for k in ("n_features", "mean_heldout_auroc")}
    if data["modules"]:
        data["modules"] = {k: data["modules"][k] for k in ("mean_auroc_hidden", "best_k", "gain_vs_additive", "n_pairs")}
    if data["order"]:
        data["order"].pop("comparisons", None)
    if data["transfer"]:
        data["transfer"].pop("heldout", None)
    html = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False))
    Path(args.out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.out).write_text(html)
    print(f"wrote {args.out}")


TEMPLATE = r"""<title>진화 법칙 지도</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans+KR:wght@400;500;700&family=IBM+Plex+Mono:wght@400;500&display=swap">
<style>
/* Layout: a single reading column (lab notebook), wide figures scroll inside their own frames */
:root {
  --bg: #f5f6f2; --panel: #ffffff; --fg: #1d2420; --muted: #5e6a63; --line: #d9ddd5;
  --keep: #1f6f78; --keep-soft: #cfe6e7; --lose: #c2551e; --lose-soft: #f6dccd; --accent: #1f6f78;
  --pending: #8a7a2b;
  --sans: "IBM Plex Sans KR", "Apple SD Gothic Neo", "Malgun Gothic", system-ui, sans-serif;
  --mono: "IBM Plex Mono", ui-monospace, "SFMono-Regular", Menlo, monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #121614; --panel: #1a201d; --fg: #e3e8e4; --muted: #9aa69f; --line: #2c3530;
  --keep: #5fb8c1; --keep-soft: #1d3a3d; --lose: #e98a55; --lose-soft: #4a2b1c; --accent: #5fb8c1;
  --pending: #d1bd62; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #121614; --panel: #1a201d; --fg: #e3e8e4; --muted: #9aa69f; --line: #2c3530;
  --keep: #5fb8c1; --keep-soft: #1d3a3d; --lose: #e98a55; --lose-soft: #4a2b1c; --accent: #5fb8c1;
  --pending: #d1bd62; color-scheme: dark }
body { background: var(--bg); color: var(--fg); font-family: var(--sans); font-size: 15px; line-height: 1.6; }
.wrap { max-width: 980px; margin: 0 auto; padding-inline: 16px; padding-block: 28px 64px; display: grid; gap: 40px; }
h1 { font-size: clamp(26px, 5vw, 36px); line-height: 1.2; margin: 0; text-wrap: balance; font-weight: 700; letter-spacing: -0.01em; }
h2 { font-size: 20px; margin: 0; text-wrap: balance; }
p { margin: 0; max-width: 65ch; }
.lede { color: var(--muted); }
.eyebrow { font-family: var(--mono); font-size: 12px; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent); }
section { display: grid; gap: 14px; }
.stats { display: flex; flex-wrap: wrap; gap: 8px 22px; font-family: var(--mono); font-size: 13px; color: var(--muted); }
.stats b { color: var(--fg); font-weight: 500; font-variant-numeric: tabular-nums; }
.flow { display: grid; grid-template-columns: repeat(auto-fit, minmax(230px, 1fr)); gap: 12px; }
.law { background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 14px 16px; display: grid; gap: 6px; min-width: 0; position: relative; }
.law .id { font-family: var(--mono); font-size: 13px; color: var(--accent); }
.law .scope { font-size: 14px; }
.law .data { font-size: 13px; color: var(--muted); }
.law.pending { border-style: dashed; }
.law.pending .id { color: var(--pending); }
.tag { display: inline-block; font-family: var(--mono); font-size: 11px; padding: 1px 7px; border-radius: 99px; border: 1px solid currentColor; }
.frame { overflow-x: auto; background: var(--panel); border: 1px solid var(--line); border-radius: 10px; padding: 12px; }
table.heat { border-collapse: separate; border-spacing: 3px; font-size: 13px; min-width: 760px; }
.heat th { font-weight: 500; color: var(--muted); font-size: 12px; text-align: center; padding: 4px; vertical-align: bottom; }
.heat th.row { text-align: left; color: var(--fg); font-size: 13px; white-space: nowrap; padding-right: 10px; }
.heat td.group { font-family: var(--mono); font-size: 11px; color: var(--accent); padding-top: 12px; }
.heat td.cell { width: 76px; height: 38px; text-align: center; border-radius: 5px; font-family: var(--mono); font-variant-numeric: tabular-nums; font-size: 12px; }
.heat td.cell.ns { background-image: repeating-linear-gradient(45deg, transparent 0 5px, color-mix(in srgb, var(--bg) 55%, transparent) 5px 7px); }
.legend { display: flex; flex-wrap: wrap; gap: 6px 18px; font-size: 12px; color: var(--muted); align-items: center; }
.swatch { display: inline-block; width: 14px; height: 14px; border-radius: 3px; vertical-align: -2px; margin-right: 5px; }
.findings { display: grid; gap: 10px; padding: 0; margin: 0; list-style: none; }
.findings li { display: grid; grid-template-columns: 28px 1fr; gap: 10px; align-items: start; }
.findings .k { font-family: var(--mono); font-size: 12px; color: var(--accent); padding-top: 3px; }
svg text { fill: var(--fg); font-family: var(--sans); }
svg .muted { fill: var(--muted); }
.two { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.two > * { min-width: 0; }
.note { font-size: 13px; color: var(--muted); }
.pending-box { border: 1px dashed var(--pending); border-radius: 10px; padding: 14px 16px; display: grid; gap: 6px; }
.pending-box .tag { color: var(--pending); justify-self: start; }
:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
</style>

<div class="wrap">
  <header style="display:grid;gap:12px">
    <div class="eyebrow">organelle-evo · 연구 요약</div>
    <h1>진화 법칙 지도</h1>
    <p class="lede">공생 세균이 소기관이 되는 과정, 그리고 자유생활 생물이 기생생물이 되는 과정에서 어떤 유전자가 남고 어떤 유전자가 사라지는지, 그리고 극한 환경 세균이 단백질 서열을 어떻게 바꾸는지를 실제 유전체에서 학습한 법칙들입니다.</p>
    <div class="stats" id="stats"></div>
  </header>

  <section>
    <div class="eyebrow">법칙 계보</div>
    <h2>법칙은 어떻게 쌓였나</h2>
    <div class="flow" id="flow"></div>
  </section>

  <section>
    <div class="eyebrow">법칙 지도</div>
    <h2>무엇이 남고, 무엇이 사라지나</h2>
    <p class="note">칸의 숫자는 유전자가 사라지는 속도에 대한 효과입니다. 파란색은 <b>남는 쪽</b>, 주황색은 <b>사라지는 쪽</b>이고, 빗금 친 칸은 95% 신뢰구간이 0을 포함해 확실하지 않은 값입니다.</p>
    <div class="frame"><table class="heat" id="heat"></table></div>
    <div class="legend" id="legend"></div>
  </section>

  <section>
    <div class="eyebrow">핵심 발견</div>
    <h2>지금까지 알게 된 것</h2>
    <ul class="findings" id="findings"></ul>
  </section>

  <section>
    <div class="eyebrow">검증</div>
    <h2>처음 보는 기생생물의 유전자 소실을 맞힐 수 있나</h2>
    <p class="note">기생생물 하나를 빼고 학습한 뒤, 그 종이 어떤 유전자군을 잃었는지 맞히게 했습니다. 점수는 AUROC이고, 0.5는 무작위, 1.0은 완벽입니다.</p>
    <div class="frame"><svg id="dots" role="img" aria-label="보류 기생생물별 예측 정확도"></svg></div>
    <div class="legend" id="dotlegend"></div>
  </section>

  <section>
    <div class="eyebrow">실험</div>
    <h2>말라리아 원충의 원형을 다른 법칙으로 진화시키기</h2>
    <p class="note">알베올라타 계통수로 공통 조상의 유전자군을 복원한 뒤(말라리아 원충은 빼고 복원해 정답이 새지 않게 함), 여러 법칙으로 진화시켜 실제 말라리아 원충과 비교했습니다.</p>
    <div class="two">
      <div class="frame"><svg id="tree" viewBox="0 0 360 236" role="img" aria-label="알베올라타 계통수"></svg></div>
      <div class="frame"><svg id="plasbars" role="img" aria-label="법칙별 정확도"></svg></div>
    </div>
    <div class="frame"><table class="heat" id="plasclass" style="min-width:560px"></table></div>
  </section>

  <section id="axes-sec" hidden>
    <div class="eyebrow">축별 법칙</div>
    <h2>기생을 세 축으로 나눠 보니</h2>
    <p class="note">법칙을 "기본 + 기생 효과 + 세포 안 효과 + 미토콘드리아 퇴화 효과"의 합으로 학습했습니다. 진핵생물 32종, 비교 쌍 22개입니다.</p>
    <div class="two">
      <div class="frame"><svg id="aic" role="img" aria-label="모델 비교"></svg></div>
      <div class="frame"><table class="heat" id="axeshl" style="min-width:320px"></table></div>
    </div>
    <h2 style="font-size:17px">말라리아 원충 원형, 다시: 자유생활 친척(Chromera·Vitrella)과 함께 복원</h2>
    <div class="frame"><table class="heat" id="plas2" style="min-width:620px"></table></div>
    <p class="note" id="plas2note"></p>
  </section>

  <section id="r2" hidden>
    <div class="eyebrow">법칙 탐색 2라운드 · 진핵생물 <span id="r2n"></span></div>
    <h2>특성을 늘리고, 새로운 종류의 법칙을 찾다</h2>
    <p class="note">유전자군을 묘사하는 특성을 8개에서 56개로 늘렸습니다(GO 기능, Pfam 클랜, 기능 키워드, 자유생활 종에서의 흔한 정도). 그리고 "어떤 유전자가 사라지나" 말고도 <b>얼마나</b>, <b>어떤 순서로</b>, <b>함께</b>, <b>늘어나는 쪽</b>을 따로 물었습니다.</p>
    <div class="two">
      <div class="frame"><svg id="featbars" role="img" aria-label="특성 풍부화 전후 예측 정확도"></svg></div>
      <div class="frame"><svg id="sevbars" role="img" aria-label="생활 방식별 유전자군 소실 비율"></svg></div>
    </div>
    <div class="flow" id="r2laws"></div>
  </section>

  <section id="r3" hidden>
    <div class="eyebrow">법칙 탐색 3라운드 · 단백질 서열과 계통 보정</div>
    <h2>환경 적응은 단백질 서열에 있다</h2>
    <p class="note">극한 환경 세균의 유전자 소실은 환경으로 예측되지 않았습니다. 그래서 단백질 아미노산 조성을 봤고, 모든 종 단위 법칙을 NCBI 분류 단계별 분산 GLS로 다시 검정했습니다.</p>
    <div class="flow" id="r3laws"></div>
    <h2 style="font-size:17px">계통 보정 전후 유의성</h2>
    <p class="note">점이 오른쪽일수록 강한 증거입니다(−log₁₀ p). 회색은 보정 전(종을 독립으로 취급), 색은 보정 후입니다. 점선은 p = 0.05입니다.</p>
    <div class="frame"><svg id="phylo" role="img" aria-label="계통 보정 전후 p값"></svg></div>
  </section>

  <section>
    <div class="eyebrow">다음</div>
    <h2>진행 중인 작업과 다음 단계</h2>
    <div class="flow" id="next"></div>
  </section>
</div>

<script>
const D = __DATA__;
const $ = (id) => document.getElementById(id);
const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
const f2 = (x) => (x >= 0 ? "+" : "−") + Math.abs(x).toFixed(2);

$("stats").innerHTML = [
  ["공생체·소기관 유전체", D.stats.symbiont_genomes],
  ["진핵생물", (D.n_species || D.stats.eukaryotes) + "종"],
  ["비교 쌍", (D.severity ? Object.keys(D.severity.severity).length : 22) + "개"],
  ["저장된 법칙", D.n_laws + "개"],
  ...(D.n_literature ? [["문헌 법칙", D.n_literature + "개"]] : []),
].map(([k, v]) => `<span>${k} <b>${v}</b></span>`).join("");

const laws = [
  {id: "endosymbiosis_v1", scope: "의무적 공생에서의 유전체 축소. 소기관과 곤충 공생세균이 어떤 유전자를 남기는가.",
   data: `실제 유전체 ${D.stats.symbiont_genomes}개 · 세 시스템의 법칙이 서로 다름 (ΔAIC ${D.stats.delta_aic_endo.toFixed(0)})`, tag: "저장됨"},
  {id: "eukaryote_lifestyle_v1", scope: "진핵생물 유전자군의 복제와 소실. 자유생활과 기생을 따로 학습.",
   data: `진핵생물 23종, 14쌍 · 기생이 법칙을 바꿈 (ΔAIC ${D.stats.delta_aic_life.toFixed(0)})`, tag: "저장됨"},
  {id: "eukaryote_axes_v1", scope: "기본 법칙 + 기생 효과 + 세포 안 효과 + 미토콘드리아 퇴화 효과로 나눈 법칙.",
   data: D.axes_done ? `진핵생물 32종, 22쌍 · 나누는 편이 더 잘 맞음 (ΔAIC ${D.axes_metrics.aic_relative.parasite_only.toFixed(0)})` : "진핵생물 32종, 22쌍 · 분석 중", tag: D.axes_done ? "저장됨" : "진행 중", pending: !D.axes_done},
];
$("flow").innerHTML = laws.map((l, i) => `
  <div class="law ${l.pending ? "pending" : ""}">
    <div style="display:flex;justify-content:space-between;gap:8px;align-items:center">
      <span class="id">${String(i + 1)}. ${l.id}</span><span class="tag" style="color:${l.pending ? "var(--pending)" : "var(--accent)"}">${l.tag}</span>
    </div>
    <div class="scope">${l.scope}</div>
    <div class="data">${l.data}</div>
  </div>`).join("");

function heatColor(w) {
  const t = Math.min(Math.abs(w) / 2.5, 1);
  const base = w < 0 ? css("--keep") : css("--lose");
  return `color-mix(in srgb, ${base} ${Math.round(12 + t * 78)}%, var(--panel))`;
}
(function heat() {
  const feats = D.features;
  let h = "<tr><th></th>" + feats.map(([, ko]) => `<th>${ko}</th>`).join("") + "</tr>";
  let group = null;
  for (const r of D.rows) {
    if (r.group !== group) { group = r.group; h += `<tr><td class="group" colspan="${feats.length + 1}">${group}</td></tr>`; }
    h += `<tr><th class="row" scope="row">${r.label}</th>` + feats.map(([k]) => {
      const c = r.cells[k]; const [lo, hi] = c.ci95; const ns = lo <= 0 && hi >= 0;
      const strong = Math.abs(c.weight) > 1.4;
      return `<td class="cell ${ns ? "ns" : ""}" style="background-color:${heatColor(c.weight)};color:${strong ? "var(--panel)" : "var(--fg)"}" title="${r.label} · ${k}: ${f2(c.weight)} [${lo.toFixed(2)}, ${hi.toFixed(2)}]">${f2(c.weight)}</td>`;
    }).join("") + "</tr>";
  }
  $("heat").innerHTML = h;
  $("legend").innerHTML = `<span><span class="swatch" style="background:${heatColor(-2.5)}"></span>강하게 남음</span>
    <span><span class="swatch" style="background:${heatColor(-0.6)}"></span>약하게 남음</span>
    <span><span class="swatch" style="background:${heatColor(0.6)}"></span>약하게 사라짐</span>
    <span><span class="swatch" style="background:${heatColor(2.5)}"></span>강하게 사라짐</span>
    <span><span class="swatch" style="background:${heatColor(0.3)};background-image:repeating-linear-gradient(45deg,transparent 0 3px,var(--bg) 3px 5px)"></span>불확실</span>`;
})();

const sim = D.similarity;
const sc = D.scenario;
const findings = [
  ["에너지와 번역은 어디서나 남는다", "전자전달 핵심, ATP 합성효소, 번역 장치는 소기관·공생세균·기생생물 모두에서 남는 쪽입니다."],
  ["RNA 중합효소는 시스템마다 반대", "미토콘드리아는 세균형 RNA 중합효소를 버렸고(소실 효과 +1.02), 엽록체는 강하게 지킵니다(−2.55). 실제 역사와 같은 방향입니다."],
  ["막단백질이 남는 효과는 미토콘드리아에서만", "핵으로 옮겨 갈 길이 있을 때만 나타나는 효과로, 소수성 가설과 맞습니다."],
  ["기생은 법칙을 바꾼다", `기생 계통은 유전자군을 대량으로 잃지만 핵심 장치는 더 강하게 지킵니다. 이 소실 법칙은 저장된 엽록체 공생 법칙과 상관 ${sim.parasite_loss_vs_plastid.correlation.toFixed(2)}로 닮았습니다.`],
  ...(D.axes_done ? [["미토콘드리아 퇴화가 에너지 유전자를 버리게 한다", `기생을 세 축으로 나누니, 전자전달 유전자를 버리는 효과는 기생 자체가 아니라 미토콘드리아 퇴화(+${D.axes_metrics.loss_effects.reduced_mitochondria.redox_core.weight.toFixed(2)})와 세포 안 생활(+${D.axes_metrics.loss_effects.intracellular.redox_core.weight.toFixed(2)})에서 왔습니다. 기생 자체는 ATP 합성효소를 오히려 더 지킵니다(${D.axes_metrics.loss_effects.parasite.atp_synthase.weight.toFixed(2)}).`]] : []),
  ["자유생활 아메바를 기생으로 전환하면", `딕티오스텔리움(유전자군 ${sc.become_parasite.families_now.toLocaleString()}개)이 기생 법칙으로 진화하면 약 ${Math.round(sc.become_parasite.families_after[1]).toLocaleString()}개가 남습니다. 실제 기생 아메바인 이질아메바는 ${sc.actual_Entamoeba_families.toLocaleString()}개입니다(학습에 포함된 쌍이라 독립 검증은 아님).`],
];
$("findings").innerHTML = findings.map(([t, d], i) => `<li><span class="k">${String(i + 1).padStart(2, "0")}</span><div><b>${t}</b><br><span class="note">${d}</span></div></li>`).join("");

(function dots() {
  const rows = D.heldout, W = 720, rowH = 30, top = 28, left = 190, right = 20;
  const H = top + rows.length * rowH + 30;
  const x = (v) => left + (v - 0.5) / 0.45 * (W - left - right);
  const series = [["copies", "복제 수 기준선", css("--muted")], ["law", "학습된 법칙", css("--lose")],
                  ["ref", "엽록체 공생 법칙(참고)", css("--keep")], ["memo", "다른 기생생물 소실 빈도(암기)", css("--fg")]];
  let s = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">`;
  for (const t of [0.5, 0.6, 0.7, 0.8, 0.9]) {
    s += `<line x1="${x(t)}" x2="${x(t)}" y1="${top - 8}" y2="${H - 24}" stroke="${css("--line")}"/>`;
    s += `<text x="${x(t)}" y="${H - 8}" text-anchor="middle" font-size="11" class="muted">${t.toFixed(1)}</text>`;
  }
  rows.forEach((r, i) => {
    const y = top + i * rowH + rowH / 2;
    s += `<text x="${left - 12}" y="${y + 4}" text-anchor="end" font-size="12" font-style="italic">${r.name}</text>`;
    const vals = series.map(([k]) => r[k]);
    s += `<line x1="${x(Math.min(...vals))}" x2="${x(Math.max(...vals))}" y1="${y}" y2="${y}" stroke="${css("--line")}" stroke-width="2"/>`;
    series.forEach(([k, , c], j) => {
      s += `<circle cx="${x(r[k])}" cy="${y}" r="${j === 1 ? 6 : 4.5}" fill="${c}" stroke="${css("--panel")}" stroke-width="1.5"><title>${series[j][1]}: ${r[k].toFixed(3)}</title></circle>`;
    });
  });
  $("dots").outerHTML = s + "</svg>";
  $("dotlegend").innerHTML = series.map(([, n, c]) => `<span><span class="swatch" style="background:${c};border-radius:50%"></span>${n}</span>`).join("");
})();

(function tree() {
  const svg = $("tree"), c = css("--fg"), acc = css("--accent"), lose = css("--lose"), mut = css("--muted");
  const leaves = [["말라리아 원충", 30, true], ["톡소플라스마", 70], ["크립토스포리디움", 110], ["테트라히메나", 160], ["백점충", 200]];
  let s = "";
  const lx = 210;
  leaves.forEach(([n, y, hl]) => { s += `<text x="${lx + 8}" y="${y + 4}" font-size="13" ${hl ? `fill="${lose}" font-weight="700"` : ""}>${n}</text>`; });
  const path = (d, col = c, w = 1.6, dash = "") => `<path d="${d}" stroke="${col}" stroke-width="${w}" fill="none" ${dash ? `stroke-dasharray="${dash}"` : ""}/>`;
  // (Plasmodium, Toxoplasma) joins at x=150; + Cryptosporidium at x=100; ciliates at x=130; root at x=40
  s += path(`M150 30 H${lx}`, lose, 2.2, "5 4") + path(`M150 30 V70 M150 70 H${lx}`);
  s += path(`M100 50 H150 M100 50 V110 M100 110 H${lx}`);
  s += path(`M130 160 H${lx} M130 160 V200 M130 200 H${lx}`);
  s += path(`M40 80 V180 M40 80 H100 M40 180 H130`);
  s += `<circle cx="40" cy="130" r="9" fill="${acc}"/>`;
  s += `<text x="14" y="222" font-size="11" fill="${acc}">● 복원한 원형 · 유전자군 ${D.plasmodium.ancestor_families_without_plasmodium.toLocaleString()}개</text>`;
  s += `<text x="${lx + 8}" y="222" font-size="10" class="muted">점선: 채점할 정답</text>`;
  svg.innerHTML = s;
})();

(function plasbars() {
  const a = D.plasmodium.auroc_which_families_lost;
  const ko = {"parasite (Plasmodium pair held out)": "기생 법칙", "parasite (no apicomplexan seen)": "기생 법칙 (아피콤플렉사 미학습)",
    "free-living": "자유생활 법칙", "reference: endosymbiosis (mitochondrion)": "미토콘드리아 공생 법칙", "reference: endosymbiosis (plastid)": "엽록체 공생 법칙",
    "reference: endosymbiosis (insect_endosymbiont)": "곤충 공생세균 법칙", "baseline: fewer copies lost first": "기준선: 복제 수"};
  const items = Object.entries(a).sort((p, q) => q[1] - p[1]);
  const W = 420, rowH = 26, left = 190, H = items.length * rowH + 34;
  const x = (v) => left + (v - 0.5) / 0.2 * (W - left - 40);
  let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px">`;
  items.forEach(([k, v], i) => {
    const y = 8 + i * rowH, base = k.startsWith("baseline");
    s += `<text x="${left - 8}" y="${y + 15}" text-anchor="end" font-size="12">${ko[k] || k}</text>`;
    s += `<rect x="${x(0.5)}" y="${y + 3}" width="${x(v) - x(0.5)}" height="16" rx="3" fill="${base ? css("--muted") : k.startsWith("reference") ? css("--keep") : css("--lose")}"/>`;
    s += `<text x="${x(v) + 5}" y="${y + 15}" font-size="11" font-family="var(--mono)">${v.toFixed(2)}</text>`;
  });
  s += `<text x="${x(0.5)}" y="${H - 6}" font-size="11" class="muted">0.5 = 무작위 · 모든 법칙이 기준선 근처</text></svg>`;
  $("plasbars").outerHTML = s;
})();

(function plasclass() {
  const fl = D.plasmodium.fraction_lost_by_class;
  const cols = [["actual Plasmodium", "실제 말라리아 원충"], ["parasite (no apicomplexan seen)", "기생 법칙 예측"], ["reference: endosymbiosis (mitochondrion)", "미토콘드리아 법칙 예측"]];
  const classes = Object.keys(fl["actual Plasmodium"]);
  const name = {redox_core: "전자전달 핵심", atp_synthase: "ATP 합성효소", translation: "번역 장치", transcription: "전사(RNA 중합효소)", protein_targeting: "단백질 수송"};
  let h = `<tr><th class="row">원형이 가진 유전자군 중 사라진 비율</th>${cols.map(([, n]) => `<th>${n}</th>`).join("")}</tr>`;
  for (const c of classes) {
    const actual = fl["actual Plasmodium"][c];
    h += `<tr><th class="row">${name[c]}</th>` + cols.map(([k]) => {
      const v = fl[k][c]; const off = Math.abs(v - actual) > 0.2;
      return `<td class="cell" style="background-color:${off ? `color-mix(in srgb, ${css("--lose")} 30%, var(--panel))` : "transparent"}">${Math.round(v * 100)}%</td>`;
    }).join("") + "</tr>";
  }
  h += `<tr><td colspan="4" class="note" style="padding-top:8px">색칠한 칸은 실제와 20%p 넘게 어긋난 예측입니다. 기생 법칙은 호흡 유전자를 버린 이질아메바·미포자충을 닮아 전자전달 유전자 소실을 과대 예측했고, 미토콘드리아 법칙은 소기관 전용 규칙(RNA 중합효소 버리기)을 핵 유전체에 적용해 틀렸습니다.</td></tr>`;
  $("plasclass").innerHTML = h;
})();


if (D.axes_done && D.axes_metrics) {
  $("axes-sec").hidden = false;
  const am = D.axes_metrics;
  (function aic() {
    const a = am.aic_relative, ko = {shared: "법칙 하나", parasite_only: "기생 / 자유생활", axes: "세 축으로 나눔"};
    const items = Object.entries(a), W = 380, left = 120, rowH = 34, H = items.length * rowH + 40;
    const mx = Math.max(...Object.values(a)) || 1, x = (v) => left + v / mx * (W - left - 60);
    let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px"><text x="0" y="14" font-size="12" class="muted">최선 모델 대비 ΔAIC (작을수록 좋음)</text>`;
    items.forEach(([k, v], i) => {
      const y = 26 + i * rowH;
      s += `<text x="${left - 8}" y="${y + 16}" text-anchor="end" font-size="12">${ko[k]}</text>`;
      s += `<rect x="${left}" y="${y + 4}" width="${Math.max(x(v) - left, 3)}" height="18" rx="3" fill="${k === "axes" ? css("--keep") : css("--muted")}"/>`;
      s += `<text x="${Math.max(x(v), left + 3) + 6}" y="${y + 17}" font-size="11">${v === 0 ? "최선" : "+" + v.toFixed(0)}</text>`;
    });
    $("aic").outerHTML = s + "</svg>";
  })();
  (function hl() {
    const e = am.loss_effects, rows = [["reduced_mitochondria", "미토콘드리아 퇴화"], ["intracellular", "세포 안"], ["parasite", "기생"]];
    const cols = [["redox_core", "전자전달 핵심"], ["atp_synthase", "ATP 합성효소"], ["translation", "번역 장치"]];
    let h = `<tr><th class="row">축이 더하는 소실 효과</th>${cols.map(([, n]) => `<th>${n}</th>`).join("")}</tr>`;
    for (const [r, n] of rows) {
      h += `<tr><th class="row">+ ${n}</th>` + cols.map(([c]) => {
        const w = e[r][c].weight, se = e[r][c].se, ns = Math.abs(w) < 1.96 * se;
        return `<td class="cell ${ns ? "ns" : ""}" style="background-color:${heatColor(w)};color:${Math.abs(w) > 1.4 ? "var(--panel)" : "var(--fg)"}">${f2(w)}</td>`;
      }).join("") + "</tr>";
    }
    $("axeshl").innerHTML = h;
  })();
  (function plas2() {
    const p = am.plasmodium_ancestor, act = p.actual_fraction_lost_by_class;
    const cls = [["redox_core", "전자전달 핵심"], ["atp_synthase", "ATP 합성효소"], ["translation", "번역 장치"], ["protein_targeting", "단백질 수송"]];
    const order = Object.entries(p.laws).sort((a, b) => b[1].auroc - a[1].auroc);
    const ko = (k) => k.replace("free-living", "자유생활").replace("parasite", "기생").replace(", intracellular", " · 세포 안")
      .replace(", reduced mito", " · 미토콘드리아 퇴화").replace(", aerobic", " · 호흡 유지").replace("reference: endosymbiosis ", "참고: 공생 법칙 ")
      .replace("(mitochondrion)", "(미토콘드리아)").replace("(plastid)", "(엽록체)").replace("(insect_endosymbiont)", "(곤충 공생세균)");
    let h = `<tr><th class="row">적용한 법칙</th><th>AUROC</th>${cls.map(([, n]) => `<th>${n}<br>소실 비율</th>`).join("")}</tr>`;
    h += `<tr><th class="row"><b>실제 말라리아 원충</b></th><td class="cell">—</td>${cls.map(([c]) => `<td class="cell"><b>${Math.round(act[c] * 100)}%</b></td>`).join("")}</tr>`;
    for (const [k, v] of order) {
      const mark = v.matches_plasmodium_biology;
      h += `<tr><th class="row" style="${mark ? "color:var(--lose);font-weight:700" : ""}">${ko(k)}${mark ? " ← 실제 생활 방식" : ""}</th><td class="cell">${v.auroc.toFixed(3)}</td>` +
        cls.map(([c]) => { const d = Math.abs(v.fraction_lost_by_class[c] - act[c]);
          return `<td class="cell" style="background-color:${d > 0.2 ? `color-mix(in srgb, ${css("--lose")} 30%, var(--panel))` : "transparent"}">${Math.round(v.fraction_lost_by_class[c] * 100)}%</td>`; }).join("") + "</tr>";
    }
    $("plas2").innerHTML = h;
    $("plas2note").textContent = `원형(유전자군 ${p.ancestor_families.toLocaleString()}개)에서 말라리아 원충은 ${p.lost.toLocaleString()}개를 잃었습니다. 실제 생활 방식에 맞는 법칙이 1위지만 차이는 작습니다. 대신 "미토콘드리아 퇴화"가 붙은 법칙은 전자전달 유전자 소실을 77–95%로 크게 과대 예측해, 에너지 축을 나눈 것이 어디서 효과가 있는지 보여줍니다. 색칠한 칸은 실제와 20%p 넘게 어긋난 예측입니다.`;
  })();
}

if (D.enrich && D.severity) {
  $("r2").hidden = false;
  $("r2n").textContent = `${D.n_species}종`;
  (function featbars() {
    const m = D.enrich.mean_heldout_auroc;
    const items = [["copies_only", "복제 수 기준선", css("--muted")], ["base", "법칙 (특성 8개)", css("--muted")],
                   ["enriched", `법칙 (특성 ${D.enrich.n_features.enriched}개)`, css("--lose")], ["memorisation", "암기 기준선", css("--fg")]];
    const W = 400, left = 130, rowH = 32, H = items.length * rowH + 46;
    const x = (v) => left + (v - 0.5) / 0.4 * (W - left - 50);
    let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px"><text x="0" y="14" font-size="12" class="muted">처음 보는 기생생물이 잃는 유전자군 맞히기 (AUROC)</text>`;
    items.forEach(([k, n, c], i) => {
      const y = 26 + i * rowH;
      s += `<text x="${left - 8}" y="${y + 16}" text-anchor="end" font-size="12" ${k === "enriched" ? 'font-weight="700"' : ""}>${n}</text>`;
      s += `<rect x="${x(0.5)}" y="${y + 4}" width="${x(m[k]) - x(0.5)}" height="18" rx="3" fill="${c}"/>`;
      s += `<text x="${x(m[k]) + 6}" y="${y + 17}" font-size="11" font-family="var(--mono)">${m[k].toFixed(3)}</text>`;
    });
    s += `<text x="${x(0.5)}" y="${H - 6}" font-size="11" class="muted">5-fold, 기생 쌍 ${Object.keys(D.order.severity).length}개 · 0.5 = 무작위</text>`;
    $("featbars").outerHTML = s + "</svg>";
  })();
  (function sevbars() {
    const t = D.severity.typical_share_lost;
    const items = [["free_living", "자유생활 대조"], ["extracellular_parasite", "세포 밖 기생"],
                   ["intracellular_parasite", "세포 안 기생"], ["intracellular_reduced_mito", "세포 안 + 미토콘드리아 퇴화"]];
    const W = 400, left = 170, rowH = 32, H = items.length * rowH + 46;
    const x = (v) => left + v * (W - left - 44);
    let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:${W}px"><text x="0" y="14" font-size="12" class="muted">조상 유전자군 중 잃는 비율 (severity_v1)</text>`;
    items.forEach(([k, n], i) => {
      const y = 26 + i * rowH;
      s += `<text x="${left - 8}" y="${y + 16}" text-anchor="end" font-size="12">${n}</text>`;
      s += `<rect x="${left}" y="${y + 4}" width="${x(t[k]) - left}" height="18" rx="3" fill="color-mix(in srgb, ${css("--lose")} ${Math.round(30 + t[k] * 70)}%, var(--panel))"/>`;
      s += `<text x="${x(t[k]) + 6}" y="${y + 17}" font-size="11" font-family="var(--mono)">${Math.round(t[k] * 100)}%</text>`;
    });
    s += `<text x="0" y="${H - 6}" font-size="11" class="muted">계통 하나를 빼고 맞히기: 오차 ${D.severity.loco_rmse_logit.mean_only.toFixed(2)} → ${D.severity.loco_rmse_logit.all_axes.toFixed(2)}</text>`;
    $("sevbars").outerHTML = s + "</svg>";
  })();
  const o = D.order.containment_over_random, md = D.modules, ex = D.expansion, conv = ex.convergent.map((c) => c.family);
  const cards = [
    ["severity_v1", "얼마나 잃나: 생활 방식의 덧셈", `잃는 비율은 기생(+${D.severity.coefficients.parasite.weight.toFixed(2)}), 미토콘드리아 퇴화(+${D.severity.coefficients.reduced_mitochondria.weight.toFixed(2)})가 더해지며 커집니다. 세포 안 효과(+${D.severity.coefficients.intracellular.weight.toFixed(2)})는 계통 단위로 다시 뽑으면 불확실합니다.`],
    ["loss_order_v1", "어떤 순서로 잃나: 계통을 넘어 같은 순서", `서로 다른 계통의 기생생물 ${D.order.n_cross_clade_comparisons.toLocaleString()}쌍 모두에서, 더 줄어든 쪽이 덜 줄어든 쪽의 소실을 무작위의 ${o.median.toFixed(2)}배로 함께 잃었습니다. 유전자군별 소실률 순위도 일치합니다(Spearman ${D.order.mild_vs_harsh_spearman.toFixed(2)}).`],
    ...(D.nested ? [["loss_order_v2", "그 순서는 유전자별 성향이다: 네 시스템 공통", `미토콘드리아·엽록체·곤충 공생세균·기생생물 모두에서 소실은 무작위보다 훨씬 순서가 있지만(예: 기생생물 ${D.nested.eukaryote_parasites.containment.toFixed(2)} vs ${D.nested.eukaryote_parasites.row_null_mean.toFixed(2)}), 유전자별 소실률을 고정한 귀무모형(${D.nested.eukaryote_parasites.fixed_null_mean.toFixed(2)})보다 엄격하지 않습니다. 공통 규칙: 유전자 소실 ≈ 유전자별 성향 × 계통별 축소 강도, 서로 거의 독립.`]] : []),
    ["coloss_modules_v1", "함께 잃나: 거의 독립, 예외는 편모", `소실의 절반을 보여 주고 나머지를 맞히게 하면, 모듈을 넣어도 ${md.mean_auroc_hidden.k0.toFixed(3)} → ${md.mean_auroc_hidden["k" + md.best_k].toFixed(3)}로 거의 그대로입니다. 뚜렷한 예외는 편모 축사(미포자충·타일레리아·말라리아 원충이 한꺼번에 잃음)와 B12 대사입니다.`],
    ["convergent_expansion_v1", "무엇을 늘리나: 아미노산 수송체", `기생생물은 유전자군을 대조군보다 덜 늘리지만(${(ex.expansion_rate.parasites * 100).toFixed(1)}% vs ${(ex.expansion_rate.controls * 100).toFixed(1)}%), ${conv.join(", ")}는 ${ex.clades.length}개 계통 중 5곳에서 독립적으로 늘어났습니다. 숙주에서 영양을 가져오는 쪽으로 수렴합니다.`],
    ["eukaryote_axes_v3", "특성 56개로 다시 본 축별 효과", "미토콘드리아 퇴화는 전자전달·미토콘드리아 유전자군 소실을 크게 높입니다. 기생생물은 대체로 편모를 지키지만, 세포 안에 살거나 미토콘드리아가 퇴화하면 편모도 버립니다."],
  ];
  if (D.transfer) {
    const t = D.transfer.mean_auroc;
    const w = D.enrich.mean_heldout_auroc;
    cards.push(["수렴", "처음 보는 계통에도 통한다", `계통 하나를 통째로 빼고 학습하면 암기는 ${w.memorisation.toFixed(3)} → ${t.memorisation.toFixed(3)}로 떨어지지만, 법칙은 ${w.enriched.toFixed(3)} → ${t.law.toFixed(3)}로 거의 그대로입니다. 독립적으로 기생이 생겨난 계통들이 같은 종류의 유전자군을 잃는다는 뜻입니다.`]);
  }
  $("r2laws").innerHTML = cards.map(([id, h, d]) => `<div class="law"><span class="id">${id}</span><b>${h}</b><div class="data">${d}</div></div>`).join("");
}

if (D.sequence && D.phylo) {
  $("r3").hidden = false;
  const q = D.sequence, ph = Object.entries(D.phylo), surv = ph.filter(([, r]) => r.survives).length;
  const fs = D.family_seq || {};
  const r2 = ["ivywrel", "cvp", "acidic_excess"].map((k) => q.pairs_r2[k]);
  const ol = q.oligo.filter((o) => o.n_side_change < 0).length;
  const cards = [
    ["sequence_v1", "온도: IVYWREL", `${q.temperature.n}종에서 최적 온도와 r ${q.temperature.pearson_ivywrel.toFixed(2)} (Zeldovich 2007 재현). IVYWREL 하나로 처음 보는 계통의 온도를 오차 ${q.temperature.rmse_ivywrel_loo_group.toFixed(1)}°C로 맞힙니다(평균만 쓰면 ${q.temperature.rmse_mean_only.toFixed(1)}°C).`],
    ["sequence_v1", "염분: 산성 단백질체", `최적 염분과 산성 과잉 Spearman ${q.salt.spearman_acidic_excess.toFixed(2)}, 등전점 ${q.salt.spearman_median_pi.toFixed(2)}.`],
    ["sequence_v1", "환경 변화 → 조성 변화", `${q.n_pairs}개 쌍에서 환경 변화가 온도·염분 지표(IVYWREL, 전하−극성, 산성 과잉)의 변화를 R² ${Math.min(...r2).toFixed(2)}–${Math.max(...r2).toFixed(2)}로 설명합니다(쌍 하나씩 빼고 맞히기). 같은 쌍에서 유전자 소실은 환경으로 설명되지 않았습니다.`],
    ["sequence_v1", "빈영양: 질소 절약 · 공생세균: AT 편향", `빈영양 ${q.oligo.length}쌍 중 ${ol}쌍에서 곁사슬 질소 감소. 공생세균은 유전체가 작을수록 FYMINK 증가(Spearman ${q.symb.spearman_size_fymink.toFixed(2)}), 등전점 상승(${q.symb.spearman_size_pi.toFixed(2)}).`],
    ...(fs.ivywrel ? [["family_sequence_v1", "유전자군 단위로 보면", `온도 적응은 유전자군 ${fs.ivywrel.families_tested.toLocaleString()}개 중 ${Math.round(fs.ivywrel.share_positive * 100)}%, 염분 적응은 ${Math.round(fs.acidic_excess.share_positive * 100)}%가 적응 방향으로 바뀝니다. 막단백질·수송체는 덜 바뀝니다.`]] : []),
    ["phylo_check_v1", `계통 보정: ${surv} / ${ph.length} 유지`, "세포 안 생활 효과만 탈락했습니다. 빈영양 질소 절약은 보정 전에는 보이지 않다가 보정 뒤에 유의해졌습니다."],
  ];
  $("r3laws").innerHTML = cards.map(([id, h, d]) => `<div class="law"><span class="id">${id}</span><b>${h}</b><div class="data">${d}</div></div>`).join("");
  const KO = {ivywrel_vs_temperature: "IVYWREL ~ 온도", cvp_vs_temperature: "전하−극성 ~ 온도", acidic_vs_salt: "산성 과잉 ~ 염분",
    nitrogen_vs_oligotrophy: "곁사슬 질소 ~ 빈영양", fymink_vs_anoxia: "FYMINK ~ 무산소", regulator_scaling: "조절 유전자 스케일링",
    symbiont_fymink_vs_size: "공생세균 FYMINK ~ 크기", severity_parasite: "잃는 비율 ~ 기생", severity_intracellular: "잃는 비율 ~ 세포 안",
    severity_reduced_mitochondria: "잃는 비율 ~ 미토 퇴화",
    pair_ivywrel_colder: "Δ IVYWREL ~ 추위", pair_cvp_colder: "Δ 전하−극성 ~ 추위",
    pair_acidic_excess_saltier: "Δ 산성 과잉 ~ 염분", pair_fymink_anaerobic: "Δ FYMINK ~ 무산소"};
  const label = (k) => KO[k] || k.replace(/^pair_/, "Δ ").replace(/_/g, " ");
  const lp = (p) => Math.min(-Math.log10(Math.max(p, 1e-12)), 12);
  const W = 360, left = 150, rowH = 24, H = ph.length * rowH + 40;
  const x = (v) => left + v / 12 * (W - left - 20);
  let s = `<svg viewBox="0 0 ${W} ${H}" width="100%" style="max-width:640px">`;
  s += `<line x1="${x(lp(0.05))}" x2="${x(lp(0.05))}" y1="0" y2="${H - 28}" stroke="${css("--muted")}" stroke-dasharray="3 3"/>`;
  ph.forEach(([k, r], i) => {
    const y = 12 + i * rowH, a = x(lp(r.ols[1])), b = x(lp(r.rank_gls[1]));
    const c = r.survives ? css("--keep") : css("--lose");
    s += `<text x="${left - 8}" y="${y + 4}" text-anchor="end" font-size="10.5" ${r.survives ? "" : 'font-weight="700"'}>${label(k)}</text>`;
    s += `<line x1="${a}" x2="${b}" y1="${y}" y2="${y}" stroke="${css("--line")}" stroke-width="2"/>`;
    s += `<circle cx="${a}" cy="${y}" r="4.5" fill="${css("--muted")}" opacity="0.6"><title>보정 전 p ${r.ols[1].toExponential(1)}</title></circle>`;
    s += `<circle cx="${b}" cy="${y}" r="5.5" fill="${c}"><title>보정 후 p ${r.rank_gls[1].toExponential(1)} · 공유 역사 ${Math.round(r.shared_history * 100)}%</title></circle>`;
  });
  [0, 3, 6, 9, 12].forEach((t) => { s += `<text x="${x(t)}" y="${H - 8}" text-anchor="middle" font-size="11" font-family="var(--mono)" class="muted">${t === 12 ? "≥12" : t}</text>`; });
  $("phylo").outerHTML = s + "</svg>";
}

$("next").innerHTML = [
  ["완료", "특성 풍부화", D.enrich ? `특성을 8개에서 ${D.enrich.n_features.enriched}개로 늘려 처음 보는 기생생물 예측이 ${D.enrich.mean_heldout_auroc.base.toFixed(3)} → ${D.enrich.mean_heldout_auroc.enriched.toFixed(3)}로 올랐습니다. 아직 암기 기준선(${D.enrich.mean_heldout_auroc.memorisation.toFixed(3)})보다 낮습니다.` : "진행 중"],
  ["완료", "계통 보정", D.phylo ? `분류 단계별 분산 GLS로 ${Object.values(D.phylo).filter((r) => r.survives).length} / ${Object.keys(D.phylo).length} 법칙 유지.` : "진행 중"],
  ...(D.gc ? [["완료", "GC 함량 교란 검증", `GC를 공변량으로 넣자 온도 IVYWREL 효과는 ${Math.round(D.gc.species.ivywrel_vs_temperature.retained_share_of_effect * 100)}%, 염분 산성 과잉은 ${Math.round(D.gc.species.acidic_vs_salt.retained_share_of_effect * 100)}% 남았습니다. 빈영양 질소 절약(${Math.round(D.gc.species.nitrogen_vs_oligotrophy.retained_share_of_effect * 100)}%)과 무산소 FYMINK, 공생세균 AT 편향은 GC로 설명됩니다.`]] : [["다음", "GC 함량 교란 검증", "GC를 공변량으로 넣어 서열 법칙이 적응인지 돌연변이 편향인지 가립니다."]]),
  ["다음", "서열 기반 계통수", "분류 체계 대신 리보솜 단백질 서열로 계통수를 만들어 보정을 다시 합니다."],
  ["한계", "지금 알고 있는 약점", "조상 대리로 현생 근연종을 쓰고, 계통 보정은 분류 체계를 근사 계통수로 씁니다. 유전자는 있다·없다 수준만 봅니다."],
].map(([t, h, d]) => `<div class="law ${t === "진행 중" ? "pending" : ""}"><span class="tag" style="justify-self:start;color:${t === "진행 중" ? "var(--pending)" : "var(--accent)"}">${t}</span><b>${h}</b><div class="data">${d}</div></div>`).join("");
</script>
"""

if __name__ == "__main__":
    main()
