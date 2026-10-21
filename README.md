<p align="center"><img src="assets/hero.png" alt="云间 Cloudmere" width="100%"></p>

<h1 align="center">云间 Cloudmere</h1>

<p align="center"><b>一组能直接装进 Bot 的成员，每位只把一件事做好。</b></p>

<p align="center">青鸟 Bluebird · 试金 Touchstone · cloudmere · Grok Bot 提示词助手和验证助手 · 仓库 <a href="https://github.com/yunjian-ai/yunjian">github.com/yunjian-ai/yunjian</a></p>

<p align="center">
  <a href="CHANGELOG.md"><img alt="青鸟" src="https://img.shields.io/badge/青鸟-v0.1.0-1f6feb"></a>
  <a href="CHANGELOG.md"><img alt="试金" src="https://img.shields.io/badge/试金-v0.1.0-b08d2b"></a>
  <a href="LICENSE"><img alt="license" src="https://img.shields.io/badge/license-CC%20BY%204.0%20%2B%20MIT-555555"></a>
  <a href="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml"><img alt="CI" src="https://github.com/yunjian-ai/yunjian/actions/workflows/ci.yml/badge.svg"></a>
</p>

<p align="center"><a href="#english">English</a> · <a href="#青鸟--bluebird">青鸟</a> · <a href="#试金--touchstone">试金</a> · <a href="#安装">安装</a> · <a href="#路线图">路线图</a> · <a href="#常见问题">常见问题</a></p>

---

## 云间是什么

云间是一个 Grok Bot 系列。云上住着几位成员，每位都是一个可以分享、一键导入的 Bot，专管一件事：写提示词、做 Skill、蒸馏资料……成员之间共用同一套规范、安装方式和检查，但各自独立发版，装一位、不装另一位都可以。

现在有两位成员：管提示词的 **青鸟**，管验证的 **试金**。

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

1. 打开成员的分享链接，导入到你的 Grok Bot（链接即将公布）。
2. 第一次对话时，它会先问你能不能从本仓库装完整技能；你说可以，大约一分钟装好，不装插件，也不要任何密钥。
3. 装好后直接开始第一次见面。

手动安装（任何能跑 shell 的 Bot，不需要 gh）：

```bash
# 青鸟
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/qingniao-v0.1.0/members/qingniao/dist/install.sh | bash
# 试金
curl -fsSL https://raw.githubusercontent.com/yunjian-ai/yunjian/shijin-v0.1.0/members/shijin/dist/install.sh | bash
```

Claude Code 等能装 Skill 的 AI：把 `members/<成员>/skills/` 下的五个文件夹复制进技能目录即可。

**更新：** 对它说一句「更新青鸟」或「更新试金」。每位成员每周最多自动检查一次，有新版先用几行话告诉你改了什么，你同意才装。你的用户档案、提示词库、验收档案都存在你自己的记忆里，更新不会覆盖。只发布打过标签、考过的版本。

**开始前想好这几样，三分钟就能用**

- 你最常让 AI 干的一两件事：做图、做视频、写文案，还是写长期规则。
- 你常用的 AI 和工具：豆包、Kimi、GPT、Claude、即梦、Midjourney……
- 你的行业、卖什么、给谁看——提示词里常要交代的背景。
- 哪些内容不能写（比如价格、客户名字、极限词）。
- 好用的提示词要不要存成提示词库，存在哪。

## 示例

[`members/qingniao/examples/`](members/qingniao/examples/) 里是青鸟对各类请求的回答：做图、视频、Midjourney、改图、模板、Bot 岗位指令、系列短片、改提示词、夹带指令、生成提示词的提示词。全部是示例数据。

[`members/shijin/examples/`](members/shijin/examples/) 里是虚构店主「阿青」从第一次见面走到两版对比的全过程，以及「老林」的一次完整演练。

每位成员的 `tests/考题.md` 是 12 道考题和合格标准，每次发版前用全新的 AI 只装这位成员照做，按它判分。

## 路线图

| 成员 | 职能 | 状态 |
|---|---|---|
| 青鸟 Bluebird | 提示词 | ✅ v0.1.0 |
| 试金 Touchstone | 验证 | ✅ v0.1.0 |
| 千机 Gear | Skill | 筹备中 |
| 凝露 Dew | 蒸馏 | 筹备中 |
| 经纬 Loom | 本体 | 筹备中 |

## 常见问题

**会替我直接写文案吗？** 青鸟只管提示词。你说「直接帮我写」，它会先问一句：要它直接写，还是要一段让 AI 写的提示词。

**简单的事也要回答一堆问题吗？** 不用。简单的事一条回复就交出提示词，没给的细节用【】留出来，或者猜一个并告诉你猜了什么。

**写出来的提示词换个 AI 还能用吗？** 能。青鸟默认按通用写法写，并在用法里说明在别的工具上要不要调；你说了用哪个工具，它就按那个工具的写法写。

**试金会替我把东西改好吗？** 不会。它只查不改，给你问题清单和改法；提示词可以交给青鸟改。

**试金说「判不了」是什么意思？** 东西没给全、或者没法真跑起来时，它不硬判，会写清还缺什么、问你一个最关键的问题。

**要装插件或者给密钥吗？** 不用。

**仓库连不上怎么办？** 青鸟先用已经装上的技能帮你写，下次对话再装。

## 参与开发

```bash
python3 tools/validate.py                    # 格式、大小、交叉引用、禁用词
python3 tools/pack.py                        # 生成各成员 dist/ 配方和分享卡
python3 members/qingniao/tests/run_tests.py  # 青鸟：夹具和反向用例
python3 members/shijin/tests/run_tests.py    # 试金：夹具和反向用例
```

只用 Python 3 标准库。规则见 [CONTRIBUTING.md](CONTRIBUTING.md)，结构如下：

```
shared/             所有成员共用的规范和安装技能写法
tools/              检查、打包、提示词和报告的机械检查
members/qingniao/   青鸟：skills/ · examples/ · tests/ · dist/
members/shijin/     试金：skills/ · examples/ · tests/ · dist/
assets/             图片素材
```

## 许可

版权所有 © 2026 杨先生。双许可，详见 [LICENSE](LICENSE)：

- **内容**（技能、示例、资料卡、记忆、考题、shared/ 和所有文档）：[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/deed.zh-hans)。转载或改编请署名「云间 Cloudmere · 杨先生」，并附仓库链接。
- **工具代码**（tools/、tests/ 里的脚本、.github/、安装脚本）：MIT。

---

## English

**Cloudmere** is a family of shareable Grok Bots called *members*. Each member does one job well and ships on its own versioned tag.

**Bluebird**, the first member, turns one sentence of what you want into a ready-to-paste prompt. It picks the right structure for the job — text, image, video, or long-term rules and bot instructions — and for simple requests it answers in a single reply, leaving 【placeholders】 with examples instead of firing off questions. For long-term prompts it interviews you one question at a time and ships test cases and a version number. It also fixes prompts that don't work by changing as little as possible, and saves good prompts to your own prompt library.

- **Install:** import Bluebird from its share link (coming soon). On first chat it asks before installing its full skill set from a pinned tag of this repo. No plugins, no keys.
- **Update:** say 「更新青鸟」 ("update Bluebird"). It checks at most weekly, summarises what changed, and installs only after you say yes. Your profile and prompt library are never overwritten.
- **Skills:** first meeting, write a prompt, fix a prompt, plus install and update.

**Touchstone**, the second member, checks what you are about to ship — prompts, skills, web pages, mini apps — and returns one verdict (ship / fix first / redo / cannot judge) plus an evidence-backed issue list graded critical, risky or suggestion. It runs real checks where it can (Lighthouse for web pages, five manual checks for apps), writes exams for another AI to take and grades the answer sheets, swaps order when comparing two versions, never grades its own work, and reviews without rewriting.
- **Roadmap:** 青鸟 Bluebird, prompts (✅ v0.1.0); 试金 Touchstone, verification (✅ v0.1.0); 千机 Gear, skills; 凝露 Dew, distillation; 经纬 Loom, ontology.
- **License:** © 2026 杨先生. Content under CC BY 4.0; tooling under MIT.
