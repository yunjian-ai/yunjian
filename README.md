<p align="center"><img src="assets/hero.png" alt="云间Bot · 起元 Cloudmere" width="100%"></p>

<h1 align="center">云间Bot · 起元 Cloudmere</h1>

<p align="center"><b>一元复始，万象更新。</b><br>云上住着几位手艺人：青鸟替你传话，千机替你造器，凝露替你炼知，经纬替你立根，试金替你验真；遇上一个人做不完的大事，总指挥起元操盘替你调度五位。你只管开口。</p>

<p align="center">青鸟 Bluebird · 千机 Gear · 凝露 Dew · 经纬 Loom · 试金 Touchstone · 起元操盘 Genesis · cloudmere · Grok Bot 提示词、Skill、蒸馏、本体、验证助手 · 仓库 <a href="https://github.com/yunjian-ai/yunjian">github.com/yunjian-ai/yunjian</a></p>

<p align="center">
  <a href="CHANGELOG.md"><img alt="青鸟" src="https://img.shields.io/badge/青鸟-v0.1.10-1f6feb"></a>
  <a href="CHANGELOG.md"><img alt="千机" src="https://img.shields.io/badge/千机-v0.1.9-2e8b57"></a>
  <a href="CHANGELOG.md"><img alt="凝露" src="https://img.shields.io/badge/凝露-v0.1.6-5b8fa8"></a>
  <a href="CHANGELOG.md"><img alt="经纬" src="https://img.shields.io/badge/经纬-v0.1.2-7a5c99"></a>
  <a href="CHANGELOG.md"><img alt="试金" src="https://img.shields.io/badge/试金-v0.1.10-b08d2b"></a>
  <a href="CHANGELOG.md"><img alt="起元操盘" src="https://img.shields.io/badge/起元操盘-v0.1.2-8b3a3a"></a>
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-CC%20BY%204.0%20%2B%20MIT-555555"></a>
  <a href="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml/badge.svg"></a>
</p>

<p align="center"><a href="#english">English</a> · <a href="#青鸟--bluebird">青鸟</a> · <a href="#千机--gear">千机</a> · <a href="#凝露--dew">凝露</a> · <a href="#经纬--loom">经纬</a> · <a href="#试金--touchstone">试金</a> · <a href="#起元操盘--genesis">起元操盘</a> · <a href="#安装">安装</a> · <a href="#路线图">路线图</a> · <a href="#常见问题">常见问题</a></p>

---

## 云间Bot · 起元系列是什么

云间Bot · 起元系列是一组为 Bot 做的成员，装进 Grok Bot 就能用。想象云上有个小地方，住着几位手艺人：一位替你把话说清楚交给 AI，一位替你把一套做法造成能反复用的工具，一位替你把做好的东西验一验……每位手艺人只守一门手艺，导入哪位就请来哪位。他们照同一份规矩干活、用同一种方式安装、过同一套检查，版本却各管各的，互不牵连。

名字取自「一元复始，万象更新」：起元，是一切的开端。这一系列给你的是造 AI 的本事——说清话、造工具、炼知识、立根基、验真假，做哪一行都用得上。

这一次推出的是**云间Bot · 起元系列**，共五位成员：管提示词的 **青鸟**，管 Skill 的 **千机**，管蒸馏的 **凝露**，管本体的 **经纬**，管验证的 **试金**。另有一位总指挥 **起元操盘**：五位各管一门，碰上一个人做不完的大事，由它统筹五位一起做。

## 青鸟 · Bluebird

> 你说一句想让 AI 干什么，它给你一段能直接贴进 AI 的话。

**三个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的用户档案，然后马上写第一段提示词；支持「演练」模式，只打印不存 |
| 2 | 写提示词 | 认活（写还是改、写给谁、多复杂）→ 写 → 自查 → 交出提示词和一句用法 |
| 3 | 改提示词 | 判断毛病属于哪一类，只改能堵住它的最少几句，逐条标出 |

另有两个后台技能：`qingniao-install` 负责安装，`qingniao-update` 负责更新。

## 千机 · Gear

> 你有一套反复在做的做法，它帮你造成 AI 每次都照着做的 Skill，换个 AI 也照做。

**五个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的 Skill 档案，然后马上造第一个；支持「演练」模式 |
| 2 | 收流程 | 从刚跑通的对话里抽出做法 → 清单、初稿、试题一起交 → 试用 → 定稿 |
| 3 | 造 | 采访、照你讲的、照别人的结构、打包知识卡，四种起点都能造 |
| 4 | 改 | 判错了、标准变了、叫不出来、乱出来，各有改法 |
| 5 | 装和串 | 各家 AI 的装法、装前先审、接成一条线、配成一个 Bot |

另有两个后台技能：`qianji-install` 负责安装，`qianji-update` 负责更新。

## 凝露 · Dew

> 你把一堆资料交给它，它整理成一张关系清楚的知识网：每张卡一个判断，原话原样、带出处，卡和卡之间连着关系，再配一张地图。

**五个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的蒸馏档案，马上开始第一份；支持「演练」模式 |
| 2 | 先变成文字 | 录音、视频、图片、扫描件、聊天记录转成文字；经验靠采访 |
| 3 | 梳理 | 全貌、骨架、关键清单、拆法，给你看一眼 |
| 4 | 拆解＋逆向 | 一个判断一张卡，往回挖依据，挂关系，记进度 |
| 5 | 整合＋复用 | 合并、标出说法不一样、连关系、出地图、查一遍、交付 |

另有两个后台技能：`ninglu-install` 负责安装，`ninglu-update` 负责更新。

## 经纬 · Loom

> 你要做的一件事——一家店、一个应用、一个技能——它陪你立起这件事的母体：根是什么、有哪些方面、里面有什么东西、彼此什么关系、以前做过什么、将来缺什么，知识带出处，存成以后任何人、任何 AI 都能站在上面看清全貌的底座。

**五个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的母体档案，马上立根；支持「演练」模式 |
| 2 | 立根和立经线 | 根、主干、要回答的问题；维度、东西、属性、关系、状态、谁能做什么、空枝 |
| 3 | 穿纬线 | 把资料和卡挂进母体；判同名不同义、重复、矛盾；挂不上的反过来补骨架 |
| 4 | 存成底座 | 文件夹 / Obsidian / 飞书多维表格，地图和给 AI 的用法，检查，真动作验 |
| 5 | 接着长 | 新情况、改规则、冷藏、验收、记版本 |

另有两个后台技能：`jingwei-install` 负责安装，`jingwei-update` 负责更新。

## 试金 · Touchstone

> 你把做好的东西交给它，它告诉你能不能交出去、哪里要改，每条都有证据。

**三个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的验收档案，然后马上查第一样东西；支持「演练」模式 |
| 2 | 查 | 认类型 → 定标准 → 逐项查 → 分级 → 结论；要交出去时做交付验收，附交付清单 |
| 3 | 考 | 定合格线和考题 → 写委托交给另一家 AI → 判答卷；两个版本换顺序对比 |

另有两个后台技能：`shijin-install` 负责安装，`shijin-update` 负责更新。

## 起元操盘 · Genesis

> 你要做一件一个助手做不完的大事——做一个要资料、要考试的 Bot，做一个项目，把一个部门或一家公司用 AI 梳理一遍——它问清楚、排好路线、派五位去做、每段都验过，只在四个要紧处请你拍板，最后交付、复盘。

**十个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的操盘档案；支持「演练」模式 |
| 2 | 前门 | 判断归不归它、多大、走哪几段、哪四处要你拍板；回头来就说三行 |
| 3 | 需求整理 | 问清需求，交出需求书（关口一） |
| 4 | 定路线 | 判大小、排五位、定第一站和每段验收标准（关口二） |
| 5 | 派活收活 | 写交接单派给五位，收回先交试金验 |
| 6 | 关口 | 备好建议和选项，只认你本人的回复，记进决策记录 |
| 7 | 查进度 | 在哪、什么过期、下一步 |
| 8 | 收尾 | 交付清单、签收（关口四）、复盘 |
| 9 | 记忆管家 | 什么记进项目文件、什么记进长期记忆，敏感信息不进记忆 |
| 10 | 派单给真人 | 给同事、外包写清要求和验收标准，由你转发 |

另有两个后台技能：`caopan-install` 负责安装（顺带查五位装齐没有），`caopan-update` 负责更新。

## 安装

1. 在 Grok Bot 里点开某位成员的分享链接，把它请进来：

   | 成员 | 分享链接 |
   |---|---|
   | 青鸟 Bluebird | https://x.ai/bot/9CwXPs6jsmaQ7HObWmQce |
   | 千机 Gear | https://x.ai/bot/JYKF36-3atI76W5QYdIq3 |
   | 凝露 Dew | https://x.ai/bot/9zPoGWngujInyf31EjpzL |
   | 经纬 Loom | https://x.ai/bot/yZLB_EF-gFtOe8WRFTPeq |
   | 试金 Touchstone | https://x.ai/bot/58rS6M89eG7fl_6UouP6y |
   | 起元操盘 Genesis（要调动五位，建议六位都请进来） | https://x.ai/bot/2OahtdVJ5dShzLr9yqL7U |

2. 第一次对话时，它会先问你能不能从本仓库装完整技能；你说可以，大约一分钟装好，不装插件，也不要任何密钥。
3. 装好后直接开始第一次见面。

手动安装（任何能跑 shell 的 Bot，不需要 gh）：

```bash
# 青鸟
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/qingniao-v0.1.10/members/qingniao/dist/install.sh | bash
# 千机
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/qianji-v0.1.9/members/qianji/dist/install.sh | bash
# 凝露
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/ninglu-v0.1.6/members/ninglu/dist/install.sh | bash
# 经纬
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/jingwei-v0.1.2/members/jingwei/dist/install.sh | bash
# 试金
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/shijin-v0.1.10/members/shijin/dist/install.sh | bash
# 起元操盘（它要调动五位，五位也一起装上）
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/caopan-v0.1.2/members/caopan/dist/install.sh | bash
```

Claude Code 等能装 Skill 的 AI：在上面的命令里 `bash` 前面加上技能目录，比如青鸟是 `QINGNIAO_SKILL_DIR=~/.claude/skills bash`（千机 `QIANJI_`、凝露 `NINGLU_`、经纬 `JINGWEI_`、试金 `SHIJIN_`、起元操盘 `CAOPAN_`）；也可以把 `members/<成员>/skills/` 下的文件夹整个复制进技能目录。

**更新：** 装好后它只问你一句以后怎么更新——
- **自动**（推荐）：它在 Grok Bot 里建一个每周一上午 9 点的定时任务，自己查有没有新版；有新版先告诉你改了哪几处，你点头才装。
- **一句话**：你说「更新青鸟」「更新千机」「更新凝露」「更新经纬」「更新试金」或「更新起元操盘」，它再查。

随时说「打开自动更新」「关掉自动更新」就能改。你的用户档案、提示词库、Skill 档案、蒸馏档案、母体档案、验收档案都留在你自己的记忆里，换版本不会动它们。放出来的每个版本都打了标签、过了考试。

**坏了能自己修：** 技能被删了、改乱了，跟它说「青鸟坏了」或「修一下青鸟」。它先体检（安装命令后面加 `-s -- --check`，只看不改），告诉你缺了哪个、哪个和原版不一样，你同意才恢复；你自己改过的技能会先备份到 `~/yunjian-backup/`。选了自动更新的，每周检查时也会顺带体检。

**反馈：** 用得不顺，跟它说「我要反馈」。它把问题整理成一张十行以内的反馈单，先去掉姓名、电话、账号这些隐私给你看，再给你提交的地方：[反馈表单](https://www.feishu.cn/share/base/form/shrcnFyVGCVJkpcH7lfjOD8Ec6b)（不用注册）或本仓库的 [Issues](https://github.com/yunjian-ai/yunjian/issues)。由你自己提交，它不会在后台替你发。

**开始前想好这几样，三分钟就能用**

- 你最常让 AI 干的一两件事：做图、做视频、写文案，还是写长期规则。
- 你常用的 AI 和工具：豆包、Kimi、GPT、Claude、即梦、Midjourney……
- 你的行业、卖什么、给谁看——提示词里常要交代的背景。
- 哪些内容不能写（比如价格、客户名字、极限词）。
- 好用的提示词要不要存成提示词库，存在哪。

## 示例

[`members/qingniao/examples/`](members/qingniao/examples/) 里是青鸟对各类请求的回答：做图、视频、Midjourney、改图、模板、Bot 岗位指令、系列短片、改提示词、夹带指令、生成提示词的提示词。全部是示例数据。

[`members/qianji/examples/`](members/qianji/examples/) 里是虚构茶叶店主「阿茶」从第一次见面、收流程、造、改，一直走到配成一个 Bot 的全过程，以及「小林」的一次完整演练。

[`members/ninglu/examples/`](members/ninglu/examples/) 里是虚构茶叶店主「阿茶」把一本书和一段培训录音蒸成知识网的全过程（变成文字、梳理、拆解和逆向、整合和交付），以及「小周」把客户群聊天蒸成新人手册的完整演练。

[`members/jingwei/examples/`](members/jingwei/examples/) 里是虚构茶叶店主「阿茶」给自己的茶铺立母体的全过程（第一次见面、立根和立经线、挂证据和判同名不同义、存成底座、接着长），以及「小林」给小程序搭母体的完整演练。

[`members/shijin/examples/`](members/shijin/examples/) 里是虚构店主「阿青」从第一次见面走到两版对比的全过程，以及「老林」的一次完整演练。

[`members/caopan/examples/`](members/caopan/examples/) 里是虚构操盘手「阿岚」替茶叶网店做客服 AI 化的全过程（第一次见面、需求书、路线图和关口、派活收活和查进度、派单和收尾），以及她给自己的瑜伽馆做会员咨询 Bot 的完整演练。

每位成员的 `tests/考题.md` 是考题和合格标准（青鸟、试金各 12 道，千机 15 道，凝露 18 道，经纬 17 道，起元操盘 15 道），每次发版前用全新的 AI 只装这位成员照做，按它判分。

## 路线图

| 系列 | 成员 | 职能 | 状态 |
|---|---|---|---|
| 起元 | 青鸟 Bluebird | 提示词 | ✅ v0.1.10 |
| 起元 | 千机 Gear | Skill | ✅ v0.1.9 |
| 起元 | 凝露 Dew | 蒸馏 | ✅ v0.1.6 |
| 起元 | 试金 Touchstone | 验证 | ✅ v0.1.10 |
| 起元 | 经纬 Loom | 本体 | ✅ v0.1.2 |
| 起元 | 起元操盘 Genesis | 统筹五位做大事 | ✅ v0.1.2 |

## 常见问题

**会替我直接写文案吗？** 青鸟只管提示词。你说「直接帮我写」，它会先问一句：要它直接写，还是要一段让 AI 写的提示词。

**简单的事也要回答一堆问题吗？** 不用。简单的事一条回复就交出提示词，没给的细节用【】留出来，或者猜一个并告诉你猜了什么。

**写出来的提示词换个 AI 还能用吗？** 能。青鸟默认按通用写法写，并在用法里说明在别的工具上要不要调；你说了用哪个工具，它就按那个工具的写法写。

**试金会替我把东西改好吗？** 不会。它只查不改，给你问题清单和改法；提示词可以找青鸟改，Skill 可以找千机改。

**千机和青鸟有什么不一样？** 青鸟写的是一段这一次用的提示词；千机造的是 Skill，装进 AI 以后每次开工自动带上，不用你再贴。只用一次的话，千机会建议你找青鸟。

**千机会替我把 Skill 发到网上吗？** 不会。它只给你自己发的步骤，并提醒你先查有没有密钥、手机号、客户资料。

**试金说「判不了」是什么意思？** 东西没给全、或者没法真跑起来时，它不硬判，会写清还缺什么、问你一个最关键的问题。

**凝露会把我的资料改短、删掉敏感的地方吗？** 不会。它是整理，不是删改：原话一字不改，名字、数字、价格照原文，出处写到能翻回去的位置；资料里没讲的它不补。

**凝露和千机怎么配合？** 凝露把资料整理成知识卡，千机把这套卡做成 AI 每次都带着的 Skill。

**经纬和凝露有什么不一样？** 按工程大小分：凝露把一份资料（一本书、一堆聊天记录）整理成一张知识网，是一根枝；经纬给一整件事（一家店、一个应用、一个技能）立母体——根、方方面面的维度、里面的东西和关系、以前做过的和将来要长的——是整棵树。凝露整理好的卡可以挂进经纬的母体当证据。

**经纬会帮我搭数据库、数据仓库吗？** 默认不搭。母体存成一个文件夹（也能放进 Obsidian 或飞书多维表格），任何 AI 都能读；什么时候才值得上数据仓库、图数据库，它会照实说清，并告诉你母体怎么接过去。

**要装插件或者给密钥吗？** 不用。

**仓库连不上怎么办？** 青鸟先用已经装上的技能帮你写，下次对话再装。

**起元操盘和五位是什么关系？** 五位各管一门手艺，各自就能用；起元操盘不亲手干专家的活，只在一件事要几位接力时统筹：问清、排路线、派活、验收、请你拍板。只想写一段提示词，直接找青鸟就好。

**一定要装齐六位吗？** 用起元操盘时要，它派活靠五位的技能；装它的时候会先查五位缺谁，问过你再一起装。

## 参与开发

```bash
python3 tools/validate.py                    # 格式、大小、交叉引用、禁用词
python3 tools/pack.py                        # 生成各成员 dist/ 配方和分享卡
python3 members/qingniao/tests/run_tests.py  # 青鸟：夹具和反向用例
python3 members/shijin/tests/run_tests.py    # 试金：夹具和反向用例
python3 members/qianji/tests/run_tests.py    # 千机：夹具和反向用例
python3 members/ninglu/tests/run_tests.py    # 凝露：夹具和反向用例
python3 members/jingwei/tests/run_tests.py   # 经纬：夹具和反向用例
python3 members/caopan/tests/run_tests.py    # 起元操盘：夹具和反向用例
```

脚本只依赖 Python 3 自带的库，不用另装东西。怎么参与见 [CONTRIBUTING.md](CONTRIBUTING.md)；仓库里大致是这样：

```
shared/             所有成员共用的规范和安装技能写法
tools/              检查、打包、提示词和报告的机械检查
members/qingniao/   青鸟：skills/ · examples/ · tests/ · dist/
members/qianji/     千机：skills/ · examples/ · tests/ · dist/
members/ninglu/     凝露：skills/ · examples/ · tests/ · dist/
members/jingwei/    经纬：skills/ · examples/ · tests/ · dist/
members/shijin/     试金：skills/ · examples/ · tests/ · dist/
members/caopan/     起元操盘：skills/ · examples/ · tests/ · dist/
assets/             图片素材
```

## 许可

© 2026 GangGe。内容和代码分开授权，全文在 [LICENSE](LICENSE)：

- **文字类**（成员的技能、卡片、示例、考题，shared/ 里的规范，以及各种说明文档）用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)：可以转载、改编，注明「云间Bot Cloudmere · GangGe」并附上仓库地址即可。
- **工具代码**（tools/、tests/ 里的脚本、.github/、安装脚本）：MIT。

---

## English

**Cloudmere (云间Bot · 起元)** is a small set of members built for bots such as Grok Bot, each a specialist with a single craft. Qiyuan (起元, "the origin") is the first series: it gives you the craft of building AI — clear prompts, reusable skills, distilled knowledge, solid foundations, honest verification. Install only the ones you need; they share one set of house rules and checks, but every member is released and versioned separately.

**Bluebird**, the first member, turns one sentence of what you want into a ready-to-paste prompt. It picks the right structure for the job — text, image, video, or long-term rules and bot instructions — and for simple requests it answers in a single reply, leaving 【placeholders】 with examples instead of firing off questions. For long-term prompts it interviews you one question at a time and ships test cases and a version number. It also fixes prompts that don't work by changing as little as possible, and saves good prompts to your own prompt library.

- **Install:** open a member's share link in Grok Bot (links in the 安装 section above). In the first chat it asks your permission, then pulls the full skill set from a tagged release of this repo. Nothing else gets installed and no keys are needed.
- **Update:** right after installing it asks once how you want updates: *automatic* (a weekly Monday 9 am scheduled task checks for a new release, tells you what changed and waits for your yes) or *on request* (say 「更新青鸟」). Your profile, prompt library and review notes stay in your own memory and are left untouched.
- **Self-repair:** say 「修一下青鸟」 and it runs a read-only check (`bash -s -- --check`), lists missing or altered skills, and restores the originals once you agree — anything you edited is backed up to `~/yunjian-backup/` first.
- **Feedback:** say 「我要反馈」 and it drafts a short, privacy-scrubbed report for you to review and submit yourself via the [feedback form](https://www.feishu.cn/share/base/form/shrcnFyVGCVJkpcH7lfjOD8Ec6b) or [Issues](https://github.com/yunjian-ai/yunjian/issues). It never sends anything on its own.
- **Skills:** first meeting, write a prompt, fix a prompt, plus install and update.

**Touchstone**, the second member, checks what you are about to ship — prompts, skills, web pages, mini apps — and returns one verdict (ship / fix first / redo / cannot judge) plus an evidence-backed issue list graded critical, risky or suggestion. It runs real checks where it can (Lighthouse for web pages, five manual checks for apps), writes exams for another AI to take and grades the answer sheets, swaps order when comparing two versions, never grades its own work, and reviews without rewriting.
**Gear**, the third member, turns a workflow you just got working, or a judgment you have never written down, into a reusable Skill that any AI will follow. It keeps only the path that finally worked, turns your corrections into rules, follows the official Agent Skills spec, writes test cases first, delivers checklist, draft and tests together, and trial-runs the Skill in a fresh chat before calling it done. It also fixes skills with minimal changes and version bumps, shows how to install in each AI, reviews downloaded skills without running them, and chains skills or packs them into a bot.
**Dew**, the fourth member, organizes a pile of material — books, courses, chat logs, recordings, or know-how that lives only in your head — into a linked web of knowledge cards: one idea per card, original quote kept word for word, source down to the page or minute, original / summarized / inferred kept apart, named links between cards, and a map. It turns audio, video and photos into text first, works in chunks you can resume, and ships `check_cards.py` to verify quotes against the source.
**Loom**, the fifth member, builds the ontology — the mother structure — of whatever you run: a shop, a company, an app or a single skill. It writes the roots (what it is, what for, what holds it up), the main lines, every dimension, the things in each (properties, named relations, states, who can do what), past, present and the missing branches still to grow; every fact carries its source, look-alike names are told apart instead of merged, and conflicts are laid out for you to decide. The result is a plain folder (or Obsidian / Feishu Base) with a map and a how-to for AI, plus `check_mother.py` for mechanical checks.
**Genesis** (起元操盘) is the conductor of the series. When a job is too big for one member — a bot that needs material and an exam, a project, or an AI makeover for a department or a whole company — it clarifies the requirements, plans a route whose first stop is the smallest slice that can run end to end, hands each stage to the right member with a seven-field handoff note, sends every result to Touchstone before calling it done, and stops at four gates (requirements, route, plan, delivery) where only your own reply counts. It keeps a ledger so it can tell you in three lines where things stand, what is stale and what comes next, then wraps up with a delivery list and a retrospective.
- **Roadmap:** Qiyuan (起元) — 青鸟 Bluebird, prompts (✅ v0.1.10); 千机 Gear, skills (✅ v0.1.9); 凝露 Dew, distillation (✅ v0.1.6); 试金 Touchstone, verification (✅ v0.1.10); 经纬 Loom, ontology (✅ v0.1.2); 起元操盘 Genesis, conductor (✅ v0.1.2).
- **License:** © 2026 GangGe. Content under CC BY 4.0; tooling under MIT.
