"""千机测试：①夹具（check_skill 该抓的抓、不该抓的不抓）②仓库检查要通过 ③反向用例（往仓库副本里埋错，检查脚本必须拦住）。
用法：python3 members/qianji/tests/run_tests.py"""
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(HERE.parent / "skills" / "qianji-build"))
from check_skill import check  # noqa: E402
from common import run_negative_cases  # noqa: E402

fails = 0


def report(ok, name, detail=""):
    global fails
    fails += not ok
    print(("✅ " if ok else "❌ ") + name + (f"  {detail}" if detail and not ok else ""))


# ① 夹具：查出的问题类别必须和 expected 完全一致（不漏报，也不误报）
for e in sorted((HERE / "expected").glob("*.json")):
    exp = json.loads(e.read_text(encoding="utf-8"))
    got = sorted({re.match(r"\[(.+?)\]", x).group(1) for x in check(HERE / "fixtures" / e.stem / exp["skill"])})
    report(got == sorted(exp["expect"]), f"夹具 {e.stem}", f"得到 {got} 应为 {exp['expect']}｜{exp['why']}")

# ② 仓库检查本身要通过
r = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)], capture_output=True, text=True)
report(r.returncode == 0, "仓库检查通过", r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr)

# ③ 反向用例：埋一个错，validate 必须报出对应类别
SK = Path("members/qianji/skills")


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
run_negative_cases("qianji", [
    ("budget", append(SK / "qianji-capture/SKILL.md", "啊" * 3000)),
    ("private", append(SK / "qianji-build/规则卡.md", "\n" + banned + "\n")),
    ("xref", append(SK / "qianji-ship/SKILL.md", "\n交给 qianji-nonexistent。\n")),
    ("xref", append(SK / "qianji-ship/SKILL.md", "\n见 `不存在的卡.md`。\n")),
    ("frontmatter", lambda d: (d / SK / "qianji-improve/SKILL.md").write_text("没有头部\n", encoding="utf-8")),
    ("version", lambda d: (d / "members/qianji/VERSION").write_text("v1\n")),
    ("instructions", edit_ins("members/qianji/profile.json", lambda t: t.replace("qianji-capture", "某技能"))),
    ("instructions", edit_ins("members/qianji/profile.json", lambda t: t.replace("不到 7 个", "不到 5 个"))),
    ("install", lambda d: (d / "members/qianji/memory.md").write_text("【安装记录】去别处装。\n", encoding="utf-8")),
    ("install", edit_ins("members/qianji/profile.json", lambda t: t.replace("装的比 qianji-v{{VERSION}} 旧", "装的不是 qianji-v{{VERSION}}"))),  # 只升不降：写成「不是这一版」会劝回旧版
    ("install", lambda d: (d / "members/qianji/memory.md").write_text((d / "members/qianji/memory.md").read_text(encoding="utf-8").replace("不装回旧版", "重装"), encoding="utf-8")),  # 只升不降：漏写「不装回旧版」
    ("install", lambda d: (d / "members/qianji/memory.md").write_text((d / "members/qianji/memory.md").read_text(encoding="utf-8").replace("\n\n", "\n"), encoding="utf-8")),  # 两条记忆并成一条：平台改不准一条里的几格
    ("install", lambda d: (d / "members/qianji/profile.json").write_text((d / "members/qianji/profile.json").read_text(encoding="utf-8").replace("安装状态", "安装记录"), encoding="utf-8")),  # 岗位说明还写旧的「安装记录」
    ("install", lambda d: (d / "members/qianji/skills/qianji-update/SKILL.md").write_text((d / "members/qianji/skills/qianji-update/SKILL.md").read_text(encoding="utf-8").replace("整条删掉", "改一下"), encoding="utf-8")),  # 更新技能没写整条换新
    ("rehearsal", lambda d: (d / SK / "qianji-getting-started/SKILL.md").write_text((d / SK / "qianji-getting-started/SKILL.md").read_text(encoding="utf-8").replace("## 演练模式", "## 试一试"), encoding="utf-8")),
    # 发布会挑走、以前 validate 却不扫的地方：夹具说明（.json）、技能里的脚本（.py）、改名后公开的设计摘要
    ("private", lambda d: (d / "members/qianji/tests/expected/01-version-top.json").write_text(
        json.dumps({"skill": "topic-check", "expect": ["头信息"], "why": banned + "式写法"}, ensure_ascii=False), encoding="utf-8")),
    ("private", append(SK / "qianji-build/check_skill.py", "\n# " + banned + "\n")),
    ("private", append(Path("发布素材/qianji-DESIGN.md"), "\n" + banned + "\n")),
    # 名单上的另一个词（同样用码点拼），埋进示例，validate 也要拦（考试材料是原始资料，不扫）
    ("private", append(Path("members/qianji/examples/01-第一次见面-阿茶.md"), "\n" + "".join(map(chr, (0x5DE5, 0x5177, 0x7BB1))) + "\n")),
    # 禁用词.txt 加了词、哈希名单没跟上：两份名单不一致要报
    ("private", append(Path("tools/禁用词.txt"), "\n新加的词\n")),
], report)

print("\n" + ("全部通过" if not fails else f"{fails} 项没过"))
sys.exit(1 if fails else 0)
