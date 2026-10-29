#!/usr/bin/env python3
"""勘察：拆别人的东西之前，先看清它是什么。只读，绝不运行、不修改目标；只用 Python 自带的库。

用法：
  python3 勘察.py <文件或文件夹>                 看体量、许可证线索、Skill/Bot 结构、可疑的行、加密或二进制文件
  python3 勘察.py <文件夹> --json                 同上，机器读的格式
  python3 勘察.py <文件夹> --存档 <存档文件夹>     一字不改复制一份，写存档清单（大小、校验码），复制完逐个比对

熵计算、文件头识别、入口文件清单改写自 peek.py：
MIT License, Copyright (c) 2026 REA Expert Council.
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit
persons to whom the Software is furnished to do so, subject to the following conditions: The above copyright notice and
this permission notice shall be included in all copies or substantial portions of the Software. THE SOFTWARE IS PROVIDED
"AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED.
"""
import collections
import hashlib
import json
import math
import re
import shutil
import sys
from datetime import date
from pathlib import Path

MAX_READ = 8 * 1024 * 1024
MAX_HITS = 20
MAGIC = [(b"\x7fELF", "Linux 可执行"), (b"MZ", "Windows 可执行"), (b"\xcf\xfa\xed\xfe", "macOS 可执行"),
         (b"\xca\xfe\xba\xbe", "macOS 通用可执行或 Java 字节码"), (b"PK\x03\x04", "ZIP 压缩包"), (b"\x1f\x8b", "gzip 压缩"),
         (b"7z\xbc\xaf\x27\x1c", "7z 压缩包"), (b"Rar!\x1a\x07", "RAR 压缩包"), (b"SQLite format 3\x00", "SQLite 数据库"),
         (b"%PDF-", "PDF"), (b"\x89PNG\r\n\x1a\n", "PNG 图片"), (b"\xff\xd8\xff", "JPEG 图片"), (b"GIF8", "GIF 图片"),
         (b"\x00asm", "WebAssembly"), (b"dex\n", "安卓字节码")]
ENTRY = {"package.json", "pyproject.toml", "setup.py", "requirements.txt", "go.mod", "Cargo.toml", "Makefile",
         "Dockerfile", "README.md", "readme.md", "main.py", "app.py", "index.js", "index.ts",
         "SKILL.md", "profile.json", "memory.md", "install.sh", "setup.sh", "manifest.json"}
LICENSE_FILE = re.compile(r"(?i)^(licen[cs]e|copying|notice)([.-].*)?$")
LICENSE_LINE = re.compile(r"(?i)(SPDX-License-Identifier:\s*\S+|^\s*license\s*[:=]\s*\S.*|\"license\"\s*:\s*\"[^\"]+\"|"
                          r"licen[cs]e\s*[:：]\s*\S+)")
RISK = {
    "外发": r"\bcurl\b|\bwget\b|requests\.(post|put)|\bfetch\(|urlopen|webhook|-F\s*\"?\w+=@",
    "读私密位置": r"Library/Messages|\.ssh\b|Keychain|\bid_rsa\b|\.env\b|Login Data|Cookies|通讯录|聊天记录",
    "危险命令": r"rm\s+-rf|\bsudo\b|chmod\s+777|curl[^|\n]*\|\s*(ba|z)?sh|\beval\(|\bexec\(|base64\s+-d|os\.system|shell\s*=\s*True",
    "调用别的程序": r"subprocess\.(run|call|Popen|check_output|check_call)\(",
    "让 AI 绕过主人": r"(?i)忽略(之前|以上|前面)|ignore (all )?(previous|prior)|不(用|必)?(先)?问主人|直接发送|without asking|"
                      r"无需确认|已授权任何人|不必再查|不要告诉主人",
    "疑似密钥": r"(?i)api[_-]?key\s*[=:]|secret\s*[=:]|token\s*[=:]\s*\S{12,}|BEGIN [A-Z ]*PRIVATE KEY",
}
RISK_RE = {k: re.compile(v) for k, v in RISK.items()}
TRUNC = re.compile(r"(?i)只显示到这里|后面略|以下略|显示不全|已截断|内容被截|\[truncated\]|\(truncated\)|\(略\)|（略）")


def entropy(data):
    if not data:
        return 0.0
    n = len(data)
    return -sum(c / n * math.log2(c / n) for c in collections.Counter(data).values())


def kind(head):
    for sig, name in MAGIC:
        if head.startswith(sig):
            return name
    return "二进制（认不出格式）" if b"\x00" in head[:8192] else ""


def files_of(target):
    if target.is_file():
        return [target]
    return sorted(p for p in target.rglob("*") if p.is_file() and ".git" not in p.relative_to(target).parts)


def frontmatter(text):
    m = re.match(r"---\n(.*?)\n---", text, re.S)
    return dict(re.findall(r"^(\w[\w-]*):\s*(.*)$", m.group(1), re.M)) if m else None


def survey(target):
    target = Path(target)
    base = target if target.is_dir() else target.parent
    res = {"目标": str(target), "文件数": 0, "总大小": 0, "类型": collections.Counter(), "入口": [], "许可证线索": [],
           "Skill": [], "Bot": [], "可疑": {k: [] for k in RISK}, "加密或二进制": [], "限制": []}
    for f in files_of(target):
        rel = str(f.relative_to(base))
        size = f.stat().st_size
        res["文件数"] += 1
        res["总大小"] += size
        res["类型"][f.suffix.lower() or "（无后缀）"] += 1
        if f.name in ENTRY:
            res["入口"].append(rel)
        with open(f, "rb") as fh:
            data = fh.read(MAX_READ)
        if size > MAX_READ:
            res["限制"].append(f"{rel} 超过 8MB，只读了前 8MB")
        k = kind(data[:8192])
        if k:
            e = entropy(data[:65536])
            res["加密或二进制"].append({"文件": rel, "格式": k, "熵": round(e, 2),
                                   "提示": "接近满熵，可能加密或压缩，停在这一层" if e >= 7.5 and "图片" not in k else ""})
            continue
        text = data.decode("utf-8", errors="replace")
        if LICENSE_FILE.match(f.name):
            first = next((x.strip() for x in text.splitlines() if x.strip()), "（空文件）")
            res["许可证线索"].append(f"{rel} 第一行：{first[:80]}")
        for i, line in enumerate(text.splitlines(), 1):
            if LICENSE_LINE.search(line) and not LICENSE_FILE.match(f.name):
                res["许可证线索"].append(f"{rel} 第 {i} 行：{line.strip()[:80]}")
            for cat, rx in RISK_RE.items():
                if rx.search(line) and len(res["可疑"][cat]) < MAX_HITS:
                    res["可疑"][cat].append(f"{rel} 第 {i} 行：{line.strip()[:100]}")
        if f.name == "SKILL.md":
            fm = frontmatter(text)
            res["Skill"].append(f"{rel}：" + ("没有头信息" if fm is None else
                                f"name={fm.get('name', '（缺）')}，description {'有' if fm.get('description') else '缺'}"
                                + (f"，license={fm['license']}" if fm.get("license") else "")))
        if f.name in ("profile.json", "memory.md", "指令.md", "记忆.md", "settings.json"):
            res["Bot"].append(f"{rel}（{size} 字节）")
    if not res["许可证线索"]:
        res["许可证线索"].append("没找到（查了：LICENSE / COPYING / NOTICE 文件名，各文件里的 license 字样和 SPDX 标识）")
    res["限制"].append("只读了文字和文件头，没有运行任何文件；可疑的行是按字面找的，要回原文看上下文再下结论")
    res["类型"] = res["类型"].most_common(8)
    return res


def show(r):
    out = [f"# 勘察：{r['目标']}", f"体量：{r['文件数']} 个文件，{r['总大小']} 字节；类型 "
           + "、".join(f"{k}×{n}" for k, n in r["类型"]), "入口：" + ("、".join(r["入口"]) or "没找到常见入口文件")]
    out += ["\n## 许可证线索"] + [f"- {x}" for x in r["许可证线索"]]
    if r["Skill"] or r["Bot"]:
        out += ["\n## Skill / Bot 结构"] + [f"- {x}" for x in r["Skill"] + r["Bot"]]
    out.append("\n## 可疑的行")
    hits = [(c, x) for c, xs in r["可疑"].items() for x in xs]
    out += [f"- 【{c}】{x}" for c, x in hits] or ["- 没找到（按字面找的，不等于没有）"]
    if r["加密或二进制"]:
        out += ["\n## 加密或二进制"] + [f"- {x['文件']}：{x['格式']}，熵 {x['熵']} {x['提示']}" for x in r["加密或二进制"]]
    out += ["\n## 限制"] + [f"- {x}" for x in r["限制"]]
    return "\n".join(out)


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def archive(target, dest):
    """一字不改复制，写存档清单；复制完逐个比校验码，有一个不一致就返回 False。"""
    target, dest = Path(target), Path(dest)
    base = target if target.is_dir() else target.parent
    rows, ok = [], True
    for f in files_of(target):
        rel = f.relative_to(base)
        (dest / "原件" / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, dest / "原件" / rel)
        same = sha(f) == sha(dest / "原件" / rel)
        ok &= same
        cut = [i for i, x in enumerate(f.read_bytes().decode("utf-8", "replace").splitlines(), 1) if TRUNC.search(x)]
        whole = f"疑似截断（第 {'、'.join(map(str, cut))} 行）" if cut else "待核对：完整 / 截断 / 缺"
        rows.append(f"| `{rel}` | {f.stat().st_size} | `{sha(f)[:16]}` | {'一致' if same else '❌ 不一致'} | {whole} |")
    (dest / "存档清单.md").write_text(
        f"# 存档清单\n\n目标：`{target}`　存档日期：{date.today()}　来源：待填（链接、谁给的、哪天拿到）\n\n"
        "| 文件 | 字节 | 校验码（前 16 位） | 复制后比对 | 全不全 |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n",
        encoding="utf-8")
    return ok


def main(argv):
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__.split("\n\n熵计算")[0])
        return 0
    target = Path(argv[0])
    if not target.exists():
        print(f"找不到：{target}")
        return 2
    if "--存档" in argv:
        dest = argv[argv.index("--存档") + 1]
        ok = archive(target, dest)
        print(f"{'✅' if ok else '❌'} 存档到 {dest}（{'全部一致' if ok else '有文件复制后不一致'}），清单：{dest}/存档清单.md")
        return 0 if ok else 1
    r = survey(target)
    print(json.dumps(r, ensure_ascii=False, indent=1) if "--json" in argv else show(r))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
