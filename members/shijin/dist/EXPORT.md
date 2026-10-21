# 导出试金分享卡（给 Grok Bot 看的操作单）· v0.1.0

调用 `CreateBotShareJson`，参数全部取自同目录 `dist/template.json`（由 `tools/pack.py` 生成，标签 shijin-v0.1.0），逐字使用，不要改写：

| 参数 | 填什么 |
|---|---|
| name | `试金 Touchstone` |
| 资料卡指令（profile.description） | template.json → `profile.description`（第一句是「每次对话的第一件事：检查 shijin- 技能有没有 5 个……」） |
| 店面简介（≤400 字符） | template.json → `_meta.storefront` |
| visibility | `public` |
| gettingStarted | `shijin-install`（不是 shijin-getting-started） |
| skills | 只放两个：`shijin-install`、`shijin-getting-started`（template.json → `skills`） |
| memory | template.json → `memory`（kind=log，「试金安装记录」那一条） |

**不放进卡里：** 其余 3 个技能，由 shijin-install 第一轮从标签 shijin-v0.1.0 装进去。主人的验收档案也不放。

**导出后自测（必须做）：** 用一个全新的 Bot 导入新卡，说「你好」。试金应先问一句能不能从仓库安装；回答「可以」后，回复第一句是「已装好 5 个技能（试金 v0.1.0）。」，接着是第一次见面的第 1 题。再让它 `ls` 技能目录，确认有 5 个 shijin- 技能，`shijin-check/` 里有 4 张卡、`shijin-exam/` 里有 `考试卡.md`。

**导出前检查：** `python3 tools/pack.py --check` 显示最新；仓库是公开的；卡里没有密钥、内部网址、真实客户信息。
