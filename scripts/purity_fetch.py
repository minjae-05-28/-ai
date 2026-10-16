"""TCGA PanCanAtlas ABSOLUTE tumour purity for pre-registration 19, fetched on a GitHub runner.

  data/tcga_purity/absolute.tsv   sample barcode -> purity (and the source URL in source.txt)
"""

import time
import urllib.request
from pathlib import Path

OUT = Path("data/tcga_purity")
URLS = ["https://api.gdc.cancer.gov/data/4f277128-f793-4354-a13d-30cc7fe9f6b5",
        "https://pancanatlas.xenahubs.net/download/TCGA_mastercalls.abs_tables_JSedit.fixed.txt",
        "https://pancanatlas.xenahubs.net/download/TCGA_mastercalls.abs_tables_JSedit.fixed.txt.gz"]


def get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return r.read()
        except Exception as e:
            print(f"attempt {i + 1} {url}: {e}", flush=True)
            time.sleep(10 * (i + 1))
    return None


def main():
    import gzip
    OUT.mkdir(parents=True, exist_ok=True)
    for url in URLS:
        raw = get(url)
        if raw is None:
            continue
        if raw[:2] == b"\x1f\x8b":
            raw = gzip.decompress(raw)
        text = raw.decode(errors="replace")
        head = text.splitlines()[0].split("\t")
        if "purity" not in head:
            print(f"{url}: no purity column ({head[:6]})", flush=True)
            continue
        si, pi = head.index("sample"), head.index("purity")
        rows = ["sample\tpurity"]
        for line in text.splitlines()[1:]:
            x = line.split("\t")
            if len(x) > max(si, pi) and x[pi] not in ("", "NA"):
                rows.append(f"{x[si]}\t{x[pi]}")
        (OUT / "absolute.tsv").write_text("\n".join(rows) + "\n")
        (OUT / "source.txt").write_text(url + "\n")
        print(f"{len(rows) - 1} samples with purity from {url}", flush=True)
        return
    (OUT / "source.txt").write_text("not available\n")
    print("purity not available", flush=True)


if __name__ == "__main__":
    main()
