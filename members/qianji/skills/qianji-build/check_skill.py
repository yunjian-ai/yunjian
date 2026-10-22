"""检查一个 Skill 文件夹合不合官方规格（只用 Python 自带的库）。
用法：python3 check_skill.py <Skill 文件夹>
没问题打印「✅ 通过」，返回 0；有问题逐条打印「❌ [类别] 说明」，返回 1。
正文里用反引号写的文件名算「引用」：要在本文件夹里，或者在同一组兄弟技能的文件夹里（几个技能共用的卡）。"""
import re
import sys
from pathlib import Path

ALLOWED = {"name", "description", "license", "compatibility", "metadata", "allowed-tools"}  # 官方规格只认这 6 项
VAGUE = ("看情况", "酌情", "视情况")  # 判断规则里不许出现的空话
MAX_LINES = 500  # 官方建议正文不超过 500 行


def frontmatter(text):
    """返回 (头信息里的顶层字段, 正文)；没有头信息返回 (None, 全文)。"""
    m = re.match(r"^---\n(.*?)\n---\n?", text, re.S)
    if not m:
        return None, text
    keys, cur = {}, None
    for line in m.group(1).split("\n"):
        k = re.match(r"^([A-Za-z][\w-]*):\s*(.*)$", line)
        if k:
            cur = k.group(1)
            keys[cur] = k.group(2).strip()
        elif cur and line.startswith((" ", "\t")):
            keys[cur] = (keys[cur] + " " + line.strip()).strip()  # 多行写法接起来
    for k, v in keys.items():
        keys[k] = re.sub(r"^[>|][-+]?\s*", "", v).strip().strip('"').strip("'")
    return keys, text[m.end():]


def check(folder):
    folder, errs = Path(folder), []
    f = folder / "SKILL.md"
    if not f.exists():
        return ["[文件] 文件夹里没有 SKILL.md"]
    keys, body = frontmatter(f.read_text(encoding="utf-8"))
    if keys is None:
        return ["[头信息] 第一行要是 ---，头信息写在两行 --- 之间"]
    for k in sorted(set(keys) - ALLOWED):
        hint = "（版本号放进 metadata，写成 metadata 下面一行 version: \"1.0\"）" if k == "version" else ""
        errs.append(f"[头信息] 多了「{k}」，官方只认 {'、'.join(sorted(ALLOWED))}{hint}")
    name, desc = keys.get("name", ""), keys.get("description", "")
    if not name:
        errs.append("[name] 缺 name")
    else:
        if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", name) or len(name) > 64:
            errs.append(f"[name] 「{name}」只能用小写字母、数字和单个连字符，最多 64 个字符")
        if name != folder.name:
            errs.append(f"[name] 「{name}」要和文件夹名「{folder.name}」一样")
        if "anthropic" in name or "claude" in name:
            errs.append("[name] 不能含 anthropic、claude")
    if not desc:
        errs.append("[description] 缺 description")
    else:
        if len(desc) > 1024:
            errs.append(f"[description] {len(desc)} 个字符，上限 1024")
        if "<" in desc or ">" in desc:
            errs.append("[description] 不能有尖括号 < >")
    n = body.count("\n") + 1
    if n > MAX_LINES:
        errs.append(f"[正文] {n} 行，超过 {MAX_LINES} 行，长的挪到附件")
    for w in VAGUE:
        if w in body:
            errs.append(f"[空话] 正文里有「{w}」，改成具体条件")
    prose = re.sub(r"```.*?```", "", body, flags=re.S)  # 代码块里是示范（如目录树），不算引用
    refs = set(re.findall(r"\]\(([^)\s#]+)\)", prose))
    for chunk in re.findall(r"`([^`]+)`", prose):
        refs.update(t for t in chunk.split() if re.fullmatch(r"[\w./-]+\.(md|py|sh|js|json|txt|csv)", t))
    for r in sorted(refs):
        shared = any((sib / r).exists() for sib in folder.parent.iterdir() if sib.is_dir())
        if not r.startswith(("http", "/", "~")) and not (folder / r).exists() and not shared:
            errs.append(f"[引用] 正文提到「{r}」，文件夹里没有")
    return errs


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    errs = check(sys.argv[1])
    print("\n".join("❌ " + e for e in errs) if errs else "✅ 通过")
    sys.exit(1 if errs else 0)
