"""仓库检查（规矩见 shared/成员规范.md 第五节）。只用标准库。
用法：python3 tools/validate.py [仓库根目录]   有错误时退出码为 1，逐条列出。"""
import hashlib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import LIM, hash_hits, is_material, norm, parse_frontmatter, public_picks  # noqa: E402

REQUIRED = ("install", "update", "getting-started")
LESSON = re.compile(r"第[一二三四五六七八九十0-9]+课")


def public_files(root):
    """装进 Bot、放进公开仓库的文件：和 tools/publish.py 用同一份白名单（common.public_picks），
    发布会挑走的每个文件都扫，不论后缀（.md、.json、.py、.sh……）；开发仓库里的内部文档不扫。"""
    seen = set()
    for src, _ in [(root / "README.md", ""), (root / "CHANGELOG.md", ""), (root / "CONTRIBUTING.md", "")] + public_picks(root):
        for f in sorted(src.rglob("*")) if src.is_dir() else [src]:
            if f.is_file() and f not in seen and f.name != ".DS_Store" and "__pycache__" not in f.parts:
                seen.add(f)
                yield f


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
        if "云间工作室出品" not in p.get("name", ""):
            errors.append(f"[profile] {name}: 名字里没有「云间工作室出品」")
        if b > LIM["profile_bytes"]:
            errors.append(f"[budget] {name}: profile.json {b} 字节 > {LIM['profile_bytes']}")
    if (m / "memory.md").exists():
        total += (m / "memory.md").stat().st_size
    skills = sorted(d for d in (m / "skills").iterdir() if d.is_dir())
    names, corpus = {d.name for d in skills}, {}
    # 岗位说明（shared/岗位说明写法.md 第四节）
    if prof.exists():
        ins = json.loads(prof.read_text(encoding="utf-8")).get("instructions", "")
        if not ins.startswith("你是"):
            errors.append(f"[instructions] {name}: 岗位说明要以「你是」开头")
        for s in sorted(names - {f"{name}-install", f"{name}-update"}):
            if s not in ins:
                errors.append(f"[instructions] {name}: 岗位说明没派到技能 {s}")
        # 装法三处一致（shared/安装写法.md）：岗位说明、安装记录、安装技能都带同一条安装命令
        cmd = f"{{{{REPO}}}}/{name}-v{{{{VERSION}}}}/members/{name}/dist/install.sh"
        places = {"岗位说明": ins, "memory.md": (m / "memory.md").read_text(encoding="utf-8") if (m / "memory.md").exists() else "",
                  f"{name}-install": (m / "skills" / f"{name}-install" / "SKILL.md").read_text(encoding="utf-8")
                  if (m / "skills" / f"{name}-install" / "SKILL.md").exists() else ""}
        for where, text in places.items():
            if cmd not in text:
                errors.append(f"[install] {name}: {where} 里没有标准安装命令（见 shared/安装写法.md）")
        for n in re.findall(r"不到 ?(\d+) ?个", ins):
            if int(n) != len(names):
                errors.append(f"[instructions] {name}: 岗位说明写「不到 {n} 个」，实际有 {len(names)} 个技能")
    for d in skills:
        f = d / "SKILL.md"
        if not f.exists():
            errors.append(f"[frontmatter] {d.name}: 没有 SKILL.md")
            continue
        text = f.read_text(encoding="utf-8")
        corpus[d.name] = text
        if d.name.endswith("-getting-started") and "## 演练模式" not in text:
            errors.append(f"[rehearsal] {d.name}: 入门技能缺「## 演练模式」一节（见 shared/成员规范.md）")
        if not d.name.endswith(("-install", "-update")) and re.search(r"写进记忆|存进记忆|写入记忆", text) and "演练" not in text:
            errors.append(f"[rehearsal] {d.name}: 会写记忆，但没写演练模式下只打印")
        meta = parse_frontmatter(text)
        if not meta or not meta.get("name") or not meta.get("description"):
            errors.append(f"[frontmatter] {d.name}: 缺 name 或 description")
        else:
            if meta["name"] != d.name:
                errors.append(f"[frontmatter] {d.name}: 头信息里的名字「{meta['name']}」跟文件夹名对不上")
            if not meta["name"].startswith(name + "-"):
                errors.append(f"[frontmatter] {d.name}: name 必须以 {name}- 开头")
            if len(meta["description"]) > LIM["description_chars"]:
                errors.append(f"[frontmatter] {d.name}: 说明写长了，上限 {LIM['description_chars']} 字符")
        for extra in d.iterdir():
            if extra.is_file():
                total += extra.stat().st_size
                if extra.name == "SKILL.md" and extra.stat().st_size > LIM["skill_bytes"]:
                    errors.append(f"[budget] {d.name}/SKILL.md {extra.stat().st_size} 字节 > {LIM['skill_bytes']}")
            if extra.is_file() and extra.suffix == ".md" and extra.name != "SKILL.md":
                corpus[f"{d.name}/{extra.name}"] = extra.read_text(encoding="utf-8")
    # 示例（shared/成员规范.md）：一位虚构主人从头走到尾＋一份全流程演练，开头都标「示例数据（虚构主人）」
    ex = sorted((m / "examples").glob("*.md")) if (m / "examples").is_dir() else []
    if not any("全流程" in f.name for f in ex) or len(ex) < 3:
        errors.append(f"[examples] {name}: 示例要有一位虚构主人走一遍（至少 2 份）＋一份「全流程」演练")
    for f in ex:
        head = "\n".join(f.read_text(encoding="utf-8").splitlines()[:5])
        if "示例数据" not in head and "【示例】" not in head:
            errors.append(f"[examples] {name}/examples/{f.name}: 开头没标「示例数据（虚构主人）」")
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
        mentioned = set(re.findall(r"\b" + re.escape(name) + r"-[a-z]{2,}(?:-[a-z]+)*\b", text))
        for ref in mentioned:
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
    # 两份名单要一致：发布扫描用 禁用词.txt 的明文，这里用 scrub_hashes.json 的哈希；明文里有、哈希里没有的词，这里就会漏
    wp = root / "tools" / "禁用词.txt"
    if wp.exists():
        have = {(e["len"], e["sha256"]) for e in entries}
        for i, w in enumerate((x for x in wp.read_text(encoding="utf-8").splitlines() if x.strip()), 1):
            n = norm(w)
            if (len(n), hashlib.sha256(n.encode()).hexdigest()) not in have:
                errors.append(f"[private] tools/禁用词.txt 第 {i} 个词（首字「{n[:1]}」）不在 scrub_hashes.json 里，用 tools/scrub_hash.py 补上")
    for f in public_files(root):
        try:
            text = f.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue  # 图片等二进制文件
        rel = f.relative_to(root)
        if is_material(rel):
            continue
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
    target = sys.argv[1] if len(sys.argv) > 1 else str(Path(__file__).resolve().parent.parent)
    sys.exit(main(target))
