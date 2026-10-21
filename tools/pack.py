"""把一位成员打包成 Bot 用的配方。用法：python3 tools/pack.py [成员...] [--check]
产出 members/<成员>/dist/：recipe.json（全部技能，安装用）、template.json（Grok Bot 分享卡：安装技能＋第一次见面＋一条记忆）、install.sh。
--check：只比对不写；dist 不是最新就退出码 1（CI 用）。只用标准库。"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG = json.loads((ROOT / "tools" / "config.json").read_text(encoding="utf-8"))


def frontmatter(text):
    block = re.match(r"^---\n(.*?)\n---\n", text, re.S).group(1)
    name = re.search(r"^name:\s*(\S+)", block, re.M).group(1)
    desc = re.search(r"^description:\s*(?:>-\s*\n)?(.*)", block, re.M | re.S).group(1)
    return name, " ".join(l.strip() for l in desc.splitlines())


def build(member):
    m = ROOT / "members" / member
    version = (m / "VERSION").read_text().strip()
    subst = {"{{OWNER}}": CONFIG["github_owner"], "{{REPO}}": CONFIG["repo"], "{{VERSION}}": version}
    # 安装技能里写的仓库名是 yunjian，和 config 一致；占位符统一在这里填
    def fill(t):
        for k, v in subst.items():
            t = t.replace(k, v)
        return t

    skills = []
    for d in sorted(p for p in (m / "skills").iterdir() if p.is_dir()):
        text = fill((d / "SKILL.md").read_text(encoding="utf-8"))
        name, desc = frontmatter(text)
        files = {f.name: fill(f.read_text(encoding="utf-8")) for f in sorted(d.iterdir()) if f.is_file() and f.name != "SKILL.md"}
        skills.append({"name": name, "description": desc, "content": text, "files": files})
    profile = json.loads(fill((m / "profile.json").read_text(encoding="utf-8")))
    memory = fill((m / "memory.md").read_text(encoding="utf-8"))
    tag = f"{member}-v{version}"
    recipe = {"member": member, "version": version, "repo": f"https://github.com/{CONFIG['github_owner']}/{CONFIG['repo']}",
              "tag": tag, "profile": profile, "memory": memory, "skills": skills}
    card = (f"{member}-install", f"{member}-getting-started")
    thin = {
        "profile": {"name": profile["name"], "description": profile["instructions"]},
        "memory": [{"kind": "log", "content": memory}],
        "skills": [{k: s[k] for k in ("name", "description", "content")} for s in skills if s["name"] in card],
        "gettingStarted": {"skill": f"{member}-install"},
        "_meta": {"member": member, "version": version, "tag": tag, "storefront": profile["description"]},
    }
    dump = lambda o: json.dumps(o, ensure_ascii=False, indent=1) + "\n"
    out = {m / "dist" / "recipe.json": dump(recipe), m / "dist" / "template.json": dump(thin)}
    if (m / "install.sh").exists():
        out[m / "dist" / "install.sh"] = fill((m / "install.sh").read_text(encoding="utf-8"))
    if (m / "EXPORT.md").exists():
        out[m / "dist" / "EXPORT.md"] = fill((m / "EXPORT.md").read_text(encoding="utf-8"))
    return out


def main():
    names = [a for a in sys.argv[1:] if not a.startswith("--")]
    check = "--check" in sys.argv
    members = names or [p.name for p in (ROOT / "members").iterdir() if (p / "skills").is_dir()]
    stale = []
    for mb in members:
        for path, content in build(mb).items():
            if check:
                if not path.exists() or path.read_text(encoding="utf-8") != content:
                    stale.append(str(path.relative_to(ROOT)))
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
                print(f"写好 {path.relative_to(ROOT)}（{len(content.encode())} 字节）")
    if stale:
        print("❌ dist 不是最新，请运行 python3 tools/pack.py：", *stale)
        return 1
    if check:
        print("✅ dist 是最新的")
    return 0


if __name__ == "__main__":
    sys.exit(main())
