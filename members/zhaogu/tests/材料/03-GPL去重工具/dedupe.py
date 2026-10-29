# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025 Hana Sato
"""按字面相似度合并重复段落：两段的字集合重合超过 0.8 就算重复，留长的那段。"""
import sys


def similar(a, b):
    sa, sb = set(a), set(b)
    return len(sa & sb) / max(1, len(sa | sb))


def dedupe(paras, th=0.8):
    kept = []
    for p in paras:
        for i, k in enumerate(kept):
            if similar(p, k) > th:
                kept[i] = max(p, k, key=len)
                break
        else:
            kept.append(p)
    return kept


if __name__ == "__main__":
    text = open(sys.argv[1], encoding="utf-8").read()
    print("\n\n".join(dedupe([p for p in text.split("\n\n") if p.strip()])))
