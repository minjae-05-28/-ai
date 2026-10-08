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
    ap.add_argument("--list-only", action="store_true", help="record the article's supplementary links, download nothing")
    ap.add_argument("--figshare", default="", help="figshare article id")
    ap.add_argument("--files", default="", help="comma-separated figshare file names to download; "
                                                "empty = write the file list only (names and sizes)")
    args = ap.parse_args()
    out = Path("results/external") / args.name
    out.mkdir(parents=True, exist_ok=True)
    index = []
    if args.figshare:
        meta = json.loads(get(f"https://api.figshare.com/v2/articles/{args.figshare}") or b"{}")
        files = [{"name": f["name"], "bytes": f["size"], "url": f["download_url"]} for f in meta.get("files", [])]
        (out / "figshare_files.json").write_text(json.dumps({"title": meta.get("title"), "doi": meta.get("doi"),
                                                             "files": files}, indent=1))
        print(f"figshare {args.figshare}: {len(files)} files")
        want = {w for w in args.files.split(",") if w}
        for f in files:
            if f["name"] in want:
                data = get(f["url"])
                if data:
                    (out / f["name"]).write_bytes(data)
                    index.append({"file": f["name"], "source": f["url"], "bytes": len(data)})
        if not want:
            return
    if args.pmcid and not args.list_only:
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
    if (not index or args.list_only) and args.article:
        page = get(args.article)
        links = sorted(set(re.findall(rb'https://static-content\.springer\.com/esm/[^"\'\s<>]+', page or b"")))
        print(f"article page: {len(links)} supplementary links")
        if args.list_only:
            (out / "article_links.json").write_text(json.dumps([x.decode() for x in links], indent=1))
            return
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
