"""查一个操盘项目文件夹走到哪了、哪里不对（只用 Python 自带的库）。
用法：python3 check_caopan.py <项目文件夹>
逐条打印「❌ [类别] 说明」，最后打印三行：在哪、什么过期、下一步。没问题返回 0，有问题返回 1。
类别：过期（下游比上游旧）、交接单（七栏缺栏）、验收（结论不是三选一）、关口（往下走了却没有主人本人、或经主人转达的决定记录）。
九段的固定文件名见同目录 `流程卡.md`。"""
import re
import sys
from pathlib import Path

# 段号 → (段名, 产物路径)；目录用 / 结尾
STAGES = [
    ("01", "① 需求整理", "01-需求书.md"),
    ("02", "② 定路线", "02-路线图.md"),
    ("03", "③ 蒸馏", "03-知识/"),
    ("04", "④ 立本体", "04-母体/"),
    ("05", "⑤ 规划", "05-规划清单.md"),
    ("06", "⑥ 开发", "06-成品/"),
    ("07", "⑦ 验证", "07-验收/"),
    ("08", "⑧ 封装交付", "08-交付/交付清单.md"),
    ("09", "⑨ 复盘", "09-复盘.md"),
]
# 下游 → 依赖的上游（上游改过、下游没跟着改，就是过期）
DEPENDS = {"02": ["01"], "03": ["02", "原始资料/"], "04": ["03"], "05": ["02", "03", "04"],
           "06": ["05"], "08": ["06", "07"], "09": ["08"]}
# 有了这一段的产物，说明哪个关口必须已经过了
GATES = {"02": "关口一", "03": "关口二", "06": "关口三", "09": "关口四"}
FIELDS = ("这一段", "目标", "交回格式", "边界", "用到的料", "验收标准", "结果")
VERDICTS = ("部分通过", "不通过", "通过")  # 先比长的，免得「部分通过」被当成「通过」


def mtime(p):
    """文件取修改时间；文件夹取里面最新的那个文件；不存在返回 None。"""
    if p.is_file():
        return p.stat().st_mtime
    if p.is_dir():
        ts = [f.stat().st_mtime for f in p.rglob("*") if f.is_file()]
        return max(ts) if ts else None
    return None


def path_of(root, key):
    for code, _, rel in STAGES:
        if code == key:
            return root / rel.rstrip("/")
    return root / key.rstrip("/")


def check(root):
    root, errs = Path(root), []
    have = {code: mtime(root / rel.rstrip("/")) is not None for code, _, rel in STAGES}
    # ① 过期
    stale = []
    for down, ups in DEPENDS.items():
        td = mtime(path_of(root, down))
        if td is None:
            continue
        for up in ups:
            tu = mtime(path_of(root, up))
            if tu is not None and tu > td:
                name_d = next((n for c, n, _ in STAGES if c == down), down)
                name_u = next((n for c, n, _ in STAGES if c == up), up.rstrip("/"))
                stale.append(f"{name_d} 比 {name_u} 旧")
    errs += [f"[过期] {s}，要回头重做或重新确认" for s in stale]
    # ② 交接单：任何 md 里写了「### 交接单」的，七栏都要有
    for f in sorted(root.rglob("*.md")):
        text = f.read_text(encoding="utf-8", errors="ignore")
        for block in re.split(r"(?m)^### 交接单", text)[1:]:
            block = re.split(r"(?m)^#{1,3} ", block)[0]
            miss = [k for k in FIELDS if not re.search(rf"(?m)^\s*-\s*{k}(（[^）\n]*）)?[：:]", block)]  # 栏名后可带「（收活时填）」这类说明
            if miss:
                errs.append(f"[交接单] {f.relative_to(root)} 缺栏：{'、'.join(miss)}")
    # ③ 验收：07-验收/ 里每份都要有一行「结论：通过 / 部分通过 / 不通过」
    vdir = root / "07-验收"
    if vdir.is_dir():
        for f in sorted(vdir.glob("*.md")):
            m = re.search(r"结论[：:]\s*(\S+)", f.read_text(encoding="utf-8", errors="ignore"))
            if not m or not m.group(1).startswith(VERDICTS):
                errs.append(f"[验收] {f.name} 没写结论，或结论不是「通过 / 部分通过 / 不通过」")
    # ④ 关口：往下走了，决策记录里要有主人本人的决定
    dec = root / "决策记录.md"
    dtext = dec.read_text(encoding="utf-8", errors="ignore") if dec.exists() else ""
    for code, gate in GATES.items():
        if have.get(code):
            ok = any(gate in line and ("主人本人" in line or "经主人转达" in line) for line in dtext.splitlines())  # 需求方的点头由主人转达也算
            if not ok:
                errs.append(f"[关口] 已经有 {next(n for c, n, _ in STAGES if c == code)} 的产物，但决策记录里没有「{gate}」由主人本人定的记录")
    # 三行
    done = [n for c, n, _ in STAGES if have[c]]
    where = done[-1] if done else "还没开始（没有需求书）"
    nxt = next((n for c, n, _ in STAGES if not have[c]), "全部九段都有产物")
    lines = [f"在哪：{where}（有产物不等于做完，看验收结论和签收）",
             f"什么过期：{'；'.join(stale) if stale else '没有'}",
             f"下一步：{'先处理过期的' if stale else nxt}"]
    return errs, lines


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        return 2
    errs, lines = check(sys.argv[1])
    for e in errs:
        print("❌ " + e)
    print("\n".join(lines))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
