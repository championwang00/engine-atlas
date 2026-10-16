# 规范统一 · N6 批（ea050 ea059 ea068 ea069 ea070 ea071）

依据：`figure-style-spec.md`，参考 `ea023.html`。

## 做法
6 张图共用同一套"截面切片"运行时（只有 `SCENES.<key>` 不同），所以只替换了共享运行时，场景几何不动：

- 文字：删掉引线标注（`labels`，全部中文）和"示意"字样，只保留左上角 `label()`，与 ea023 逐字一致（x16 y24，600 11px 等宽，#44443f）。
- 标签（`CFG.tag` + 相位）：
  - ea050 `SPCCI · 16:1 CR · 000°`
  - ea059 `SPARK · 1 PLUG · 000°`
  - ea068 `CHAMBER · 3 SHAPES · 000°`
  - ea069 `CVCC · PRE-CHAMBER · 000°`
  - ea070 `TJI · PRE-CHAMBER · 000°`
  - ea071 `HCCI · NO SPARK · 000°`
- 删除：`<defs>` 里的径向渐变（火焰/火花彩色光晕）、蓝色电火花折线、透明度、自定义 `.iso-edge/.iso-crease/.lab/.ldr/.inl` 描边颜色覆盖。
- 高亮：每帧最多一个零件组使用 kit 的 `lit`。取当前最强的燃烧/火花光晕，画成一枚很薄的 `lit` 小圆片，贴在截面上；电火花折线不再绘制。
- 填色：`back/under/inlays` 平面改为 kit 的 `--anatomy-shade-0/1/2` 加 `--anatomy-lo` 描边；`lines` 改为 kit `lineSvg` 的 `lo` 档。
- 底座：用 `slabOf(..., zBase-11, 11, P, 8, 1.2)` 和 `tone:'mid'`，加 `insetPlan(plan,5)` 的 faint 内线；平面取机构全周期包围盒（运行时扫描 12 帧），每边外扩 14。不画 halo、底脚和投影。
- 相机：默认 az -58 / el 28，`fitProjection pad:14`，缩放取 360° 扫描的最小值。包围点集里含底座四角。
- 动效：`phi` 以 55°/s 前进，按 720° 取模，场景 `t = phi/720`。拖动时水平 ×0.45 改 az（不限范围），垂直 ×0.3 改 el（限 8–70）。
- `window.FIG = { play, reset, playing, view, setPhi }`，保留旧的 `set` 兼容。支持 `?still`/`?embed`/`?az`/`?el`/`?phi`，以及 `prefers-reduced-motion`。保留 `_embed-lite.js`。

## 验证
用 headless Chrome（playwright）检查 4 个方位：az -58/32/122/212，phi 0/180/360/540。
- 6 张图都没有控制台错误。
- 运行时 `<text>` 都恰好 1 个，渐变或 filter 节点都是 0 个。
- 每帧 `data-lit` 不超过 1 个。
- 实体包围盒都在 720×440 以内，四边留白不少于 14px，不裁切。
- 截面朝向会随视角在前后两面之间翻转，遮挡正确。
- 用 `poster.mjs` 重新生成了 6 张 svg，每张 `<text>` 都是 1 个。

## 已知限制
- 截面切片图本身又高又窄。按 360° 最小缩放后，主体宽度约占画面 40–70%（ea068 三联图约 68%），低于规范写的 85%。高度大约占 80%。
- ea071（HCCI）的场景没有达到阈值的光晕，所以整段循环都没有 `lit` 零件。

备份：`<key>.pre-spec.html`。
