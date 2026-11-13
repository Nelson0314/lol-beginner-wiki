"""從 Riot 官方 Data Dragon 下載簡報用圖片，並輸出繁中（zh_TW）官方譯名供 glossary 核對。

用法：python tools/fetch_ddragon.py
輸出：assets/img/**、assets/img/manifest.json（每張圖的來源網址與 zh_TW 名稱）
"""
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets" / "img"
CDN = "https://ddragon.leagueoflegends.com"

CHAMPS = ["Garen", "Malphite", "Warwick", "Amumu", "Annie", "Lux", "Ashe", "MissFortune",
          "Caitlyn", "Leona", "Soraka", "Nautilus", "Jinx", "Ahri"]
SPELLS = ["SummonerFlash", "SummonerTeleport", "SummonerSmite", "SummonerDot", "SummonerHaste", "SummonerHeal"]
ITEMS = {"1055": "doran-blade", "1054": "doran-shield", "1001": "boots", "3006": "berserker-greaves",
         "2003": "health-potion", "2055": "control-ward", "3340": "stealth-ward", "3364": "oracle-lens",
         "3363": "farsight", "1036": "long-sword", "1053": "vampiric-scepter", "3153": "botrk"}


def get(url):
    req = urllib.request.Request(url, headers={"User-Agent": "lol-beginner-wiki/1.0"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def save(url, rel, manifest, name):
    p = IMG / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists():
        p.write_bytes(get(url))
    manifest[rel] = {"url": url, "zh_TW": name}


def main():
    ver = json.loads(get(f"{CDN}/api/versions.json"))[0]
    data = lambda f: json.loads(get(f"{CDN}/cdn/{ver}/data/zh_TW/{f}"))["data"] if not f.startswith("runes") else json.loads(get(f"{CDN}/cdn/{ver}/data/zh_TW/{f}"))
    manifest = {"_version": ver}
    champs = data("champion.json")
    for c in CHAMPS:
        n = f"{champs[c]['name']}（{champs[c]['title']}）"
        save(f"{CDN}/cdn/{ver}/img/champion/{c}.png", f"champion/{c}.png", manifest, n)
        save(f"{CDN}/cdn/img/champion/loading/{c}_0.jpg", f"loading/{c}.jpg", manifest, n)
    for c in ["Garen", "Jinx", "Ahri", "Leona"]:
        save(f"{CDN}/cdn/img/champion/splash/{c}_0.jpg", f"splash/{c}.jpg", manifest, champs[c]["name"])
    spells = data("summoner.json")
    for s in SPELLS:
        save(f"{CDN}/cdn/{ver}/img/spell/{s}.png", f"spell/{s}.png", manifest, spells[s]["name"])
    items = data("item.json")
    for i, slug in ITEMS.items():
        if i in items:
            save(f"{CDN}/cdn/{ver}/img/item/{i}.png", f"item/{slug}.png", manifest, items[i]["name"])
        else:
            print("item missing", i, slug)
    for path in data("runesReforged.json"):
        save(f"{CDN}/cdn/img/{path['icon']}", f"rune/{path['key']}.png", manifest, path["name"])
    save(f"{CDN}/cdn/{ver}/img/map/map11.png", "map/summoners-rift.png", manifest, "召喚峽谷")
    (IMG / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1), encoding="utf-8")
    for k, v in manifest.items():
        if k != "_version" and not k.startswith(("loading", "splash")):
            print(k, v["zh_TW"])
    print("version", ver)


if __name__ == "__main__":
    sys.exit(main())
