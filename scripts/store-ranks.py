"""Where your app shows up in App Store search, for the searches your listing targets.

    python scripts/store-ranks.py store-ranks.json                       # measure now, print a dated markdown table
    python scripts/store-ranks.py store-ranks.json --append              # ...and append it to the config's "doc"
    python scripts/store-ranks.py store-ranks.json --save-json run.json  # ...and keep the raw rows
    python scripts/store-ranks.py store-ranks.json --from-json run.json  # re-render saved rows, no network

The config (copy scripts/store-ranks.example.json) names your App Store id, the doc to append to, and the searches to
check per storefront. Keep the searches identical between runs: the point is comparing like with like.

READ IT AS A PROXY. It uses Apple's iTunes Search API, which Apple publishes for programmatic use (about 20 calls a
minute), returning up to 200 iPhone apps, unpersonalised, which is close
to search on a phone but not the same. Store search moves for weeks after a metadata change, so take a baseline the
day a listing changes, rerun at about one and four weeks, and judge only from the second rerun.

Google Play is deliberately not measured: Play has no search API, and its robots.txt disallows automated reads of
its search pages. Read the
Play Console's store listing acquisition report by search term instead.

Needs no key and writes nothing but the doc and the optional JSON. Paces itself, because the Search API is rate
limited (expect about four seconds a search, with back-off on errors).
"""
import argparse
import datetime
import json
import pathlib
import sys
import time
import urllib.parse
import urllib.request

UA = "store-ranks/1.0 (+https://github.com/melroyds/golden-path)"


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def apple(apple_id, term, country):
    q = urllib.parse.urlencode({"term": term, "country": country, "entity": "software", "limit": 200})
    err = ""
    for attempt in range(3):
        try:
            ids = [r.get("trackId") for r in json.loads(get("https://itunes.apple.com/search?" + q))["results"]]
            return {"rank": ids.index(apple_id) + 1 if apple_id in ids else None, "of": len(ids)}
        except Exception as e:  # a rate limit or a blip: back off and retry
            err = str(e)
            time.sleep(20 * (attempt + 1))
    return {"error": err}


def measure(cfg):
    apple_id = int(cfg["apple_id"])
    rows = []
    for s in cfg["storefronts"]:
        for term in s["terms"]:
            rows.append({"country": s["country"], "term": term, "apple": apple(apple_id, term, s["country"])})
            print(".", end="", file=sys.stderr, flush=True)
            time.sleep(3.5)
    print(file=sys.stderr)
    return rows


def cell(r):
    if r is None:
        return "n/a"
    if "error" in r:
        return "error"
    return f"**{r['rank']}**" if r["rank"] else f"not in {r['of']}"


def render(rows, date):
    out = [f"### {date}", "", "| Store | Search | App Store |", "|---|---|---|"]
    out += [f"| {r['country'].upper()} | {r['term']} | {cell(r.get('apple'))} |" for r in rows]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("config", help="your copy of scripts/store-ranks.example.json")
    ap.add_argument("--append", action="store_true", help="also append the table to the config's doc")
    ap.add_argument("--save-json", metavar="FILE", help="also write the measured rows to FILE, for --from-json")
    ap.add_argument("--from-json", metavar="FILE", help="render rows saved by --save-json instead of measuring")
    ap.add_argument("--date", default=datetime.date.today().isoformat(), help="the date heading (default today)")
    a = ap.parse_args()
    cfg_path = pathlib.Path(a.config)
    cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    rows = json.loads(pathlib.Path(a.from_json).read_text(encoding="utf-8")) if a.from_json else measure(cfg)
    if a.save_json:
        pathlib.Path(a.save_json).write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    section = render(rows, a.date)
    sys.stdout.reconfigure(encoding="utf-8")
    print(section)
    if a.append:
        doc = (cfg_path.parent / cfg.get("doc", "store-search-ranks.md")).resolve()
        doc.parent.mkdir(parents=True, exist_ok=True)
        with doc.open("a", encoding="utf-8", newline="\n") as f:
            f.write("\n" + section)
