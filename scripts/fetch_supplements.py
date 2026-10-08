"""Download a paper's supplementary files (run on Actions: journals are not reachable from the sandbox).

    python scripts/fetch_supplements.py --name zmasek2011 --pmcid PMC3091302 \
        --article https://genomebiology.biomedcentral.com/articles/10.1186/gb-2011-12-1-r4
        -> results/external/<name>/  (every file, plus index.json with source URLs and sizes)

Tries Europe PMC's supplementary-files endpoint (one zip of all files) first, then the links to
static-content.springer.com/esm on the article page. Nothing here is interpreted; the files are
kept as published so the comparison script can say exactly what it read.
"""

import argparse
import io
import json
import re
import time
import urllib.request
import zipfile
from pathlib import Path


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 organelle-evo"})
            with urllib.request.urlopen(req, timeout=120) as r:
                return r.read()
        except Exception as e:
            print(f"  retry {i + 1}/{tries} {url[:100]}: {e}", flush=True)
            time.sleep(5 * (i + 1))
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--name", required=True)
    ap.add_argument("--pmcid", default="")
    ap.add_argument("--article", default="")
    args = ap.parse_args()
    out = Path("results/external") / args.name
    out.mkdir(parents=True, exist_ok=True)
    index = []
    if args.pmcid:
        url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/{args.pmcid}/supplementaryFiles"
        data = get(url)
        if data and data[:2] == b"PK":
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                for n in z.namelist():
                    if n.endswith("/"):
                        continue
                    (out / Path(n).name).write_bytes(z.read(n))
                    index.append({"file": Path(n).name, "source": url, "bytes": z.getinfo(n).file_size})
            print(f"Europe PMC: {len(index)} files")
        else:
            print(f"Europe PMC returned nothing usable ({len(data or b'')} bytes)")
    if not index and args.article:
        page = get(args.article)
        links = sorted(set(re.findall(rb'https://static-content\.springer\.com/esm/[^"\'\s<>]+', page or b"")))
        print(f"article page: {len(links)} supplementary links")
        for link in links:
            u = link.decode()
            data = get(u)
            if data:
                name = u.rsplit("/", 1)[-1].split("?")[0]
                (out / name).write_bytes(data)
                index.append({"file": name, "source": u, "bytes": len(data)})
    (out / "index.json").write_text(json.dumps(index, indent=1))
    print(json.dumps(index, indent=1))
    if not index:
        raise SystemExit("no supplementary files downloaded")


if __name__ == "__main__":
    main()
