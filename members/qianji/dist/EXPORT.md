# 千机分享卡怎么导出（照着做的操作单）· v0.1.4

在 Grok Bot 里导出。**导出功能只能导出发起导出的那个 Bot 自己**，所以分三步：
1. 新建一个 Bot，照 `dist/template.json`（由 `tools/pack.py` 按标签 qianji-v0.1.4 生成）原样放进下表的名字、资料卡指令、两个技能、一条记忆，一个字不改；
2. **先别让它装技能**（它一开口会问要不要装，先不答），不然分享卡里会带上全部技能；
3. 在这个 Bot 里用 `CreateBotShareJson` 导出它自己；导出后是草稿，要在卡上确认「发布」才公开。

| 参数 | 填什么 |
|---|---|
| name | `千机 Gear` |
| 资料卡指令（profile.description） | template.json → `profile.description`（第一句是「你是千机（Gear），云间里管 Skill的那位。」） |
| 店面简介（≤400 字符） | template.json → `_meta.storefront` |
| visibility | `public` |
| gettingStarted | `qianji-install`（不是 qianji-getting-started） |
| skills | 只放两个：`qianji-install`、`qianji-getting-started`（template.json → `skills`） |
| memory | template.json → `memory`（kind=log，「千机安装记录」那一条） |

**卡里不放的：** 另外 3 个技能——第一次聊天时由 qianji-install 从 qianji-v0.1.4 装上；主人的Skill 档案也不放。

**导完一定要试：** 新建一个干净的 Bot 导入这张卡，打个招呼。千机应先问一句能不能从仓库安装；回答「可以」后，回复第一句是开场白「您好，欢迎来到云间。我是起元系列的手艺人·千机，7 件工具已备好，接下来由我陪您把第一套做法造成 Skill。」，接着是第一次见面的第 1 题。然后请它列一下技能目录，应该能看到 7 个 qianji- 技能，`qianji-build/` 里有 4 张卡和 `check_skill.py`。

**导出之前先确认三件事：** 配方是最新的（`python3 tools/pack.py --check` 通过）；仓库对外公开；卡里没有密钥、内部网址和真实客户资料。
