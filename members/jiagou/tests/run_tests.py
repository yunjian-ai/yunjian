"""起元架构测试：拿 材料/01-假电脑 的副本查①体检数字和 expected/体检.json 一致、只读；
②瘦身预演不动文件、只动点了头的几条、改回后校验码一模一样、文件变过就拒绝；③压测只在副本里做；④协作单子缺栏要拦；⑤仓库检查要通过。
用法：python3 members/jiagou/tests/run_tests.py   只用标准库。"""
import contextlib
import hashlib
import io
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

EXAM = Path(__file__).resolve().parent
HERE = EXAM.parent / "skills" / "jiagou-check"


def load(name):
    s = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


def tree(d):
    """整棵目录的校验码：文件内容＋目录结构。"""
    h = hashlib.sha256()
    for p in sorted(d.rglob("*")):
        h.update(str(p.relative_to(d)).encode())
        if p.is_file():
            h.update(p.read_bytes())
    return h.hexdigest()


def sh(*a):
    return subprocess.run([sys.executable, *map(str, a)], capture_output=True, text=True)


class T(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="jiagou-test-"))
        self.home, self.store = self.tmp / "01-假电脑", self.tmp / "store"
        shutil.copytree(EXAM / "材料" / "01-假电脑", self.home)
        self.exp = json.loads((EXAM / "expected" / "体检.json").read_text(encoding="utf-8"))
        self.h0 = tree(self.home)

    def test_体检(self):
        r = load("体检").measure(self.home)
        cc, e = r["ClaudeCode"], self.exp
        self.assertEqual(tree(self.home), self.h0)
        self.assertEqual((cc["规则文件"][0]["行"], cc["规则文件"][0]["字"]), (e["CLAUDE.md"]["行数"], e["CLAUDE.md"]["字"]))
        self.assertEqual(cc["技能"]["截断的"], e["技能"]["说明超1536字截断的"])
        self.assertEqual(cc["技能"]["只露名字"], e["技能"]["只露名字"])
        self.assertEqual(cc["技能"]["撞车的"], [e["技能"]["说明一字不差撞车的"]])
        self.assertEqual(cc["技能"]["每次带的字"], e["技能"]["每次固定带的字（名字＋截断后的说明）"])
        self.assertEqual(cc["自动记忆"][0]["读不到的行"], e["自动记忆"]["第200行以后读不到的行数"])
        self.assertEqual(r["WorkBuddy"][0]["字"], e["WorkBuddy记忆"]["字"])
        self.assertEqual({b["名字"]: b["指令字"] for b in r["Grok"]["Bot"]}, e["Grok"]["指令字"])
        self.assertEqual(r["Grok"]["共用技能库"]["个数"], e["Grok"]["共用技能库个数"])
        self.assertEqual(r["重复"][0]["位置"], e["重复和打架"]["同一条写在几处"]["位置"])
        p = r["疑似打架"][0]
        self.assertEqual([[p["甲"]["位置"], p["甲"]["原文"]], [p["乙"]["位置"], p["乙"]["原文"]]], e["重复和打架"]["互相打架"])
        self.assertEqual(len(r["最值得做"]), 3)

    def test_体检算上at引用(self):
        p = self.tmp / "项目"
        p.mkdir()
        (p / "CLAUDE.md").write_text("\n".join(["# 规则在 AGENTS.md", "@" + "AGENTS.md", ""]), encoding="utf-8")  # 拆开写：扫描会把「换行@文件名」当邮箱
        (p / "AGENTS.md").write_text("\n".join(["第一条规矩。", "@" + "CLAUDE.md", "细则" * 50, ""]), encoding="utf-8")  # 循环引用不许死循环
        x = [f for f in load("体检").measure(self.home, [p])["ClaudeCode"]["规则文件"] if f["位置"].endswith("项目/CLAUDE.md")][0]
        self.assertEqual(x["字"], len((p / "CLAUDE.md").read_text(encoding="utf-8")) + len((p / "AGENTS.md").read_text(encoding="utf-8")))
        self.assertEqual(len(x["引用"]), 1)

    def test_体检补漏(self):
        """第 7 步对标补的：关掉自动调用的技能不算说明、CLAUDE.local.md、代理说明、同名技能。"""
        p = self.tmp / "项目"
        (p / ".claude" / "skills" / "demo-00").mkdir(parents=True)
        (p / ".claude" / "skills" / "demo-00" / "SKILL.md").write_text("---\nname: demo-00\ndescription: 项目里也叫这个名字\n---\n", encoding="utf-8")
        (p / "CLAUDE.local.md").write_text("我自己的本地规矩。\n", encoding="utf-8")
        (p / ".claude" / "agents").mkdir()
        (p / ".claude" / "agents" / "reviewer.md").write_text("---\nname: reviewer\ndescription: 审代码\n---\n正文不算\n", encoding="utf-8")
        g = self.home / ".claude" / "skills" / "demo-01" / "SKILL.md"
        g.write_text(g.read_text(encoding="utf-8").replace("---\n\n", "disable-model-invocation: true\n---\n\n", 1), encoding="utf-8")
        r = load("体检").measure(self.home, [p])
        cc = r["ClaudeCode"]
        self.assertEqual([x["档"] for x in cc["技能"]["明细"] if x["名字"] == "demo-01"], ["只给用户用"])
        self.assertIn("demo-00", cc["技能"]["同名的"])
        self.assertTrue(any(x["位置"].endswith("CLAUDE.local.md") for x in cc["规则文件"]))
        self.assertEqual(cc["代理"], {"个数": 1, "每次带的字": len("reviewer") + len("审代码")})
        self.assertEqual(r["每次固定带"]["ClaudeCode"]["代理说明"], len("reviewer") + len("审代码"))

    def test_瘦身整段挪并点名硬规矩(self):
        c = self.home / ".claude" / "CLAUDE.md"
        ls = c.read_text(encoding="utf-8").splitlines(True)
        ls.insert(150, "## 发布前\n")
        ls.insert(160, "- 发布前必须请主人点头，没点头不许发。\n")
        c.write_text("".join(ls), encoding="utf-8")
        r = load("体检").measure(self.home)
        x = [i for i in load("瘦身").items(r, self.home, "2026-10-30") if i["类"] == "挪文字" and "CLAUDE.md" in i["挪什么"]][0]
        self.assertIn("第 151～", x["挪什么"], "切口应退到标题「## 发布前」")
        self.assertTrue(x["改动"][0]["内容"].splitlines()[-2].startswith("- 第"), "前半段不该带走半个标题")
        self.assertIn("发布前必须请主人点头", x["效果"])

    def test_共用技能库占大头要提醒(self):
        """10-30 Grok 实测：146 个共用技能、目录约 2.5 万字，每个 Bot 每次都带，比各 Bot 自己的指令长得多。"""
        r = load("体检").measure(self.home, B={"共用技能库目录字": 2000})
        self.assertTrue(r["Grok"]["共用技能库"]["目录超线"])  # 排不排进前三看大小：假电脑里 CLAUDE.md 更大；真账号 2.5 万字会排第一
        self.assertTrue(any("共用技能库" in x["挪什么"] and x["类"] == "手工" for x in load("瘦身").items(r, self.home, "2026-10-30")))
        self.assertFalse(any("共用技能库 40 个" in x for x in load("体检").measure(self.home)["最值得做"]), "默认线 4,000 字，假电脑 2,838 字不该提醒")

    def test_两个项目不算重复(self):
        line = "回复一律用简体中文，专业词第一次出现要解释。"  # 假电脑全局 CLAUDE.md 里也有这句
        ps = []
        for n in ("甲项目", "乙项目"):
            p = self.tmp / n
            p.mkdir()
            (p / "CLAUDE.md").write_text("项目规则在 AGENTS.md，开工先读它。\n" + line + "\n", encoding="utf-8")
            ps.append(p)
        dup = {d["规矩"]: d["位置"] for d in load("体检").measure(self.home, ps)["重复"]}
        self.assertNotIn("项目规则在 AGENTS.md，开工先读它。", dup)  # 两个项目不会同时打开
        self.assertIn(".claude/CLAUDE.md", dup[line])  # 全局和项目会同时带上，照样算

    def test_瘦身(self):
        run = lambda *a: sh(HERE / "瘦身.py", *a, "--存到", self.store)
        self.assertEqual(run("清单", "--家", self.home).returncode, 0)
        lst = next((self.store / "瘦身").glob("清单-*.json"))
        rest = {f: hashlib.sha256(Path(f).read_bytes()).hexdigest() for x in json.loads(lst.read_text(encoding="utf-8"))["条"][2:]
                for f in x["原校验"] if Path(f).exists()}
        self.assertEqual(run("执行", "--清单", lst, "--条", "1,2").returncode, 0)
        self.assertEqual(tree(self.home), self.h0, "预演动了文件")
        self.assertNotEqual(run("执行", "--清单", lst, "--条", "6").returncode, 0, "手工条不该能执行")
        r = run("执行", "--清单", lst, "--条", "1,2", "--确认")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertNotEqual(tree(self.home), self.h0)
        self.assertEqual({f: hashlib.sha256(Path(f).read_bytes()).hexdigest() for f in rest}, rest, "没点头的条被动了")
        self.assertNotEqual(run("执行", "--清单", lst, "--条", "1", "--确认").returncode, 0, "文件变过还照旧清单执行")
        self.assertEqual(run("改回", "最近一次").returncode, 0)
        self.assertEqual(tree(self.home), self.h0, "改回后和原来不一样")
        self.assertNotEqual(run("改回", "最近一次").returncode, 0)

    def test_瘦身改回前被动过就停(self):
        run = lambda *a: sh(HERE / "瘦身.py", *a, "--存到", self.store)
        run("清单", "--家", self.home)
        lst = next((self.store / "瘦身").glob("清单-*.json"))
        run("执行", "--清单", lst, "--条", "1", "--确认")
        f = self.home / ".claude" / "CLAUDE.md"
        f.write_text(f.read_text(encoding="utf-8") + "主人后来加的一行\n", encoding="utf-8")
        self.assertNotEqual(run("改回", "最近一次").returncode, 0)
        self.assertEqual(run("改回", "最近一次", "--硬").returncode, 0)
        self.assertEqual(tree(self.home), self.h0)
        saved = list((self.store / "备份").glob("*/改回前的样子/*CLAUDE.md"))
        self.assertTrue(saved and "主人后来加的一行" in saved[0].read_text(encoding="utf-8"), "--硬 改回前要先存现在的样子")

    def _undo_blocked(self, names):
        """执行第 1 条，再在拦掉 names 这几个动作的环境里改回（10-30 考试：WorkBuddy 沙盒拦删文件、删文件夹，挪动不拦）。"""
        import os, pathlib
        run = lambda *a: sh(HERE / "瘦身.py", *a, "--存到", self.store)
        run("清单", "--家", self.home)
        run("执行", "--清单", next((self.store / "瘦身").glob("清单-*.json")), "--条", "1", "--确认")
        def no(*a, **k):
            raise OSError(5, "rm returned EISDIR")
        spots = {"rmdir": (pathlib.Path, "rmdir"), "unlink": (pathlib.Path, "unlink"), "os.rmdir": (os, "rmdir"), "rename": (os, "rename")}
        keep = {n: getattr(*spots[n]) for n in names}
        for n in names:
            setattr(*spots[n], no)
        try:
            with contextlib.redirect_stdout(io.StringIO()):  # 改回的提示不混进测试输出
                return load("瘦身").undo("最近一次", self.store, False)
        finally:
            for n in names:
                setattr(*spots[n], keep[n])

    def test_改回时不让删但能挪(self):
        self.assertFalse(self._undo_blocked(["rmdir", "unlink", "os.rmdir"]))
        self.assertEqual(tree(self.home), self.h0, "新建的挪进备份，改回后应和原来一模一样")

    def test_改回时连挪都不让(self):
        self.assertEqual(self._undo_blocked(["rmdir", "unlink", "os.rmdir", "rename"]), 1, "没回到原样还说成功")
        rec = json.loads(next((self.store / "备份").glob("*/记录.json")).read_text(encoding="utf-8"))
        self.assertTrue(rec["已改回"] and any("rules-detail" in x for x in rec["没回到原样"]))

    def test_压测(self):
        r = sh(HERE / "压测.py", "--家", self.home, "--加Bot", "30", "--目录", self.tmp / "y")
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertEqual(tree(self.home), self.h0)
        rows = {x["项"]: x for x in json.loads((self.tmp / "y" / "压测结果.json").read_text(encoding="utf-8"))["对比"]}
        self.assertEqual(rows["Grok Bot 个数"]["后"], 36)
        self.assertIn("超 200", rows["Grok 共用技能库个数"]["结论"])
        self.assertEqual(rows["Claude Code 技能目录每次带（字）"]["结论"], "不涨")

    def test_协作单子缺栏要拦(self):
        r = sh(EXAM.parent / "skills" / "jiagou-handoff" / "借用" / "danzi.py", EXAM / "材料" / "03-协作单子.md")
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("预算", r.stdout)
        self.assertIn("自检", r.stdout)

    def test_仓库检查通过(self):
        root = EXAM.parents[2]
        r = sh(root / "tools" / "validate.py", root)
        self.assertEqual(r.returncode, 0, r.stdout[-1500:])


if __name__ == "__main__":
    ok = unittest.main(verbosity=1, exit=False).result.wasSuccessful()
    print("全部通过" if ok else "有没过的，见上面")
    sys.exit(0 if ok else 1)
