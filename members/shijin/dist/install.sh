#!/usr/bin/env bash
# 试金安装脚本（tools/pack.py 填好版本后生成 dist/install.sh）。不需要 gh，不需要登录。
# 用法：curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/shijin-v0.1.1/members/shijin/dist/install.sh | bash
export GIT_TERMINAL_PROMPT=0
T=shijin-v0.1.1; R=https://github.com/yunjian-ai/yunjian
RAW=https://raw.githubusercontent.com/yunjian-ai/yunjian/$T/members/shijin/dist/recipe.json
W=/tmp/yunjian-$T; RJ=/tmp/recipe-$T.json; rm -rf "${W:?}"
git clone -q --depth 1 --branch "$T" "$R" "$W" 2>/dev/null && cp "$W/members/shijin/dist/recipe.json" "$RJ" \
  || curl -fsSL "$RAW" -o "$RJ" || { echo "FETCH_FAILED $R"; exit 1; }
# 技能目录：可用 SHIJIN_SKILL_DIR 指定；否则找 Grok Bot 的技能目录
D=${SHIJIN_SKILL_DIR:-}
if [ -z "$D" ]; then
  for cand in /home/box/agent-data/workflows /home/box/sand-data/workflows; do [ -d "$cand" ] && { D=$cand; break; }; done
fi
python3 - "$RJ" "$D" <<'PY'
import json, os, sys
r = json.load(open(sys.argv[1], encoding="utf-8")); d = sys.argv[2]
assert r["version"] == "0.1.1", "版本不对"
ok = [s for s in r["skills"] if s["name"].startswith("shijin-") and len(s["content"].encode()) <= 6144]
assert len(ok) == len(r["skills"]), "技能校验没过"
if d:
    for s in ok:
        p = os.path.join(d, s["name"]); os.makedirs(p, exist_ok=True)
        open(os.path.join(p, "SKILL.md"), "w", encoding="utf-8").write(s["content"])
        for n, t in s.get("files", {}).items():
            open(os.path.join(p, n), "w", encoding="utf-8").write(t)
    print("INSTALLED", len(ok), d)
else:
    print("NO_SKILL_DIR", len(ok), sys.argv[1])
PY
