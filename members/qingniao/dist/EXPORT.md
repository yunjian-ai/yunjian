# 青鸟分享卡怎么导出（照着做的操作单）· v0.1.8

在 Grok Bot 里导出。**导出功能只能导出发起导出的那个 Bot 自己**，所以分三步：
1. 新建一个 Bot，照 `dist/template.json`（由 `tools/pack.py` 按标签 qingniao-v0.1.8 生成）原样放进下表的名字、资料卡指令、两个技能，一个字不改（记忆在第 3 步让它自己存）；
2. **先别让它装技能**（一打开对话它就会问要不要装，先不答）；技能库是所有 Bot 共用的，先核对库里的安装、第一次见面两个技能和 template.json 一字不差，分享卡带的是库里的内容；
3. 在这个 Bot 里发一条话：先把 memory 原样存成一条记忆，再用 `CreateBotShareJson` 导出它自己（skills 只点名下表两个，memory 只放那一条）；导出后是草稿，核对卡里描述的字数和本地一致，要在卡上确认「发布」才公开。

| 参数 | 填什么 |
|---|---|
| name | `青鸟 · Bluebird ｜ 提示词`（template.json → `profile.name`） |
| description（导出工具只有这一栏，导入后它就是新 Bot 的指令，2026-10-22 实测逐字一致） | template.json → `_meta.storefront`，空一行，再接 `profile.description`（岗位说明第一句是「你是青鸟（Bluebird），云间里管提示词的那位。」）；原样、不删换行。只放简介会丢掉岗位说明 |
| visibility | `public` |
| gettingStarted | `qingniao-install`（不是 qingniao-getting-started） |
| skills | 只放两个：`qingniao-install`、`qingniao-getting-started`（template.json → `skills`） |
| memory | template.json → `memory`（kind=log，「青鸟安装记录」那一条） |

**卡里不放的：** 另外 3 个技能——第一次聊天时由 qingniao-install 从 qingniao-v0.1.8 装上；主人的用户档案、提示词库也不放。

**导完一定要试：** 新建一个干净的 Bot 导入这张卡，打个招呼。青鸟应先问一句能不能从仓库安装；回答「可以」后，回复第一句是开场白「您好，欢迎来到云间。我是起元系列的手艺人·青鸟，5 件工具已备好，接下来由我陪您把想说的话写成 AI 听得懂的提示词。」，接着是第一次见面的第 1 题。然后请它列一下技能目录，应该能看到 5 个 qingniao- 技能，`qingniao-write/` 里有 5 张卡。

**导出之前先确认三件事：** 配方是最新的（`python3 tools/pack.py --check` 通过）；仓库对外公开；卡里没有密钥、内部网址和真实客户资料。

**发布后怎么导入实测：** 卡上「复制链接」得到 `https://x.ai/bot/<编号>`；本机运行 `open "grokbot://app/v1/bot-template?id=<编号>"` 就弹出导入窗口，点「添加 Bot」。草稿不能导入，可见范围只有 public / team。
