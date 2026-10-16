"""Proliferation gene lists for pre-registration 18, fetched on a GitHub runner.

  data/human/proliferation_go.tsv    reviewed human proteins with GO cell cycle (GO:0007049), DNA replication
                                     (GO:0006260) or chromosome segregation (GO:0007059), descendants included
  data/human/hallmark_proliferation.json   MSigDB Hallmark E2F_TARGETS, G2M_CHECKPOINT, MITOTIC_SPINDLE symbols
"""

import json
import time
import urllib.request
from pathlib import Path

OUT = Path("data/human")
UNIPROT = ("https://rest.uniprot.org/uniprotkb/stream?query=%28proteome%3AUP000005640%29%20AND%20%28reviewed%3Atrue%29"
           "%20AND%20%28go%3A0007049%20OR%20go%3A0006260%20OR%20go%3A0007059%29&fields=accession%2Cgene_primary&format=tsv")
HALLMARK = ["https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2023.2.Hs/h.all.v2023.2.Hs.symbols.gmt",
            "https://data.broadinstitute.org/gsea-msigdb/msigdb/release/2023.1.Hs/h.all.v2023.1.Hs.symbols.gmt"]
SETS = ["HALLMARK_E2F_TARGETS", "HALLMARK_G2M_CHECKPOINT", "HALLMARK_MITOTIC_SPINDLE"]


def get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return r.read()
        except Exception as e:
            print(f"attempt {i + 1} {url}: {e}", flush=True)
            time.sleep(10 * (i + 1))
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = get(UNIPROT)
    (OUT / "proliferation_go.tsv").write_bytes(raw)
    print(f"GO proliferation proteins: {len(raw.decode().splitlines()) - 1}", flush=True)
    out = {"source": None, "sets": {}}
    for url in HALLMARK:
        g = get(url)
        if g is None:
            continue
        for line in g.decode().splitlines():
            x = line.split("\t")
            if x[0] in SETS:
                out["sets"][x[0]] = x[2:]
        out["source"] = url
        break
    (OUT / "hallmark_proliferation.json").write_text(json.dumps(out, indent=1))
    print({k: len(v) for k, v in out["sets"].items()}, out["source"], flush=True)


if __name__ == "__main__":
    main()
