"""检查一个 Bot 上岗包合不合五层上岗（只用 Python 自带的库；规矩见同目录 上岗包卡.md）。
用法：python3 check_bot.py <上岗包文件夹>
没问题打印「✅ 通过」，返回 0；有问题逐条打印「❌ [类别] 说明」，返回 1。"""
import re
import sys
from pathlib import Path

MAX_RULES, MAX_STATE, MAX_MEMORY, MAX_PLATFORM_RULE = 8, 3000, 480, 1000
MUST_GATE = {"花钱": ("付款", "花钱", "支付", "购买"), "对外发": ("发送", "发帖", "发表", "发布", "发消息", "私信", "外发"),
             "删除": ("删除", "删掉", "覆盖"), "改账户": ("账户", "账号", "密码", "权限")}
NOT_WORK = ("install", "update", "getting-started")


def check(folder):
    d, errs = Path(folder), []
    ins_f = d / "岗位说明.md"
    ins = ins_f.read_text(encoding="utf-8").strip() if ins_f.exists() else ""
    paras = [p for p in re.split(r"\n\s*\n", ins) if p.strip()]
    skills = sorted(p.parent.name for p in (d / "skills").glob("*/SKILL.md"))
    if not ins:
        errs.append("[岗位] 缺 岗位说明.md")
    else:
        if not ins.startswith("你是"):
            errs.append("[岗位] 岗位说明要以「你是」开头")
        if len(paras) != 5:
            errs.append(f"[岗位] 岗位说明要正好五段（现在 {len(paras)} 段，段之间空一行）")
        if len(paras) < 2 or "先读进度文件" not in paras[1] or "说一句停在哪" not in paras[1]:
            errs.append("[岗位] 第 2 段没写「每次接活（含主人说接着、到哪了）先读进度文件、说一句停在哪」")
        if len(paras) < 3 or "先打开对应技能" not in paras[2]:
            errs.append("[岗位] 第 3 段没写「接到活先打开对应技能照着做」")
        for s in skills:
            if not s.endswith(NOT_WORK) and s not in ins:
                errs.append(f"[岗位] 技能 {s} 没派到")
        rules = next((p for p in paras if p.strip().startswith("做法：")), None)
        if rules is None:
            errs.append("[原则] 没有「做法：」一段")
        else:
            n = len([x for x in re.split(r"[；。]", rules.strip()[3:]) if x.strip()])
            if n > MAX_RULES:
                errs.append(f"[原则] 「做法：」{n} 条，最多 {MAX_RULES} 条（某件活才用的挪进技能）")
    for s in skills:
        if s in ("getting-started", "install", "update"):
            errs.append(f"[流程] 技能 {s} 没加前缀，共用技能库里会和别的 Bot 重名")
        if not s.endswith(NOT_WORK):
            text = (d / "skills" / s / "SKILL.md").read_text(encoding="utf-8")
            for need in ("先读进度", "写进度"):  # 「不写进度」不算写了
                if not re.search(rf"(?<!不){need}", text):
                    errs.append(f"[流程] {s} 没写「{need}」")
    tpl = d / "进度模板.md"
    if not tpl.exists():
        errs.append("[状态] 缺 进度模板.md")
    else:
        t = tpl.read_text(encoding="utf-8")
        if len(t) > MAX_STATE:
            errs.append(f"[状态] 进度模板 {len(t)} 字，超过 {MAX_STATE}")
        for block in ("现在做到哪", "下一步", "等主人定", "纠正"):
            if block not in t:
                errs.append(f"[状态] 进度模板缺「{block}」一块")
    gate = d / "硬闸.md"
    rows = [ln.strip()[2:] for ln in gate.read_text(encoding="utf-8").splitlines() if ln.strip().startswith("- ")] if gate.exists() else []
    if not rows:
        errs.append("[硬闸] 缺 硬闸.md，或里面一条都没有")
    for r in rows:
        who = r.split("→", 1)[1].strip() if "→" in r else ""
        if not who:
            errs.append(f"[硬闸] 「{r[:15]}…」没写谁拦（格式：不许做的事 → 谁拦）")
        for q in re.findall(r"「([^」]+)」", who):
            if len(q) > MAX_PLATFORM_RULE:
                errs.append(f"[硬闸] 平台规则原文 {len(q)} 字，一条最多 {MAX_PLATFORM_RULE}")
    for kind, words in MUST_GATE.items():
        if rows and not any(w in r for r in rows for w in words):
            errs.append(f"[硬闸] 没有「{kind}」这一类（花钱、对外发、删除、改账户四类都要有）")
    mem = d / "记忆.md"
    if mem.exists():
        for e in [x.strip() for x in re.split(r"\n\s*\n", mem.read_text(encoding="utf-8")) if x.strip()]:
            if len(e) > MAX_MEMORY:
                errs.append(f"[记忆] 「{e[:12]}…」{len(e)} 字，一条超过 {MAX_MEMORY} 平台会截掉后半截")
            if re.search(r"规矩|做法：|一律|必须", e):
                errs.append(f"[记忆] 「{e[:12]}…」像是规矩，规矩放岗位说明「做法」或技能，不进记忆")
    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    errs = check(sys.argv[1])
    print("\n".join("❌ " + e for e in errs) if errs else "✅ 通过")
    sys.exit(1 if errs else 0)
