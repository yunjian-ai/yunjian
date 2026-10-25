"""经纬测试：①夹具（check_mother 该抓的抓、不该抓的不抓）②仓库检查要通过 ③反向用例（往仓库副本里埋错，检查脚本必须拦住）
④乱输入不崩（装了 hypothesis 才跑）。
用法：python3 members/jingwei/tests/run_tests.py"""
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE.parent / "skills" / "jingwei-store"))
from check_mother import check  # noqa: E402
from common import run_negative_cases  # noqa: E402

fails = 0


def report(ok, name, detail=""):
    global fails
    fails += not ok
    print(("✅ " if ok else "❌ ") + name + (f"  {detail}" if detail and not ok else ""))


# ① 夹具：查出的问题类别必须和 expected 完全一致（不漏报，也不误报）
for e in sorted((HERE / "expected").glob("*.json")):
    exp = json.loads(e.read_text(encoding="utf-8"))
    errs, _, _ = check(HERE / "fixtures" / e.stem / exp["path"])
    got = sorted({re.match(r"\[(.+?)\]", x).group(1) for x in errs})
    report(got == sorted(exp["expect"]), f"夹具 {e.stem}", f"得到 {got} 应为 {exp['expect']}｜{exp['why']}")

# ①½ --map 能把关系总表写进地图
with tempfile.TemporaryDirectory() as t:
    d = Path(t) / "母体"
    shutil.copytree(HERE / "fixtures" / "06-合格的一套", d)
    r = subprocess.run([sys.executable, str(HERE.parent / "skills" / "jingwei-store" / "check_mother.py"), str(d), "--map"],
                       capture_output=True, text=True)
    m = (d / "05-地图.md").read_text(encoding="utf-8")
    report(r.returncode == 0 and "| 茶品 | 来自 | 货源 |" in m, "--map 写出关系总表", r.stdout[-200:])

# ② 仓库检查本身要通过
r = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)], capture_output=True, text=True)
report(r.returncode == 0, "仓库检查通过", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)

# ③ 反向用例：埋一个错，validate 必须报出对应类别
SK = Path("members/jingwei/skills")


def append(rel, text):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8") + text, encoding="utf-8")


def edit_ins(rel, fn):
    """改岗位说明（profile.json 的 instructions）"""
    def go(d):
        p = json.loads((d / rel).read_text(encoding="utf-8"))
        p["instructions"] = fn(p["instructions"])
        (d / rel).write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return go


def edit(rel, a, b):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8").replace(a, b), encoding="utf-8")


banned = "".join(map(chr, (0x5DE5, 0x5177, 0x7BB1)))          # 名单上的词用码点拼出来，仓库里不出现明文
run_negative_cases("jingwei", [
    ("budget", append(SK / "jingwei-frame/SKILL.md", "啊" * 3000)),
    ("private", append(SK / "jingwei-frame/母体卡.md", "\n" + banned + "\n")),
    ("xref", append(SK / "jingwei-weave/SKILL.md", "\n交给 jingwei-nonexistent。\n")),
    ("xref", append(SK / "jingwei-store/SKILL.md", "\n见 `不存在的卡.md`。\n")),
    ("frontmatter", lambda d: (d / SK / "jingwei-weave/SKILL.md").write_text("没有头部\n", encoding="utf-8")),
    ("version", lambda d: (d / "members/jingwei/VERSION").write_text("v1\n")),
    ("instructions", edit_ins("members/jingwei/profile.json", lambda t: t.replace("jingwei-weave", "某技能"))),
    ("instructions", edit_ins("members/jingwei/profile.json", lambda t: t.replace("不到 7 个", "不到 5 个"))),
    ("install", lambda d: (d / "members/jingwei/memory.md").write_text("【安装记录】去别处装。\n", encoding="utf-8")),
    ("install", edit_ins("members/jingwei/profile.json", lambda t: t.replace("装的比 jingwei-v{{VERSION}} 旧", "装的不是 jingwei-v{{VERSION}}"))),  # 只升不降
    ("install", edit("members/jingwei/memory.md", "不装回旧版", "重装")),  # 只升不降：漏写「不装回旧版」
    ("install", lambda d: (d / "members/jingwei/memory.md").write_text((d / "members/jingwei/memory.md").read_text(encoding="utf-8").replace("\n\n", "\n"), encoding="utf-8")),  # 两条记忆并成一条：平台改不准一条里的几格
    ("install", lambda d: (d / "members/jingwei/profile.json").write_text((d / "members/jingwei/profile.json").read_text(encoding="utf-8").replace("安装状态", "安装记录"), encoding="utf-8")),  # 岗位说明还写旧的「安装记录」
    ("install", lambda d: (d / "members/jingwei/skills/jingwei-update/SKILL.md").write_text((d / "members/jingwei/skills/jingwei-update/SKILL.md").read_text(encoding="utf-8").replace("整条删掉", "改一下"), encoding="utf-8")),  # 更新技能没写整条换新
    ("rehearsal", edit(SK / "jingwei-getting-started/SKILL.md", "## 演练模式", "## 试一试")),
    ("private", append(SK / "jingwei-store/check_mother.py", "\n# " + banned + "\n")),
    ("greeting", edit("members/jingwei/memory.md", "您好，欢迎来到云间。", "你好。")),
    ("private", append(Path("members/jingwei/examples/01-第一次见面-阿茶.md"), "\n" + banned + "\n")),
], report)

# ④ 乱输入不崩：往母体文件夹里随便写，只能报问题，不能抛异常
try:
    from hypothesis import given, settings, strategies as st
except ImportError:
    print("（没装 hypothesis，跳过④）")
else:
    pieces = st.sampled_from(["## 根\n", "## 关系\n", "- 购买 → [[茶品]]\n", "- 有关 → [[x]]\n", "| 维度 | 定义 | 状态 |\n",
                              "|---|---|---|\n", "| 客户 | 人 | 有 |\n", "---\n维度: 客户\n别名: [a, b]\n---\n", "## 证据\n",
                              "- K1｜第 3 段｜「原话」\n", "## 状态流转\n| 从 | 到 |\n| a | b |\n", "```\n", "→[[]]｜\n"])
    files = st.sampled_from(["00-根.md", "01-规则.md", "东西/茶品.md", "东西/x.md", "03-空枝和缺口.md", "05-地图.md"])

    @settings(max_examples=300, deadline=None, database=None)
    @given(st.lists(st.tuples(files, st.lists(st.one_of(pieces, st.text(max_size=30)), max_size=12)), max_size=8))
    def no_crash(spec):
        with tempfile.TemporaryDirectory() as t:
            for name, parts in spec:
                f = Path(t) / name
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text("".join(parts), encoding="utf-8")
            errs, warns, edges = check(t)
            assert isinstance(errs, list) and isinstance(warns, list) and isinstance(edges, list)
    try:
        no_crash()
        report(True, "乱输入 300 例不崩")
    except Exception as ex:  # noqa: BLE001
        report(False, "乱输入不崩", repr(ex)[:200])

print("\n" + ("全部通过" if not fails else f"{fails} 项没过"))
sys.exit(1 if fails else 0)
