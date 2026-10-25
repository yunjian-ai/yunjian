"""凝露测试：①夹具（check_cards 该抓的抓、不该抓的不抓）②仓库检查要通过 ③反向用例（往仓库副本里埋错，检查脚本必须拦住）
④乱输入不崩（装了 hypothesis 才跑）。
用法：python3 members/ninglu/tests/run_tests.py"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE.parent / "skills" / "ninglu-distill"))
from check_cards import check  # noqa: E402
from common import run_negative_cases  # noqa: E402

fails = 0


def report(ok, name, detail=""):
    global fails
    fails += not ok
    print(("✅ " if ok else "❌ ") + name + (f"  {detail}" if detail and not ok else ""))


# ① 夹具：查出的问题类别必须和 expected 完全一致（不漏报，也不误报）
for e in sorted((HERE / "expected").glob("*.json")):
    exp = json.loads(e.read_text(encoding="utf-8"))
    base = HERE / "fixtures" / e.stem
    src = base / exp["source"] if exp.get("source") else None
    got = sorted({re.match(r"\[(.+?)\]", x).group(1) for x in check(base / exp["path"], src)})
    report(got == sorted(exp["expect"]), f"夹具 {e.stem}", f"得到 {got} 应为 {exp['expect']}｜{exp['why']}")

# ② 仓库检查本身要通过
r = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)], capture_output=True, text=True)
report(r.returncode == 0, "仓库检查通过", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)

# ③ 反向用例：埋一个错，validate 必须报出对应类别
SK = Path("members/ninglu/skills")


def append(rel, text):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8") + text, encoding="utf-8")


def edit_ins(rel, fn):
    """改岗位说明（profile.json 的 instructions）"""
    def go(d):
        p = json.loads((d / rel).read_text(encoding="utf-8"))
        p["instructions"] = fn(p["instructions"])
        (d / rel).write_text(json.dumps(p, ensure_ascii=False, indent=2), encoding="utf-8")
    return go


banned = "".join(map(chr, (0x5DE5, 0x5177, 0x7BB1)))          # 名单上的词用码点拼出来，仓库里不出现明文
run_negative_cases("ninglu", [
    ("budget", append(SK / "ninglu-plan/SKILL.md", "啊" * 3000)),
    ("private", append(SK / "ninglu-distill/蒸馏卡.md", "\n" + banned + "\n")),
    ("private", append(SK / "ninglu-ingest/转写卡.md", "\n" + "".join(map(chr, (0x5DE5, 0x5177, 0x7BB1))) + "\n")),
    ("xref", append(SK / "ninglu-merge/SKILL.md", "\n交给 ninglu-nonexistent。\n")),
    ("xref", append(SK / "ninglu-merge/SKILL.md", "\n见 `不存在的卡.md`。\n")),
    ("frontmatter", lambda d: (d / SK / "ninglu-distill/SKILL.md").write_text("没有头部\n", encoding="utf-8")),
    ("version", lambda d: (d / "members/ninglu/VERSION").write_text("v1\n")),
    ("instructions", edit_ins("members/ninglu/profile.json", lambda t: t.replace("ninglu-ingest", "某技能"))),
    ("instructions", edit_ins("members/ninglu/profile.json", lambda t: t.replace("不到 7 个", "不到 5 个"))),
    ("install", lambda d: (d / "members/ninglu/memory.md").write_text("【安装记录】去别处装。\n", encoding="utf-8")),
    ("install", edit_ins("members/ninglu/profile.json", lambda t: t.replace("装的比 ninglu-v{{VERSION}} 旧", "装的不是 ninglu-v{{VERSION}}"))),  # 只升不降：写成「不是这一版」会劝回旧版
    ("install", lambda d: (d / "members/ninglu/memory.md").write_text((d / "members/ninglu/memory.md").read_text(encoding="utf-8").replace("不装回旧版", "重装"), encoding="utf-8")),  # 只升不降：漏写「不装回旧版」
    ("install", lambda d: (d / "members/ninglu/memory.md").write_text((d / "members/ninglu/memory.md").read_text(encoding="utf-8").replace("\n\n", "\n"), encoding="utf-8")),  # 两条记忆并成一条：平台改不准一条里的几格
    ("install", lambda d: (d / "members/ninglu/profile.json").write_text((d / "members/ninglu/profile.json").read_text(encoding="utf-8").replace("安装状态", "安装记录"), encoding="utf-8")),  # 岗位说明还写旧的「安装记录」
    ("install", lambda d: (d / "members/ninglu/skills/ninglu-update/SKILL.md").write_text((d / "members/ninglu/skills/ninglu-update/SKILL.md").read_text(encoding="utf-8").replace("整条删掉", "改一下"), encoding="utf-8")),  # 更新技能没写整条换新
    ("rehearsal", lambda d: (d / SK / "ninglu-getting-started/SKILL.md").write_text((d / SK / "ninglu-getting-started/SKILL.md").read_text(encoding="utf-8").replace("## 演练模式", "## 试一试"), encoding="utf-8")),
    ("private", append(SK / "ninglu-distill/check_cards.py", "\n# " + banned + "\n")),
    ("greeting", lambda d: (d / "members/ninglu/memory.md").write_text((d / "members/ninglu/memory.md").read_text(encoding="utf-8").replace("您好，欢迎来到云间。", "你好。"), encoding="utf-8")),
    ("private", append(Path("members/ninglu/examples/01-第一次见面-阿茶.md"), "\n" + banned + "\n")),
], report)

# ④ 乱输入不崩：随便什么文字喂进去，只能报问题，不能抛异常
try:
    from hypothesis import given, settings, strategies as st
except ImportError:
    print("（没装 hypothesis，跳过④）")
else:
    pieces = st.sampled_from(["# 标题\n", "> 主题\n", "- 类型：规则\n", "- 可信度：原文\n", "- 出处：第 3 页\n",
                              "- 原话：「」\n", "- 关系：属于 → \n", "- 关系：独立\n", "## 正文\n", "```\n", "；→←\n"])

    @settings(max_examples=300, deadline=None, database=None)
    @given(st.lists(st.one_of(pieces, st.text(max_size=40)), max_size=30))
    def no_crash(parts):
        with tempfile.TemporaryDirectory() as t:
            f = Path(t) / "卡.md"
            f.write_text("".join(parts), encoding="utf-8")
            assert isinstance(check(f), list) and isinstance(check(f, f), list)
    try:
        no_crash()
        report(True, "乱输入 300 例不崩")
    except Exception as ex:  # noqa: BLE001
        report(False, "乱输入不崩", repr(ex)[:200])

print("\n" + ("全部通过" if not fails else f"{fails} 项没过"))
sys.exit(1 if fails else 0)
