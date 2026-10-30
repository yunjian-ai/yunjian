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

# ①½ 上岗包夹具（qianji-bot/check_bot.py）：合格的不许误伤；每次只埋一个错，必须报出对应类别
import shutil, tempfile  # noqa: E402
sys.path.insert(0, str(HERE.parent / "skills" / "qianji-bot"))
from check_bot import check as check_bot  # noqa: E402
GOOD = HERE / "fixtures" / "07-bot-good" / "阿禾评论助手-上岗包"
report(check_bot(GOOD) == [], "上岗包夹具 合格的不误伤", str(check_bot(GOOD)))


def sub(rel, a, b):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8").replace(a, b), encoding="utf-8")


LONG = "发笔记的流程：" + "先看数据、再选题、写正文、做封面、配图、通读、定时发、回评论、记数据。" * 16
BOT_CASES = [
    ("岗位", "只有一句指令", lambda d: (d / "岗位说明.md").write_text("你是小红书助手，帮阿禾做小红书。\n", encoding="utf-8")),
    ("岗位", "第 2 段没读进度", sub("岗位说明.md", "装齐以后每次接活（含主人说接着、到哪了）先读进度文件（~/.hepinglun/进度.md，没有就照进度模板建）、说一句停在哪，不靠聊天记录。", "")),
    ("岗位", "第 2 段没说停在哪", sub("岗位说明.md", "、说一句停在哪，不靠聊天记录", "")),
    ("岗位", "第 3 段没写先打开技能", sub("岗位说明.md", "接到活先打开对应技能照着做，短活也一样，不凭印象答。", "")),
    ("岗位", "技能没派到", sub("岗位说明.md", "要回评论用 hepinglun-reply。", "要回评论找我。")),
    ("原则", "做法超过 8 条", sub("岗位说明.md", "做法：", "做法：" + "；".join(f"规矩{i}" for i in range(9)) + "；")),
    ("流程", "干活技能没写进度", sub("skills/hepinglun-reply/SKILL.md", "1. 先读进度文件。", "1. 开始。")),
    ("流程", "技能没加前缀", lambda d: (d / "skills/hepinglun-getting-started").rename(d / "skills/getting-started")),
    ("状态", "缺进度模板", lambda d: (d / "进度模板.md").unlink()),
    ("状态", "进度模板太长", lambda d: (d / "进度模板.md").write_text((d / "进度模板.md").read_text(encoding="utf-8") + "字" * 3000, encoding="utf-8")),
    ("硬闸", "没写谁拦", sub("硬闸.md", "→ 平台先询问：「任何付款、购买、充值之前先询问。」", "→ ")),
    ("硬闸", "缺对外发这一类", sub("硬闸.md", "- 在小红书发表评论或回复 → 平台先询问：「替我在小红书发表评论、回复评论或私信之前先询问。」\n", "")),
    ("记忆", "一条超过 480 字", lambda d: (d / "记忆.md").write_text("主人档案：称呼阿禾。\n\n" + LONG + "\n", encoding="utf-8")),
    ("记忆", "规矩写进了记忆", lambda d: (d / "记忆.md").write_text("主人档案：称呼阿禾。\n\n规矩：回评论前一律先给阿禾看。\n", encoding="utf-8")),
]
for cat, why, mut in BOT_CASES:
    with tempfile.TemporaryDirectory() as t:
        dst = Path(t) / GOOD.name
        shutil.copytree(GOOD, dst)
        mut(dst)
        got = {re.match(r"\[(.+?)\]", x).group(1) for x in check_bot(dst)}
        report(cat in got, f"上岗包埋错 {why}", f"得到 {sorted(got)} 应含 {cat}")

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
    ("budget", append(SK / "qianji-capture/SKILL.md", "啊" * 33000)),  # 超过 96KB 硬上限（预算.json）,
    ("private", append(SK / "qianji-build/规则卡.md", "\n" + banned + "\n")),
    ("xref", append(SK / "qianji-ship/SKILL.md", "\n交给 qianji-nonexistent。\n")),
    ("xref", append(SK / "qianji-ship/SKILL.md", "\n见 `不存在的卡.md`。\n")),
    ("frontmatter", lambda d: (d / SK / "qianji-improve/SKILL.md").write_text("没有头部\n", encoding="utf-8")),
    ("version", lambda d: (d / "members/qianji/VERSION").write_text("v1\n")),
    ("export", lambda d: (d / "members/qianji/EXPORT.md").write_text((d / "members/qianji/EXPORT.md").read_text(encoding="utf-8").replace("另外 6 个技能", "另外 3 个技能"), encoding="utf-8")),  # 导出说明的卡外技能数没跟着技能数改
    ("instructions", edit_ins("members/qianji/profile.json", lambda t: t.replace("qianji-capture", "某技能"))),
    ("instructions", edit_ins("members/qianji/profile.json", lambda t: t.replace("不到 8 个", "不到 5 个"))),
    ("install", lambda d: (d / "members/qianji/memory.md").write_text("【安装记录】去别处装。\n", encoding="utf-8")),
    ("install", edit_ins("members/qianji/profile.json", lambda t: t.replace("装的比 qianji-v{{VERSION}} 旧", "装的不是 qianji-v{{VERSION}}"))),  # 只升不降：写成「不是这一版」会劝回旧版
    ("install", lambda d: (d / "members/qianji/memory.md").write_text((d / "members/qianji/memory.md").read_text(encoding="utf-8").replace("不装回旧版", "重装"), encoding="utf-8")),  # 只升不降：漏写「不装回旧版」
    ("install", lambda d: (d / "members/qianji/memory.md").write_text((d / "members/qianji/memory.md").read_text(encoding="utf-8").replace("\n\n", "\n"), encoding="utf-8")),  # 几条记忆并成一条：平台改不准一条里的几格
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
