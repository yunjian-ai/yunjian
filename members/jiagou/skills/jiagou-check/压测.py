"""压测（起元架构）：回答「再加 N 个 Bot／N 个技能，会不会更慢」。只把主人的配置和技能复制进临时目录，在副本里照现有的克隆出新的，
前后各体检一次，逐项报哪几样跟着涨、哪几样不涨、到没到线。主人的电脑一个字不动（只读）。
用法：python3 压测.py [--家 ~] [--项目 目录 …] [--grok 目录] [--加Bot 30] [--每Bot技能 几个，默认照现有的平均] [--加技能 0]
                     [--新技能档 开|只露名字|只给用户用] [--目录 空的临时目录，默认自动建] [--预算 自己的预算.json]
结果：<目录>/压测结果.json，屏幕上打一张前后对比表。只用标准库。"""
import argparse
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

_s = importlib.util.spec_from_file_location("体检", Path(__file__).with_name("体检.py"))
体检 = importlib.util.module_from_spec(_s)
_s.loader.exec_module(体检)
档 = {"开": "on", "只露名字": "name-only", "只给用户用": "user-invocable-only"}


def cp(src, dst):
    if src.is_dir():
        shutil.copytree(src, dst, symlinks=False, dirs_exist_ok=True)
    elif src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def copy_config(home, projects, gdir, W):
    """只复制体检要量的那几样：规则、设置、技能、记忆索引、WorkBuddy 记忆、Grok 的 Bot 档案和共用技能库。"""
    H = W / "家"
    for p in [".claude/CLAUDE.md", ".claude/settings.json", ".claude/skills", ".claude/agents", ".claude/rules", ".workbuddy/MEMORY.md"]:
        cp(home / p, H / p)
    for f in list((home / ".claude" / "projects").glob("*/memory/MEMORY.md")) + list((home / ".workbuddy").glob("user-*/MEMORY.md")):
        cp(f, H / f.relative_to(home))
    ps = []
    for k, p in enumerate(projects):
        q = W / "项目" / f"{k + 1:02d}-{p.name}"
        for n in ["CLAUDE.md", ".claude/CLAUDE.md", "CLAUDE.local.md", ".claude/settings.json", ".claude/settings.local.json", ".claude/skills", ".claude/agents"]:
            cp(p / n, q / n)
        ps.append(q)
    g = None
    if gdir:
        g = H / "box" / "agent-data"
        for f in gdir.glob("agents/*/profile.json"):
            cp(f, g / f.relative_to(gdir))
        cp(gdir / "workflows", g / "workflows")
    return H, ps, g


def clone_skills(src_dir, dst_dir, n, tag):
    """照已有技能克隆 n 个（名字换掉，说明照抄），返回新名字。没有可照的就造一个短说明的。"""
    srcs = sorted(src_dir.glob("*/SKILL.md")) if src_dir.exists() else []
    names = []
    for k in range(n):
        name = f"{tag}-{k + 1:03d}"
        if srcs:
            s = srcs[k % len(srcs)]
            t = s.read_text(encoding="utf-8", errors="replace").replace(f"name: {s.parent.name}", f"name: {name}", 1)
        else:
            t = f"---\nname: {name}\ndescription: 压测造的技能 {name}。\n---\n\n照说明做。\n"
        (dst_dir / name).mkdir(parents=True)
        (dst_dir / name / "SKILL.md").write_text(t, encoding="utf-8")
        names.append(name)
    return names


def grow(H, g, add_bots, per_bot, add_skills, state):
    if g and add_bots:
        bots = sorted(g.glob("agents/*/profile.json"))
        for k in range(add_bots):
            prof = json.loads(bots[k % len(bots)].read_text(encoding="utf-8")) if bots else {"name": "", "description": "你是压测助手。"}
            prof["name"] = f"压测助手{k + 1:03d}"
            d = g / "agents" / f"yace-{k + 1:03d}"
            d.mkdir(parents=True)
            (d / "profile.json").write_text(json.dumps(prof, ensure_ascii=False, indent=2), encoding="utf-8")
        clone_skills(g / "workflows", g / "workflows", add_bots * per_bot, "yace-shared")
    if add_skills:
        sd = H / ".claude" / "skills"
        sd.mkdir(parents=True, exist_ok=True)
        names = clone_skills(sd, sd, add_skills, "yace-skill")
        if state != "on":
            f = H / ".claude" / "settings.json"
            cfg = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
            cfg.setdefault("skillOverrides", {}).update({n: state for n in names})
            f.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def 数(r):
    cc, g = r["ClaudeCode"], r["Grok"] or {}
    bots = g.get("Bot", [])
    return {
        "Claude Code 规则文件（字）": 体检.规则常驻(cc),
        "Claude Code 技能个数": cc["技能"]["个数"],
        "Claude Code 技能目录每次带（字）": cc["技能"]["每次带的字"],
        "Claude Code 代理说明（字）": cc["代理"]["每次带的字"],
        "自动记忆读得到的（字）": max((m["字"] - m["读不到的字"] for m in cc["自动记忆"]), default=0),
        "WorkBuddy 读得到的（字）": sum(w["字"] - w["读不到的字"] for w in r["WorkBuddy"]),
        "Grok Bot 个数": len(bots),
        "Grok 单个 Bot 最大指令（字）": max((b["指令字"] for b in bots), default=0),
        "Grok 指令超线的 Bot": sum(b["超线"] for b in bots),
        "Grok 共用技能库个数": g.get("共用技能库", {}).get("个数", 0),
        "Grok 共用技能库目录（字）": g.get("共用技能库", {}).get("目录字", 0),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--家", default="~")
    ap.add_argument("--项目", nargs="*", default=[])
    ap.add_argument("--grok", default="")
    ap.add_argument("--加Bot", type=int, default=0)
    ap.add_argument("--每Bot技能", type=int, default=-1)
    ap.add_argument("--加技能", type=int, default=0)
    ap.add_argument("--新技能档", choices=list(档), default="开")
    ap.add_argument("--目录", default="")
    ap.add_argument("--预算", default="")
    a = ap.parse_args()
    if not (a.加Bot or a.加技能):
        raise SystemExit("要给 --加Bot 或 --加技能（比如 --加Bot 30）")
    home = Path(a.家).expanduser().resolve()
    W = Path(a.目录).expanduser().resolve() if a.目录 else Path(tempfile.mkdtemp(prefix="jiagou-压测-"))
    if W == home or home in W.parents:
        raise SystemExit(f"--目录 {W} 在 --家 里面，会改动主人的电脑；换一个")
    if W.exists() and any(W.iterdir()):
        raise SystemExit(f"{W} 不是空的，换个空目录（不覆盖任何东西）")
    B = json.loads(Path(a.预算).expanduser().read_text(encoding="utf-8")) if a.预算 else None
    projects = [Path(p).expanduser().resolve() for p in a.项目]
    gdir = 体检.grok_dir(home, a.grok)
    H, ps, g = copy_config(home, projects, gdir, W)
    r0 = 体检.measure(H, ps, str(g or ""), B)
    if a.加Bot and not g:
        raise SystemExit("这台电脑上没找到 Grok 沙盒，加不了 Bot（Grok 的压测要在 Grok 桌面版 Bot 里跑，或用 --grok 指目录）")
    n_bots = len(r0["Grok"]["Bot"]) if r0["Grok"] else 0
    per = a.每Bot技能 if a.每Bot技能 >= 0 else round(r0["Grok"]["共用技能库"]["个数"] / n_bots) if n_bots else 0
    grow(H, g, a.加Bot, per, a.加技能, 档[a.新技能档])
    r1 = 体检.measure(H, ps, str(g or ""), B)
    b, f = 数(r0), 数(r1)
    lim = r1["预算"]
    line = {"Grok 共用技能库个数": lim["共用技能库个数"], "Grok 单个 Bot 最大指令（字）": lim["Bot指令字"]}
    rows = []
    for k in b:
        tag = "跟着涨" if f[k] > b[k] else "不涨"
        if k in line and f[k] > line[k]:
            tag += f"，🔴 超 {line[k]}"
        rows.append({"项": k, "前": b[k], "后": f[k], "结论": tag})
    out = {"副本目录": str(W), "加了": {"Bot": a.加Bot, "每Bot带进共用技能库": per, "Claude Code 技能": a.加技能, "新技能档": a.新技能档}, "对比": rows,
           "说明": "每个 Bot 只带自己的指令＋自己的记忆＋账号共用记忆；共用技能库是全账号一份，Bot 越多越大。记忆量不到（不在沙盒里），没算进来。"}
    (W / "压测结果.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"# 压测（副本在 {W}，主人的电脑没动）\n\n加了：{a.加Bot} 个 Bot（每个往共用技能库带 {per} 个技能）、{a.加技能} 个 Claude Code 技能（{a.新技能档}）\n")
    print("| 项 | 前 | 后 | 结论 |\n|---|---|---|---|")
    print("\n".join(f"| {x['项']} | {x['前']} | {x['后']} | {x['结论']} |" for x in rows))
    print(f"\n{out['说明']}\n结果：{W / '压测结果.json'}")


if __name__ == "__main__":
    main()
