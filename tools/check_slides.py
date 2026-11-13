"""⑦ 簡報檢查的自動部分。

P1 每張投影片有 data-wiki 且檔案存在；投影片上出現的術語必須也出現在綁定的 Wiki 頁（可追溯性的近似檢查）。
P2 每個術語在簡報中第一次出現的那張投影片，必須以 <dfn> 解釋它。
P3 每張投影片條列不超過 6 項、表格不超過 7 列。
P5 不得出現範圍外的關鍵字。
語意層面（說法是否真的被 Wiki 支持、新手是否看得懂）由人工逐張檢查，結果寫入 wiki/log.md。
用法：python tools/check_slides.py
"""
import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"
OUT_OF_SCOPE = ["克制", "counter", "ARAM", "隨機單中", "大混戰"]


def glossary_terms():
    terms = []
    for line in (WIKI / "glossary.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| ([^|]+?) \|", line)
        if m and m.group(1) not in ("術語", "------", "建議"):
            terms.append(m.group(1).strip())
    return sorted(terms, key=len, reverse=True)


def find_terms(text, terms):
    """最長優先比對，已比對的字元遮蔽，避免「路線任務」被算成「路線」。"""
    found = set()
    for t in terms:
        if t in text:
            found.add(t)
            text = text.replace(t, "\0" * len(t))
    return found


def plain(s):
    s = re.sub(r"<span class=\"en\">.*?</span>", "", s, flags=re.S)
    # 遊戲名稱「英雄聯盟」不視為術語「英雄」
    return html.unescape(re.sub(r"<[^>]+>", " ", s)).replace("英雄聯盟", "")


def main():
    terms = glossary_terms()
    src = (ROOT / "slides" / "index.html").read_text(encoding="utf-8")
    slides = re.findall(r'<section class="slide"( data-wiki="([^"]*)")?>(.*?)</section>', src, re.S)
    problems, seen = [], set()
    for n, (_, wiki, body) in enumerate(slides, 1):
        if not wiki or not (WIKI / wiki).exists():
            problems.append(f"P1 #{n}: data-wiki 缺少或檔案不存在（{wiki}）")
            continue
        text = plain(body)
        here = find_terms(text, terms)
        dfns = {plain(d).strip() for d in re.findall(r"<dfn>(.*?)</dfn>", body, re.S)}
        wiki_text = (WIKI / wiki).read_text(encoding="utf-8")
        if wiki != "index.md":
            for t in sorted(here):
                if t not in wiki_text:
                    problems.append(f"P1 #{n}: 術語「{t}」不在綁定頁 {wiki}")
        for t in sorted(here - seen):
            if t not in dfns:
                problems.append(f"P2 #{n}: 「{t}」第一次出現但沒有 <dfn> 解釋")
        for d in dfns:
            if d in seen:
                problems.append(f"P2 #{n}: 「{d}」已在前面解釋過，重複 <dfn>")
        seen |= here
        lis = len(re.findall(r"<li>", body))
        trs = len(re.findall(r"<tr>", body))
        if lis > 6:
            problems.append(f"P3 #{n}: 條列 {lis} 項（上限 6）")
        if trs > 7:
            problems.append(f"P3 #{n}: 表格 {trs} 列（上限 7）")
        for k in OUT_OF_SCOPE:
            if k in text:
                problems.append(f"P5 #{n}: 出現範圍外關鍵字「{k}」")
    for x in problems:
        print(x)
    print(f"共 {len(slides)} 張，{len(problems)} 個問題")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
