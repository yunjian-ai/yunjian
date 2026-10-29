---
name: title-spark
description: Writes product titles from product notes. Use when the user asks for product titles, listing titles, or 标题.
---
# 标题火花

## 步骤
1. 读主人给的商品资料（文字或表格）。
2. 找出最打动人的 3 个卖点，每个写一句理由。
3. 每个卖点写 3 个标题，用「痛点 + 卖点 + 场景」三段公式。
4. 标题长度 12～20 个字，超了就删修饰词。
5. 运行 `python3 scripts/score.py "<标题>"` 给每个标题打分。
6. 输出一张表：卖点｜标题｜分数，分数从高到低。

## 限制
- 不写「最」「第一」这类极限词。
- 资料里没有的功效不写。
