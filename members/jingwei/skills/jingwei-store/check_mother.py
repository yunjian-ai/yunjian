"""经纬的母体检查：查一个母体文件夹是不是照 `母体格式.md` 搭的，能数出来的毛病一条条报。只用 Python 自带的库。
用法：python3 check_mother.py <母体文件夹> [--map]
问题一行一条，以 ❌ [类别] 开头；只提醒不算错的以 ⚠️ 开头；没有问题打印 ✅。
--map：把关系总表写进 05-地图.md 的两个标记之间（问题清零才写）。
它只查格式和能数的：定义写得准不准、关系连得对不对、证据是不是真支撑，还要人看。"""
import re
import sys
from pathlib import Path

FILES = ("00-根.md", "01-规则.md", "03-空枝和缺口.md", "04-矛盾和待定.md", "05-地图.md", "06-改动记录.md")
VAGUE = {"有关", "相关", "关联", "联系", "关系", "其他", "等"}
STATES = {"草稿", "已定", "冷藏"}
TIMES = {"以前", "现在", "将来"}
# 出处要写到翻得回去的位置：数字，或「第…段/页/条/章/节…」
PLACE = re.compile(r"[0-9０-９]|第[一二三四五六七八九十百零〇两]+[章节页条段集讲回问行]")
REL = re.compile(r"^\s*[-*]\s*(.+?)\s*(?:→|->)\s*\[\[([^\]|#]+)(?:[|#][^\]]*)?\]\]\s*(.*)$")
START, END = "<!-- 关系总表开始 -->", "<!-- 关系总表结束 -->"


def sections(text):
    """按「## 标题」切节，返回 {标题: 正文}；代码块里的井号不算。"""
    out, cur, fence = {}, None, False
    for line in text.splitlines():
        if line.startswith("```"):
            fence = not fence
        if not fence and line.startswith("## "):
            cur = line[3:].strip()
            out[cur] = []
        elif cur is not None:
            out[cur].append(line)
    return {k: "\n".join(v).strip() for k, v in out.items()}


def table(text):
    """读第一张 Markdown 表，返回字典列表（表头作键）；分隔行跳过。"""
    rows = [ln.strip() for ln in text.splitlines() if ln.strip().startswith("|")]
    if not rows:
        return []
    cells = lambda ln: [c.strip() for c in ln.strip().strip("|").split("|")]
    head = cells(rows[0])
    return [dict(zip(head, cells(r))) for r in rows[1:] if not re.fullmatch(r"[\s|:\-]+", r)]


def front(text):
    """读顶部 --- 之间的「键: 值」；别名写成 [a, b]。"""
    m = re.match(r"---\s*\n(.*?)\n---\s*\n", text, re.S)
    meta = {}
    if m:
        for ln in m.group(1).splitlines():
            if ":" in ln:
                k, v = ln.split(":", 1)
                meta[k.strip()] = v.strip()
    return meta, (text[m.end():] if m else text)


def names(v):
    v = (v or "").strip().strip("[]")
    return [x.strip().strip("\"'") for x in re.split(r"[,，、]", v) if x.strip().strip("\"'")]


def load(root):
    root = Path(root)
    things = {}
    for f in sorted((root / "东西").glob("*.md")) if (root / "东西").is_dir() else []:
        meta, body = front(f.read_text(encoding="utf-8"))
        things[f.stem] = {"meta": meta, "sec": sections(body), "file": f.name}
    return root, things


def check(root):
    root, things = load(root)
    errs, warns = [], []
    E = lambda c, m: errs.append(f"[{c}] {m}")
    for n in FILES:
        if not (root / n).is_file():
            E("结构", f"缺 {n}")
    if not things:
        E("结构", "东西/ 文件夹里一样东西都没有")
    txt = lambda n: (root / n).read_text(encoding="utf-8") if (root / n).is_file() else ""

    # 根
    r = sections(txt("00-根.md"))
    for s in ("根", "主干", "边界", "要回答的问题"):
        if (root / "00-根.md").is_file() and not r.get(s):
            E("根", f"00-根.md 的「{s}」没写")
    qs = re.findall(r"^\s*[-*]\s*Q\d*\s*[：:]", r.get("要回答的问题", ""), re.M)
    if r.get("要回答的问题") is not None and not qs:
        E("根", "要回答的问题一个都没列（写成「- Q1：…」）")
    if qs and r.get("要回答的问题", "").count("答对了省下") < len(qs):
        E("根", "有的问题下面没写「答对了省下」")

    # 规则
    g = sections(txt("01-规则.md"))
    dims = {row.get("维度", ""): row for row in table(g.get("维度", "")) if row.get("维度")}
    if (root / "01-规则.md").is_file() and not dims:
        E("规则", "维度表是空的")
    for d, row in dims.items():
        if not row.get("定义"):
            E("规则", f"维度「{d}」没写定义")
        if row.get("状态") not in ("有", "空枝"):
            E("规则", f"维度「{d}」的状态只能写「有」或「空枝」")
    rels = {}
    for row in table(g.get("关系词表", "")):
        k = row.get("关系", "")
        if not k:
            continue
        if k in VAGUE:
            E("规则", f"关系词表里「{k}」太空，换成具体的动词")
        if not row.get("定义"):
            E("规则", f"关系「{k}」没写定义")
        rels[k] = row
    allowed = {}
    for row in table(g.get("状态取值", "")):
        if row.get("东西"):
            allowed[row["东西"]] = set(names(row.get("取值", "").replace("/", ",")))

    # 东西：名字和别名不能撞
    owner = {}
    for n, t in things.items():
        for a in [n] + names(t["meta"].get("别名")):
            if a in owner and owner[a] != n:
                E("东西", f"「{a}」同时是「{owner[a]}」和「{n}」的名字或别名，同名要先判是不是一回事")
            owner.setdefault(a, n)
    edges, linked = [], set()
    for n, t in things.items():
        m, sec = t["meta"], t["sec"]
        if not sec.get("定义"):
            E("东西", f"{t['file']} 没写定义")
        if dims and m.get("维度") not in dims:
            E("东西", f"{t['file']} 的维度「{m.get('维度', '')}」不在维度表里")
        if m.get("状态") and m["状态"] not in STATES:
            E("东西", f"{t['file']} 的状态只能是草稿 / 已定 / 冷藏")
        if m.get("时间") and not set(names(m["时间"])) <= TIMES:
            E("东西", f"{t['file']} 的时间只能写以前 / 现在 / 将来")
        for ln in sec.get("关系", "").splitlines():
            if not ln.strip():
                continue
            mm = REL.match(ln)
            if not mm:
                E("关系", f"{t['file']} 这行关系写法不对，要写「- 关系名 → [[对方]]」：{ln.strip()[:40]}")
                continue
            k, to, tail = mm.group(1).strip(), mm.group(2).strip(), mm.group(3)
            if k in VAGUE:
                E("关系", f"{t['file']}：「{k}」太空，换成具体的动词")
            elif rels and k not in rels:
                E("关系", f"{t['file']}：关系「{k}」不在关系词表里")
            target = owner.get(to)
            if target is None:
                E("关系", f"{t['file']}：指向的「{to}」不是母体里的东西（死链）")
            else:
                linked |= {n, target}
                edges.append((n, k, target, "待确认" if "待确认" in tail else ""))
        for ln in sec.get("证据", "").splitlines():
            ln = ln.strip()
            if not ln.startswith(("-", "*")):
                continue
            parts = [p.strip() for p in ln.lstrip("-* ").split("｜")]
            if len(parts) < 3 or not PLACE.search(parts[1]):
                E("证据", f"{t['file']} 这条证据没写翻得回去的出处（写成「来源｜第几段或日期｜原话」）：{ln[:40]}")
        for row in table(sec.get("状态流转", "")):
            for s in (row.get("从", ""), row.get("到", "")):
                if s and n in allowed and s not in allowed[n]:
                    E("状态", f"{t['file']}：状态「{s}」不在状态取值表里")
                elif s and n not in allowed:
                    E("状态", f"{t['file']} 写了状态流转，但状态取值表里没有「{n}」这一行")
                    break
    for n in things:
        if n not in linked and len(things) > 1:
            warns.append(f"⚠️ 「{n}」没有和任何东西连上")
    pend = sum(txt(f"东西/{t['file']}").count("待确认") for t in things.values())
    if pend:
        warns.append(f"⚠️ 还有 {pend} 处待确认，交付前请主人过一遍")
    if (root / "03-空枝和缺口.md").is_file() and not table(sections(txt("03-空枝和缺口.md")).get("空枝", "")):
        warns.append("⚠️ 空枝表是空的：主人提到的将来的事都该在这里")
    return errs, warns, edges


def write_map(root, edges):
    p = Path(root) / "05-地图.md"
    text = p.read_text(encoding="utf-8")
    if START not in text or END not in text:
        return False
    rows = ["| 从 | 关系 | 到 | 备注 |", "|---|---|---|---|"] + [f"| {a} | {k} | {b} | {x} |" for a, k, b, x in edges]
    new = text.split(START)[0] + START + "\n" + "\n".join(rows) + "\n" + END + text.split(END, 1)[1]
    p.write_text(new, encoding="utf-8")
    return True


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    root = argv[0]
    if not Path(root).is_dir():
        print(f"❌ [结构] 找不到文件夹 {root}")
        return 1
    errs, warns, edges = check(root)
    for e in errs:
        print("❌ " + e)
    for w in warns:
        print(w)
    if not errs:
        print(f"✅ 母体格式没问题：{len(load(root)[1])} 样东西、{len(edges)} 条关系")
        if "--map" in argv:
            print("已写进 05-地图.md 的关系总表" if write_map(root, edges) else "⚠️ 05-地图.md 里没有关系总表的两个标记，没写")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
