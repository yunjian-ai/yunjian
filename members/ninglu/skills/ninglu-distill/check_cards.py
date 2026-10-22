"""凝露的卡片检查：查一套知识卡是不是真实、可信、连上了关系（照 `卡片格式.md`）。只用 Python 自带的库。
用法：python3 check_cards.py <卡片文件夹或单个 .md 文件> [--source <原文文件或文件夹>]
一个文件里可以有好几张卡，每张以「# 标题」开头。查出的问题一行一条，以 ❌ [类别] 开头；没有问题打印 ✅。
给了 --source 才查「原话在不在原文里」。它只查这些能数出来的，提炼得准不准、关系连得对不对，还要回原文看。"""
import re
import sys
from pathlib import Path

TYPES = {"定义", "规则", "方法", "案例", "数字", "观点", "模板", "故事"}
LEVELS = {"原文", "归纳", "推测"}
RELS = {"属于", "前提", "依据", "举例", "细化", "顺序", "反驳"}
META = ("类型", "可信度", "出处", "原话", "关系")
SKIP = {"目录.md", "进度.md", "取用说明.md"}
# 出处要有能翻回去的位置：数字，或「第…章/页/节/讲/问…」
PLACE = re.compile(r"[0-9０-９]|第[一二三四五六七八九十百零〇两]+[章节页条段集讲回问]")


def split_cards(text):
    """按「# 标题」切成一张张卡；代码块里的井号不算。"""
    cards, cur, fence = [], None, False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and re.match(r"#\s+\S", line) and not line.startswith("##"):
            cur = {"title": line[1:].strip(), "lines": []}
            cards.append(cur)
        elif cur is not None:
            cur["lines"].append(line)
    return cards


def parse(card):
    meta, body, theme, in_body = {}, [], "", False
    for line in card["lines"]:
        m = re.match(r"\s*[-*]\s*(类型|可信度|出处|原话|关系)\s*[：:]\s*(.*)$", line)
        if m and not in_body:
            meta[m.group(1)] = m.group(2).strip()
        elif line.startswith("> ") and not in_body and not theme:
            theme = line[2:].strip()
        elif line.startswith("## "):
            in_body = in_body or line[3:].strip() == "正文"
        elif in_body:
            body.append(line)
    return meta, "\n".join(body).strip(), theme


def squash(s):
    """比对原话时忽略空白和常见标点的差别（全角半角、换行）。"""
    return re.sub(r"[\s，。,.；;：:！!？?、「」『』“”\"'（）()…—\-]", "", s)


def relations(text):
    """「属于 → 进货看三样；举例 ← 某卡」→ [(关系, 卡名)]；写「独立」返回 None。"""
    if text.strip() in ("独立", "独立。"):
        return None
    out = []
    for part in re.split(r"[；;]", text):
        m = re.match(r"\s*(\S+?)\s*(→|←|↔|->|<-)\s*(.+?)\s*$", part)
        if m:
            out.append((m.group(1), m.group(3)))
        elif part.strip():
            out.append(("?", part.strip()))
    return out


def load_source(path):
    if not path:
        return None
    p = Path(path)
    files = sorted(p.rglob("*")) if p.is_dir() else [p]
    return squash("\n".join(f.read_text(encoding="utf-8", errors="ignore") for f in files if f.is_file()))


def check(path, source=None):
    path = Path(path)
    files = sorted(path.rglob("*.md")) if path.is_dir() else [path]
    src = load_source(source)
    cards = []
    for f in files:
        if f.name in SKIP:
            continue
        found = split_cards(f.read_text(encoding="utf-8"))
        if not found:
            return [f"[字段] {f.name}: 没找到卡（每张以「# 标题」开头）"]
        cards += [(f.name, c) for c in found]
    if not cards:
        return ["[字段] 没找到任何卡"]
    titles = {c["title"] for _, c in cards}
    # 地图里的名字（目录.md）也算能指向的地方：章、节、主题不一定单独出卡
    for f in files:
        if f.name == "目录.md":
            titles |= {re.sub(r"^[#\-*\s\d.、]+", "", ln).split("｜")[0].strip() for ln in f.read_text(encoding="utf-8").splitlines()}
    out = []
    for where, card in cards:
        meta, body, theme = parse(card)
        name = f"{where}「{card['title']}」"
        missing = (["一句话"] if not theme else []) + [k for k in META if not meta.get(k)] + ([] if body else ["正文"])
        if missing:
            out.append(f"[字段] {name}: 缺 {'、'.join(missing)}")
        if meta.get("类型") and meta["类型"] not in TYPES:
            out.append(f"[类型] {name}: 类型「{meta['类型']}」不在清单里（{'/'.join(sorted(TYPES))}）")
        if meta.get("可信度") and meta["可信度"] not in LEVELS:
            out.append(f"[可信度] {name}: 可信度「{meta['可信度']}」只能是 原文 / 归纳 / 推测")
        place = meta.get("出处", "")
        if place and not all(PLACE.search(p) for p in re.split(r"[；;]", place) if p.strip()):
            out.append(f"[出处] {name}: 出处「{place}」有一处没写能翻回去的位置（页码、章节、时间）")
        quote = meta.get("原话", "")
        quotes = re.findall(r"「(.+?)」", quote) or ([quote] if quote else [])
        if quote and src is not None and meta.get("可信度") != "推测":
            for q in quotes:
                if squash(q) and squash(q) not in src:
                    out.append(f"[原话] {name}: 原话「{q[:20]}…」在原文里找不到（是不是改了字？）")
                    break
        if body and quotes and squash(body) == squash("".join(quotes)):
            out.append(f"[提炼] {name}: 正文和原话一字不差，还没整理成自己的话")
        rel = relations(meta.get("关系", "")) if meta.get("关系") else []
        if rel is not None and meta.get("关系"):
            if not any(r == "属于" for r, _ in rel):
                out.append(f"[关系] {name}: 没挂「属于」（它在骨架里的位置）")
            for r, target in rel:
                if r not in RELS and r != "?":
                    out.append(f"[关系] {name}: 关系「{r}」不在清单里（{'/'.join(sorted(RELS))}）")
                elif r == "?":
                    out.append(f"[关系] {name}: 「{target}」看不出是什么关系（写成「关系 → 卡名」）")
                elif r != "属于" and target not in titles:
                    out.append(f"[关系] {name}: 指向的「{target}」找不到这张卡")
    return out


if __name__ == "__main__":
    args = sys.argv[1:]
    source = None
    if "--source" in args:
        i = args.index("--source")
        source = args[i + 1] if i + 1 < len(args) else None
        args = args[:i] + args[i + 2:]
    if len(args) != 1:
        sys.exit(__doc__)
    problems = check(args[0], source)
    for p in problems:
        print("❌", p)
    print("✅ 全部卡片合格" if not problems else f"共 {len(problems)} 处问题")
    sys.exit(1 if problems else 0)
