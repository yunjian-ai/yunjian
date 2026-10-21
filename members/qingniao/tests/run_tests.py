"""跑青鸟的夹具：fixtures/ 里每个提示词，检查结果要和 expected/ 里同名文件的问题代码一致。
干净样例的 expect 是空列表，用来防误报。用法：python3 members/qingniao/tests/run_tests.py"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent.parent.parent / "tools"))
from check_prompt import check  # noqa: E402

fails = 0
for f in sorted((HERE / "fixtures").glob("*.json")):
    got = sorted({i["code"] for i in check(json.loads(f.read_text(encoding="utf-8")))})
    exp = json.loads((HERE / "expected" / f.name).read_text(encoding="utf-8"))
    want = sorted(exp["expect"])
    ok = got == want
    fails += not ok
    print(("✅" if ok else "❌"), f.stem, "得到", got, "应为", want, "" if ok else "｜" + exp.get("why", ""))
print("全部通过" if not fails else f"{fails} 个没过")
sys.exit(1 if fails else 0)
