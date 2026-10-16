# 发动机图谱 · 单图画风规范（以 ea023.html 为基准）

适用：`assets/figures/ea*.html` 全部 85 张。基准图 `ea023.html`（水平对置）。
原则：**一张图 = 一块浅灰底 + 一块底座板 + 一台白色实体机构 + 左上角一行标签**。此外什么都没有。

---

## 1. 画面

| 项 | 规定 | ea023 依据 |
|---|---|---|
| 尺寸 | `<svg id="fig" viewBox="0 0 720 440" width="720" height="440">`，`display:block;max-width:100%;height:auto` | L114 |
| 页面背景 | `body{background:#d9d9d6}`；`.iso-page{width:720px;margin:0 auto}`；无卡片、无边框、无圆角、无阴影 | L114 |
| 主题 | `<body class="iso" data-theme="light">`，只用 anatomy kit 的 light 变量；不要自定义调色 | L14-23 |
| 相机 | 默认 **方位角 az = -58°，俯角 el = 28°**（`CFG.az/el` 可按机型微调，范围 az 任意、el 20–35°）。`fitProjection(pts, 720, 440, {pad: 14, azimuth, elevation})`；缩放取 **全 360° 方位扫描的最小 scale**（`camera()` 做法），保证拖动旋转时主体永不出框、不缩放跳变 | L2040-2051 |
| 主体占比 | 包围盒（含底座板）占画面宽度 ≈ 85–92%，高度 ≈ 80–90%；主体视觉中心落在画面中心 `(360, 220)` | `pad:14` |
| 留白 | 四边最少 14px；左上角 `x<220, y<40` 区域由标签独占，机构不要顶进去（必要时 `headroom: 36`） | |
| 底座板 | 一块圆角薄板 `slabOf({x,y,w,d,r:9}, zBase-11, 11, P, 8, 1.2)`，`tone:'mid'`，厚度 **11 单位**，平面尺寸 = 机构在地面的包围盒 **每边外扩 14 单位**（前后各加 ~60 给飞轮/皮带轮余量）；板顶面加一条 `insetPlan(plan,5)` 的 `faint` 内描线；板位于所有零件之下（排序 key `-8e5`）。板下**不画投影、不画 halo、不画地平线/网格** | L2029-2064 |
| 支座 | 轴承座等支撑件从底座板顶面长出，`tone:'mid'` | L2066-2069 |

## 2. 渲染

- **只用 anatomy kit 原语**：`solidSvg` / `lineSvg` / `slabOf` / `prismOf` / `lathe` / `frameOf`，CSS 用 kit 自带 `.iso-*` 规则（L24-79）。禁止自写 canvas/WebGL/自制光照渲染器。
- **四档明暗**：侧面由 kit 的 `SHADES=4` 自动分配 `--anatomy-shade-0..3`（#dcdcd9 / #e5e5e2 / #ededea / #f4f4f1），顶面 `--anatomy-top:#ffffff`。不得改这些变量值。
- **描边**：`--anatomy-weight:.6px`，`vector-effect:non-scaling-stroke`。外轮廓 `tone:'hi'`（#26262a），折痕/棱 `crease:'faint'`（#d4d4d6）或 `'lo'`（#b4b4b8）。结构件默认 `tone:'hi'`，底座/支座/垫块 `tone:'mid'`（#8a8a8f）。
- **唯一高亮**：正在做功 / 当前关键部件用 **kit 的 `lit:true`**（白顶 + 黑边 #000），且**一帧内最多一个零件组**（ea023：仅做功气缸的活塞冠 `lit: ph < 180`）。不用橙色、不用红绿蓝 tone 填色、不用描边加粗。
  - 例外：流体流向允许 `lineSvg(..., {flow:true})` 的点线一条，tone 限 `lo`。
- **禁止**：灰塑料/金属质感、任意 `<linearGradient>/<radialGradient>`（fadeLineSvg 内置渐变除外）、`filter: drop-shadow/blur`（kit 的 halo 也不用）、`opacity<1` 的半透明壳体/剖切穿透、发光、彩色材质分区、箭头图形、尺寸标注线、辅助坐标轴、运动轨迹虚线圆。

## 3. 文字

**图内唯一允许的文字是左上角一行标签。** 实现必须与 ea023 一致：

```js
const label = (txt) => `<text x="16" y="24" style="font:600 11px ui-monospace,monospace;letter-spacing:.08em;fill:#44443f">${txt}</text>`;
// 每帧 draw() 末尾追加：
label(`${CFG.tag} · ${String(Math.round(phi)).padStart(3,'0')}°`)
```

- 位置 `x=16 y=24`，字号 11px，字重 600，等宽字体，字距 .08em，颜色 `#44443f`，全大写英文。
- 内容模板：`<英文简称> · <关键参数> · <曲轴角/相位>`，三段，用 ` · ` 分隔，总长 ≤ 32 字符。
  - 第一段：机型英文缩写（BOXER / V8 / W16 / ROTARY / VTEC / TURBO …）
  - 第二段：一个关键几何或配置参数（`180°`、`90° BANK`、`4 CYL`、`2 ROTOR`、`DOHC`）
  - 第三段：实时相位，三位补零 + `°`（`000°`–`719°`）。**若必须表达状态**（冲程名、VTEC HI/LO、涡轮 SPOOL、阀门 OPEN），只能替换或追加到第三段，如 `PWR 215°`、`HI-CAM 090°`，仍为大写英文、≤ 12 字符。
- `CFG.tag` 存前两段，如 `"BOXER · 180°"`。
- **一律删除**：仪表盘/表盘/指针、转速/温度/压力读数、图例色块与 `.iso-legend`、`plateHtml` 的四角文字（fig/title/hint/readout）、说明段落、"示意"/"Schematic"/"简化"字样、冲程名浮标（INTAKE/COMPRESSION…）、零件名引线标注、数值标注、任何中文、`faceTextSvg` 刻在零件面上的文字、SVG `<title>`（`aria-label` 保留，可中文）。
- 检查命令：`grep -c "<text" eaXXX.html` 运行时 DOM 中 `<text>` 节点数必须 **恰好 1**。

## 4. 动效

- 默认自动播放；速度 **55°/s 曲轴角**（`phi = (phi + dt*55) % 720`，四冲程以 720° 循环；二冲程/转子按自身周期取模），`dt` 上限 0.05s。
- 循环：无缝取模循环，无起停缓动、无回放。
- 交互：仅 **pointer 拖动旋转**（水平 ×0.45 → az，垂直 ×0.3 → el，el 夹在 8–70），`touch-action:none; cursor:grab`。**图内不放任何按钮、滑块、文字提示。**
- 控制 API：暴露 `window.FIG = { play(on), reset(), playing(), view(az,el), setPhi(p) }`，由 `_embed-lite.js` 的外部控件调用。
- URL 参数：`?still` / `?embed` 不自动播放；`?az=&el=&phi=` 设初始态。
- `prefers-reduced-motion: reduce` → 不自动播放，静止在 `phi=0`（或该机型最具代表性的相位），仍可拖动。

## 5. 逐张检查清单（10 项）

- [ ] 1. `viewBox="0 0 720 440"`，`body` 背景 `#d9d9d6`，无卡片/边框/阴影。
- [ ] 2. `data-theme="light"`，kit 变量未被覆盖；无自定义颜色（允许的 hex 只有 `#d9d9d6`、`#44443f` 和 kit 变量）。
- [ ] 3. 有一块 `tone:'mid'` 的圆角底座板，厚 11，排在最底；机构全部"站"在板上。
- [ ] 4. 默认 az/el 取值合理（主体不重叠成一团），全方位旋转不出框、不缩放跳变。
- [ ] 5. 运行时 `<text>` 节点恰好 1 个，位于 `(16,24)`，样式与第 3 节逐字一致。
- [ ] 6. 标签为三段 `A · B · 000°`，全大写英文，≤ 32 字符。
- [ ] 7. 源码不含 `gradient`、`filter`、`opacity=`（<1）、`iso-halo`、`iso-legend`、`iso-plate-corner`、`faceTextSvg(` 调用、`anatomy-red/green/blue` 填色、`#ff`开头的非 kit 颜色。
- [ ] 8. 同一帧 `data-lit` 零件组 ≤ 1，且对应"当前做功/关键"部件。
- [ ] 9. 速度 55°/s，`FIG.play/reset/playing/view/setPhi` 齐全，图内无按钮；加载 `_embed-lite.js`。
- [ ] 10. `prefers-reduced-motion` 下静止；`?still` 生效。

## 6. 改造步骤（对已有图）

1. **删**：`plateHtml`/`.iso-plate*`/`.iso-legend` 的 DOM 与调用；所有 `faceTextSvg`、`<text>`、`<foreignObject>`、HTML 覆盖层（仪表、读数、按钮、图例、说明）；自写 `<defs>` 渐变与 filter；halo；`opacity`/半透明壳；箭头与标注线；红绿蓝 tone。
2. **换底**：复制 ea023 L2029-2037（`zBase/baseHalfX/baseY0/baseY1/pts`）和 L2060-2064 的底座板块，按本机型包围盒计算；删除原有地面、网格、投影、台架。
3. **换相机**：复制 ea023 `camera()`（L2040-2051）及 `fitProjection(... pad:14)`；设 `CFG.az/el`（默认 -58/28）；主体包围盒点集 `pts` 必须包含底座四角。
4. **换标签**：复制 L2152 `label()` 和 `draw()` 末尾追加逻辑；在 `CFG` 填 `tag`（两段）；把冲程/状态信息压进第三段，其余文字删光。
5. **换高亮**：找出"当前做功/关键"部件，仅它 `lit: <条件>`；其他零件回到 `tone:'hi'|'mid'` 默认。
6. **换动效**：对齐 55°/s、取模周期、拖动参数、`window.FIG`、`prefers-reduced-motion`、`?still/?embed`，去掉图内控件。
7. **对照清单 10 项逐条勾选**，用 `?still&phi=0` 和 `?still&phi=360` 各截一帧，与 ea023 并排比对画风。
