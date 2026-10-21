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
CONFIG = json.loads((ROOT / "tools" / "config.json").read_text(encoding="utf-8"))
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
    """反向用例：把仓库复制一份、埋一个错，validate 必须失败并报出对应类别。cases = [(类别, 改法函数), ...]"""
    for tag, fn in cases:
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td) / "repo"
            shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns(".git", "__pycache__", "发布", "资料", "考试记录"))
            fn(dst)
            r = subprocess.run([sys.executable, str(dst / "tools" / "validate.py"), str(dst)], capture_output=True, text=True)
            report(r.returncode == 1 and f"[{tag}]" in r.stdout, f"validate 能拦住 {tag}")
