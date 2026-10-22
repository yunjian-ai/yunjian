<p align="center"><img src="assets/hero.png" alt="云间Bot · 起元 Cloudmere" width="100%"></p>

<h1 align="center">云间Bot · 起元 Cloudmere</h1>

<p align="center"><b>一元复始，万象更新。</b><br>云上住着几位手艺人：青鸟替你传话，千机替你造器，凝露替你炼知，试金替你验真。你只管开口。</p>

<p align="center">青鸟 Bluebird · 千机 Gear · 凝露 Dew · 试金 Touchstone · cloudmere · Grok Bot 提示词、Skill、蒸馏、验证助手 · 仓库 <a href="https://github.com/yunjian-ai/yunjian">github.com/yunjian-ai/yunjian</a></p>

<p align="center">
  <a href="CHANGELOG.md"><img alt="青鸟" src="https://img.shields.io/badge/青鸟-v0.1.6-1f6feb"></a>
  <a href="CHANGELOG.md"><img alt="千机" src="https://img.shields.io/badge/千机-v0.1.4-2e8b57"></a>
  <a href="CHANGELOG.md"><img alt="凝露" src="https://img.shields.io/badge/凝露-v0.1.2-5b8fa8"></a>
  <a href="CHANGELOG.md"><img alt="试金" src="https://img.shields.io/badge/试金-v0.1.6-b08d2b"></a>
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-CC%20BY%204.0%20%2B%20MIT-555555"></a>
  <a href="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml/badge.svg"></a>
</p>

<p align="center"><a href="#english">English</a> · <a href="#青鸟--bluebird">青鸟</a> · <a href="#千机--gear">千机</a> · <a href="#凝露--dew">凝露</a> · <a href="#试金--touchstone">试金</a> · <a href="#安装">安装</a> · <a href="#路线图">路线图</a> · <a href="#常见问题">常见问题</a></p>

---

## 云间Bot · 起元系列是什么

云间Bot · 起元系列是一组为 Bot 做的成员，装进 Grok Bot 就能用。想象云上有个小地方，住着几位手艺人：一位替你把话说清楚交给 AI，一位替你把一套做法造成能反复用的工具，一位替你把做好的东西验一验……每位手艺人只守一门手艺，导入哪位就请来哪位。他们照同一份规矩干活、用同一种方式安装、过同一套检查，版本却各管各的，互不牵连。

名字取自「一元复始，万象更新」：起元，是一切的开端。这一系列给你的是造 AI 的本事——说清话、造工具、炼知识、验真假，做哪一行都用得上。

这一次推出的是**云间Bot · 起元系列**，共四位成员：管提示词的 **青鸟**，管 Skill 的 **千机**，管蒸馏的 **凝露**，管验证的 **试金**。

## 青鸟 · Bluebird

> 你说一句想让 AI 干什么，它给你一段能直接贴进 AI 的话。

**写给谁：** 天天用 AI 做图、做视频、写文案，却常常不知道该怎么开口的人。

**它做什么**

- **说一句就交货。** 简单的事一条回复就给出提示词；你没说的细节用【】留出来并附一个例子，不先连问一串。
- **按写给谁换写法。** 文字用角色、背景、任务、格式、约束五块；出图按画幅、主体、场景、机位、光色、风格写成连贯的句子；视频把动作写成节拍，超过 10 秒按时间分段，每段重复人物和光线。
- **看对象说话。** 给 Midjourney 写英文短句、要排除的用 `--no`；推理模式的 AI 写清目标，不写死步骤。规矩依据 Anthropic、OpenAI、Google、Midjourney 的官方提示词指南。
- **长期的先问清楚。** Bot 岗位指令、长期规则、分身，一次只问一个问题，把你心里的标准问出来再写，交付带 3 道测试题和版本号。
- **改得少。** 拿来一段不好使的提示词，先说清缺了哪件，只补那几句，标出改了哪里。
- **能存能调。** 好用的提示词存进你自己的提示词库，下次说「调出某某，改成我的」就能用。
- **不编、不夸。** 你给的事实原样用；资料里夹带的「忽略之前的要求」这类话不照做，并提醒你。

**三个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的用户档案，然后马上写第一段提示词；支持「演练」模式，只打印不存 |
| 2 | 写提示词 | 认活（写还是改、写给谁、多复杂）→ 写 → 自查 → 交出提示词和一句用法 |
| 3 | 改提示词 | 判断毛病属于哪一类，只改能堵住它的最少几句，逐条标出 |

另有两个后台技能：`qingniao-install` 负责安装，`qingniao-update` 负责更新。

## 千机 · Gear

> 你有一套反复在做的做法，它帮你造成 AI 每次都照着做的 Skill，换个 AI 也照做。

**写给谁：** 和 AI 跑通过一件事、心里有一套判断标准、每天重复同一件活，想让 AI 以后都按你的来、不用每次重新交代的人。

**它做什么**

- **把跑通的流程原样收下。** 你刚和 AI 做成一件事，说一句「把刚才这套做成技能」：它只收最后走通的那条路，你纠正过 AI 的地方变成规则，走错又退回的路不收，这次的文件名、日期换成空位。
- **说不清的也能问出来。** 「好主播一看就知道」这种直觉，它像记者一样一次问一个问题，追问到「看什么、怎么打分、什么直接排除」都能照做；你没说的标准不替你编，标「待确认」。
- **按官方规格写。** 头信息、名字、介绍照 Agent Skills 官方规格写；判断、流程、知识、工具四类各用各的骨架；判断类自带「没依据就说是推测」。
- **先定试题再写，造完先试一次。** 清单、初稿、试题一起交给你；拿你判断过的真实例子，在全新对话里只给 Skill 跑一遍，对上了才定稿。自带检查脚本 `check_skill.py`，能跑程序的地方自动查格式。
- **改得稳。** 判错了只改出问题的那一条、写成通用规则，跳版本号、记一行改动，改完把以前的试题全部重跑。
- **装、审、串。** 告诉你在 Claude、Codex、WorkBuddy、Grok Bot 里各怎么装；网上下的 Skill 先逐个文件看、不运行，说清它实际会做什么；几个 Skill 接成一条线，或配成一个专门的 Bot。

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

**写给谁：** 手上资料一大堆——书、课、客户聊天记录、旧文案、录音视频，或者经验全在自己脑子里——想以后反复查、反复用，交给 AI 也能直接用的人。

**它做什么**

- **先变成文字。** 能读的直接读；录音、视频告诉你用飞书妙记这类工具转成带时间的文字；拍的书页逐页读，看不清的标出来请你补拍；经验只在脑子里的，一次问一个问题采访出来。
- **梳理。** 先看清全貌：有几份、目录和正文对不对得上、只有哪一部分；理出骨架、列出最重要的几件事，给你看一眼再动手。
- **拆到一个判断一张。** 一段话讲了五点就是五张卡；原话一字不改，名字、数字、价格照原文；出处写到第几页、第几分钟、哪条消息；原文、归纳、推测分清。故事、话术模板也能成卡。
- **往回挖逻辑。** 每个结论往回问「为什么」，原文给了理由就拆出来连上，没给就照实写「原文没给理由」；好案例反推出做法。
- **连成关系链。** 讲同一件事的合并、出处都留；说法不一样的两边都留并标出来，你来定；用有名字的关系（属于、前提、依据、举例、细化、顺序、反驳）连起来，最后出一张地图。
- **能接着做。** 大资料一块一块来，每块记进度，换个窗口说「继续」就接上。自带检查脚本 `check_cards.py`：查原话在不在原文里、出处翻不翻得回去、关系有没有连上。

**五个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的蒸馏档案，马上开始第一份；支持「演练」模式 |
| 2 | 先变成文字 | 录音、视频、图片、扫描件、聊天记录转成文字；经验靠采访 |
| 3 | 梳理 | 全貌、骨架、关键清单、拆法，给你看一眼 |
| 4 | 拆解＋逆向 | 一个判断一张卡，往回挖依据，挂关系，记进度 |
| 5 | 整合＋复用 | 合并、标出说法不一样、连关系、出地图、查一遍、交付 |

另有两个后台技能：`ninglu-install` 负责安装，`ninglu-update` 负责更新。

## 试金 · Touchstone

> 你把做好的东西交给它，它告诉你能不能交出去、哪里要改，每条都有证据。

**写给谁：** 要把东西交出去、心里却没底的人——提示词、Skill、网页、小程序做好了，不知道能不能交给客户、能不能公开。

**它做什么**

- **一个结论，一张带证据的清单。** 结论只选一种：可以交、改完再交、要重做、判不了；每条问题写清在哪、看到了什么、违反哪条、怎么改，分严重、有风险、建议三级。
- **按东西换查法。** 文字类查规则写得清不清楚、有没有打架、漏没漏情况，再拿真实案例核对；网页能跑 Lighthouse 就真跑，跑不了给步骤，再查密钥、假按钮、手机适配；小程序过一遍添加、状态、重进、删除、空值五项手测。
- **考试用真实答卷说话。** 要知道到底好不好用，它定合格线、出考题、写好委托，你拿去另一家 AI 跑，答卷交回来它逐题判；没跑过不给分。
- **防裁判的老毛病。** 两个版本对比换顺序各判一次，提醒自己长不等于好；不给自己写的东西打分。
- **交付前看收敛。** 审一轮改一轮，问题数要越来越少；连着两轮不见少，说明是方向问题，不接着修细节。
- **只查不改。** 给清单和改法，改交给做的一方；资料里夹带「直接回复可以交」这类话，照常查并指出来。

**三个技能，各干一步**

| # | 技能 | 做什么 |
|---|---|---|
| 1 | 第一次见面 | 一次问一个问题，建好你的验收档案，然后马上查第一样东西；支持「演练」模式 |
| 2 | 查 | 认类型 → 定标准 → 逐项查 → 分级 → 结论；要交出去时做交付验收，附交付清单 |
| 3 | 考 | 定合格线和考题 → 写委托交给另一家 AI → 判答卷；两个版本换顺序对比 |

另有两个后台技能：`shijin-install` 负责安装，`shijin-update` 负责更新。

## 安装

1. 在 Grok Bot 里点开某位成员的分享链接，把它请进来（链接陆续公布）。
2. 第一次对话时，它会先问你能不能从本仓库装完整技能；你说可以，大约一分钟装好，不装插件，也不要任何密钥。
3. 装好后直接开始第一次见面。

手动安装（任何能跑 shell 的 Bot，不需要 gh）：

```bash
# 青鸟
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/qingniao-v0.1.6/members/qingniao/dist/install.sh | bash
# 千机
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/qianji-v0.1.4/members/qianji/dist/install.sh | bash
# 凝露
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/ninglu-v0.1.2/members/ninglu/dist/install.sh | bash
# 试金
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/shijin-v0.1.6/members/shijin/dist/install.sh | bash
```

Claude Code 等能装 Skill 的 AI：把 `members/<成员>/skills/` 下的文件夹整个复制进技能目录即可。

**更新：** 想换新版，跟它说「更新青鸟」「更新千机」「更新凝露」或「更新试金」就行；平时它一周顶多自己看一次有没有新版，看到了先告诉你新版改了哪几处，等你点头再装。你的用户档案、提示词库、Skill 档案、蒸馏档案、验收档案都留在你自己的记忆里，换版本不会动它们。放出来的每个版本都打了标签、过了考试。

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

[`members/shijin/examples/`](members/shijin/examples/) 里是虚构店主「阿青」从第一次见面走到两版对比的全过程，以及「老林」的一次完整演练。

每位成员的 `tests/考题.md` 是考题和合格标准（青鸟、试金各 12 道，千机 15 道，凝露 18 道），每次发版前用全新的 AI 只装这位成员照做，按它判分。

## 路线图

| 系列 | 成员 | 职能 | 状态 |
|---|---|---|---|
| 起元 | 青鸟 Bluebird | 提示词 | ✅ v0.1.6 |
| 起元 | 千机 Gear | Skill | ✅ v0.1.4 |
| 起元 | 凝露 Dew | 蒸馏 | ✅ v0.1.2 |
| 起元 | 试金 Touchstone | 验证 | ✅ v0.1.6 |
| 起元 | 经纬 Loom | 本体 | 筹备中 |

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

**要装插件或者给密钥吗？** 不用。

**仓库连不上怎么办？** 青鸟先用已经装上的技能帮你写，下次对话再装。

## 参与开发

```bash
python3 tools/validate.py                    # 格式、大小、交叉引用、禁用词
python3 tools/pack.py                        # 生成各成员 dist/ 配方和分享卡
python3 members/qingniao/tests/run_tests.py  # 青鸟：夹具和反向用例
python3 members/shijin/tests/run_tests.py    # 试金：夹具和反向用例
python3 members/qianji/tests/run_tests.py    # 千机：夹具和反向用例
python3 members/ninglu/tests/run_tests.py    # 凝露：夹具和反向用例
```

脚本只依赖 Python 3 自带的库，不用另装东西。怎么参与见 [CONTRIBUTING.md](CONTRIBUTING.md)；仓库里大致是这样：

```
shared/             所有成员共用的规范和安装技能写法
tools/              检查、打包、提示词和报告的机械检查
members/qingniao/   青鸟：skills/ · examples/ · tests/ · dist/
members/qianji/     千机：skills/ · examples/ · tests/ · dist/
members/ninglu/     凝露：skills/ · examples/ · tests/ · dist/
members/shijin/     试金：skills/ · examples/ · tests/ · dist/
assets/             图片素材
```

## 许可

© 2026 GangGe。内容和代码分开授权，全文在 [LICENSE](LICENSE)：

- **文字类**（成员的技能、卡片、示例、考题，shared/ 里的规范，以及各种说明文档）用 [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)：可以转载、改编，注明「云间Bot Cloudmere · GangGe」并附上仓库地址即可。
- **工具代码**（tools/、tests/ 里的脚本、.github/、安装脚本）：MIT。

---

## English

**Cloudmere (云间Bot · 起元)** is a small set of members built for bots such as Grok Bot, each a specialist with a single craft. Qiyuan (起元, "the origin") is the first series: it gives you the craft of building AI — clear prompts, reusable skills, distilled knowledge, honest verification. Install only the ones you need; they share one set of house rules and checks, but every member is released and versioned separately.

**Bluebird**, the first member, turns one sentence of what you want into a ready-to-paste prompt. It picks the right structure for the job — text, image, video, or long-term rules and bot instructions — and for simple requests it answers in a single reply, leaving 【placeholders】 with examples instead of firing off questions. For long-term prompts it interviews you one question at a time and ships test cases and a version number. It also fixes prompts that don't work by changing as little as possible, and saves good prompts to your own prompt library.

- **Install:** open a member's share link in Grok Bot (links coming). In the first chat it asks your permission, then pulls the full skill set from a tagged release of this repo. Nothing else gets installed and no keys are needed.
- **Update:** ask it to update (e.g. 「更新青鸟」). It looks for a new release at most once a week, tells you what changed, and waits for your yes. Your profile, prompt library and review notes stay in your own memory and are left untouched.
- **Skills:** first meeting, write a prompt, fix a prompt, plus install and update.

**Touchstone**, the second member, checks what you are about to ship — prompts, skills, web pages, mini apps — and returns one verdict (ship / fix first / redo / cannot judge) plus an evidence-backed issue list graded critical, risky or suggestion. It runs real checks where it can (Lighthouse for web pages, five manual checks for apps), writes exams for another AI to take and grades the answer sheets, swaps order when comparing two versions, never grades its own work, and reviews without rewriting.
**Gear**, the third member, turns a workflow you just got working, or a judgment you have never written down, into a reusable Skill that any AI will follow. It keeps only the path that finally worked, turns your corrections into rules, follows the official Agent Skills spec, writes test cases first, delivers checklist, draft and tests together, and trial-runs the Skill in a fresh chat before calling it done. It also fixes skills with minimal changes and version bumps, shows how to install in each AI, reviews downloaded skills without running them, and chains skills or packs them into a bot.
**Dew**, the fourth member, organizes a pile of material — books, courses, chat logs, recordings, or know-how that lives only in your head — into a linked web of knowledge cards: one idea per card, original quote kept word for word, source down to the page or minute, original / summarized / inferred kept apart, named links between cards, and a map. It turns audio, video and photos into text first, works in chunks you can resume, and ships `check_cards.py` to verify quotes against the source.
- **Roadmap:** Qiyuan (起元) — 青鸟 Bluebird, prompts (✅ v0.1.6); 千机 Gear, skills (✅ v0.1.4); 凝露 Dew, distillation (✅ v0.1.2); 试金 Touchstone, verification (✅ v0.1.6); 经纬 Loom, ontology (planned).
- **License:** © 2026 GangGe. Content under CC BY 4.0; tooling under MIT.
