# Restyle F：ea051–ea055 改用 kit 画风

产出：`assets/figures/ea051k/ea052k/ea053k/ea054k/ea055k.html`，以及同名 `.svg` 海报（`node poster.mjs`）。登记在 `figures-map-restyle-F.json`。原 ea05x.html 没有改动。

## 做法
- 每张图保留原有的场景几何、运动学、相位与动画逻辑。kit（`iso-kit.mjs`）经 `inline-kit.mjs` 的 `kitScript()` 内联，包在 IIFE 里，避免和页面的全局常量重名。
- 渲染层换成 kit 的方式：每个零件的可见面先投影，再按四档明暗分到 `iso-shade[0..3]`（朝上的面用 `iso-top`），然后经 `solidSvg`（ea051）或同样类名的逐面输出 `kitFaceParts`（ea052–055）画出来。外轮廓边用 `iso-edge tone hi`，棱线用 `iso-crease faint`，样式全部来自 kit 自带 CSS 与 light 主题变量，没有自定义调色。
- ea052–055 原本是逐面画家排序，这里保留原排序，只把面按零件分组来判定轮廓与棱线，所以遮挡关系与原图一致。ea051 原本按物体排序，同样保留。
- 按 `figure-style-spec.md`（以 ea023 为准）：
  - 图里只剩左上角一行标签（`x16 y24`，600 11px mono，#44443f）：`E-FUEL · CO2 LOOP` / `F1 2026 · V6` / `FLATHEAD · SV` / `OHV · PUSHROD` / `DOHC · 4 VALVE`，后面跟 `· 000°` 相位。
  - 删除了中文标注、读数和升程曲线小图。
  - 加了 mid 色调的底座板，厚 11，置于最底层。
  - 默认视角 az -58 / el 28，缩放取 360° 方位扫描下的最小值。
  - 曲轴角速度 55°/s；默认自动播放，`?still`、`?embed` 或减弱动态时暂停。
  - 提供 `window.FIG` 的 `play / reset / playing / view / setPhi`；可拖动旋转；`</body>` 前引用了 `_embed-lite.js`。
- 唯一高亮用 kit 的 `lit`：
  - ea051：合成反应器。
  - ea052：正在做功的活塞（沿用原图的 C.lit 判定）。
  - ea053–055：当前升程更大的那只气门（进气或排气）。

## 已验证
每张都检查了 4 个方位角 × 3 个相位：控制台无错误，运行时 `<text>` 恰好 1 个，720×440 范围内不裁切。

## 偏离与风险
- ea052：
  - 原图的半透明缸体（opacity 0.22）按规范去掉了，所以这张是骨架视图。
  - 三股气流和电流改成 kit `lineSvg` 的 lo 虚线，没有箭头、没有颜色。规范只允许一条 flow 线，这里有多条。
  - 画面构图偏乱，凸轮罩悬空。值得以后用 v6.html 的 kit 代码完整重建。
- ea051：流向点改成 kit mid 色圆点，不再区分 H₂ 和 CO₂ 的颜色。
- 圆柱仍是原渲染器的多边形棱柱，没有改成 kit `lathe`。轮廓与棱线已按 kit 规则处理，但曲面是分段的四档明暗。
- 生成脚本在 scratchpad：`restyleF/gen.mjs` 与 `*.rx.mjs`，做法是对原文件做字符串替换后重新生成。
