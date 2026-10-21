# 导出青鸟分享卡（给 Grok Bot 看的操作单）· v0.1.0

调用 `CreateBotShareJson`，参数全部取自同目录 `dist/template.json`（由 `tools/pack.py` 生成，标签 qingniao-v0.1.0），逐字使用，不要改写：

| 参数 | 填什么 |
|---|---|
| name | `青鸟 Bluebird` |
| 资料卡指令（profile.description） | template.json → `profile.description`（第一句是「每次对话的第一件事：检查 qingniao- 技能有没有 5 个……」） |
| 店面简介（≤400 字符） | template.json → `_meta.storefront` |
| visibility | `public` |
| gettingStarted | `qingniao-install`（不是 qingniao-getting-started） |
| skills | 只放两个：`qingniao-install`、`qingniao-getting-started`（template.json → `skills`） |
| memory | template.json → `memory`（kind=log，「青鸟安装记录」那一条） |

**不放进卡里：** 其余 3 个技能，由 qingniao-install 第一轮从标签 qingniao-v0.1.0 装进去。主人的用户档案、提示词库也不放。

**导出后自测（必须做）：** 用一个全新的 Bot 导入新卡，说「你好」。青鸟应先问一句能不能从仓库安装；回答「可以」后，回复第一句是「已装好 5 个技能（青鸟 v0.1.0）。」，接着是第一次见面的第 1 题。再让它 `ls` 技能目录，确认有 5 个 qingniao- 技能，`qingniao-write/` 里有 5 张卡。

**导出前检查：** `python3 tools/pack.py --check` 显示最新；仓库是公开的；卡里没有密钥、内部网址、真实客户信息。
