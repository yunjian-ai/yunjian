"""检查云间每位成员的格式（规矩见 shared/成员规范.md 第五节）。只用标准库。
用法：python3 tools/validate.py        有错误时退出码为 1。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL_MAX = 6144          # 单个 SKILL.md 字节上限
MEMBER_MAX = 80 * 1024    # 一位成员全部技能文件合计上限
DESC_MAX = 400            # description 字符上限
REQUIRED = ("install", "update", "getting-started")


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    block = m.group(1)
    name = re.search(r"^name:\s*(\S+)", block, re.M)
    desc = re.search(r"^description:\s*(?:>-\s*\n)?(.*)", block, re.M | re.S)
    d = " ".join(line.strip() for line in desc.group(1).splitlines()) if desc else ""
    return (name.group(1) if name else None), d


def check_member(m, errors):
    prefix = m.name if m.name != "qingniao" else "qingniao"
    prof = m / "profile.json"
    if not prof.exists():
        errors.append(f"{m.name}: 缺 profile.json")
    else:
        p = json.loads(prof.read_text(encoding="utf-8"))
        for k in ("name", "description", "instructions"):
            if not p.get(k):
                errors.append(f"{m.name}: profile.json 缺 {k}")
        if len(p.get("description", "")) > DESC_MAX:
            errors.append(f"{m.name}: profile description 超过 {DESC_MAX} 字符")
        if "云间出品" not in p.get("name", ""):
            errors.append(f"{m.name}: 名字里没有「云间出品」")
    skills = m / "skills"
    total = 0
    names = []
    for sd in sorted(p for p in skills.iterdir() if p.is_dir()):
        sk = sd / "SKILL.md"
        if not sk.exists():
            errors.append(f"{sd.name}: 缺 SKILL.md")
            continue
        text = sk.read_text(encoding="utf-8")
        size = len(text.encode("utf-8"))
        if size > SKILL_MAX:
            errors.append(f"{sd.name}: SKILL.md {size} 字节，超过 {SKILL_MAX}")
        fm = frontmatter(text)
        if not fm:
            errors.append(f"{sd.name}: 没有 frontmatter")
        else:
            name, desc = fm
            if name != sd.name:
                errors.append(f"{sd.name}: name「{name}」和目录名不一致")
            if not desc:
                errors.append(f"{sd.name}: 缺 description")
            elif len(desc) > DESC_MAX:
                errors.append(f"{sd.name}: description {len(desc)} 字符，超过 {DESC_MAX}")
        names.append(sd.name)
        # 反引号引用的 .md 文件要存在（在本目录或任何技能目录里）
        for ref in set(re.findall(r"`([^`/]+\.md)`", text)):
            if not any((d / ref).exists() for d in skills.iterdir() if d.is_dir()) and ref != "SKILL.md" \
                    and not (ROOT / ref).exists():
                errors.append(f"{sd.name}: 引用的 {ref} 找不到")
        for f in sd.iterdir():
            if f.is_file():
                total += len(f.read_bytes())
    for r in REQUIRED:
        if f"{prefix}-{r}" not in names:
            errors.append(f"{m.name}: 缺必备技能 {prefix}-{r}")
    if total > MEMBER_MAX:
        errors.append(f"{m.name}: 技能文件合计 {total} 字节，超过 {MEMBER_MAX}")
    return total, names


# 公开的文件（装进 Bot、放进公开仓库的）不能出现的词：放在 tools/禁用词.txt（一行一个），这个文件只在开发仓库里，不公开
_WORDS = ROOT / "tools" / "禁用词.txt"
_LIST = [w.strip() for w in _WORDS.read_text(encoding="utf-8").splitlines() if w.strip()] if _WORDS.exists() else []
BANNED = re.compile("|".join([re.escape(w) for w in _LIST] + [r"第[一二三四五六七八九十0-9]+课"])) if _LIST else None


def public_files():
    yield from (ROOT / p for p in ("README.md", "CHANGELOG.md"))
    yield from (ROOT / "shared").glob("*.md")
    for m in (ROOT / "members").iterdir():
        if m.is_dir():
            yield from (m / n for n in ("profile.json", "memory.md"))
            yield from (m / "skills").rglob("*.md")


def check_banned(errors):
    if BANNED is None:
        return
    for f in public_files():
        if not f.exists():
            continue
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            for hit in set(BANNED.findall(line)):
                errors.append(f"{f.relative_to(ROOT)}:{i} 公开文件里有不该出现的词「{hit}」")


def main():
    errors = []
    check_banned(errors)
    for m in sorted((ROOT / "members").iterdir()):
        if m.is_dir() and (m / "skills").exists():
            total, names = check_member(m, errors)
            print(f"{m.name}: {len(names)} 个技能，合计 {total} 字节")
    for e in errors:
        print("❌", e)
    print("✅ 全部通过" if not errors else f"共 {len(errors)} 处问题")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
