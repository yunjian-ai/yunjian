# 青鸟分享卡怎么导出（照着做的操作单）· v0.1.1

在 Grok Bot 里用 `CreateBotShareJson` 导出。每个参数都从 `dist/template.json` 原样复制（这个文件由 `tools/pack.py` 按标签 qingniao-v0.1.1 生成），不要自己改写：

| 参数 | 填什么 |
|---|---|
| name | `青鸟 Bluebird` |
| 资料卡指令（profile.description） | template.json → `profile.description`（第一句是「每次对话的第一件事：检查 qingniao- 技能有没有 5 个……」） |
| 店面简介（≤400 字符） | template.json → `_meta.storefront` |
| visibility | `public` |
| gettingStarted | `qingniao-install`（不是 qingniao-getting-started） |
| skills | 只放两个：`qingniao-install`、`qingniao-getting-started`（template.json → `skills`） |
| memory | template.json → `memory`（kind=log，「青鸟安装记录」那一条） |

**卡里不放的：** 另外 3 个技能——第一次聊天时由 qingniao-install 从 qingniao-v0.1.1 装上；主人的用户档案、提示词库也不放。

**导完一定要试：** 新建一个干净的 Bot 导入这张卡，打个招呼。青鸟应先问一句能不能从仓库安装；回答「可以」后，回复第一句是「已装好 5 个技能（青鸟 v0.1.1）。」，接着是第一次见面的第 1 题。然后请它列一下技能目录，应该能看到 5 个 qingniao- 技能，`qingniao-write/` 里有 5 张卡。

**导出之前先确认三件事：** 配方是最新的（`python3 tools/pack.py --check` 通过）；仓库对外公开；卡里没有密钥、内部网址和真实客户资料。
