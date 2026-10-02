"""Data card: every genome the project uses, with its source accession and role.

    python scripts/build_data_card.py        # writes docs/DATA.md

Regenerate after any data collection run.
"""

import json
from pathlib import Path

from organelle_evo.eukaryotes import catalog as euk
from organelle_evo.prokaryotes import catalog as pro


def read(dirname, skip=("pfam_meta.json", "family_annotations.json")):
    return {json.loads(f.read_text())["species"]: json.loads(f.read_text())
            for f in sorted(Path(dirname).glob("*.json")) if f.name not in skip}


def mark(ok):
    return "✓" if ok else ""


def main():
    comp_e, comp_p = read("data/composition/eukaryotes"), read("data/composition/prokaryotes")
    ctx_e, ctx_p = read("data/family_context/eukaryotes"), read("data/family_context/prokaryotes")
    gc = json.loads(Path("results/gc/gc.json").read_text()) if Path("results/gc/gc.json").exists() else {}
    E, P = read("data/eukaryotes"), read("data/prokaryotes")
    euk_roles = {}
    for a, d in euk.resolve_pairs(E):
        euk_roles.setdefault(a, set()).add("조상 대리")
        euk_roles.setdefault(d, set()).add("후손")
    pro_roles = {}
    for a, d in pro.resolve_pairs(P):
        pro_roles.setdefault(a, set()).add("조상 대리")
        pro_roles.setdefault(d, set()).add("후손")

    L = ["# 데이터 카드", "",
         "프로젝트가 쓰는 모든 유전체와 출처입니다. `scripts/build_data_card.py`로 생성합니다. "
         "모든 데이터는 NCBI(Datasets, GenBank)와 EBI(Pfam, InterPro)에서 GitHub Actions로 받아 저장소에 커밋했습니다.", "",
         "| 데이터 | 위치 | 출처 |", "|---|---|---|",
         "| 소기관·공생세균 유전체 (GenBank) | `data/raw/` | NCBI nuccore |",
         "| 유전자군 계수 (Pfam, HMMER 수집 임계값) | `data/eukaryotes/`, `data/prokaryotes/` | NCBI Datasets 단백질 + Pfam-A |",
         "| 유전자군 주석 (GO slim, 클랜) | `data/eukaryotes/family_annotations.json` | InterPro / pfam2go |",
         "| 단백질 조성 | `data/composition/` | 위 단백질체 |",
         "| 유전자군별 도메인 조성 | `data/family_composition/` | 위 단백질체 + Pfam |",
         "| 유전자군 맥락 (발현·오페론·도메인) | `data/family_context/` | 단백질·CDS·GFF |",
         "| 리보솜 단백질 마커 | `data/markers/` | 위 단백질체 + Pfam |",
         "| 분류 체계 | `results/taxonomy/taxonomy.json` | NCBI Taxonomy |",
         "| 유전체 GC | `results/gc/gc.json` | NCBI 어셈블리 통계, GenBank 서열 |", "",
         "참고: NCBI 어셈블리 통계는 약 절반의 유전체에서 GC를 정수 %로 반올림해 줍니다(오차 ±0.5%p, 종 간 범위 25–70%에 비해 작음).", ""]
    for title, prof, roles, comp, ctx, gcs, cat in (
            ("진핵생물", E, euk_roles, comp_e, ctx_e, gc.get("eukaryotes", {}), euk),
            ("세균·고세균", P, pro_roles, comp_p, ctx_p, gc.get("prokaryotes", {}), pro)):
        L += [f"## {title} ({len(prof)}종)", "", "| 종 | 어셈블리 | 유전자 | 역할 | 조성 | 맥락 | GC |", "|---|---|---|---|---|---|---|"]
        for s in sorted(prof):
            g = gcs.get(s, {}).get("gc")
            extra = " (기후 대상)" if s in getattr(cat, "CLIMATE_TARGETS", {}) else ""
            L.append(f"| *{s}* | {prof[s]['accession']} | {prof[s]['n_genes']:,} | {', '.join(sorted(roles.get(s, ()))) or '—'}{extra} "
                     f"| {mark(s in comp)} | {mark(s in ctx)} | {f'{g:.1%}' if g else ''} |")
        L.append("")
    L += ["## 소기관·공생세균 (GenBank 레코드)", "", "| 시스템 | 생물 | 레코드 |", "|---|---|---|"]
    for sub in ("mitochondrion", "plastid", "insect_endosymbiont"):
        for s, d in read(f"data/composition/endosymbiosis/{sub}").items():
            L.append(f"| {sub} | *{s}* | {d['accession']} |")
    Path("docs/DATA.md").write_text("\n".join(L) + "\n")
    print(f"docs/DATA.md: {len(E)} eukaryotes, {len(P)} prokaryotes")


if __name__ == "__main__":
    main()
