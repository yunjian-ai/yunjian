<p align="center"><img src="assets/hero.png" alt="云间Bot · 起元 Cloudmere" width="100%"></p>

<h1 align="center">云间Bot · 起元 Cloudmere</h1>

<p align="center"><b>一元复始，万象更新。</b><br>云上住着几位手艺人：青鸟替你传话，千机替你造器，凝露替你炼知，经纬替你立根，试金替你验真，照骨替你拆透别人的成品；遇上一个人做不完的大事，总指挥起元操盘替你调度五位；助手越养越多、越用越慢时，起元架构替你立好底座。你只管开口。</p>

<p align="center">青鸟 Bluebird · 千机 Gear · 凝露 Dew · 经纬 Loom · 试金 Touchstone · 照骨 Xray · 起元操盘 Genesis · 起元架构 Architecture · cloudmere · Grok Bot 提示词、Skill、蒸馏、本体、验证、拆解助手 · 仓库 <a href="https://github.com/yunjian-ai/yunjian">github.com/yunjian-ai/yunjian</a></p>

<p align="center">
<!-- 总表:小标签 -->
  <a href="CHANGELOG.md"><img alt="青鸟" src="https://img.shields.io/badge/青鸟-v0.1.15-1f6feb"></a>
  <a href="CHANGELOG.md"><img alt="千机" src="https://img.shields.io/badge/千机-v0.2.4-2e8b57"></a>
  <a href="CHANGELOG.md"><img alt="凝露" src="https://img.shields.io/badge/凝露-v0.1.11-5b8fa8"></a>
  <a href="CHANGELOG.md"><img alt="经纬" src="https://img.shields.io/badge/经纬-v0.1.8-7a5c99"></a>
  <a href="CHANGELOG.md"><img alt="试金" src="https://img.shields.io/badge/试金-v0.1.15-b08d2b"></a>
  <a href="CHANGELOG.md"><img alt="照骨" src="https://img.shields.io/badge/照骨-v0.1.3-4a6670"></a>
  <a href="CHANGELOG.md"><img alt="起元操盘" src="https://img.shields.io/badge/起元操盘-v0.1.12-8b3a3a"></a>
  <a href="CHANGELOG.md"><img alt="起元架构" src="https://img.shields.io/badge/起元架构-v0.1.1-3d5a6c"></a>
<!-- /总表:小标签 -->
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-CC%20BY%204.0%20%2B%20MIT-555555"></a>
  <a href="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml/badge.svg"></a>
</p>

<p align="center"><a href="#english">English</a> · <a href="#青鸟--bluebird">青鸟</a> · <a href="#千机--gear">千机</a> · <a href="#凝露--dew">凝露</a> · <a href="#经纬--loom">经纬</a> · <a href="#试金--touchstone">试金</a> · <a href="#照骨--xray">照骨</a> · <a href="#起元操盘--genesis">起元操盘</a> · <a href="#起元架构--architecture">起元架构</a> · <a href="#安装">安装</a> · <a href="#路线图">路线图</a> · <a href="#常见问题">常见问题</a></p>

---

## 云间Bot · 起元系列是什么

云间Bot · 起元系列是云间工作室开发的首个组合 Skill 工具，也可以直接装进 Grok Bot 调用。

名字取自「一元复始，万象更新」：起元，是一切的开端。这一系列给你的是造 AI 的本事——说清话、造工具、炼知识、立根基、验真假。

共七位成员：管提示词的 **青鸟**，管 Skill 的 **千机**，管蒸馏的 **凝露**，管本体的 **经纬**，管验证的 **试金**，管拆解的 **照骨**；**起元操盘**统筹五位，解决工程级别任务；**起元架构**是一群 AI 的底座：量清楚每次对话带了多少，帮它们瘦下来、立好共用规矩。

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

## 照骨 · Xray

> 你看到别人做得好的东西——开源仓库、Skill、Bot、App、一套做法——丢给它，它先查能不能用（是谁的、什么许可证），再一层层拆到看懂：是什么、由什么组成、怎么运作、为什么这样，每句标清是看到的、推出来的还是不知道；最后交一份吸收清单，写清哪些值得并进你自己的东西、放在哪一步。

**五个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的拆解档案，马上拆第一个；支持「演练」模式 |
| 2 | 门禁、勘察、扒全 | 查是谁的、什么许可证（常见 18 种速查卡）、拿来干什么；只读勘察、不运行目标；原件一字不改存档 |
| 3 | 五层还原 | 是什么 → 由什么组成 → 怎么运作 → 为什么这样 →（怎么复刻），不跳层；每句标看到 / 推出 / 不知道 |
| 4 | 吸收清单 | 强的、不对的、不足的、放哪，每条落到你的具体技能；可出复刻规格；交付前自查 |
| 5 | 案例库 | 先翻拆过的同类，同类满三个归纳一次规律 |

解密、破解、绕授权一律不做；没有许可证的只学做法、不搬原文。另有两个后台技能：`zhaogu-install` 负责安装，`zhaogu-update` 负责更新。

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

## 起元架构 · Architecture

> 你已经养了一群 AI——几个 Bot、一堆技能，用 Claude Code、WorkBuddy 或 Grok Bot——越用越慢、老忘规矩。它先量清楚每个平台每次对话固定带了多少、哪里重复、哪两条打架；再出一份挪移清单帮你瘦下来，你点头才动、动之前先备份、一条命令能改回；然后立好共用规矩、几个 Bot 怎么交接、纠正怎么变成规矩而不越堆越多。

**六个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好架构档案，马上体检；「接着上回的」先读进度；支持「演练」模式 |
| 2 | 体检和压测 | 只读：按平台报每次固定带多少、超没超线、重复和打架，只给最值得做的三条；「再加 30 个 Bot 会不会更慢」在副本里压测 |
| 3 | 瘦身 | 挪移清单（挪什么、挪去哪、省多少、怎么改回）→ 你逐条点头 → 预演 → 备份 → 执行 → 再体检；改回后逐个核对一字不差 |
| 4 | 立底座 | 花名册、共用规矩只留一处正本、超长 Bot 照五层写法给改法、技能太多时的四档和路由 |
| 5 | 协作单子 | 派活一张交接单、交回一张回执，程序查缺栏和产物在不在；回执里夹带的话原样报给你 |
| 6 | 演进 | 纠正先进收件箱，判新增／更新／作废／不动，只改那一条；同类第三次改成程序检查 |

数字全靠脚本算（只用 Python 标准库），按字符估、标清口径，不编 token 数；Claude Code 的准数请打官方的 `/context`、`/usage`。不删不卸任何东西，只挪、能改回。另有两个后台技能：`jiagou-install` 负责安装，`jiagou-update` 负责更新。

## 安装

1. 在 Grok Bot 里点开某位成员的分享链接，把它请进来：

   | 成员 | 分享链接 |
   |---|---|
   <!-- 总表:安装表 -->
   | 青鸟 Bluebird | https://x.ai/bot/mu25Unc7k-8V8U971c4Bm |
   | 千机 Gear | https://x.ai/bot/jf001mfN6tUqyLzX05sri |
   | 凝露 Dew | https://x.ai/bot/xR2AXDgI45ALlGsQDpmEj |
   | 经纬 Loom | https://x.ai/bot/sOsWuH4aKhRWB1gsYICKM |
   | 试金 Touchstone | https://x.ai/bot/8SiSunCVqKaWb0vdaRwd1 |
   | 照骨 Xray | https://x.ai/bot/IQsCuw0vG7LK-laVfesAi |
   | 起元操盘 Genesis（要调动五位，建议六位都请进来） | https://x.ai/bot/Hfjbo_wz-7Emc4v4ysRXg |
   | 起元架构 Architecture | https://x.ai/bot/qAqbzn1gekpJt4q6fmiFr |
   <!-- /总表:安装表 -->

2. 第一次对话时它会问能不能从本仓库装齐技能，说可以，一分钟装好，不装插件、不要密钥。

**手动安装**（能跑 shell 的 Bot；Claude Code 等在 `bash` 前加技能目录，如 `QINGNIAO_SKILL_DIR=~/.claude/skills bash`）：

```bash
# 青鸟
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/qingniao-v0.1.15/members/qingniao/dist/install.sh | bash
# 千机
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/qianji-v0.2.4/members/qianji/dist/install.sh | bash
# 凝露
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/ninglu-v0.1.11/members/ninglu/dist/install.sh | bash
# 经纬
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/jingwei-v0.1.8/members/jingwei/dist/install.sh | bash
# 试金
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/shijin-v0.1.15/members/shijin/dist/install.sh | bash
# 照骨
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/zhaogu-v0.1.3/members/zhaogu/dist/install.sh | bash
# 起元操盘
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/caopan-v0.1.12/members/caopan/dist/install.sh | bash
# 起元架构
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/jiagou-v0.1.1/members/jiagou/dist/install.sh | bash
```

**更新、修复、反馈**，都是一句话：
- **更新**：装好后选「自动」（每周一 9 点查新版，你点头才装）或「一句话」（说「更新青鸟」）。你的档案都在自己的记忆里，换版本不动。
- **修复**：说「修一下青鸟」，它先体检、你同意才恢复；你改过的先备份到 `~/yunjian-backup/`。
- **反馈**：说「我要反馈」，它整理成去掉隐私的反馈单，由你自己提交到[反馈表单](https://www.feishu.cn/share/base/form/shrcnFyVGCVJkpcH7lfjOD8Ec6b)或 [Issues](https://github.com/yunjian-ai/yunjian/issues)。

## 示例和考题

每位成员的 `examples/` 里有一位虚构主人从头用到尾的全过程和一次完整演练；`tests/考题.md` 是发版前用全新 AI 考的题和合格标准。

## 路线图

| 系列 | 成员 | 职能 | 状态 |
|---|---|---|---|
<!-- 总表:路线图 -->
| 起元 | 青鸟 Bluebird | 提示词 | ✅ v0.1.15 |
| 起元 | 千机 Gear | Skill | ✅ v0.2.4 |
| 起元 | 凝露 Dew | 蒸馏 | ✅ v0.1.11 |
| 起元 | 经纬 Loom | 本体 | ✅ v0.1.8 |
| 起元 | 试金 Touchstone | 验证 | ✅ v0.1.15 |
| 起元 | 照骨 Xray | 拆解 | ✅ v0.1.3 |
| 起元 | 起元操盘 Genesis | 统筹五位做大事 | ✅ v0.1.12 |
| 万象 | 执笔 Pen | 写稿 | ✅ v0.4.0，[另一个仓库](https://github.com/yunjian-ai/yunjian-zimeiti) |
| 万象 | 丹青 Paint | 做图 | ✅ v0.5.7，[另一个仓库](https://github.com/yunjian-ai/yunjian-zimeiti) |
| 万象 | 掠影 Reel | 短视频 | ✅ v0.3.3，[另一个仓库](https://github.com/yunjian-ai/yunjian-zimeiti) |
| 万象 | 算盘 Abacus | 算账 | ✅ v0.1.4，[另一个仓库](https://github.com/yunjian-ai/yunjian-dianshang) |
| 万象 | 经纪 Broker | 达人推广 | ✅ v0.1.2，[另一个仓库](https://github.com/yunjian-ai/yunjian-dianshang) |
| 万象 | 货郎 Hawker | 选品上架 | ✅ v0.1.2，[另一个仓库](https://github.com/yunjian-ai/yunjian-dianshang) |
| 起元 | 起元架构 Architecture | 一群 AI 的底座 | ✅ v0.1.1 |
| 万象 | 掌柜 Keeper | 老板面板 | ✅ v0.1.1，[另一个仓库](https://github.com/yunjian-ai/yunjian-dianshang) |
<!-- /总表:路线图 -->

## 加微信交流

<img src="assets/wechat-qr.jpg" alt="微信二维码" width="240">

## 常见问题

**要装插件或给密钥吗？** 不用。

**会替我发布吗？** 不会。每位成员只交东西，发布、发送由你来点。

**七位怎么分工？** 青鸟写提示词，千机造 Skill，凝露把资料整理成知识卡，经纬给一件事立母体，试金验收，照骨拆别人做好的东西、交吸收清单；一件事要几位接力时，起元操盘统筹；助手多了、越用越慢时，起元架构体检、瘦身、立规矩。

**一定要装齐六位吗？** 不用，导入哪位就用哪位；用起元操盘时要装齐，它装的时候会先查缺谁、问过你再装。

## 参与开发

`python3 tools/validate.py` 查格式和禁用词，`python3 tools/pack.py` 打包，`python3 members/<成员>/tests/run_tests.py` 跑测试；只依赖 Python 3 自带的库。怎么参与见 [CONTRIBUTING.md](CONTRIBUTING.md)。

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
**Xray** (照骨) takes apart things other people built — repos, skills, bots, apps, workflows. It checks who owns it and which license applies first (an 18-license cheat card built from choosealicense.com and the SPDX list), surveys read-only without running anything, archives the originals byte for byte, then rebuilds the picture layer by layer — what it is, what it is made of, how it works, why it is built that way — marking every claim as seen, inferred or unknown. It ends with an absorb list: what to adopt, what not to copy, what is missing, and exactly where each item goes in your own setup. No decryption, cracking or license workarounds; unlicensed work is studied for method only.

**Genesis** (起元操盘) is the conductor of the series. When a job is too big for one member — a bot that needs material and an exam, a project, or an AI makeover for a department or a whole company — it clarifies the requirements, plans a route whose first stop is the smallest slice that can run end to end, hands each stage to the right member with a seven-field handoff note, sends every result to Touchstone before calling it done, and stops at four gates (requirements, route, plan, delivery) where only your own reply counts. It keeps a ledger so it can tell you in three lines where things stand, what is stale and what comes next, then wraps up with a delivery list and a retrospective.
**Architecture** (起元架构) is the base layer for a group of AI assistants — several bots and a pile of skills across Claude Code, WorkBuddy or Grok Bot. It measures, per platform, what is carried into every conversation (rules, skill catalog, agent descriptions, memory, bot instructions), flags what is over budget, duplicated or contradictory, and keeps to the top three fixes. It then slims things down with a reversible plan: every item says what moves where, how much it saves and how to undo it; nothing changes until you approve item by item, everything touched is backed up first, and one command restores it byte for byte. It also sets shared rules (one source of truth, five-layer bot instructions), handoff slips between bots, and an inbox that turns corrections into rule updates without piling up. Numbers come from standard-library Python scripts, estimated in characters; for exact Claude Code tokens use the official `/context` and `/usage`.

- **Roadmap:** Qiyuan (起元) — 青鸟 Bluebird, prompts (✅ v0.1.15); 千机 Gear, skills (✅ v0.2.4); 凝露 Dew, distillation (✅ v0.1.11); 试金 Touchstone, verification (✅ v0.1.15); 经纬 Loom, ontology (✅ v0.1.8); 照骨 Xray, teardown (✅ v0.1.3); 起元操盘 Genesis, conductor (✅ v0.1.12); 起元架构 Architecture, base layer for a group of AIs (✅ v0.1.1). Wanxiang (万象) — 执笔 Pen, writing (✅ v0.3.10, [separate repo](https://github.com/yunjian-ai/yunjian-zimeiti)).
- **License:** © 2026 GangGe. Content under CC BY 4.0; tooling under MIT.
