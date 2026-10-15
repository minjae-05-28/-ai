"""Inputs for the human gene age table (pre-registration 16), fetched on a GitHub runner:

  data/human/uniprot_human.tsv.gz   reviewed human proteins: accession, gene, Pfam, Entrez, Ensembl
  data/human/litman_stein/           Litman & Stein 2019 consensus gene ages (human files of marcottelab/Gene-Ages)

Gene-family level only: no sequences are downloaded.
"""

import gzip
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

OUT = Path("data/human")
UNIPROT = ("https://rest.uniprot.org/uniprotkb/stream?query=%28proteome%3AUP000005640%29%20AND%20%28reviewed%3Atrue%29"
           "&fields=accession%2Cgene_primary%2Cxref_pfam%2Cxref_geneid%2Cxref_ensembl&format=tsv")


def get(url, tries=5):
    for i in range(tries):
        try:
            with urllib.request.urlopen(url, timeout=300) as r:
                return r.read()
        except Exception as e:
            print(f"attempt {i + 1}: {e}", flush=True)
            time.sleep(10 * (i + 1))
    raise RuntimeError(f"could not fetch {url}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    raw = get(UNIPROT)
    lines = raw.decode().splitlines()
    print(f"UniProt: {len(lines) - 1} reviewed human proteins", flush=True)
    with gzip.open(OUT / "uniprot_human.tsv.gz", "wt") as f:
        f.write("\n".join(lines) + "\n")
    tmp = Path("/tmp/gene-ages")
    shutil.rmtree(tmp, ignore_errors=True)
    r = subprocess.run(["git", "clone", "--depth", "1", "https://github.com/marcottelab/Gene-Ages", str(tmp)])
    if r.returncode != 0:
        print("Litman & Stein repository not reachable", file=sys.stderr)
        return
    dest = OUT / "litman_stein"
    dest.mkdir(exist_ok=True)
    listing = sorted(str(p.relative_to(tmp)) for p in tmp.rglob("*") if p.is_file() and ".git" not in p.parts)
    (dest / "LISTING.txt").write_text("\n".join(listing) + "\n")
    for rel in listing:
        p = tmp / rel
        if "HUMAN" in rel.upper() or p.name.lower().startswith("readme"):
            if p.stat().st_size < 50e6:
                target = dest / rel.replace("/", "__")
                shutil.copy(p, target)
                print(f"kept {rel} ({p.stat().st_size / 1e6:.1f} MB)", flush=True)


if __name__ == "__main__":
    main()
