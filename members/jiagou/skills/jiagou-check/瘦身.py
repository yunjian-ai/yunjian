"""瘦身（起元架构）：照体检结果出挪移清单 → 预演 → 主人点头的几条才执行 → 执行前先备份 → 一条命令改回。
不删任何东西：挪出去的文字放进新文件，改设置只改 skillOverrides；Grok Bot、重复、打架只出「手工条」，脚本不动，由主人定。
用法：
  python3 瘦身.py 清单 [--家 ~] [--项目 目录 …] [--grok 目录] [--预算 自己的预算.json]   只读；清单存到 <存到>/瘦身/清单-<时间>.json
  python3 瘦身.py 执行 --清单 <清单.json> --条 1,2 [--确认]   不加 --确认 只预演（打印会改什么）；加了先备份再改，改完再体检、报前后数字
  python3 瘦身.py 改回 [最近一次|<备份目录>] [--硬]          原样放回、新建的删掉；改完以后文件又被动过就先停下（--硬 照样放回）
  公共参数 --存到（默认 ~/.yunjian/jiagou，放清单和备份；除了 .yunjian，不能在 --家 里面，否则改回后校验码对不上）
只用标准库。"""
import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
from pathlib import Path

_s = importlib.util.spec_from_file_location("体检", Path(__file__).with_name("体检.py"))
体检 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(体检)
NAME_ONLY = "name-only"


def sha(f):
    f = Path(f)
    return hashlib.sha256(f.read_bytes()).hexdigest() if f.exists() else None


def lines_of(f):
    return Path(f).read_text(encoding="utf-8", errors="replace").splitlines(True)


def free_name(d, base):
    n, k = base, 2
    while (d / n).exists():
        n, k = f"{base}-{k}", k + 1
    return n


def 常驻(r):
    """每次对话固定带的字（按字符估）：规则文件全文（全局＋最大的一个项目）＋技能目录＋自动记忆读得到的部分（每个项目一份，取最大的）＋WorkBuddy 读得到的部分。"""
    cc = r["ClaudeCode"]
    return {"规则文件": 体检.规则常驻(cc), "技能目录": cc["技能"]["每次带的字"], "代理说明": cc["代理"]["每次带的字"],
            "自动记忆": max((m["字"] - m["读不到的字"] for m in cc["自动记忆"]), default=0), "WorkBuddy": sum(w["字"] - w["读不到的字"] for w in r["WorkBuddy"])}


def items(r, home, today):
    """由体检结果造清单。每条最多碰一组文件，几条之间不碰同一个文件，所以可以只点其中几条。"""
    B, cc, out = r["预算"], r["ClaudeCode"], []
    path = lambda p: Path(p) if Path(p).is_absolute() else home / p
    # ① 技能说明被截断的 → 只露名字（官方 skillOverrides 四档之一；打 /名字 照样能用）
    sk = cc["技能"]
    cut = [x for x in sk["明细"] if x["名字"] in sk["截断的"] and x["档"] == "开"]
    if cut:
        f = home / ".claude" / "settings.json"
        cfg = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
        cfg.setdefault("skillOverrides", {}).update({x["名字"]: NAME_ONLY for x in cut})
        out.append({"类": "改设置", "挪什么": f"{len(cut)} 个说明超 {B['说明截断字']} 字的技能（{'、'.join(x['名字'] for x in cut)}）改「只露名字」",
                    "挪去哪": f"{体检.rel(f, home)} 的 skillOverrides（技能文件一个字不动）", "省": sum(x["每次带"] - len(x["名字"]) for x in cut),
                    "效果": "模型只看到名字，说明不再每次带；主人打 /名字 照样能用。以后想恢复，把那几个说明压到 200 字内再改回「开」",
                    "改动": [{"文件": str(f), "内容": json.dumps(cfg, ensure_ascii=False, indent=2) + "\n"}]})
    # ② 规则文件超线 → 后半段挪进一个按需读的技能，原处留一行指路
    for x in cc["规则文件"]:
        if not x["超线"]:
            continue
        f = path(x["位置"])
        ls, keep = lines_of(f), B["CLAUDE.md行"] - 1
        heads = [i for i in range(keep // 2, keep + 1) if ls[i].startswith("#")]
        keep = heads[-1] if heads else keep  # 整段挪：切口退到最近的标题，不把一段切成两半
        hard = [norm for norm in (体检.norm(x) for x in ls[keep:]) if norm and any(w in norm for w in 体检.严)]
        sdir = (f.parent if f.parent.name == ".claude" else f.parent / ".claude") / "skills"
        name = free_name(sdir, "rules-detail")
        desc = f"{x['位置']} 第 {keep + 1} 行以后挪来的规矩细则。做事碰到规矩里没写到的、或要查细则时读。"
        point = f"（第 {keep + 1} 行以后的细则挪进技能 {name}，用到时读它。）\n"
        tail = "".join(ls[keep:])
        out.append({"类": "挪文字", "挪什么": f"{x['位置']} 第 {keep + 1}～{len(ls)} 行（{len(tail)} 字）", "挪去哪": f"新技能 {体检.rel(sdir / name, home)}/SKILL.md，原处留一行指路",
                    "省": len(tail) - len(point) - len(name) - len(desc),
                    "效果": f"{x['位置']} 变成 {keep + 1} 行；挪走的只在用到时读。常用的几条请先挪到前 {keep} 行再执行"
                    + (f"。⚠️ 挪走的部分里有 {len(hard)} 句硬规矩，请先看要不要留在前面：" + "；".join(f"「{h[:30]}」" for h in hard[:5]) if hard else ""),
                    "改动": [{"文件": str(f), "内容": "".join(ls[:keep]) + point},
                           {"文件": str(sdir / name / "SKILL.md"), "内容": f"---\nname: {name}\ndescription: {desc}\n---\n\n{tail}"}]})
    # ③ 自动记忆、WorkBuddy 记忆后面读不到的 → 挪进分题文件，原处留一行指路（常驻不变，读不到的变成用到时能读）
    mems = [(m["位置"], m["行"] - m["读不到的行"], m["读不到的行"]) for m in cc["自动记忆"] if m["读不到的行"]]
    for where, keep_n, lost in mems:
        f = path(where)
        ls, keep = lines_of(f), keep_n - 1
        g = f.parent / free_name(f.parent, f"archive-{today}.md")
        point = f"- 第 {keep + 1} 行以后的旧记忆挪进 {g.name}，用到时读。\n"
        out.append({"类": "挪文字", "挪什么": f"自动记忆 {where} 第 {keep + 1}～{len(ls)} 行（本来就读不到的 {lost} 行＋腾一行指路）", "挪去哪": f"同目录新文件 {g.name}，原处留一行指路",
                    "省": 0, "效果": f"常驻不变；后 {lost} 行从「读不到」变成「用到时能读」。更好的是顺手合并重复的几条",
                    "改动": [{"文件": str(f), "内容": "".join(ls[:keep]) + point}, {"文件": str(g), "内容": "".join(ls[keep:])}]})
    for w in r["WorkBuddy"]:
        if not w["读不到的字"]:
            continue
        fs = [home / p for p in w["文件"]]
        ls, lim = lines_of(fs[0]), B["WorkBuddy读字"] - 60
        keep, n = 0, 0
        while keep < len(ls) and n + len(ls[keep]) <= lim:
            n, keep = n + len(ls[keep]), keep + 1
        g = fs[0].parent / free_name(fs[0].parent, f"memory-archive-{today}.md")
        point = f"- 后面的旧记忆挪进 {g.name}，用到时读。\n"
        out.append({"类": "挪文字", "挪什么": f"WorkBuddy 记忆 {w['位置']} 第 {keep + 1}～{len(ls)} 行（{len(''.join(ls[keep:]))} 字，前 {B['WorkBuddy读字']} 字以外读不到的部分）",
                    "挪去哪": f"新文件 {体检.rel(g, home)}，原处留一行指路" + ("（几份一样的一起改）" if len(fs) > 1 else ""), "省": 0,
                    "效果": "常驻不变；读不到的那段变成用到时能读。更好的是压短：重复的、过时的删掉",
                    "改动": [{"文件": str(f), "内容": "".join(ls[:keep]) + point} for f in fs] + [{"文件": str(g), "内容": "".join(ls[keep:])}]})
    out.sort(key=lambda x: -x["省"])
    # ④ 手工条：脚本不动，主人定
    manual = []
    if sk["撞车的"]:
        manual.append({"挪什么": f"说明一字不差撞车的技能：{'；'.join('、'.join(g) for g in sk['撞车的'])}", "挪去哪": "主人各改一句，说清两个的区别（不然模型分不清叫哪个）"})
    for p in r["疑似打架"]:
        manual.append({"挪什么": f"疑似打架：{p['甲']['位置']}「{p['甲']['原文']}」⇄ {p['乙']['位置']}「{p['乙']['原文']}」", "挪去哪": "主人定留哪条，另一条改掉"})
    for d in r["重复"][:5]:
        manual.append({"挪什么": f"同一条写在 {len(d['位置'])} 处：「{d['规矩'][:40]}」（{'、'.join(d['位置'])}）",
                       "挪去哪": "同一个 AI 里只留一处正本；不同 AI 各读各的，可以留着，改的时候几处一起改"})
    lib = (r["Grok"] or {}).get("共用技能库", {})
    if lib.get("目录超线"):
        manual.append({"挪什么": f"Grok 共用技能库 {lib['个数']} 个技能，目录 {lib['目录字']} 字，每个 Bot 每次都带",
                       "挪去哪": "不常用的从共用库挪进归档（全账号共用，挪走后所有 Bot 都用不到）：先在 Grok 里看哪些在用，主人点名才挪；在 Grok 里操作，本机沙盒不动"})
    for b in [b for b in (r["Grok"] or {}).get("Bot", []) if b["超线"]]:
        manual.append({"挪什么": f"Grok「{b['名字']}」指令 {b['指令字']} 字，超 {B['Bot指令字']}", "挪去哪": "照五层写法改（岗位、原则 ≤8 条、流程挪进技能、状态进进度文件）；在 Grok 里改，本机沙盒不动"})
    out += [dict(m, 类="手工", 省=0, 效果="脚本不动", 改动=[]) for m in manual]
    for i, x in enumerate(out, 1):
        x["号"] = i
        x["原校验"] = {o["文件"]: sha(o["文件"]) for o in x["改动"]}
        x["怎么改回"] = "脚本不动，不用改回" if x["类"] == "手工" else "执行前自动备份；python3 瘦身.py 改回 最近一次"
    return out


def 带(d):
    return f"Claude Code {d['规则文件'] + d['技能目录'] + d['代理说明'] + d['自动记忆']} 字（规则 {d['规则文件']}、技能目录 {d['技能目录']}、代理说明 {d['代理说明']}、自动记忆 {d['自动记忆']}），WorkBuddy {d['WorkBuddy']} 字"


def show(lst):
    s = [f"# 挪移清单 · {lst['时间']}（预演：一个文件都没改）", "", f"家：{lst['家']}　每次固定带（按平台，不相加）：{带(lst['常驻'])}", ""]
    for x in lst["条"]:
        s += [f"{x['号']}. 【{x['类']}】{x['挪什么']}", f"   挪去哪：{x['挪去哪']}", f"   省多少：每次少带 {x['省']} 字　效果：{x['效果']}", f"   怎么改回：{x['怎么改回']}"]
    if not lst["条"]:
        return "\n".join(s + ["没有要挪的：没超线、没重复、没打架，现在不用瘦。"])
    return "\n".join(s + ["", "点头的几条用：python3 瘦身.py 执行 --清单 <这份清单> --条 1,2（先预演，加 --确认 才动手）"])


def plan(lst, nums):
    pick = [x for x in lst["条"] if x["号"] in nums]
    bad = sorted(set(nums) - {x["号"] for x in pick})
    if bad:
        raise SystemExit(f"清单里没有第 {bad} 条")
    hand = [x["号"] for x in pick if x["类"] == "手工"]
    if hand:
        raise SystemExit(f"第 {hand} 条是手工条，脚本不动，要主人自己改")
    changed = [f for x in pick for f, h in x["原校验"].items() if sha(f) != h]
    if changed:
        raise SystemExit("出清单以后这些文件变过，请重新出清单：\n" + "\n".join(changed))
    return pick


def run(lst, nums, store, yes):
    pick = plan(lst, nums)
    for x in pick:
        print(f"第 {x['号']} 条：{x['挪什么']}")
        for o in x["改动"]:
            f = Path(o["文件"])
            print(f"   {'会改' if f.exists() else '会新建'} {f}：{len(lines_of(f)) if f.exists() else 0} 行 → {len(o['内容'].splitlines())} 行")
    if not yes:
        print("\n（预演，一个文件都没改。主人点头后加 --确认 再跑一次）")
        return
    home = Path(lst["家"])
    before = 常驻(体检.measure(home, lst["项目"], lst["grok"], lst["预算"]))
    bdir = store / "备份" / datetime.datetime.now().strftime("%Y%m%d-%H%M%S-%f")
    (bdir / "原件").mkdir(parents=True)
    rec = {"家": str(home), "清单": lst["存在"], "条": nums, "文件": [], "新建目录": [], "已改回": False}
    for k, o in enumerate(o for x in pick for o in x["改动"]):
        f = Path(o["文件"])
        had = f.exists()
        if had:
            shutil.copy2(f, bdir / "原件" / str(k))
        d = f.parent
        while not d.exists():
            rec["新建目录"].append(str(d))
            d = d.parent
        rec["文件"].append({"文件": str(f), "原来有": had, "备份": str(k)})
    (bdir / "记录.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")  # 先记好再动手
    for x in pick:
        for o in x["改动"]:
            f = Path(o["文件"])
            f.parent.mkdir(parents=True, exist_ok=True)
            f.write_text(o["内容"], encoding="utf-8")
    for e in rec["文件"]:
        e["改后校验"] = sha(e["文件"])
    (bdir / "记录.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    after = 常驻(体检.measure(home, lst["项目"], lst["grok"], lst["预算"]))
    print(f"\n✅ 做完第 {nums} 条。备份在 {bdir}")
    cc = lambda d: d["规则文件"] + d["技能目录"] + d["代理说明"] + d["自动记忆"]
    print("前后（每次固定带的字）：" + "；".join(f"{k} {before[k]} → {after[k]}" for k in before) + f"；Claude Code 合计 {cc(before)} → {cc(after)}（WorkBuddy 各带各的，不相加）")
    print("想改回：python3 瘦身.py 改回 最近一次")


def undo(which, store, hard):
    if which == "最近一次":
        done = [d for d in sorted((store / "备份").glob("*/记录.json"), reverse=True) if not json.loads(d.read_text(encoding="utf-8"))["已改回"]]
        if not done:
            raise SystemExit("没有可改回的执行记录")
        bdir = done[0].parent
    else:
        bdir = Path(which).expanduser()
    rec = json.loads((bdir / "记录.json").read_text(encoding="utf-8"))
    if rec["已改回"]:
        raise SystemExit(f"{bdir} 已经改回过了")
    moved = [e["文件"] for e in rec["文件"] if sha(e["文件"]) != e.get("改后校验")]
    if moved and not hard:
        raise SystemExit("执行以后这些文件又被改过，直接放回会丢掉那些改动（确定要放回加 --硬）：\n" + "\n".join(moved))
    if moved:  # --硬：先把现在的样子存一份，主人后来的改动不白丢
        keep = bdir / "改回前的样子"
        keep.mkdir(exist_ok=True)
        for k, m in enumerate(moved):
            if Path(m).exists():
                shutil.copy2(m, keep / f"{k}-{Path(m).name}")
        print(f"（--硬：执行以后又改过的 {len(moved)} 个文件，现在的样子先存到 {keep}）")
    left, away = [], bdir / "改回时挪走的"  # 新建的不删、挪进备份（有的沙盒拦删除不拦挪动）；挪不动再删，删不掉照实列出来
    away.mkdir(exist_ok=True)

    def clear(p, k):
        try:
            os.rename(p, away / k)
        except OSError:
            try:
                p.rmdir() if p.is_dir() else p.unlink()
            except OSError as x:
                left.append(f"{p}（{'空文件夹' if p.is_dir() else '文件'}，运行环境不让挪也不让删：{x}）")

    for e in rec["文件"]:
        f = Path(e["文件"])
        try:
            if e["原来有"]:
                shutil.copy2(bdir / "原件" / e["备份"], f)
            elif f.exists():
                clear(f, f"文件-{e['备份']}")
        except OSError as x:
            left.append(f"{f}（{x}）")
    for k, d in enumerate(sorted(rec["新建目录"], key=len, reverse=True)):
        p = Path(d)
        if p.is_dir() and not any(p.iterdir()):
            clear(p, f"文件夹-{k}")
    bad = [e["文件"] for e in rec["文件"] if sha(e["文件"]) != (sha(bdir / "原件" / e["备份"]) if e["原来有"] else None)]
    rec["已改回"] = datetime.datetime.now().isoformat(timespec="seconds")
    rec["没回到原样"] = sorted(set(left) | set(bad))
    (bdir / "记录.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1), encoding="utf-8")
    ok = len(rec["文件"]) - len(bad)
    if rec["没回到原样"]:
        print(f"⚠️ 只改回了一部分：{ok}/{len(rec['文件'])} 个文件和执行前一字不差；这几样没回到原样：\n" + "\n".join(rec["没回到原样"])
              + f"\n备份原件还在 {bdir / '原件'}；空文件夹不影响 AI 读，可以自己删掉。记录在 {bdir}")
        return 1
    print(f"✅ 已改回：{ok} 个文件逐个核对，和执行前一字不差；新建的已拿掉；第 {rec['条']} 条撤销。记录在 {bdir}")


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("做", choices=["清单", "执行", "改回"])
    ap.add_argument("哪次", nargs="?", default="最近一次")
    ap.add_argument("--家", default="~")
    ap.add_argument("--项目", nargs="*", default=[])
    ap.add_argument("--grok", default="")
    ap.add_argument("--预算", default="")
    ap.add_argument("--存到", default="~/.yunjian/jiagou")
    ap.add_argument("--清单", default="")
    ap.add_argument("--条", default="")
    ap.add_argument("--确认", action="store_true")
    ap.add_argument("--硬", action="store_true")
    a = ap.parse_args()
    store = Path(a.存到).expanduser().resolve()
    if a.做 == "改回":
        raise SystemExit(undo(a.哪次, store, a.硬))
    if a.做 == "执行":
        if not (a.清单 and a.条):
            raise SystemExit("要给 --清单 和 --条，比如 --条 1,2")
        lst = json.loads(Path(a.清单).expanduser().read_text(encoding="utf-8"))
        return run(lst, sorted({int(n) for n in a.条.replace("，", ",").split(",") if n.strip()}), store, a.确认)
    home = Path(a.家).expanduser().resolve()
    if store == home or home in store.parents and ".yunjian" not in store.parts:
        raise SystemExit(f"--存到 {store} 在 --家 里面：清单和备份会混进被瘦身的电脑，换一个（默认 ~/.yunjian/jiagou）")
    B = json.loads(Path(a.预算).expanduser().read_text(encoding="utf-8")) if a.预算 else None
    r = 体检.measure(home, a.项目, a.grok, B)
    now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    f = store / "瘦身" / f"清单-{now}.json"
    lst = {"时间": now, "家": str(home), "项目": r["项目"], "grok": a.grok, "预算": r["预算"], "存在": str(f), "常驻": 常驻(r),
           "条": items(r, home, r["日期"])}
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(json.dumps(lst, ensure_ascii=False, indent=1), encoding="utf-8")
    print(show(lst) + f"\n清单存在 {f}")


if __name__ == "__main__":
    main()
