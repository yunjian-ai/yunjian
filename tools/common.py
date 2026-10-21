"""validate / pack / 各成员检查脚本和测试共用的小工具。只用标准库。"""
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
with open(ROOT / "tools" / "config.json", encoding="utf-8") as _fh:
    CONFIG = json.load(_fh)
LIM = CONFIG["limits"]


def parse_frontmatter(text):
    """解析 SKILL.md 开头的 name 和 description（支持 >- 折叠块）。"""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    meta, key, buf = {}, None, []
    for line in text[4:end].splitlines():
        m = re.match(r"^([a-z_]+):\s*(.*)$", line)
        if m:
            if key:
                meta[key] = " ".join(buf).strip()
            key, val = m.group(1), m.group(2).strip()
            buf = [] if val in (">-", ">", "|") else [val]
        elif key:
            buf.append(line.strip())
    if key:
        meta[key] = " ".join(buf).strip()
    return meta


def norm(t):
    return "".join(t.lower().split())


def hash_hits(text, entries):
    """按哈希名单找词：命中只回显第一个字，不暴露完整词。"""
    t, want, hits = norm(text), {(e["len"], e["sha256"]) for e in entries}, set()
    for n in {e["len"] for e in entries}:
        for i in range(len(t) - n + 1):
            if (n, hashlib.sha256(t[i:i + n].encode()).hexdigest()) in want:
                hits.add(t[i:i + n][:1] + "…")
    return hits


def run_negative_cases(member, cases, report):
    """反向用例：每个用例都在一份临时副本里埋一个错，然后跑检查脚本——它必须失败，并且报出这个类别。
    cases 是 [(类别, 埋错的函数), ...]；埋错的函数拿到副本的根目录。"""
    skip = shutil.ignore_patterns(".git", "__pycache__", "发布", "资料", "考试记录")
    has_list = (ROOT / "tools" / "scrub_hashes.json").exists()
    for tag, plant in cases:
        if tag == "private" and not has_list:
            print(f"（跳过「{tag}」：禁用词名单只在开发仓库里，公开仓库没有）")
            continue
        with tempfile.TemporaryDirectory() as tmp:
            copy_root = Path(tmp) / "副本"
            shutil.copytree(ROOT, copy_root, ignore=skip)
            plant(copy_root)
            done = subprocess.run([sys.executable, "tools/validate.py", "."], cwd=copy_root, capture_output=True, text=True)
            caught = done.returncode != 0 and ("[" + tag + "]") in done.stdout
            report(caught, f"埋了一个「{tag}」类的错，检查脚本拦住了")
