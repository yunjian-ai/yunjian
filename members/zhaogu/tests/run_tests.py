"""照骨测试：①夹具（check_teardown 该抓的抓、不该抓的不抓）②勘察.py 实测（可疑的行、许可证线索、存档一致、标截断、不运行目标）
③仓库检查要通过 ④反向用例（往仓库副本里埋错，检查脚本必须拦住）⑤乱输入不崩（装了 hypothesis 才跑）。
用法：python3 members/zhaogu/tests/run_tests.py"""
import json
import re
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
SK = HERE.parent / "skills"
sys.path[:0] = [str(ROOT / "tools"), str(SK / "zhaogu-absorb"), str(SK / "zhaogu-scan")]
from check_teardown import check  # noqa: E402
from common import run_negative_cases  # noqa: E402
import 勘察  # noqa: E402

fails = 0


def report(ok, name, detail=""):
    global fails
    fails += not ok
    print(("✅ " if ok else "❌ ") + name + (f"  {detail}" if detail and not ok else ""))


# ① 夹具：查出的问题类别必须和 expected 完全一致（不漏报，也不误报）
for e in sorted((HERE / "expected").glob("*.json")):
    exp = json.loads(e.read_text(encoding="utf-8"))
    errs, _ = check((HERE / "fixtures" / f"{e.stem}.md").read_text(encoding="utf-8"))
    got = sorted({re.match(r"\[(.+?)\]", x).group(1) for x in errs})
    report(got == sorted(exp["expect"]), f"夹具 {e.stem}", f"得到 {got} 应为 {exp['expect']}｜{exp['why']}")

# ② 勘察.py 实测：用考试材料
M = HERE / "材料"
r = 勘察.survey(M / "12-来路不明的Skill")
cats = {c for c, xs in r["可疑"].items() if xs}
report({"外发", "读私密位置", "让 AI 绕过主人"} <= cats, "勘察：来路不明的 Skill 抓到外发、读私密位置、绕过主人", str(cats))
report(any("setup.sh 第 5 行" in x for x in r["可疑"]["外发"]), "勘察：外发写到文件和行")
r = 勘察.survey(M / "01-开源标题Skill")
report(not any(r["可疑"].values()), "勘察：干净的 MIT Skill 不误报可疑", str(r["可疑"]))
report(any("LICENSE 第一行：MIT License" in x for x in r["许可证线索"]), "勘察：认出 LICENSE 第一行")
r = 勘察.survey(M / "04-许可证对不上")
report(len(r["许可证线索"]) == 2, "勘察：两处许可证说法都列出来", str(r["许可证线索"]))
r = 勘察.survey(M / "02-没许可证的Bot")
report(r["许可证线索"][0].startswith("没找到"), "勘察：没许可证写「没找到」和查了哪里")
with tempfile.TemporaryDirectory() as t:
    ok = 勘察.archive(M / "02-没许可证的Bot", Path(t) / "存档")
    same = all((Path(t) / "存档" / "原件" / f.name).read_bytes() == f.read_bytes() for f in (M / "02-没许可证的Bot").iterdir())
    lst = (Path(t) / "存档" / "存档清单.md").read_text(encoding="utf-8")
    report(ok and same, "存档：一字不改，校验码一致")
    report("| `记忆.md` |" in lst and "疑似截断（第 2 行）" in lst.split("`记忆.md`")[1].split("\n")[0], "存档：标出记忆第 2 行疑似截断")
    report("疑似截断（第 10 行）" in lst.split("`技能-评论回复.md`")[1].split("\n")[0], "存档：标出评论回复第 10 行疑似截断")
with tempfile.TemporaryDirectory() as t:  # 不该误伤：真拆 REA、Leo 时误报过的写法
    d = Path(t) / "目标"
    d.mkdir()
    (d / "a.py").write_text("import subprocess\n# build SkillHub upload package\n", encoding="utf-8")
    (d / "b.md").write_text("9. 有界能力报上限：截断必须显式标注\n失败、truncated 不许合并成通过\n", encoding="utf-8")
    r = 勘察.survey(d)
    report(not any(r["可疑"].values()), "勘察：import subprocess、注释里的 upload 不误报", str(r["可疑"]))
    勘察.archive(d, Path(t) / "存档")
    report("疑似截断" not in (Path(t) / "存档" / "存档清单.md").read_text(encoding="utf-8"), "存档：正文讲到「截断」不误标")
with tempfile.TemporaryDirectory() as t:  # 不运行目标：埋一个会留痕的脚本，勘察完痕迹不该出现
    bait = Path(t) / "目标"
    bait.mkdir()
    flag = Path(t) / "被运行了"
    (bait / "setup.sh").write_text(f"#!/bin/bash\ntouch '{flag}'\n", encoding="utf-8")
    (bait / "setup.sh").chmod(0o755)
    (bait / "run.py").write_text(f"open(r'{flag}', 'w')\n", encoding="utf-8")
    勘察.survey(bait)
    勘察.archive(bait, Path(t) / "存档")
    report(not flag.exists(), "勘察和存档都不运行目标里的脚本")

# ③ 仓库检查本身要通过
import subprocess  # noqa: E402

done = subprocess.run([sys.executable, str(ROOT / "tools" / "validate.py"), str(ROOT)], capture_output=True, text=True)
report(done.returncode == 0, "仓库检查通过", done.stdout.strip().splitlines()[-1] if done.stdout.strip() else done.stderr)

# ④ 反向用例：埋一个错，validate 必须报出对应类别
SKR = Path("members/zhaogu/skills")


def append(rel, text):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8") + text, encoding="utf-8")


def edit(rel, a, b):
    return lambda d: (d / rel).write_text((d / rel).read_text(encoding="utf-8").replace(a, b), encoding="utf-8")


def edit_ins(fn):
    def go(d):
        p = d / "members/zhaogu/profile.json"
        j = json.loads(p.read_text(encoding="utf-8"))
        j["instructions"] = fn(j["instructions"])
        p.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    return go


banned = "".join(map(chr, (0x5DE5, 0x5177, 0x7BB1)))          # 名单上的词用码点拼出来，仓库里不出现明文
run_negative_cases("zhaogu", [
    ("budget", append(SKR / "zhaogu-scan/SKILL.md", "啊" * 3000)),
    ("private", append(SKR / "zhaogu-scan/许可证卡.md", "\n" + banned + "\n")),
    ("private", append(SKR / "zhaogu-scan/勘察.py", "\n# " + banned + "\n")),
    ("xref", append(SKR / "zhaogu-layers/SKILL.md", "\n交给 zhaogu-nonexistent。\n")),
    ("xref", append(SKR / "zhaogu-absorb/SKILL.md", "\n见 `不存在的卡.md`。\n")),
    ("frontmatter", lambda d: (d / SKR / "zhaogu-library/SKILL.md").write_text("没有头部\n", encoding="utf-8")),
    ("version", lambda d: (d / "members/zhaogu/VERSION").write_text("v1\n")),
    ("instructions", edit_ins(lambda t: t.replace("zhaogu-absorb", "某技能"))),
    ("instructions", edit_ins(lambda t: t.replace("不到 7 个", "不到 5 个"))),
    ("install", edit("members/zhaogu/memory.md", "不装回旧版", "重装")),
    ("rehearsal", edit(SKR / "zhaogu-getting-started/SKILL.md", "## 演练模式", "## 试一试")),
    ("greeting", edit("members/zhaogu/memory.md", "您好，欢迎来到云间。", "你好。")),
], report)

# ⑤ 乱输入不崩
try:
    from hypothesis import given, settings, strategies as st
except ImportError:
    print("（没装 hypothesis，跳过⑤）")
else:
    pieces = st.sampled_from(["## 门禁\n", "结论：能并\n", "结论：只学做法\n", "## 结论\n", "## 待验证\n", "## 限制\n",
                              "## 吸收清单\n", "## 五层\n", "## 复刻规格\n", "拆到：L5\n", "| # | a | b | c |\n", "|---|---|---|---|\n",
                              "| 1 | x | 看到 | `a.md` 第 1 行 |\n", "| 强的 | x | 以后参考 |\n", "| 1 | x |\n", "已运行\n", "没运行\n", "|\n"])

    @settings(max_examples=300, deadline=None, database=None)
    @given(st.lists(st.one_of(pieces, st.text(max_size=30)), max_size=25))
    def no_crash(parts):
        errs, warns = check("".join(parts))
        assert isinstance(errs, list) and isinstance(warns, list)

    @settings(max_examples=60, deadline=None, database=None)
    @given(st.lists(st.tuples(st.sampled_from(["LICENSE", "SKILL.md", "a.py", "记忆.md", "x.bin"]), st.binary(max_size=300)), max_size=5))
    def survey_no_crash(spec):
        with tempfile.TemporaryDirectory() as t:
            for name, data in spec:
                (Path(t) / name).write_bytes(data)
            勘察.show(勘察.survey(t))
    try:
        no_crash()
        survey_no_crash()
        report(True, "乱输入不崩（报告 300 例、勘察 60 例）")
    except Exception as ex:  # noqa: BLE001
        report(False, "乱输入不崩", repr(ex)[:200])

print("\n" + ("全部通过" if not fails else f"{fails} 项没过"))
sys.exit(1 if fails else 0)
