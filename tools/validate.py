"""仓库检查（规矩见 shared/成员规范.md 第五节）。只用标准库。
用法：python3 tools/validate.py [仓库根目录]   有错误时退出码为 1，逐条列出。"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import LIM, hash_hits, parse_frontmatter  # noqa: E402

REQUIRED = ("install", "update", "getting-started")
LESSON = re.compile(r"第[一二三四五六七八九十0-9]+课")


def public_files(root):
    """装进 Bot、放进公开仓库的文件：只扫这些（开发仓库里的内部文档不扫）。"""
    for p in ("README.md", "CHANGELOG.md", "CONTRIBUTING.md", "发布素材/README.md", "发布素材/CONTRIBUTING.md"):
        if (root / p).exists():
            yield root / p
    yield from (root / "shared").glob("*.md")
    for m in sorted((root / "members").iterdir()):
        if not (m / "skills").is_dir():
            continue
        for n in ("profile.json", "memory.md"):
            if (m / n).exists():
                yield m / n
        for sub in ("skills", "examples"):
            yield from sorted(p for p in (m / sub).rglob("*.md")) if (m / sub).exists() else ()


def check_member(m, root, errors):
    name, total = m.name, 0
    ver = (m / "VERSION").read_text().strip() if (m / "VERSION").exists() else ""
    if not re.fullmatch(r"\d+\.\d+\.\d+", ver):
        errors.append(f"[version] {name}: VERSION 缺失或不是 x.y.z")
    prof = m / "profile.json"
    if not prof.exists():
        errors.append(f"[profile] {name}: 缺 profile.json")
    else:
        b = prof.stat().st_size
        total += b
        p = json.loads(prof.read_text(encoding="utf-8"))
        for k in ("name", "description", "intro", "instructions"):
            if not p.get(k):
                errors.append(f"[profile] {name}: profile.json 缺 {k}")
        if len(p.get("description", "")) > LIM["description_chars"]:
            errors.append(f"[profile] {name}: description 超过 {LIM['description_chars']} 字符")
        if "云间出品" not in p.get("name", ""):
            errors.append(f"[profile] {name}: 名字里没有「云间出品」")
        if b > LIM["profile_bytes"]:
            errors.append(f"[budget] {name}: profile.json {b} 字节 > {LIM['profile_bytes']}")
    if (m / "memory.md").exists():
        total += (m / "memory.md").stat().st_size
    skills = sorted(d for d in (m / "skills").iterdir() if d.is_dir())
    names, corpus = {d.name for d in skills}, {}
    for d in skills:
        f = d / "SKILL.md"
        if not f.exists():
            errors.append(f"[frontmatter] {d.name}: 没有 SKILL.md")
            continue
        text = f.read_text(encoding="utf-8")
        corpus[d.name] = text
        meta = parse_frontmatter(text)
        if not meta or not meta.get("name") or not meta.get("description"):
            errors.append(f"[frontmatter] {d.name}: 缺 name 或 description")
        else:
            if meta["name"] != d.name:
                errors.append(f"[frontmatter] {d.name}: name 是 {meta['name']}，和目录名不一致")
            if not meta["name"].startswith(name + "-"):
                errors.append(f"[frontmatter] {d.name}: name 必须以 {name}- 开头")
            if len(meta["description"]) > LIM["description_chars"]:
                errors.append(f"[frontmatter] {d.name}: description 超过 {LIM['description_chars']} 字符")
        for extra in d.iterdir():
            if extra.is_file():
                total += extra.stat().st_size
                if extra.name == "SKILL.md" and extra.stat().st_size > LIM["skill_bytes"]:
                    errors.append(f"[budget] {d.name}/SKILL.md {extra.stat().st_size} 字节 > {LIM['skill_bytes']}")
            if extra.is_file() and extra.suffix == ".md" and extra.name != "SKILL.md":
                corpus[f"{d.name}/{extra.name}"] = extra.read_text(encoding="utf-8")
    for r in REQUIRED:
        if f"{name}-{r}" not in names:
            errors.append(f"[skills] {name}: 缺必备技能 {name}-{r}")
    if total > LIM["total_bytes"]:
        errors.append(f"[budget] {name}: 合计 {total} 字节 > {LIM['total_bytes']}")
    # 交叉引用：提到的本成员技能名、反引号里的 .md 文件都要存在
    files = {p.name for p in root.rglob("*.md")}
    pool = dict(corpus)
    if (m / "memory.md").exists():
        pool["memory.md"] = (m / "memory.md").read_text(encoding="utf-8")
    for src, text in pool.items():
        for ref in set(re.findall(rf"\b{name}-[a-z][a-z-]*[a-z]\b", text)):
            if ref not in names:
                errors.append(f"[xref] {src}: 引用了不存在的技能 {ref}")
        for ref in set(re.findall(r"`([^`/\s]+\.md)`", text)):
            if ref not in files:
                errors.append(f"[xref] {src}: 引用了不存在的文件 {ref}")
    return total


def main(root):
    root = Path(root).resolve()
    errors = []
    hp = root / "tools" / "scrub_hashes.json"
    entries = json.loads(hp.read_text(encoding="utf-8"))["private"] if hp.exists() else []
    for f in public_files(root):
        text = f.read_text(encoding="utf-8")
        rel = f.relative_to(root)
        if entries and hash_hits(text, entries):
            errors.append(f"[private] {rel}: 公开文件里有名单上的词（只显示首字）：{'、'.join(sorted(hash_hits(text, entries)))}")
        if LESSON.search(text):
            errors.append(f"[private] {rel}: 公开文件里有「第几课」")
    totals = {}
    for m in sorted((root / "members").iterdir()):
        if (m / "skills").is_dir():
            totals[m.name] = check_member(m, root, errors)
    for e in errors:
        print("❌", e)
    print(("✅ 全部通过" if not errors else f"共 {len(errors)} 处问题") + "｜" + "，".join(f"{k} {v} 字节" for k, v in totals.items()))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent))
