"""体检（起元架构）：只读，一个文件都不改。量一台电脑上 Claude Code、WorkBuddy、Grok Bot 每次对话固定带多少，
哪些超了线、同一条规矩写在几处、哪两条疑似打架，最后给最值得做的三条。
Claude Code 的准数（token）以官方命令为准：/context、/usage、/skill-doctor、/doctor prompt-audit；这里只补官方没管的，字数按字符估。
用法：python3 体检.py [--家 ~] [--项目 目录 …] [--grok agent-data目录] [--预算 自己的预算.json] [--写 输出目录]
  不给 --写 就把体检表打在屏幕上；给了就写 <输出目录>/体检-<日期>.md 和 .json（输出目录不能在 --家 里面）。
只用标准库。"""
import argparse
import datetime
import hashlib
import json
import re
from pathlib import Path

预算 = {"CLAUDE.md行": 200, "说明截断字": 1536, "自动记忆行": 200, "自动记忆字节": 25 * 1024,
      "WorkBuddy读字": 4000, "Bot指令字": 4000, "共用技能库个数": 200}
口径 = {
    "CLAUDE.md行": "官方·Claude Code Memory 页：每份 200 行以内（2026-10-30 核）",
    "说明截断字": "官方·Claude Code Skills 页：description＋when_to_use 合计超 1,536 字截断（2026-10-30 核）",
    "自动记忆": "官方·Claude Code Memory 页：每次只加载 MEMORY.md 前 200 行或 25KB（2026-10-30 核）",
    "WorkBuddy读字": "推荐值：WorkBuddy 每次只读 MEMORY.md 前 4,000 字（实测记录，没找到官方说明）",
    "Bot指令字": "推荐值：Bot 指令 4,000 字以内（五层写法的预算线，可在 --预算 里改）",
    "共用技能库个数": "实测：Grok 共用技能库两百多项时会截断（没找到官方说明）",
    "字": "字＝字符（一个汉字算 1），按字符估，不是 token；准数用官方 /context、/usage",
}
OVERRIDE = {"on": "开", "name-only": "只露名字", "user-invocable-only": "只给用户用", "off": "关"}
严 = ("必须", "一律", "务必", "一定要", "都要", "不许", "禁止", "不能")
宽 = ("不用", "不必", "无需", "可以不", "随便", "就行", "也行")


def rd(f):
    return f.read_text(encoding="utf-8", errors="replace")


def rel(f, home):
    try:
        return str(f.relative_to(home))
    except ValueError:
        return str(f)


def frontmatter(text):
    """取 SKILL.md 头部的 name、description、when_to_use（不靠 yaml 库；多行值、引号、> | 都处理）。"""
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    out = {}
    if m:
        for k, v in re.findall(r"(?ms)^([\w-]+):[ \t]*(.*?)(?=^[\w-]+:|\Z)", m.group(1)):
            v = re.sub(r"\s+", " ", v).strip()
            out[k] = re.sub(r"^[>|][-+]?\s*", "", v).strip().strip("'\"")
    return out


def overrides(home, projects):
    """skillOverrides：全局 settings.json，项目的 settings.json、settings.local.json 依次覆盖。"""
    ov = {}
    for f in [home / ".claude" / "settings.json"] + [p / ".claude" / n for p in projects for n in ("settings.json", "settings.local.json")]:
        if f.exists():
            try:
                ov.update(json.loads(rd(f)).get("skillOverrides", {}) or {})
            except json.JSONDecodeError:
                pass
    return ov


def skills(dirs, ov, cut):
    rows, groups = [], {}
    for d in dirs:
        for f in sorted(d.glob("*/SKILL.md")):
            fm = frontmatter(rd(f))
            name = fm.get("name") or f.parent.name
            desc = " ".join(x for x in (fm.get("description", ""), fm.get("when_to_use", "")) if x)
            state = ov.get(name, "on")
            if state == "on" and fm.get("disable-model-invocation", "").lower() == "true":
                state = "user-invocable-only"  # 技能头里关掉了模型自动调用：模型看不到，和「只给用户用」一样
            carry = 0 if state in ("off", "user-invocable-only") else len(name) + (min(len(desc), cut) if state == "on" else 0)
            rows.append({"名字": name, "档": OVERRIDE.get(state, state), "说明字": len(desc), "每次带": carry, "目录": str(d)})
            if desc:
                groups.setdefault(desc, []).append(name)
    return {"个数": len(rows), **{v: sum(r["档"] == v for r in rows) for v in OVERRIDE.values()},
            "每次带的字": sum(r["每次带"] for r in rows),
            "截断的": sorted(r["名字"] for r in rows if r["说明字"] > cut and r["档"] == "开"),  # 只露名字的说明本来就不带
            "撞车的": sorted(sorted(v) for v in groups.values() if len(v) > 1),
            "同名的": sorted({r["名字"] for r in rows if sum(x["名字"] == r["名字"] for x in rows) > 1}), "明细": sorted(rows, key=lambda r: r["名字"])}


def imports(f, home, seen, depth=0):
    """CLAUDE.md 里「@路径」引用的文件开会话时一起加载、不省字（官方 Memory 页：相对本文件，最多 5 层）。返回引用到的文件。"""
    out = []
    for p in re.findall(r"(?<![\w`])@((?:~/)?[^\s`@]+)", rd(f)) if depth < 5 else []:
        g = (home / p[2:]) if p.startswith("~/") else (f.parent / p)
        if g.is_file() and g.resolve() not in seen:
            seen.add(g.resolve())
            out += [g] + imports(g, home, seen, depth + 1)
    return out


def agents(dirs):
    """~/.claude/agents/、项目 .claude/agents/ 里各代理的「名字＋说明」每次都带（按需的是正文）。"""
    rows = []
    for d in dirs:
        for f in sorted(d.glob("*.md")):
            fm = frontmatter(rd(f))
            rows.append(len(fm.get("name") or f.stem) + len(fm.get("description", "")))
    return {"个数": len(rows), "每次带的字": sum(rows)}


def claude(home, projects, B):
    rules = []
    for f, proj in [(home / ".claude" / "CLAUDE.md", "")] + [(x, str(p)) for p in projects for x in (p / "CLAUDE.md", p / ".claude" / "CLAUDE.md", p / "CLAUDE.local.md")]:
        if f.exists():
            t = rd(f)
            n = len(t.splitlines())
            inc = imports(f, home, {f.resolve()})
            rules.append({"位置": rel(f, home), "行": n, "字": len(t) + sum(len(rd(g)) for g in inc), "超线": n > B["CLAUDE.md行"],
                          "超出的字": len("".join(t.splitlines(True)[B["CLAUDE.md行"]:])), "引用": [rel(g, home) for g in inc], "项目": proj})
    for f in sorted((home / ".claude" / "rules").glob("*.md")):  # 没写 paths 的规则文件每次都带
        t = rd(f)
        if not re.match(r"---\n(?:.*\n)*?paths:", t):
            rules.append({"位置": rel(f, home), "行": len(t.splitlines()), "字": len(t), "超线": False, "超出的字": 0})
    mem = []
    for f in sorted((home / ".claude" / "projects").glob("*/memory/MEMORY.md")):
        lines = f.read_bytes().decode("utf-8", "replace").splitlines(True)
        keep, size = 0, 0
        for ln in lines[:B["自动记忆行"]]:
            size += len(ln.encode())
            if size > B["自动记忆字节"]:
                break
            keep += 1
        mem.append({"位置": rel(f, home), "行": len(lines), "字": sum(map(len, lines)), "读不到的行": len(lines) - keep,
                    "读不到的字": sum(map(len, lines[keep:]))})
    dirs = [home / ".claude" / "skills"] + [p / ".claude" / "skills" for p in projects]
    sk = skills([d for d in dirs if d.exists()], overrides(home, projects), B["说明截断字"])
    ag = agents([d for d in [home / ".claude" / "agents"] + [p / ".claude" / "agents" for p in projects] if d.is_dir()])
    return {"规则文件": rules, "技能": sk, "代理": ag, "自动记忆": sorted(mem, key=lambda m: (-m["行"], m["位置"]))}


def workbuddy(home, B):
    """~/.workbuddy/MEMORY.md 和 user-*/MEMORY.md；一字不差的几份算一处。"""
    seen = {}
    for f in [home / ".workbuddy" / "MEMORY.md"] + sorted((home / ".workbuddy").glob("user-*/MEMORY.md")):
        if f.exists():
            seen.setdefault(hashlib.sha256(f.read_bytes()).hexdigest(), []).append(f)
    out = []
    for fs in seen.values():
        t = rd(fs[0])
        out.append({"位置": "、".join(rel(f, home) for f in fs) + ("（几份一样）" if len(fs) > 1 else ""), "文件": [rel(f, home) for f in fs],
                    "字": len(t), "读不到的字": max(0, len(t) - B["WorkBuddy读字"])})
    return out


def grok_dir(home, given):
    for d in ([Path(given).expanduser()] if given else [home / "agent-data", home / "box" / "agent-data", Path("/home/box/agent-data")]):
        if (d / "agents").is_dir():
            return d
    return None


def grok(d, home, B):
    if d is None:
        return None
    bots = []
    for f in sorted(d.glob("agents/*/profile.json")):
        try:
            prof = json.loads(rd(f))
        except json.JSONDecodeError:
            continue
        ins = prof.get("description", "") or ""
        bots.append({"名字": prof.get("name", f.parent.name), "id": f.parent.name, "指令字": len(ins), "超线": len(ins) > B["Bot指令字"],
                     "位置": rel(f, home), "_指令": ins})
    lib = skills([d / "workflows"], {}, B["说明截断字"]) if (d / "workflows").exists() else {"个数": 0, "每次带的字": 0}
    return {"目录": rel(d, home), "Bot": bots, "共用技能库": {"个数": lib["个数"], "目录字": lib["每次带的字"], "超线": lib["个数"] > B["共用技能库个数"]},
            "量不到": ["各 Bot 自己的记忆（不在沙盒里）：请在那个 Bot 里问一句「你有几条记忆、多少字」", "账号共用记忆（在云端，沙盒里没有）"]}


def norm(ln):
    s = re.sub(r"^\s*(?:[-*+]\s+|\d+[.、)]\s*|#+\s*|>\s*)", "", ln).strip()
    return s if len(s) >= 12 else ""


def sources(home, cc, wb, gk):
    """[(位置, 文本, 哪个项目)]：规则文件连同 @ 引用的一起算；项目为空的（全局、WorkBuddy、Grok）和谁都同时在。"""
    p = lambda x: Path(x) if Path(x).is_absolute() else home / x
    out = [(r["位置"], "\n".join(rd(p(x)) for x in [r["位置"]] + r.get("引用", [])), r.get("项目", "")) for r in cc["规则文件"]]
    out += [(w["位置"], rd(home / w["文件"][0]), "") for w in wb]
    out += [(f"Grok {b['名字']}", b["_指令"], "") for b in (gk or {}).get("Bot", [])]
    return out


def dup_and_conflict(srcs):
    """同一条写在两处以上（跨文件、跨 AI、跨 Bot）；疑似打架：两处说同一件事，一处要求、一处放宽（只比不同的两处，要人看）。"""
    where, lines, grp = {}, [], {n: g for n, _, g in srcs}
    together = lambda a, b: not grp[a] or not grp[b] or grp[a] == grp[b]  # 两个不同项目的文件不会同时带上
    for name, text, _ in srcs:
        for ln in text.splitlines():
            s = norm(ln)
            if s:
                where.setdefault(s, [])
                if name not in where[s]:
                    where[s].append(name)
                lines.append((name, s))
    dup = sorted(({"规矩": k, "位置": v} for k, v in where.items() if any(together(a, b) for i, a in enumerate(v) for b in v[i + 1:])), key=lambda x: (-len(x["位置"]), x["规矩"]))
    bg = lambda s: {s[i:i + 2] for i in range(len(s) - 1) if re.fullmatch(r"[一-鿿]{2}", s[i:i + 2])}
    pol = bg("".join(严 + 宽))
    short = [(n, s, bg(s) - pol) for n, s in dict.fromkeys(lines) if len(s) <= 80]  # 打架的多是短句；长段落共用词多，比了全是误报
    strict = [x for x in short if any(w in x[1] for w in 严)]
    lax = [x for x in short if any(w in x[1] for w in 宽)]
    pairs = [{"甲": {"位置": a, "原文": s}, "乙": {"位置": b, "原文": t}} for a, s, x in strict for b, t, y in lax
             if a != b and together(a, b) and s != t and len(x & y) >= 2 and len(x & y) / min(len(x), len(y)) >= 0.15]
    return dup, pairs[:20]


def top3(r, B):
    """最值得做的三条：先打架（模型会随便挑一条听），再按影响的字数排。"""
    c = []
    if r["疑似打架"]:
        c.append((10 ** 9, f"有 {len(r['疑似打架'])} 对规矩疑似打架（例：{r['疑似打架'][0]['甲']['位置']} 和 {r['疑似打架'][0]['乙']['位置']}），请主人定留哪条"))
    for f in r["ClaudeCode"]["规则文件"]:
        if f["超线"]:
            c.append((f["超出的字"], f"{f['位置']} {f['行']} 行，超了 {B['CLAUDE.md行']} 行（多 {f['超出的字']} 字）：专门的流程挪进技能或细则文件"))
    sk = r["ClaudeCode"]["技能"]
    if sk["截断的"]:
        c.append((len(sk["截断的"]) * B["说明截断字"], f"{len(sk['截断的'])} 个技能说明超 {B['说明截断字']} 字被截断（{'、'.join(sk['截断的'][:5])}）：压短或改只露名字"))
    for m in r["ClaudeCode"]["自动记忆"]:
        if m["读不到的行"]:
            c.append((m["读不到的字"], f"自动记忆 {m['位置']} {m['行']} 行，后 {m['读不到的行']} 行读不到：挪进分题文件"))
    for w in r["WorkBuddy"]:
        if w["读不到的字"]:
            c.append((w["读不到的字"], f"WorkBuddy 记忆 {w['字']} 字，后 {w['读不到的字']} 字读不到：压短"))
    if r["Grok"]:
        over = [b for b in r["Grok"]["Bot"] if b["超线"]]
        if over:
            c.append((sum(b["指令字"] - B["Bot指令字"] for b in over), f"Grok {len(over)} 个 Bot 指令超 {B['Bot指令字']} 字（{'、'.join(b['名字'] for b in over)}）：照五层写法改"))
    if r["重复"]:
        c.append((sum(len(d["规矩"]) * (len(d["位置"]) - 1) for d in r["重复"]), f"{len(r['重复'])} 条规矩写在两处以上（最多的一条在 {len(r['重复'][0]['位置'])} 处）：只留一个正本"))
    return [t for _, t in sorted(c, key=lambda x: -x[0])[:3]]


def 规则常驻(cc):
    """规则文件每次带的字：全局的＋最大的那一个项目（一次对话只开一个项目）。"""
    by = {}
    for f in cc["规则文件"]:
        by[f.get("项目", "")] = by.get(f.get("项目", ""), 0) + f["字"]
    return by.pop("", 0) + max(by.values(), default=0)


def measure(home, projects=(), grok_given="", B=None):
    """量一次，返回体检结果（dict）。只读。"""
    B = dict(预算, **(B or {}))
    home = Path(home).expanduser().resolve()
    projects = [Path(p).expanduser().resolve() for p in projects]
    cc, wb = claude(home, projects, B), workbuddy(home, B)
    gk = grok(grok_dir(home, grok_given), home, B)
    dup, conf = dup_and_conflict(sources(home, cc, wb, gk))
    if gk:
        for b in gk["Bot"]:
            b.pop("_指令")
    r = {"日期": datetime.date.today().isoformat(), "家": str(home), "项目": [str(p) for p in projects], "预算": B, "口径": 口径,
         "ClaudeCode": cc, "WorkBuddy": wb, "Grok": gk, "重复": dup, "疑似打架": conf}
    cm = max((m["字"] - m["读不到的字"] for m in cc["自动记忆"]), default=0)
    r["每次固定带"] = {"ClaudeCode": {"规则": 规则常驻(cc), "技能目录": cc["技能"]["每次带的字"], "代理说明": cc["代理"]["每次带的字"], "自动记忆": cm},
                    "WorkBuddy": max((w["字"] - w["读不到的字"] for w in wb), default=0)}
    if gk:
        lib, ins = gk["共用技能库"]["目录字"], [b["指令字"] for b in gk["Bot"]]
        r["每次固定带"]["Grok每个Bot"] = [lib + min(ins, default=0), lib + max(ins, default=0)]
    r["最值得做"] = top3(r, B)
    return r


def 总数行(r):
    c = r["每次固定带"]["ClaudeCode"]
    s = [f"- Claude Code：约 {sum(c.values())} 字（规则 {c['规则']}＋技能目录 {c['技能目录']}＋代理说明 {c['代理说明']}＋自动记忆读得到的 {c['自动记忆']}；规则按全局＋最大的一个项目、记忆按一个项目算；"
         "MCP 工具说明、插件带的技能、内置提示词量不到，准数打 `/context`）",
         f"- WorkBuddy：约 {r['每次固定带']['WorkBuddy']} 字（记忆读得到的部分）"]
    g = r["每次固定带"].get("Grok每个Bot")
    if g:
        s.append(f"- Grok：每个 Bot 约 {g[0]}～{g[1]} 字（自己的指令＋共用技能库目录；记忆量不到，没算）")
    return s


def render(r):
    B, cc = r["预算"], r["ClaudeCode"]
    s = [f"# 体检表 · {r['日期']}", "", "> 只读，一个文件都没改。**字＝字符，按字符估**；Claude Code 的准数（token）请在 Claude Code 里打 `/context`（看什么占了上下文）、"
         "`/usage`（按技能、插件分摊用量）；技能花费和使用次数打 `/skill-doctor`，规则过时和打架打 `/doctor prompt-audit`。", "",
         "## 每次固定带（按平台；各带各的，平台之间不相加）", ""] + 总数行(r) + ["", "## 最值得做的三条", ""] + ([f"{i}. {t}" for i, t in enumerate(r["最值得做"], 1)] or ["- 没有超线、重复或打架的，现在不用瘦。"]) + ["", "## Claude Code", "", "| 规则文件 | 行 | 字 | 超线 |", "|---|---|---|---|"]
    s += [f"| {f['位置']}{'（含 @ 引用 ' + '、'.join(f['引用']) + '）' if f.get('引用') else ''} | {f['行']} | {f['字']} | {'🔴 超 ' + str(B['CLAUDE.md行']) + ' 行' if f['超线'] else '—'} |" for f in cc["规则文件"]]
    sk = cc["技能"]
    s += ["", f"技能 {sk['个数']} 个：开 {sk['开']}、只露名字 {sk['只露名字']}、只给用户用 {sk['只给用户用']}、关 {sk['关']}；**每次固定带 {sk['每次带的字']} 字**（名字＋截断后的说明）。",
          f"- 说明超 {B['说明截断字']} 字会被截断的：{'、'.join(sk['截断的']) or '无'}",
          f"- 说明一字不差撞车的（路由会乱）：{'；'.join('、'.join(g) for g in sk['撞车的']) or '无'}",
          f"- 全局和项目里同名的技能（只会认一个）：{'、'.join(sk['同名的']) or '无'}"]
    mem = [m for m in cc["自动记忆"] if m["读不到的行"]] or cc["自动记忆"][:1]
    s += [f"- 自动记忆 {m['位置']}：{m['行']} 行，{'🔴 后 ' + str(m['读不到的行']) + ' 行读不到' if m['读不到的行'] else '都读得到'}" for m in mem]
    s += ["", "## WorkBuddy", ""] + ([f"- {w['位置']}：{w['字']} 字{'，🔴 后 ' + str(w['读不到的字']) + ' 字读不到' if w['读不到的字'] else ''}" for w in r["WorkBuddy"]] or ["- 没找到 WorkBuddy 记忆"])
    g = r["Grok"]
    if g:
        s += ["", f"## Grok Bot（{g['目录']}）", "", "| Bot | 指令字 | 超线 |", "|---|---|---|"]
        s += [f"| {b['名字']} | {b['指令字']} | {'🔴' if b['超线'] else '—'} |" for b in g["Bot"]]
        s += ["", f"共用技能库 {g['共用技能库']['个数']} 个，目录 {g['共用技能库']['目录字']} 字{'（🔴 超 ' + str(B['共用技能库个数']) + ' 个会截断）' if g['共用技能库']['超线'] else ''}。", "",
              "**量不到的**：" + "；".join(g["量不到"]) + "。不编数。"]
    else:
        s += ["", "## Grok Bot", "", "- 这台电脑上没找到 Grok 沙盒（只在 Grok 桌面版 Bot 里能量）。"]
    s += ["", f"## 同一条写在几处（{len(r['重复'])} 条）", ""] + ([f"- 「{d['规矩'][:40]}」：{'、'.join(d['位置'])}" for d in r["重复"][:10]] or ["- 无"])
    s += ["", f"## 疑似打架（{len(r['疑似打架'])} 对，要主人定留哪条）", ""] + ([f"- {p['甲']['位置']}「{p['甲']['原文'][:40]}」⇄ {p['乙']['位置']}「{p['乙']['原文'][:40]}」" for p in r["疑似打架"]] or ["- 无"])
    s += ["", "## 口径", ""] + [f"- {k}：{v}" for k, v in r["口径"].items()]
    return "\n".join(s) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--家", default="~")
    ap.add_argument("--项目", nargs="*", default=[])
    ap.add_argument("--grok", default="")
    ap.add_argument("--预算", default="")
    ap.add_argument("--写", default="")
    a = ap.parse_args()
    B = json.loads(Path(a.预算).expanduser().read_text(encoding="utf-8")) if a.预算 else None
    r = measure(a.家, a.项目, a.grok, B)
    if not a.写:
        print(render(r))
        return
    out = Path(a.写).expanduser().resolve()
    if out == Path(r["家"]) or Path(r["家"]) in out.parents and ".yunjian" not in out.parts:
        raise SystemExit(f"输出目录 {out} 在 --家 里面，会改动被体检的电脑；换一个（默认放 ~/.yunjian/jiagou/体检/）")
    out.mkdir(parents=True, exist_ok=True)
    (out / f"体检-{r['日期']}.md").write_text(render(r), encoding="utf-8")
    (out / f"体检-{r['日期']}.json").write_text(json.dumps(r, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"已写 {out / ('体检-' + r['日期'] + '.md')} 和 .json")


if __name__ == "__main__":
    main()
