"""青鸟测试：①夹具 ②仓库检查要通过 ③反向用例（往仓库副本里埋错，检查脚本必须拦住）。
用法：python3 members/qingniao/tests/run_tests.py"""
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from check_prompt import check  # noqa: E402
from common import run_negative_cases  # noqa: E402

fails = 0


def report(ok, name, detail=""):
    global fails
    fails += not ok
    print(("✅ " if ok else "❌ ") + name + (f"  {detail}" if detail and not ok else ""))


# ① 夹具：查出的问题代码必须和 expected 完全一致（不漏报，也不误报）
for f in sorted((HERE / "fixtures").glob("*.json")):
    got = sorted({i["code"] for i in check(json.loads(f.read_text(encoding="utf-8")))})
    exp = json.loads((HERE / "expected" / f.name).read_text(encoding="utf-8"))
    report(got == sorted(exp["expect"]), f"夹具 {f.stem}", f"得到 {got} 应为 {exp['expect']}｜{exp.get('why', '')}")

# ② 仓库检查本身要通过
r = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)], capture_output=True, text=True)
report(r.returncode == 0, "仓库检查通过", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)

# ③ 反向用例：埋一个错，validate 必须报出对应类别
SK = Path("members/qingniao/skills")


def append(rel, text):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8") + text, encoding="utf-8")


banned = "".join(map(chr, (0x8BFE, 0x4EF6)))          # 名单上的词用码点拼出来，仓库里不出现明文
run_negative_cases("qingniao", [
    ("budget", append(SK / "qingniao-write/SKILL.md", "啊" * 3000)),
    ("private", append(SK / "qingniao-write/规则卡.md", "\n" + banned + "\n")),
    ("xref", append(SK / "qingniao-write/SKILL.md", "\n交给 qingniao-nonexistent。\n")),
    ("xref", append(SK / "qingniao-write/SKILL.md", "\n见 `不存在的卡.md`。\n")),
    ("frontmatter", lambda d: (d / SK / "qingniao-improve/SKILL.md").write_text("没有头部\n", encoding="utf-8")),
    ("version", lambda d: (d / "members/qingniao/VERSION").write_text("v1\n")),
], report)

print("\n" + ("全部通过" if not fails else f"{fails} 项没过"))
sys.exit(1 if fails else 0)
