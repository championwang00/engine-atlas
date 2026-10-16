> 2026-10-15 当前实施已完成静态可用交付并追加深度内容/预览范围；下文保留原交接基线，旧52条/30术语数量已过时。当前87稳定ID、83目录、110术语、F1独立10时段，见[DELIVERY.md](DELIVERY.md)与[最终覆盖矩阵](work/coverage-final.md)。第三轮视觉8.3/10，未达9分，按预算停止；待核实和缺图如实保留。

# 发动机图谱 Engine Atlas · 交接说明

写给接手的 AI（GPT / Codex）。读完这份文档就能继续干，不需要回看之前的对话。
最后更新：2026-10-15。

---

## 1. 项目是什么

一个面向中文读者的“汽车发动机全史”百科站：外燃机 + 内燃机（混动只记内燃机部分），**不收录纯电驱**（电机、电池、燃料电池）。
独立站，不属于 PITWALL（`/Users/chaopiwang/Desktop/F1` 里的 Next.js F1 项目）；它只是放在那个仓库的 `outputs/` 下，**不要把它接进 Next 应用**。

当前形态：纯静态 HTML（无框架），由两个 Python 脚本生成。

| 页面 | 说明 |
|---|---|
| `index.html` | 总览：52 个条目按 7 个年代分组的等大网格；顶栏 logo + 类型筛选 + 视图缩放；左栏年代导航 |
| `e/ea-001.html … ea-052.html` | 每个条目的详情页（面包屑、详细介绍、图位、事实表、上一条/下一条） |
| `glossary.html` | 术语表（30 条，悬停卡片的“术语表”去处） |
| `timeline.html layouts.html f1.html entry.html compare.html tree.html about.html` | **旧版草稿，样式已过时，没有入口**。可删除或重做，见第 7 节 |

## 2. 用户已经定下的决策（不要推翻）

内容与范围
- 独立站；中文优先；不收录电驱；不放照片（**唯一例外**：悬停卡片里的车型外观图，只用 Wikimedia Commons 自由许可图并署名）。
- 发动机示意图位**一律留空**（灰色方块，`.tile`），之后嵌入用 anatomy 技能做的等轴测图。不要用别的图填。
- 每个发动机都要有自己的详情页。
- 难懂名词要有悬停解释小卡片 + 正确的跳转逻辑；车型/发动机型号悬停要出现外观图或至少一句简介。
- 没有数据的字段**整行不显示**，不要出现“待补充”。
- 不确定的数据必须标“待核实”，不能编造；来源只用真实打开过的 URL。

视觉
- 参考 Specs 规格表风格（浅灰底、发丝线规格行、灰色图位、一个橙色点缀）+ 缩微胶片档案气质，**做减法，非必要不增加元素**。
- 布局：顶部横向导航（logo + 类型筛选）→ 左栏年代导航（只做滚动定位，没有“全部”）→ 右侧内容；铺满浏览器宽度，外面不要圈背景；空间越大，内容越多/越大。
- 字体：**IBM Plex Mono**（与 taylorpenton.com Big Bird 页面同款）+ Noto Sans SC 补中文。Big Bird 是商业字体（$25，仅拉丁），**未购买，不要使用**。
- 线条：只用一种浅灰发丝线（`--line`）；年代分组标题下是唯一的黑线（有意保留）；横线边到边并与竖线相交，不留空。
- 橙色只用于“当前所在年代”的小圆点。
- logo：四根倾斜小竖条（活塞，按 1‑3‑4‑2 顺序升降）+ 大写 `ENGINES`，宽度等于左栏宽度。
- 视图缩放：右上角 `− 100% +`，50%–300% 档位，Ctrl/⌘+滚轮、`+ - 0` 快捷键，存 localStorage。
- 转场：点击条目 → 图位放大飞到详情页位置，其余元素由近到远淡出（跨页面 View Transitions）；返回时图位缩回原卡片，并恢复原滚动位置（返回用 `history.back()`，不要用锚点跳转）。参数遵循 emil-design-engineering（≤400ms，ease-out-quint，只动 transform/opacity，支持 prefers-reduced-motion）。

## 3. 文件地图（`/Users/chaopiwang/Desktop/F1/outputs/engine-atlas/`）

生成与样式
- `atlas.py` — **主生成器**：条目数据 `E`、年代 `ERAS`、类型 `TYPES`；生成 `index.html`、`e/*.html`、`glossary.html`。
- `make.py` — 旧页面生成器；末尾 `exec(open("atlas.py"))`，所以**总是跑 `python3 make.py` 或 `python3 atlas.py`**，两者最终都会产出新版页面。
- `assets/atlas.css` — 新版全部样式（rem 单位，随视口缩放）。`assets/archive.css` 是旧页面样式，已不用于首页/详情页。
- `audit_cards.py` — 扫描详情页里“像车型但没有悬停卡”的名字。

数据（均为 JSON，id 形如 `EA-048`）
- `entries.json` — 52 个条目的 id/年份/类别/名称（由 `atlas.py` 的 `E` 导出，顺序即编号顺序）。
- `content.json` — 每个条目的 `principle / examples / tradeoffs / status / sources / verify`（来自研究大纲）。
- `intro-1…4.json` — 每个条目 3 段详细介绍 + 来源 + `verify` + `note`（联网查证）。
- `mentions-1…4.json` — 文章与“代表车型”里每个车型/发动机型号的悬停卡：`match`（原文子串）、`name`、`year`、`brief`（≤45 字）、`image`（Commons 缩略图+作者+许可）。
- `cars2.json` — “代表车型”那一行各项的配图（`mentions` 提供简介，`cars2` 提供图片）；`cars.json` 是旧版，仅作兜底。
- `terms.json` — 30 条术语（`aliases` 用于自动加链接；`entry` 映射到对应词条页）。
- `content-gaps.md`、`coverage-review.md`、`design-review.md` — 缺口清单、内容覆盖评审、设计评审。

相关文件（项目外一层）
- `/Users/chaopiwang/Desktop/F1/outputs/engines/engine-encyclopedia-outline.md` — 研究大纲（原始内容与来源）。
- `…/engines/engine-encyclopedia-plan.md` — 站点计划（信息架构、数据模型、里程碑）。
- `…/engines/{v12,v8,v6}.html`（及 `-light`）— 用 anatomy 技能做的 V 型发动机等轴测图，源码 `build.mjs / live.js / model.mjs`。

## 4. 怎么运行

```bash
cd /Users/chaopiwang/Desktop/F1/outputs/engine-atlas
python3 atlas.py                         # 重新生成 index / e/*.html / glossary.html
python3 -m http.server 8766              # 预览：http://localhost:8766/index.html
python3 audit_cards.py                   # 检查还有哪些车型名没有悬停卡
```

注意：
- 转场（View Transitions）要 Chrome 126+ / Safari 18.2+，且必须经 `http://`，不要用 `file://` 测。
- 预览时 CSS 容易被缓存，改样式后在页面里执行 `fetch('assets/atlas.css',{cache:'reload'})` 再刷新。
- 改 `atlas.py` 里的 f-string 时，JS 大括号要写成 `{{ }}`。

## 5. 数据流

```
atlas.py 里的 E（条目名/年份/类别/一句话）
   ├─ content.json     → 事实表：原理 / 代表车型 / 优点与代价 / 现状 / 来源
   ├─ intro-*.json     → 详情页左侧“详细介绍”；来源并入“来源”行
   ├─ mentions-*.json  → 介绍文章与各字段里的车型/发动机悬停卡（简介 + 图）
   ├─ cars2.json       → “代表车型”那一行各项的配图
   └─ terms.json       → 术语悬停卡 + 跳转（有词条页的跳词条，否则跳 glossary.html#id）
```

悬停链接规则：同一段文字里同一个术语/车型只在第一次出现时加链接；页面不给自己加链接；`.term` 与 `.car` 的卡片共用 `.tip`，脚本在每个详情页底部内联。

## 6. 已知问题（先处理，别带着上线）

1. **结构化字段与新介绍矛盾**（`content.json` 旧说法 vs `intro-*.json` 查证结果）。至少这些：
   - EA-001：Cugnot 速度（3 mph vs 维基 3.6 km/h；1769 为模型，全尺寸车 1770）
   - EA-004：Hippomobile “行驶约 50 英里”不符（维基约 11 km）；“热效率约 4%”无依据
   - EA-006：奥托 1876 为发动机问世，1877 才是美国专利
   - EA-011 / EA-012：直列双缸、直列六缸的起始年份（1895 Daimler Phoenix / 1903 Spyker 60 HP）
   - EA-016：Zombug 在来源页中不存在
   - EA-018：Kompressor 1921 展出、量产 1922/1923
   - EA-019：BRM H16 实际使用到 1968 赛季
   - EA-023：Subaru 年份口径（1966 EA 系列 / 1971 前驱）；Benz 水平对置双缸为 1897
   - EA-029：Jetfire 先于 Corvair Monza
   - EA-032：Nissan 300ZX 1987 “首个电控 VVT”、BMW VANOS 1992 在维基上无依据
   - EA-036：“产量近 190 万”无依据；EA-039：2.4 JTD 为首款共轨乘用车发动机
   - EA-043 / EA-047：F1 缸径上限 98 mm、2007 年 19,000 rpm 有来源；“缸径 80 × 行程 53”只有 2026 规则有来源
   - EA-044：“功率约降一半”口径不一致；EA-046：Volt 2010 交付 vs 2011–2019 车型年；EA-050：“仅日本与欧洲”只支持欧洲
   处理原则：**以来源为准**，改 `content.json`，并在 `note` 里留痕；拿不准就标“待核实”。
2. 30/52 个条目带“待核实”标签（来自大纲的 11 条待核实清单 + 无依据项），发布前应逐条打开来源核对并回写 `verify`。
3. 首页卡片文案 `atlas.py` 里的 `E` 与 `content.json` 是两份，注意同步（例如 EA-028 已改为“往复力平衡但有摇摆力矩”）。
4. 窄屏（≤760px）下的顶栏、年代条、缩放、面包屑只按规则写过，**没有实际截图验证**；超宽屏也没测。
5. Wikimedia 图片是外链加载（upload.wikimedia.org），不是本地副本；署名和许可已在卡片里显示。部署前决定是否本地化。
6. 悬停卡里“发动机型号 · 装车示例：车型名”是间接对应，不是该发动机本身的照片，卡片标题已写明。

## 7. 待办（按优先级）

P0
1. 按 `coverage-review.md` 补 **12 个条目**：侧置气门、OHV、OHC/DOHC、三元催化、ECU、化油器、点火系统、直喷柴油、涡轮柴油、柴油后处理、乙醇/灵活燃料、F1 涡轮时代 + Cosworth DFV；并把 260 D→狄塞尔、RENESIS 等→转子机、二冲程汽车→二冲程、VTEC/Valvetronic/VC-Turbo/SPCCI 降为下位变体。每个新条目都要走同一套流水线：`E` 里加一条 → `content.json` → `intro-*.json`（联网查证）→ `mentions-*.json` → 术语。
2. 解决第 6 节的矛盾与“待核实”。
3. 类别从 8 类拆到 11–12 类（新增“配气机构”“供油·点火·电控”“燃烧·排放·冷却”“柴油机”“著名机型”），年代由 7 段改 8 段（拆开 2011–今，把 1769 纳入首段名称）；F1 规则时代从条目表移出，做成单独的年代表。要同时改 `TYPES`、`ERAS`、`era_of`、首页筛选和左栏。
4. 术语库扩到 50–60 条（配气相位、OHV/OHC、爆震、EGR、三元催化、DPF、SCR、ECU 等）。

P1
5. **发动机示意图接入**（见第 8 节）：用 anatomy 技能为核心条目做图，嵌入详情页 `.fig .tile[data-embed]` 与首页卡片图位；V12/V8/V6 已有，先接这三张。要保持图位尺寸比例 720×440，并保持转场里的图位放大效果。
6. 旧页面（timeline/layouts/f1/glossary 旧版等）：删除或按新风格重做；`make.py` 的旧页面生成逻辑可一并移除。
7. 窄屏与超宽屏检查；键盘可达性（卡片、悬停卡可聚焦、`aria` 标签）；`prefers-reduced-motion`。
8. 搜索（顶栏），目前没有。

P2
9. 英文版（结构化字段 + `[locale]` 路由 + hreflang）。
10. 部署（Vercel，静态站点）：`vercel` 本地登录见 `/Users/chaopiwang/.claude/CLAUDE.md`；**部署/推送需要用户明确授权**，本文不构成授权。
11. 是否购买 Big Bird 授权并用于标题（用户尚未决定）。

## 8. anatomy 技能（GPT 没有，需要先装）

作用：生成“用真实物体解释概念”的等轴测 SVG/HTML 交互图（V12/V8/V6 就是用它做的）。MIT 许可，只用 Node 内置模块，需要 Node ≥ 20.10，检查用 Chrome/Chromium。

安装（任选一种）：
```bash
# Codex
npx skills add wheresryan22/anatomy -g -a codex          # 装到 ~/.agents/skills/anatomy
# 或直接克隆
git clone https://github.com/wheresryan22/anatomy.git ~/.agents/skills/anatomy
# Claude Code
npx skills add wheresryan22/anatomy -g -a claude-code    # 装到 ~/.claude/skills/anatomy
```
官方页面与说明：https://skills.wheresryan.sh/anatomy （打包文件 `https://skills.wheresryan.sh/anatomy/anatomy.zip`）。装好后入口文件是 `SKILL.md`，参考资料在 `references/`（`craft.md`、`kit.md`、`motion.md`、`verify.md` 等），示例在 `examples/`（`dial-indicator` 最小）。

使用本项目的发动机图时要注意：
- `outputs/engines/build.mjs` 里 import 路径写死为 `/Users/chaopiwang/.claude/skills/anatomy/…`，换机器或换目录要改成实际安装路径（Codex 通常是 `~/.agents/skills/anatomy`）。
- 构建命令：`node outputs/engines/build.mjs [v12|v8|v6]`，生成 `v12.html`、`v12-light.html` 等。
- 图的最新约束（2026-10-15）：默认显示骨架并自动播放；系统减弱动态时暂停，可手动播放。关闭“骨架视图”开关可查看封闭实体外观。旋转视角保留播放或暂停状态，Shift手动转曲轴时暂停。更完整的多模式开关（真实外观 / 关键解释 / 运动机构 / 真剖面）已记在 `engine-encyclopedia-plan.md` 末尾，**尚未实现**。
- anatomy 的 SKILL.md 要求先按“Figure / Hero / Epic”给出规模和耗时估计再动手；做多张图时建议先做 Figure 级。
- 技能自带的 `--audit` 与 `scripts/lines.mjs` 检查对发动机图**尚未跑过**，接入前应跑一遍。

## 9. 工作方式要点

- 联网查证资料是这个项目的核心：每条事实要有真实打开过的来源；与现有内容冲突时以来源为准，并在 `note` 里写明。
- Wikimedia Commons API 需要带自定义 User-Agent，且要礼貌限速（≥0.5 秒），否则会 429；只接受 CC0 / 公有领域 / CC BY / CC BY-SA；缩略图用宽 960 的 URL。
- 大批量研究任务可以拆给子代理并行（每批 ~13 个条目），输出到独立 JSON，再合并。
- 用户习惯：每次改动先说明结论和影响，诚实报告“没验证的部分”，不要夸大；批评界面时多半是对“细节一致性”的要求（对齐、线条颜色、间距）。
- 用户给过的体验反馈都在第 2 节；新增功能前先对照那一节，避免回退。

---

## 10. 给 GPT 的开场提示词（可直接粘贴）

> 你接手一个叫“发动机图谱 Engine Atlas”的静态站点项目，位置：`/Users/chaopiwang/Desktop/F1/outputs/engine-atlas/`。
> 先完整阅读 `HANDOFF.md`（里面有已定决策、文件地图、运行方式、已知问题、待办和技能安装方法），再读 `coverage-review.md`、`content-gaps.md`、`design-review.md`。
> 你的目标是把待办清单从 P0 到 P2 全部做完，并且每一步都要验证后再汇报。
>
> 工作规则：
> 1. 不推翻第 2 节的任何决策；发动机示意图位保持留空，直到你用 anatomy 技能做出图并嵌入。
> 2. 先安装 anatomy 技能（第 8 节），再做发动机图。
> 3. 所有事实必须来自你联网打开过的页面；与现有内容冲突时以来源为准并留痕；不确定标“待核实”。
> 4. 不要把项目接进 Next.js；不要 push、不要部署，除非我明确说“部署”。
> 5. 每完成一批，用本地服务器在浏览器里实际看一遍（桌面 + 390px 宽 + 悬停卡 + 转场 + 返回滚动位置），不要只靠推断；告诉我哪些你**没有**验证。
>
> 建议顺序：先解决 `HANDOFF.md` 第 6 节的矛盾 → 补 12 个条目并拆类别 → 扩术语 → 接入发动机图 → 清理旧页面 → 窄屏/可访问性检查。每做完一个大块，给我一份简短汇报：改了什么、验证了什么、还剩什么。

### 2026-10-15 转场连续性修复（第二轮）

上一轮仍可见新旧正文双曝、顶栏提前换层和模型相位交叉。当前已移除root opacity、nearby卡片快照和独立bar/rail快照，仅保留engine/plate 400ms几何变化；旧图快照隐藏，新图快照直接呈现。详情增加真实figure-viewport：海报与iframe内容使用同一rect，iframe在viewport下方保留54px控制区，避免控制条漂移。BFCache恢复时保留共享目标名称直到转场结束。默认骨架、播放、switch及历史状态保持原行为。资源版本transition-fix-2。

主场景1939×1241在真实Codex浏览器与独立Chrome连续帧中复查；6个目标/尺寸/语言/减少动态回归、慢iframe及静态包核对通过。移动目标页字体首次绘制仍可能晚约40–50ms，正文随后补绘，未宣称所有字体/网络条件均无重绘。根因、before/after、时序、验证和源码diff见work/flash-round2/delivery.md。
