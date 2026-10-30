"""起元操盘测试：①夹具（check_caopan 该抓的抓、不该抓的不抓）②仓库检查要通过 ③反向用例（往仓库副本里埋错，检查脚本必须拦住）④乱输入不崩（装了 hypothesis 才跑）。
用法：python3 members/caopan/tests/run_tests.py"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE.parent / "skills" / "caopan-start"))
from check_caopan import check  # noqa: E402
from common import run_negative_cases  # noqa: E402

fails = 0


def report(ok, name, detail=""):
    global fails
    fails += not ok
    print(("✅ " if ok else "❌ ") + name + (f"  {detail}" if detail and not ok else ""))


# ① 夹具：Git 不保存修改时间，先复制到临时目录、按 mtimes.json 的先后设好时间，再查
for e in sorted((HERE / "expected").glob("*.json")):
    exp = json.loads(e.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory() as t:
        d = Path(t) / e.stem
        shutil.copytree(HERE / "fixtures" / e.stem, d)
        order = json.loads((d / "mtimes.json").read_text(encoding="utf-8"))
        (d / "mtimes.json").unlink()
        for i, rel in enumerate(order):
            os.utime(d / rel, (1_700_000_000 + i * 60, 1_700_000_000 + i * 60))
        errs, lines = check(d)
        got = sorted({re.match(r"\[(.+?)\]", x).group(1) for x in errs})
        report(got == sorted(exp["expect"]) and len(lines) == 3, f"夹具 {e.stem}", f"得到 {got} 应为 {exp['expect']}｜{exp['why']}")

# ② 仓库检查本身要通过
r = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)], capture_output=True, text=True)
report(r.returncode == 0, "仓库检查通过", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)

# ③ 反向用例：埋一个错，validate 必须报出对应类别
SK = Path("members/caopan/skills")


def append(rel, text):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8") + text, encoding="utf-8")


def edit(rel, old, new):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


def edit_ins(rel, fn):
    def go(d):
        p = json.loads((d / rel).read_text(encoding="utf-8"))
        p["instructions"] = fn(p["instructions"])
        (d / rel).write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return go


banned = "".join(map(chr, (0x5DE5, 0x5177, 0x7BB1)))          # 名单上的词用码点拼出来，仓库里不出现明文
run_negative_cases("caopan", [
    ("budget", append(SK / "caopan-relay/SKILL.md", "啊" * 33000)),  # 超过 96KB 硬上限（预算.json）,
    ("private", append(SK / "caopan-start/规则卡.md", "\n" + banned + "\n")),
    ("private", append(SK / "caopan-start/check_caopan.py", "\n# " + banned + "\n")),
    ("xref", append(SK / "caopan-route/SKILL.md", "\n交给 caopan-nonexistent。\n")),
    ("xref", append(SK / "caopan-gate/SKILL.md", "\n见 `不存在的卡.md`。\n")),
    ("frontmatter", lambda d: (d / SK / "caopan-wrap/SKILL.md").write_text("没有头部\n", encoding="utf-8")),
    ("instructions", edit_ins("members/caopan/profile.json", lambda t: t.replace("caopan-relay", "某技能"))),
    ("instructions", edit_ins("members/caopan/profile.json", lambda t: t.replace("不到 12 个", "不到 7 个"))),
    ("install", edit("members/caopan/memory.md", "不装回旧版", "重装")),
    ("rehearsal", edit(SK / "caopan-getting-started/SKILL.md", "## 演练模式", "## 试一试")),
    ("greeting", edit("members/caopan/memory.md", "您好，欢迎来到云间。", "你好。")),
], report)

# ④ 乱输入不崩：往项目文件夹里随便写，只能报问题，不能抛异常
try:
    from hypothesis import given, settings, strategies as st
except ImportError:
    print("（没装 hypothesis，跳过④）")
else:
    pieces = st.sampled_from(["### 交接单 · 第 3 段\n", "- 这一段：③\n", "- 边界：只蒸\n", "- 结果：通过\n", "结论：通过\n",
                              "结论：部分通过\n", "结论：\n", "关口二｜主人本人\n", "关口一\n", "## 标题\n", "｜｜\n"])
    files = st.sampled_from(["01-需求书.md", "02-路线图.md", "03-知识/卡.md", "04-母体/根.md", "05-规划清单.md", "06-成品/a.md",
                             "07-验收/x.md", "08-交付/交付清单.md", "09-复盘.md", "决策记录.md", "交接单.md", "原始资料/a.txt"])

    @settings(max_examples=300, deadline=None, database=None)
    @given(st.lists(st.tuples(files, st.lists(st.one_of(pieces, st.text(max_size=30)), max_size=10)), max_size=10))
    def no_crash(spec):
        with tempfile.TemporaryDirectory() as t:
            for name, parts in spec:
                f = Path(t) / name
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text("".join(parts), encoding="utf-8")
            errs, lines = check(t)
            assert isinstance(errs, list) and len(lines) == 3
    try:
        no_crash()
        report(True, "乱输入 300 例不崩")
    except Exception as ex:  # noqa: BLE001
        report(False, "乱输入不崩", repr(ex)[:200])

print("\n" + ("全部通过" if not fails else f"{fails} 项没过"))
sys.exit(1 if fails else 0)
