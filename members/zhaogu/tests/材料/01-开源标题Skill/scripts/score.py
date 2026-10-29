"""给标题打分：长度合适 +40，有数字 +20，有场景词 +20，没有极限词 +20。"""
import sys

SCENE = ["通勤", "居家", "出差", "约会", "办公室", "宿舍"]
BANNED = ["最", "第一", "顶级"]


def score(t):
    s = 40 if 12 <= len(t) <= 20 else 0
    s += 20 if any(c.isdigit() for c in t) else 0
    s += 20 if any(w in t for w in SCENE) else 0
    s += 20 if not any(w in t for w in BANNED) else 0
    return s


if __name__ == "__main__":
    for t in sys.argv[1:]:
        print(score(t), t)
