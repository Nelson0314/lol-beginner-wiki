"""④ 交叉比對的自動部分：C3 出處、C4 術語、第三方標記、連結。

用法：python tools/check_wiki.py
語意層面的檢查（C1 衝突、C2 譯名、敘述是否真的被來源支持）由人工完成，結果寫入 wiki/log.md。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WIKI = ROOT / "wiki"


def glossary_terms():
    terms = set()
    for line in (WIKI / "glossary.md").read_text(encoding="utf-8").splitlines():
        m = re.match(r"^\| ([^|]+?) \|", line)
        if m and m.group(1) not in ("術語", "------"):
            terms.add(m.group(1).strip())
    return terms


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else ""


def main():
    terms = glossary_terms()
    problems = []
    pages = [p for p in WIKI.rglob("*.md")
             if "sources" not in p.parts and p.name not in ("log.md", "index.md", "glossary.md")]
    for p in sorted(pages):
        rel = p.relative_to(WIKI).as_posix()
        text = p.read_text(encoding="utf-8")
        fm = frontmatter(text)
        m = re.search(r"sources:\s*\[(.*?)\]", fm)
        fm_src = {s.strip() for s in m.group(1).split(",")} if m else set()
        if not fm_src:
            problems.append(f"C3 {rel}: frontmatter 沒有 sources")
        if "## 來源" not in text:
            problems.append(f"C3 {rel}: 缺少「## 來源」段")
        body = text[len(fm) + 8:]
        cited = set(re.findall(r"S\d+", re.sub(r"## 來源.*", "", body, flags=re.S)))
        for s in sorted(cited - fm_src):
            problems.append(f"C3 {rel}: 內文引用 {s} 但 frontmatter 未列")
        listed = set(re.findall(r"\[(S\d+)\]", text.split("## 來源")[-1])) if "## 來源" in text else set()
        for s in sorted(fm_src - listed):
            problems.append(f"C3 {rel}: frontmatter 列 {s} 但「## 來源」未連結")
        for term in re.findall(r"\*\*(.+?)\*\*", body):
            t = re.sub(r"（.*?）", "", term).strip()
            if t not in terms:
                problems.append(f"C4 {rel}: 粗體術語「{t}」不在 glossary")
        for line in body.splitlines():
            if "S9" in line and "建議" not in line and "S9" in fm_src and not line.startswith(("- [S9]", "|")):
                problems.append(f"規則3 {rel}: 引用 S9 的行未標「建議」：{line.strip()[:40]}")
        for link in re.findall(r"\]\(([^)#]+\.md)\)", text):
            if not (p.parent / link).resolve().exists():
                problems.append(f"連結 {rel}: {link} 不存在")
    for x in problems:
        print(x)
    print(f"共 {len(pages)} 頁，{len(problems)} 個問題")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
