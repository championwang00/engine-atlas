# 发动机图谱首页 · 档案风格审美评审与改版方案

评审对象：`outputs/engine-atlas/index.html`（样式 `assets/atlas.css`，生成脚本 `atlas.py`）
评审方式：本地起服务，Chrome 实测 1440×900 桌面、390×844 手机，并点击「气缸布局」查看筛选态。
不改布局结构（顶栏 + 左侧年代栏 + 右侧内容区，铺满宽度，无外框）。所有图位保持空白。

---

## 0. 一句话结论

页面已经有了「规格表」的骨架（浅灰底、大标题、发丝线规格行、灰色图位、一个橙点），但它的**线条层级是倒的、字体回退失控、中英两套标签没有分层规则、橙色和胶囊按钮把档案感拉回了"现代 SaaS"**。改版不需要推翻，只要把三件事做对：**线条分三级、文字分两层（档案代码层 = 等宽英文；内容层 = 中文无衬线）、橙色只表达"当前位置"**，再把缩微胶片的四个克制元素（画格坐标、对位角标、等宽编号、胶片头信息行）放进去。

---

## 1. 实测观察

**桌面 1440px**
- 顶栏 56px：logo「发动机图谱 ENGINE ATLAS」+ 9 个圆角胶囊筛选，激活态是实心黑胶囊。
- 左栏 200px：`ERA` 小标 + 8 行年代，行间发丝线，当前项左侧橙点。
- 内容区：132px 的 Inter「Engines」，右下角 11.5px 的中文导语；下面一行 mono「显示 52 / 52 … FICHE EA-0000 · DRAFT」；再往下是组标题「~1860  4 items  蒸汽与雏形期  –（橙色）」。
- 条目卡：黑色圆点 + 中文名 + 右侧「EA-001」；**2px 黑色粗线**压在三行规格上；规格行「年份 / 1769」中间悬着一个「/」；图位是 1.25:1 的大灰块、中心十字、左下角「STEAM CAR · 图位」；最后一句中文说明。
- 一屏里灰色图位的面积占条目卡的 55% 以上，52 个灰块是页面最重的视觉元素。

**筛选态（点「气缸布局」）**
- 组标题计数正确更新为「2 items / 9 items」，空组隐藏。但左栏「全部 52」没有跟着变（内容区显示「显示 17 / 52」）；只有 2 条的组在 4 列网格里留两个空洞；meta 行没有说明当前筛选的类型；胶囊激活态是黑底白字，和橙点"当前位置"形成两套激活语言。

**手机 390px**
- 顶栏胶囊 + 年代栏胶囊叠成**两排可横滑的胶囊**（约 110px 的固定头部），年代栏下方露出一条灰色滚动条；年代胶囊里又塞了一个橙点。
- 每张卡约 700px 高（图位 286px），52 张卡滚动长度超过 3 万像素。
- 规格行拉到全宽后，「/」孤零零地悬在距右值 24px 处。

---

## 2. 风格不协调问题清单（按严重度排序）

### P0-1 线条层级倒置：条目卡比组标题重，组标题比页面标题重
- 元素：`.spec{border-top:2px solid var(--ink)}` vs `.group>header{border-bottom:1px solid var(--rule)}`（13% 透明度）vs `.top{border-bottom:1px solid var(--rule)}`。
- 为什么不协调：档案/规格表的阅读秩序是「册 > 组 > 条目 > 规格行」，线条粗细应该递减。现在页面里最粗、最黑的线出现在 52 张小卡上，而划分年代的组线只是一根淡灰发丝，页面标题下面也是发丝线。结果整页看上去是 52 个各自为政的小表格，年代分组被淹没。参考图里"规格行用发丝线"，意味着**粗线只能出现在组一级或册一级**。

### P0-2 字体回退失控：等宽字体栈没有中文，导致同一张卡里出现三种中文字体
- 元素：`--mono:"JetBrains Mono","Geist Mono",ui-monospace,Menlo,monospace`，被用于 `.spec dd`（类别值是中文：「外燃机」「雏形与循环」「待核实」）、`.tile span`（「图位」）、`.meta`（「显示 52 / 52」）、`.group .cnt`。
- 为什么不协调：JetBrains Mono 没有 CJK 字形，中文会跳过 Noto Sans SC 直接落到系统默认中文字体（Mac 上是 PingFang，Windows 上可能是微软雅黑/宋体），和标题的 Noto Sans SC、正文的 Inter+Noto 混在一张卡里。此外 `.spec dd` 对中文施加了 `text-transform:uppercase;letter-spacing:.04em`，`.item h3` 用 `font-weight:600` 而 Noto Sans SC 只加载了 400/500/700，中文标题被推到 700，比 Inter 600 的英文明显更黑。`.item p` 和 `.top p` 用 11.5px 排中文，低于中文可读下限（12px）。

### P0-3 页面有三个名字，大标题的语言和档案语义脱节
- 元素：`.bar .logo`「发动机图谱 / ENGINE ATLAS」、`.top h1`「Engines」、`<title>`「发动机图谱 Engine Atlas」。
- 为什么不协调：一个档案册只有一个册名。132px 的「Engines」是参考图式的超大无衬线，但它既不是册名（Engine Atlas），也不是中文页面的内容语言；右下角 11.5px 的中文导语和它形成 11:1 的字号比，参考图的大标题与说明比约 6–7:1。大标题本身可以保留（这是参考图的核心特征），但它要么是「发动机图谱」，要么是「Engine Atlas」，且要配一行胶片头式的 mono 信息行（册号、条目数、年份跨度、状态）来交代"这是一张档案卡的头"。

### P0-4 橙色被用在两个语义上，且折叠按钮把橙色放大成装饰
- 元素：`.rail li a[aria-current=true]::before{background:var(--orange)}`（当前年代）和 `.group .tg{color:var(--orange);font-size:22px}`（折叠「–」）。
- 为什么不协调：参考图"只用一个橙色点缀"的意思是橙色只有一个职责。现在橙点表示"你在这里"，而每个组标题右端又有一个 22px 的橙色减号，一屏里出现 2–3 个橙色减号，比橙点更显眼，读者会以为它是警示或操作入口。折叠是次要控件，应回到 `--ink-3` 的 mono 符号。

### P1-5 圆角胶囊筛选与档案语言冲突
- 元素：`.types button{border-radius:999px;border:1px solid var(--rule)}`，`[aria-pressed=true]{background:var(--ink);color:var(--panel)}`；窄屏 `.rail li a{border-radius:999px;background:#0000000a}`。
- 为什么不协调：整页的其他元素都是直角和发丝线（规格行、图位、分组线），胶囊是唯一的圆形语汇，而且是 2020 年代 SaaS 的标志性控件。实心黑胶囊的激活态又是页面上最黑的色块，抢过组标题。档案里的"类型筛选"更像索引页的标签条：直角、文字 + 等宽计数、激活态用 2px 下划线压在顶栏底线上。

### P1-6 中英混排没有分层规则
- 元素：`.group .cnt`「4 items」、`.spec dd`「DRAFT」vs「待核实」（同一字段两种语言）、`.tile span`「STEAM CAR · 图位」、`.meta`「显示 52 / 52 | FICHE EA-0000 · DRAFT」、`.rail h4`「ERA」。
- 为什么不协调：英文有时是档案代码（EA-001、FICHE），有时是内容（Steam car 是英文名），有时是界面文案（items、DRAFT）。中文同理。读者无法判断大写 mono 的「DRAFT」和中文的「待核实」是不是同一类信息。英文名只出现在图位标签里且被转成全大写，损失了作为"第二名称"的价值。

### P1-7 编号与状态的信息层级不对
- 元素：`.item h3::before`（5px 黑圆点）、`.item h3 em`（EA-001，10px mono，右对齐）、`.spec dd`「DRAFT」。
- 为什么不协调：档案的编号是画格的坐标，应该像胶片画格那样放在格子的左上角作为"眉头"（参考 `archive.css .frame .co`），现在它被挤在标题行右端最小字号。黑圆点是纯装饰项目符号，52 张卡 52 个点，没有信息。状态「DRAFT」大写 mono 比年份「1769」更醒目，但状态是最次要的字段。

### P1-8 图位占位处理：太大、太圆、标签混杂
- 元素：`.tile{aspect-ratio:1.25;border-radius:2px}`，`.tile::before/::after`（中心十字），`.tile span`「Steam car · 图位」。
- 为什么不协调：52 个 1.25:1 的灰块是页面最重的元素，使"空"成为主角；2px 圆角和周围的直角发丝线打架；中心十字的意思是"对位"，但没有角标配合，读起来像一个加号/上传按钮；标签把英文名和"图位"两类信息挤在一起。缩微胶片的空画格应该是：直角、更浅的底板、四角对位角标、左下角一个 mono 图号（FIG. 001），尺寸比现在矮一档（3:2）。

### P1-9 顶栏与左栏的层级没有拉开，三条发丝线在角上交汇
- 元素：`.bar{border-bottom:1px solid var(--rule)}`、`.rail{border-right:1px solid var(--rule)}`、`.rail li a{border-top:1px solid var(--rule)}`，`.rail{padding-top:22px}` vs `.top{padding-top:32px}`。
- 为什么不协调：顶栏、左栏、列表行全是同一根 13% 的发丝线，看不出哪条是"结构线"。左栏「ERA」小标的顶边与右侧大标题的顶边没有对齐（22px vs 32px），左右两栏像两个独立页面拼在一起。顶栏 logo 与胶囊之间没有分隔，logo 又重复了 ENGINE ATLAS。

### P1-10 组标题一行里三种字体、三个基线
- 元素：`.group h2`（Inter 34px）、`.group .cnt`（mono 11px）、`.group .nm`（Noto 12px）、`.group .tg`（Inter 22px）。
- 为什么不协调：参考图的组标题是「ACF-01  9 items」——代码 + 计数，同一个 mono 层。现在缺少年代代码（E0–E6 已在 `id` 里却没有显示），中文名和计数混在同一行且 `align-items:baseline` 后 34px 与 11px 的基线差让它们看起来悬空。「~1860」里的波浪号在 Inter 中偏高偏小，和「1861–1900」的连字符不成系统。

### P2-11 筛选态的反馈不完整
- 元素：`.rail a[data-era=all] i` 不更新；`.meta` 不显示当前类型；`.items{grid-template-columns:repeat(auto-fill,minmax(250px,1fr))}` 在 2 条时留两个空洞。
- 为什么不协调：档案检索的核心是"你现在看到的是哪一页的哪一部分"。左栏「全部 52」与内容区「显示 17 / 52」互相矛盾；没有任何地方写着"类型：气缸布局"。

### P2-12 窄屏：两排胶囊 + 露出的滚动条 + 超长卡片
- 元素：`@media(max-width:980px) .rail{flex-direction:row;...}`、`.rail ol{overflow-x:auto}`（未隐藏滚动条）、`.tile` 仍是 1.25:1。
- 为什么不协调：手机上固定头部 110px 全是胶囊；年代胶囊里再放橙点是"胶囊里的胶囊"；灰色滚动条暴露了实现细节；每张卡 700px 高让"图谱一页看全"在手机上变成 3 万像素的瀑布。

### P2-13 间距没有节奏
- 元素：`34/22/20/14/10/9/7/6/5px` 散落在 `.items gap`、`.group padding-top`、`.item h3 padding-bottom`、`.spec div padding` 等处。
- 为什么不协调：规格表的美感来自可数的节拍。建议全部落到 4px 网格，且卡内用 8/12，组间用 40/48。

### P2-14 规格行的「/」分隔列是噪音
- 元素：`.spec div{grid-template-columns:1fr 24px auto}` + `.spec span`「/」。
- 为什么不协调：发丝线本身已经是分隔，斜杠在宽卡里悬在中间，在窄卡里贴着值，两种状态都不好看。参考图的规格行只有"左标签、右值、一根发丝线"。

---

## 3. 统一设计语言：「档案 × 规格表」

### 3.1 原则
1. **两层文字**：档案代码层（编号、册号、坐标、计数、图号）= 等宽 Latin 大写；内容层（名称、类别、状态、说明、年代名）= 中文无衬线，英文名作为第二名称用无衬线小字。不再出现中文等宽、英文内容大写。
2. **三级线条**：粗细只表达层级，不表达装饰。
3. **一个橙色，一个语义**：橙色 = "当前位置/当前选择"（左栏当前年代、当前类型标签）。其他一切用墨色阶。
4. **空画格是档案的一部分，不是缺失**：直角、浅底板、四角对位角标、mono 图号。
5. **直角**：全页 `border-radius:0`。

### 3.2 色板
| 变量 | 值 | 用途 |
|---|---|---|
| `--bg` | `#EAEAE8` | 页面底（略提亮，让图位底板有层次） |
| `--plate` | `#DFDFDC` | 图位底板（比现在的 #d5d5d3 浅一档，减少灰块重量） |
| `--plate-2` | `#D4D4D1` | 图位 hover |
| `--ink` | `#151515` | 主文字、结构线 |
| `--ink-2` | `#55554F` | 说明文字、次级文字 |
| `--ink-3` | `#8A8A85` | 代码层、计数、图号 |
| `--rule` | `rgba(21,21,21,.16)` | 发丝线（L0） |
| `--rule-2` | `#151515` | 结构线（L1/L2） |
| `--orange` | `#FF4D12` | 唯一强调色，只用于"当前" |
| `--orange-ink` | `#C23A0B` | 橙色作为文字时的可读版本（AA 对比） |

不引入第二个彩色；「待核实」不用橙色，用 `--ink` 加 mono 标记「?」。

### 3.3 字体栈与字号阶梯
Google Fonts：`Inter:wght@400;500;600`、`JetBrains+Mono:wght@400;500`、`Noto+Sans+SC:wght@400;500;600`。不用衬线（Noto Serif SC 属于旧"胶片档案风"的书卷感，和规格表冲突，此处不用）。

```
--sans: "Inter","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;
--mono: "JetBrains Mono","Noto Sans SC","PingFang SC",ui-monospace,Menlo,monospace;  /* 加 CJK 回退 */
```

| 阶 | 字号/行高 | 字体 | 用途 |
|---|---|---|---|
| Display | `clamp(48px,7.2vw,104px)/.95`，500，`-.03em`（Latin -.045em） | sans | 页面大标题 |
| H2 | `28px/1`，500，tabular，`-.02em` | sans | 组年代 |
| H3 | `13.5px/1.35`，600 | sans | 条目中文名 |
| Body | `12.5px/1.6` | sans | 说明、导语 |
| Spec | `12px/1` | sans（值为数字时 mono） | 规格行 |
| Label | `10.5px/1`，500，`.08em`，uppercase | mono | 代码层：编号、坐标、计数、图号、胶片头 |
| Micro | `9.5px/1`，`.08em` | mono | 图位角落 |

中文规则：`letter-spacing` 只用于 Latin mono；中文一律 0；中文最小 12px；中文粗体只用 500/600。

### 3.4 线条体系
| 级 | 规格 | 只用于 |
|---|---|---|
| L2 结构粗线 | `2px solid var(--rule-2)` | 页面标题区底线（全页一根） |
| L1 结构线 | `1px solid var(--rule-2)` | 组标题底线、条目卡头线（名称与规格之间） |
| L0 发丝线 | `1px solid var(--rule)` | 规格行、顶栏底线、左栏右分割线（用户指定浅灰）、左栏行线、图位边框 |
| 标记 | `1px var(--ink)` @ `.35` | 图位四角对位角标 |

### 3.5 间距网格
4px 基准。
- 顶栏高 48；左栏宽 184；`--gut: clamp(16px,2vw,28px)`。
- 标题区：上 40 / 下 20；组：上 48，组标题下 16；卡网格 gap `40px 24px`。
- 卡内：眉头→名称 6；名称→头线 8；规格行 7 上 7 下；规格→图位 12；图位→说明 10。
- 左栏：顶部 padding 与标题区眉头对齐（40px）。

### 3.6 组件规范

**顶栏 `.bar`**（48px，底线 L0）
左：monogram「EA」mono 500 + 「发动机图谱」sans 600 14px；右端：mono 胶片头信息「FICHE EA-0000 · 52 FR · DRAFT」（窄屏隐藏）。中：类型标签条——直角、无边框、文字 12px 500 + mono 计数 10.5px `--ink-3`，`padding 0 12px`，占满 48px 高；激活态：文字 `--ink` + 底部 2px `--orange` 下划线压在顶栏底线上（这是橙色的第二个"当前"实例，与左栏同义）。hover：文字 `--ink`。

**年代栏 `.rail`**（184px，右侧 L0 分割线）
小标「年代 · ERA」mono；每行三列：mono 代码「E0」(`--ink-3`) / 年代 sans 500 tabular / mono 计数；行线 L0；当前行：左侧 2px 橙色内描边 `box-shadow:inset 2px 0 var(--orange)`，代码变 `--ink`。筛选后为 0 的行 `opacity:.35`，「全部」计数同步。

**组标题 `.group>header`**（底线 L1）
`E0` mono 代码（`--ink-3`，与左栏一致）→ `–1860` H2 → `蒸汽与雏形期` sans 13px `--ink-2` → 右推 `4 ITEMS` mono → 折叠 `–/+` mono 12px `--ink-3` 24×24 直角。波浪号改为「–1860」，「2011–今」保留。

**条目卡 `.item`**
1. 眉头 `.hd`：左 `EA-001` mono 500 `--ink`；右 `E0 · 01` 画格坐标 mono `--ink-3`（年代内序号）。
2. 名称 `h3`：中文 13.5px 600；其下 `small` 英文名 sans 11px `--ink-2`。
3. 头线 L1（替换现在的 2px）。
4. 规格 `.spec`：两列 `auto 1fr`，标签 sans `--ink-2`，值右对齐；数字值 mono tabular；中文值 sans；行线 L0；去掉「/」列。状态值：「草稿」`--ink-3`；「待核实」`--ink` + 前缀 mono「?」。
5. 图位 `.tile`：`aspect-ratio:3/2`，底 `--plate`，边框 L0，四角 8px 对位角标（`.35` 透明度），左下 mono「FIG. 001」`--ink-3`，无中心十字（十字留给日后真正放图时的对位）。必须为空。
6. 说明 `p`：12.5px/1.6 `--ink-2`，`max-width:44ch`。

**标题区 `.top`**（底线 L2）
眉头 mono「ENGINE ATLAS · FICHE EA-0000 · 52 FRAMES · 1769–2026 · DRAFT」→ Display「发动机图谱」→ 右下导语 12.5px `--ink-2` `max-width:36ch`。
（备选 B：若坚持 Latin 大标题，用「Engine Atlas」两行排，眉头改中文「发动机图谱 · 档案卡 EA-0000」；不要再用「Engines」。）
标题区下的 `.meta`：左「显示 52 / 52」，右「类型 · 全部」，均 mono，筛选时同步。

**筛选项**：见顶栏。窄屏时年代栏改成同样的直角标签条（mono 年代 + 计数，激活 2px 橙色下划线），隐藏滚动条，两条标签条共用一根 L0 底线。

**档案元素清单（只用这五个）**：胶片头信息行（标题眉头 + 顶栏右端）、画格坐标（E0 · 01）、等宽编号（EA-001 / FIG. 001）、图位对位角标、组代码（E0–E6）。不用印章、不用穿孔条、不用斜纹空格、不用旋转文字。

---

## 4. CSS 改动清单（以 `assets/atlas.css` 为基准）

> 附录 A 给出可整体替换的完整 `atlas.css`；下表按优先级列出每处改动，便于分批落地。

### P0
```css
/* 1. 变量：色板 + 等宽栈加中文回退 */
:root{
  --bg:#EAEAE8; --plate:#DFDFDC; --plate-2:#D4D4D1;
  --ink:#151515; --ink-2:#55554F; --ink-3:#8A8A85;
  --rule:rgba(21,21,21,.16); --rule-2:#151515;
  --orange:#FF4D12; --orange-ink:#C23A0B;
  --sans:"Inter","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;
  --mono:"JetBrains Mono","Noto Sans SC","PingFang SC",ui-monospace,Menlo,monospace;
  --gut:clamp(16px,2vw,28px); --bar:48px; --rail:184px;
}
html{background:var(--bg)}
body{font:12.5px/1.6 var(--sans)}
.app{grid-template-columns:var(--rail) minmax(0,1fr);background:var(--bg)}

/* 2. 线条层级：卡头线降为 1px，组线升为 1px 墨色，标题区 2px */
.spec{border-top:1px solid var(--rule-2)}
.group>header{border-bottom:1px solid var(--rule-2)}
.top{border-bottom:2px solid var(--rule-2)}

/* 3. 中文回退/字重/字号 */
.item h3{font:600 13.5px/1.35 var(--sans);letter-spacing:0;display:block;padding-bottom:8px}
.item h3::before{content:none}
.item h3 small{display:block;font:400 11px/1.4 var(--sans);color:var(--ink-2);margin-top:2px}
.item p{font-size:12.5px;line-height:1.6;max-width:44ch}
.top p{font-size:12.5px;max-width:36ch}
.spec dd{font:400 12px/1 var(--sans);text-transform:none;letter-spacing:0;text-align:right;font-variant-numeric:tabular-nums}
.spec dd.n{font-family:var(--mono)}        /* 年份 */

/* 4. 橙色只表示"当前"：折叠按钮回到墨灰 mono */
.group .tg{color:var(--ink-3);font:400 12px/1 var(--mono);width:24px;height:24px;border:1px solid var(--rule)}
.group .tg:hover{color:var(--ink);border-color:var(--ink)}
```

### P1
```css
/* 5. 筛选项：胶囊 → 直角标签条 */
.bar{height:var(--bar);gap:0;padding:0 var(--gut);background:var(--bg)}
.bar .logo{display:flex;align-items:baseline;gap:8px;padding-right:20px;margin-right:4px;border-right:1px solid var(--rule);height:100%;align-items:center}
.bar .logo b{font:500 11px var(--mono);letter-spacing:.1em;color:var(--ink-3)}
.bar .logo small{display:none}
.types{gap:0;height:100%}
.types button{height:100%;padding:0 12px;border:0;border-radius:0;border-bottom:2px solid transparent;font:500 12px/1 var(--sans);color:var(--ink-2);gap:6px;margin-bottom:-1px}
.types button i{font:400 10.5px var(--mono);color:var(--ink-3);letter-spacing:.04em}
.types button:hover{color:var(--ink)}
.types button[aria-pressed=true]{background:transparent;color:var(--ink);border-bottom-color:var(--orange)}
.types button[aria-pressed=true] i{color:var(--ink-3)}
.bar .id{margin-left:auto;flex:none;font:400 10.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}

/* 6. 条目眉头：编号 + 画格坐标 */
.item .hd{display:flex;justify-content:space-between;font:500 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin-bottom:6px}
.item .hd b{font-weight:500;color:var(--ink)}
.item h3 em{display:none}

/* 7. 规格行：两列，去掉斜杠列 */
.spec div{grid-template-columns:auto 1fr;gap:12px;padding:7px 0;font-size:12px}
.spec span{display:none}
.spec dt{font-weight:400;color:var(--ink-2)}
.spec dd[data-s="check"]{color:var(--ink)}
.spec dd[data-s="check"]::before{content:"? ";font-family:var(--mono);color:var(--ink-3)}
.spec dd[data-s="draft"]{color:var(--ink-3)}

/* 8. 图位：3:2、直角、浅底板、角标、图号 */
.tile{margin-top:12px;background:var(--plate);aspect-ratio:3/2;border-radius:0;border:1px solid var(--rule)}
.tile::before,.tile::after,.tile i{content:"";position:absolute;width:8px;height:8px;border:1px solid var(--ink);opacity:.35;background:none}
.tile::before{top:6px;left:6px;border-width:1px 0 0 1px}
.tile::after{right:6px;bottom:6px;border-width:0 1px 1px 0}
.tile i{top:6px;right:6px;border-width:1px 1px 0 0}
.tile i+i{top:auto;right:auto;bottom:6px;left:6px;border-width:0 0 1px 1px}
.tile span{left:10px;bottom:9px;font:400 9.5px var(--mono);letter-spacing:.08em;color:var(--ink-3);text-transform:uppercase}
.item:hover .tile{background:var(--plate-2)}

/* 9. 左栏：代码列 + 当前行左描边 */
.rail{top:var(--bar);height:calc(100vh - var(--bar));padding:40px 0 26px var(--gut);gap:20px}
.rail h4{font:500 10.5px var(--mono);letter-spacing:.1em}
.rail li a{grid-template-columns:22px 1fr auto;gap:8px;padding:8px 16px 8px 0;font-size:12.5px;color:var(--ink-2)}
.rail li a::before{content:attr(data-co);width:auto;height:auto;border-radius:0;background:none;font:400 10.5px var(--mono);color:var(--ink-3);letter-spacing:.06em}
.rail li a[aria-current=true]{box-shadow:inset 2px 0 var(--orange);padding-left:8px;color:var(--ink)}
.rail li a[aria-current=true]::before{background:none;color:var(--ink)}

/* 10. 组标题：代码 + 年代 + 名称 + 计数 + 折叠 */
.group{padding-top:48px}
.group>header{gap:14px;padding-bottom:16px}
.group .co{font:500 10.5px var(--mono);letter-spacing:.1em;color:var(--ink-3)}
.group h2{font:500 28px/1 var(--sans);letter-spacing:-.02em}
.group .nm{font:400 13px var(--sans);color:var(--ink-2)}
.group .cnt{margin-left:auto;font:400 10.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}
.group .tg{margin-left:0}

/* 11. 标题区：眉头 + 中文大标题 */
.top{padding:40px 0 20px;grid-template-columns:1fr minmax(0,320px)}
.top .eb{font:400 10.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-bottom:18px}
.top h1{font:500 clamp(48px,7.2vw,104px)/.95 var(--sans);letter-spacing:-.03em}
.top h1:lang(en){letter-spacing:-.045em}
.meta{padding:12px 0 0;font:400 10.5px var(--mono);letter-spacing:.06em;text-transform:none}

/* 12. 网格节奏 */
.items{gap:40px 24px;padding-top:24px;grid-template-columns:repeat(auto-fill,minmax(232px,1fr))}
```

### P2
```css
/* 13. 窄屏：两条直角标签条共用底线，隐藏滚动条，图位 16:9 */
@media (max-width:980px){
  .bar .id{display:none}
  .types{scrollbar-width:none}.types::-webkit-scrollbar{display:none}
  .rail{top:var(--bar);height:auto;flex-direction:row;padding:0 16px;gap:0;border-right:0;border-bottom:1px solid var(--rule);align-items:stretch}
  .rail ol{display:flex;gap:0;overflow-x:auto;scrollbar-width:none}
  .rail ol::-webkit-scrollbar{display:none}
  .rail li a{border:0!important;border-radius:0;background:none;padding:12px 10px;grid-template-columns:auto auto;gap:6px;white-space:nowrap;font:500 12px/1 var(--mono);border-bottom:2px solid transparent!important;margin-bottom:-1px}
  .rail li a::before{content:none}
  .rail li a[aria-current=true]{box-shadow:none;padding-left:10px;border-bottom-color:var(--orange)!important}
  .main{padding:0 16px 40px}
  .top{grid-template-columns:1fr;padding-top:28px}
  .tile{aspect-ratio:16/9}
  .group{padding-top:36px}
}
@media (max-width:620px){.items{grid-template-columns:1fr;gap:32px}}
/* 14. 全页直角 */
*{border-radius:0}
```

---

## 5. `atlas.py` 结构改动

| 优先级 | 位置 | 改动 |
|---|---|---|
| P0 | `FONTS` | Noto Sans SC 权重改为 `400;500;600`；其余不变。 |
| P0 | `status()` | 返回中文：`"待核实"` / `"草稿"`；并输出 `data-s="check"` / `"draft"` 到 `<dd>`。 |
| P0 | `.top` | 改为：`<header class="top"><div><p class="eb">Engine Atlas · Fiche EA-0000 · {len(E)} frames · 1769–2026 · Draft</p><h1>发动机图谱</h1></div><p>…导语…</p></header>`（备选 B：`<h1 lang="en">Engine<br>Atlas</h1>`，眉头改为「发动机图谱 · 档案卡 EA-0000」）。 |
| P0 | `.bar .logo` | `<a class="logo" href="#top"><b>EA</b>发动机图谱</a>`，去掉 `<small>`；在 `</nav>` 后加 `<span class="id">Fiche EA-0000 · {len(E)} fr · Draft</span>`。 |
| P1 | 条目卡 | 在 `<article>` 内先输出眉头：`<div class="hd"><b>EA-{n:03d}</b><span>{k.upper()} · {i:02d}</span></div>`（`i` 为年代内序号）；`<h3>{cn}<small>{en}</small></h3>`；`<dl class="spec">` 三行改为 `<div><dt>年份</dt><dd class="n">{ys}</dd></div><div><dt>类别</dt><dd>{TL[t]}</dd></div><div><dt>状态</dt><dd data-s="{code}">{text}</dd></div>`；图位改为 `<div class="tile" aria-hidden="true"><i></i><i></i><span>FIG. {n:03d}</span></div>`（保持空，英文名已移到 h3）。 |
| P1 | 组标题 | `<header><span class="co">{k.upper()}</span><h2>{lab}</h2><span class="nm">{name}</span><span class="cnt">{len(items)} items</span><button class="tg" aria-label="折叠"><span>–</span></button></header>`；`ERAS` 第一项标签 `"~1860"` 改为 `"–1860"`。 |
| P1 | 左栏 | `<h4>年代 · Era</h4>`；每个 `<a>` 加 `data-co="{k.upper()}"`（「全部」用 `data-co="ALL"`）。 |
| P1 | `.meta` | `<span id="shown">显示 52 / 52</span><span id="flt">类型 · 全部</span>`。 |
| P1 | JS `apply()` | 增加：更新 `.rail a[data-era=all] i` 为 `total`；更新 `#flt` 为 `'类型 · '+（当前按钮文本去掉计数）`；组计数文本改为 `i+' items'` 保持不变。折叠按钮切换时把 `span` 文本在 `–`/`+` 间切换（替代 `rotate(90deg)`）。 |
| P2 | `TYPES` | 「混动与F1」改为「混动与 F1」（中英间空格），「供油·气门·燃烧」保留。 |
| P2 | `<html>` | 在 `<h1>` 为英文时加 `lang="en"`，让 `:lang(en)` 字距规则生效。 |

---

## 6. 验收清单
- 一屏内只出现一种橙色用法（当前年代 + 当前类型下划线，同一语义）。
- 从上到下的线粗：标题区 2px > 组线 1px 墨 > 卡头线 1px 墨 > 规格/发丝 1px 16%。
- 任何中文都由 Noto Sans SC 渲染（在 DevTools 的 Rendered Fonts 里不应出现 PingFang/雅黑）。
- 所有 mono 文本都是 Latin/数字；所有中文都是 sans。
- 52 个图位全部为空，只含四角角标和 `FIG. nnn`。
- 筛选「气缸布局」后：左栏「全部 17」、meta「显示 17 / 52 · 类型 · 气缸布局」。
- 390px：固定头部 ≤ 96px，无可见滚动条，无圆角。

---

## 附录 A · 完整替换版 `assets/atlas.css`

```css
/* Engine Atlas — archive × spec sheet. Two text layers (mono Latin codes / sans Chinese content), three rule weights, one orange. */
:root{
  --bg:#EAEAE8; --plate:#DFDFDC; --plate-2:#D4D4D1;
  --ink:#151515; --ink-2:#55554F; --ink-3:#8A8A85;
  --rule:rgba(21,21,21,.16); --rule-2:#151515;
  --orange:#FF4D12; --orange-ink:#C23A0B;
  --sans:"Inter","Noto Sans SC","PingFang SC","Microsoft YaHei",sans-serif;
  --mono:"JetBrains Mono","Noto Sans SC","PingFang SC",ui-monospace,Menlo,monospace;
  --gut:clamp(16px,2vw,28px); --bar:48px; --rail:184px;
}
*{box-sizing:border-box;margin:0;border-radius:0}
html{background:var(--bg);scroll-behavior:auto}
@media (prefers-reduced-motion:no-preference){html{scroll-behavior:smooth}}
body{font:12.5px/1.6 var(--sans);color:var(--ink);-webkit-font-smoothing:antialiased}
a{color:inherit;text-decoration:none}
button{font:inherit;color:inherit;cursor:pointer;background:none;border:0}
.mono,.co,.cnt,.id,.eb{font-family:var(--mono)}

/* layout */
.app{width:100%;display:grid;grid-template-columns:var(--rail) minmax(0,1fr);min-height:100vh;background:var(--bg)}
.main{padding:0 var(--gut) 72px;min-width:0}

/* top bar: fiche header */
.bar{position:sticky;top:0;z-index:30;height:var(--bar);display:flex;align-items:stretch;padding:0 var(--gut);background:var(--bg);border-bottom:1px solid var(--rule)}
.bar .logo{flex:none;display:flex;align-items:center;gap:8px;padding-right:20px;margin-right:4px;border-right:1px solid var(--rule);font:600 14px/1 var(--sans);letter-spacing:0}
.bar .logo b{font:500 11px var(--mono);letter-spacing:.1em;color:var(--ink-3)}
.types{display:flex;min-width:0;flex:1;overflow-x:auto;scrollbar-width:none}
.types::-webkit-scrollbar{display:none}
.types button{flex:none;display:inline-flex;align-items:center;gap:6px;padding:0 12px;margin-bottom:-1px;border-bottom:2px solid transparent;font:500 12px/1 var(--sans);color:var(--ink-2);white-space:nowrap}
.types button i{font:400 10.5px var(--mono);font-style:normal;color:var(--ink-3);letter-spacing:.04em}
.types button:hover{color:var(--ink)}
.types button[aria-pressed=true]{color:var(--ink);border-bottom-color:var(--orange)}
.bar .id{margin-left:auto;flex:none;align-self:center;font:400 10.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}

/* era rail */
.rail{position:sticky;top:var(--bar);align-self:start;height:calc(100vh - var(--bar));padding:40px 0 26px var(--gut);border-right:1px solid var(--rule);display:flex;flex-direction:column;gap:20px;overflow:auto}
.rail h4{font:500 10.5px var(--mono);letter-spacing:.1em;color:var(--ink-3);text-transform:uppercase;margin-bottom:8px}
.rail ol{list-style:none;padding:0}
.rail li a{display:grid;grid-template-columns:22px 1fr auto;align-items:baseline;gap:8px;padding:8px 16px 8px 0;border-top:1px solid var(--rule);color:var(--ink-2);font-size:12.5px}
.rail li:last-child a{border-bottom:1px solid var(--rule)}
.rail li a::before{content:attr(data-co);font:400 10.5px var(--mono);letter-spacing:.06em;color:var(--ink-3)}
.rail li a b{font-weight:500;color:var(--ink);font-variant-numeric:tabular-nums}
.rail li a i{font:400 10.5px var(--mono);font-style:normal;color:var(--ink-3)}
.rail li a:hover{color:var(--ink)}
.rail li a[aria-current=true]{box-shadow:inset 2px 0 var(--orange);padding-left:8px;color:var(--ink)}
.rail li a[aria-current=true]::before{color:var(--ink)}
.rail li a.off{opacity:.35}

/* title block */
.top{display:grid;grid-template-columns:1fr minmax(0,320px);gap:var(--gut);align-items:end;padding:40px 0 20px;border-bottom:2px solid var(--rule-2)}
.top .eb{font:400 10.5px/1 var(--mono);letter-spacing:.1em;text-transform:uppercase;color:var(--ink-3);margin-bottom:18px}
.top h1{font:500 clamp(48px,7.2vw,104px)/.95 var(--sans);letter-spacing:-.03em}
.top h1:lang(en){letter-spacing:-.045em}
.top p{font-size:12.5px;line-height:1.6;color:var(--ink-2);max-width:36ch}
.meta{display:flex;justify-content:space-between;font:400 10.5px var(--mono);color:var(--ink-3);padding:12px 0 0;letter-spacing:.06em}

/* group */
.group{padding-top:48px}
.group>header{display:flex;align-items:baseline;gap:14px;padding-bottom:16px;border-bottom:1px solid var(--rule-2);scroll-margin-top:calc(var(--bar) + 16px)}
.group .co{font:500 10.5px var(--mono);letter-spacing:.1em;color:var(--ink-3)}
.group h2{font:500 28px/1 var(--sans);letter-spacing:-.02em;font-variant-numeric:tabular-nums}
.group .nm{font:400 13px var(--sans);color:var(--ink-2)}
.group .cnt{margin-left:auto;font:400 10.5px var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3)}
.group .tg{width:24px;height:24px;display:grid;place-items:center;align-self:center;border:1px solid var(--rule);color:var(--ink-3);font:400 12px/1 var(--mono)}
.group .tg:hover{color:var(--ink);border-color:var(--ink)}
.group.shut .items{display:none}

/* grid + card */
.items{display:grid;grid-template-columns:repeat(auto-fill,minmax(232px,1fr));grid-auto-flow:row dense;gap:40px 24px;padding-top:24px}
.item{min-width:0}
.item.s6{grid-column:span 2}
.item[hidden]{display:none}
.item .hd{display:flex;justify-content:space-between;font:500 10.5px/1 var(--mono);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-3);margin-bottom:6px}
.item .hd b{font-weight:500;color:var(--ink)}
.item h3{font:600 13.5px/1.35 var(--sans);padding-bottom:8px}
.item h3 small{display:block;font:400 11px/1.4 var(--sans);color:var(--ink-2);margin-top:2px}
.spec{border-top:1px solid var(--rule-2)}
.spec div{display:grid;grid-template-columns:auto 1fr;gap:12px;padding:7px 0;border-bottom:1px solid var(--rule);font-size:12px;line-height:1;align-items:baseline}
.spec dt{color:var(--ink-2)}
.spec dd{margin:0;text-align:right;font-variant-numeric:tabular-nums}
.spec dd.n{font-family:var(--mono)}
.spec dd[data-s="draft"]{color:var(--ink-3)}
.spec dd[data-s="check"]{color:var(--ink)}
.spec dd[data-s="check"]::before{content:"? ";font-family:var(--mono);color:var(--ink-3)}

/* empty figure plate: registration ticks + figure number, nothing else */
.tile{position:relative;margin-top:12px;aspect-ratio:3/2;background:var(--plate);border:1px solid var(--rule);overflow:hidden;transition:background .15s}
.s6 .tile{aspect-ratio:3/1}
.tile::before,.tile::after,.tile i{content:"";position:absolute;width:8px;height:8px;border:1px solid var(--ink);opacity:.35}
.tile::before{top:6px;left:6px;border-width:1px 0 0 1px}
.tile::after{right:6px;bottom:6px;border-width:0 1px 1px 0}
.tile i{top:6px;right:6px;border-width:1px 1px 0 0}
.tile i+i{top:auto;right:auto;bottom:6px;left:6px;border-width:0 0 1px 1px}
.tile span{position:absolute;left:10px;bottom:9px;font:400 9.5px/1 var(--mono);letter-spacing:.08em;color:var(--ink-3);text-transform:uppercase}
.item:hover .tile{background:var(--plate-2)}
.item p{margin-top:10px;font-size:12.5px;line-height:1.6;color:var(--ink-2);max-width:44ch}
.empty{display:none;padding:80px 0;color:var(--ink-3);font:12px var(--mono)}.empty.on{display:block}

/* narrow */
@media (max-width:980px){
  .app{grid-template-columns:1fr}
  .bar .id{display:none}
  .rail{position:sticky;top:var(--bar);z-index:20;height:auto;flex-direction:row;align-items:stretch;padding:0 16px;gap:0;border-right:0;border-bottom:1px solid var(--rule);background:var(--bg);overflow:hidden}
  .rail h4{display:none}
  .rail ol{display:flex;gap:0;overflow-x:auto;scrollbar-width:none}
  .rail ol::-webkit-scrollbar{display:none}
  .rail li a{border:0;border-bottom:2px solid transparent;margin-bottom:-1px;padding:12px 10px;grid-template-columns:auto auto;gap:6px;white-space:nowrap;font:500 12px/1 var(--mono)}
  .rail li:last-child a{border-bottom:2px solid transparent}
  .rail li a::before{content:none}
  .rail li a[aria-current=true]{box-shadow:none;padding-left:10px;border-bottom-color:var(--orange)}
  .main{padding:0 16px 48px}
  .top{grid-template-columns:1fr;padding-top:28px}
  .group{padding-top:36px}
  .tile{aspect-ratio:16/9}
}
@media (max-width:620px){.items{grid-template-columns:1fr;gap:32px}.item.s6{grid-column:auto}.s6 .tile{aspect-ratio:16/9}}
```
