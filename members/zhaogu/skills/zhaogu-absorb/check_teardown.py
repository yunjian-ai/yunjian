#!/usr/bin/env python3
"""查拆解报告（格式见同目录 `报告格式.md`）：门禁有结论、结论都有三态和出处、不知道没混进结论、不跳层、
吸收清单三栏齐且每行落到位置、只学做法的标了重写、没跑过不说跑过、不把活推给主人。只用 Python 自带的库。

用法：python3 check_teardown.py <报告.md>
输出：每条问题一行「❌ [类别] 说明」，提醒一行「⚠️ …」；没有 ❌ 退出码 0。
"""
import re
import sys
from pathlib import Path

VERDICTS = ("能并", "改了能并", "只学做法", "拒绝")
WEAK = re.compile(r"感觉|猜|大概|一般都|应该是|估计|^—$|^-$|^$")
SOURCE = re.compile(r"`[^`]+`|第\s*\d+\s*(-|～|~)?\s*\d*\s*行|输出|截图|结论\s*\d")
VAGUE = re.compile(r"^(以后参考|参考|待定|看情况|再说|以后再说|—|-|无|)$")
RAN = re.compile(r"已运行|跑过了|自测通过|测试通过|已测试|已检测|已扫描")
NOT_RAN = re.compile(r"没有运行|没运行|未运行|不能执行|跑不了|没有执行|未执行")
PUSH = re.compile(r"请主人自己|主人自己去|您自己去查|您自己查|自己去查一下")


def sections(text):
    out, cur = {}, None
    for line in text.splitlines():
        m = re.match(r"##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            cur = m.group(1)
            out[cur] = []
        elif cur:
            out[cur].append(line)
    return out


def rows(lines):
    """表格的数据行（跳过表头和分隔行），每行拆成格子。"""
    table = [ln for ln in lines if ln.strip().startswith("|")]
    return [[c.strip() for c in ln.strip().strip("|").split("|")] for ln in table[2:]]


def find(secs, *names):
    for k, v in secs.items():
        if any(n in k for n in names):
            return v
    return None


def check(text):
    errs, warns = [], []
    secs = sections(text)
    head = text.split("\n## ")[0]
    gate = find(secs, "门禁")
    verdict = ""
    if gate is None:
        errs.append("[结构] 没有「门禁」一节")
    else:
        m = re.search(r"结论[:：]\s*(\S+)", "\n".join(gate))
        verdict = next((v for v in VERDICTS if m and v in m.group(1)), "")
        if not verdict:
            errs.append("[门禁] 门禁一节没有「结论：能并 / 改了能并 / 只学做法 / 拒绝」")
    if verdict == "拒绝":
        return errs, warns
    for need in ("结论", "待验证", "限制"):
        if find(secs, need) is None:
            errs.append(f"[结构] 没有「{need}」一节")

    for r in rows(find(secs, "结论") or []):
        if len(r) < 4:
            errs.append(f"[结构] 结论表这一行格子不够：{'|'.join(r)[:40]}")
            continue
        n, claim, state, src = r[0], r[1], r[2], r[3]
        if state == "不知道":
            errs.append(f"[推测进结论] 结论 {n} 标了「不知道」，应挪进待验证")
        elif state not in ("看到", "推出"):
            errs.append(f"[三态] 结论 {n} 没标看到 / 推出：「{state}」")
        elif state == "看到" and not SOURCE.search(src):
            errs.append(f"[出处] 结论 {n} 标了看到，出处没写到文件和行：「{src}」")
        elif state == "推出" and (WEAK.search(src) or not src):
            errs.append(f"[依据] 结论 {n} 标了推出，依据站不住：「{src}」")
        if state == "看到" and re.search(r"大概|可能|估计|应该是", claim):
            errs.append(f"[三态] 结论 {n} 句子里是猜测口气却标了看到")

    for r in rows(find(secs, "待验证") or []):
        if len(r) < 3 or not r[2] or VAGUE.match(r[2]):
            errs.append(f"[待验证] 待验证 {r[0] if r else '?'} 没写找了哪里")

    want = re.search(r"拆到[:：]\s*(\S+)", head)
    want = want.group(1) if want else ""
    layers = "\n".join(find(secs, "五层") or [])
    top = 5 if ("L5" in want or find(secs, "复刻规格") is not None) else 4 if "L4" in want else 0
    if top:
        missing = [f"L{i}" for i in range(1, top) if f"L{i}" not in layers]
        if missing:
            errs.append(f"[跳层] 拆到 L{top}，五层里缺 {'、'.join(missing)}")
    if top == 5 and find(secs, "复刻规格") is None:
        errs.append("[结构] 拆到 L5，没有「复刻规格」一节")
    spec = find(secs, "复刻规格")
    if spec is not None and "验收" not in "\n".join(spec):
        errs.append("[结构] 复刻规格没写验收标准")

    absorb = find(secs, "吸收清单")
    if absorb is None:
        if "吸收" in want:
            errs.append("[结构] 拆到里写了吸收清单，没有「吸收清单」一节")
    else:
        seen = set()
        for r in rows(absorb):
            if len(r) < 3:
                errs.append(f"[结构] 吸收清单这一行格子不够：{'|'.join(r)[:40]}")
                continue
            col, what, where = r[0], r[1], r[2]
            seen.add(col)
            if col not in ("强的", "不对的", "不足的"):
                errs.append(f"[四栏] 吸收清单「{col}」不是强的 / 不对的 / 不足的")
            if VAGUE.match(where) or (where.startswith("待主人定") and len(where) <= 6):
                errs.append(f"[落位] 「{what[:20]}」没落到具体位置：「{where}」")
            if verdict == "只学做法" and col == "强的" and "重写" not in "|".join(r):  # 不对的不学、不足的是自己补，不用标
                errs.append(f"[重写] 门禁是只学做法，「{what[:20]}」没标用自己的话重写")
        for col in ("强的", "不对的", "不足的"):
            if col not in seen:
                errs.append(f"[四栏] 吸收清单没有「{col}」这一栏（没有就写一行「无，查过……」）")

    body = re.sub(r"`[^`]*`", "", text)
    if RAN.search(body) and NOT_RAN.search(body):
        errs.append("[跑过] 一处说跑过、测过，另一处说没运行，对不上")
    if PUSH.search(body):
        errs.append("[推给主人] 把该自己做的推给了主人：「" + PUSH.search(body).group(0) + "」")
    if find(secs, "自查") is None:
        warns.append("没有「自查」一节：交付前写一句做完 / 做了一部分 / 没证据")
    return errs, warns


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    errs, warns = check(Path(argv[0]).read_text(encoding="utf-8"))
    for e in errs:
        print("❌", e)
    for w in warns:
        print("⚠️", w)
    print("✅ 没有问题" if not errs else f"共 {len(errs)} 处要改")
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
