# Restyle A：ea001 / ea003 / ea004 / ea006 / ea007 → *k 版本（按 figure-style-spec.md 二次修订）

新文件：`assets/figures/ea001k|ea003k|ea004k|ea006k|ea007k.html` 和对应的 `.svg` 海报。登记文件是 `figures-map-restyle-A.json`。原始 ea*.html 没有改动。

## 已对齐的规范项
- **文字**：运行时 `<text>` 恰好 1 个，左上 (16,24)，样式与 spec 第 3 节一致，内容为三段大写英文：
  - ea001 `STEAM · DOUBLE-ACTING · 040°`
  - ea003 `STIRLING · BETA · 040°`
  - ea004 `LENOIR · 1-CYL DA · PWR 120°`
  - ea006 `OTTO · 4-STROKE · PWR 060°`
  - ea007 `TWO-STROKE · PORTED · SCAV 200°`
  - 冲程名已并入第三段。
- **已删除**：原标题、中文读数、冲程大字、相位环/曲线仪表、零件引线标注、蒸汽/工质流向虚线、火花星形，以及所有半透明（fill-opacity）的工质/气口色块。
- **颜色**：body 改为 `class="iso" data-theme="light"`，并内联 kit light 变量。所有填色在输出时映射到 `--anatomy-top / --anatomy-shade-3..0`（四档）。外轮廓 `--anatomy-hi`，宽 .6；折痕 `--anatomy-faint`，宽 .6；`vector-effect:non-scaling-stroke`。没有渐变、filter 或 halo。
- **高亮**：ea004 / ea006 / ea007 只在做功段把活塞剖面切换为 kit lit（`--anatomy-lit-top` + `--anatomy-lit` 黑边，带 `data-lit`），同一帧只有一组。
- **底座板**：每张都加了一块厚 11 的底座板，平面为机构包围盒外扩 14（前侧多 40），排在最底层。
- **相机**：默认 az -58 / el 28，缩放取方位扫描范围内的最小 scale，旋转时不缩放跳变。
- **动效**：速度 55°/s。拖动倍率为水平 0.45、垂直 0.3，el 夹在 8–70。`window.FIG` 新增 `view(az,el)` 和 `setPhi(p)`，原有 play/reset/playing 保留。`?still` / `?embed` 和减弱动态下都不自动播放。

## 验证
每张检查了 az -85/-58/-20/40 × 相位 40/200/560：
- 控制台：0 报错；
- `<text>` 数：12 帧都恰好为 1；
- 遮挡：没发现错误。

## 与 spec 的偏差 / 未完成
1. **没有用 kit 原语重建零件（违反 spec 第 2 节第一条）。** 实际仍用原图的几何和画家排序。输出层改为 kit light 变量、四档、细描边和 lit，但不是 `solidSvg/prismOf/lathe/slabOf` 生成的，所以没有 kit 的 seamless 车削明暗，也没有 audit 记录。底座板是直角薄板，不是 `slabOf` 圆角板，也没有 `insetPlan` 内描线。
2. **方位角被限制在 −85°…45°，没有做到 spec 要求的任意方位。** 这 5 张都是 y=0 的半剖图，原图的剖面层固定画在最上面；从背面看时剖面会盖住前面的零件，所以必须夹住方位角。
3. ea001 / ea003 没有 lit 高亮。双作用汽缸和斯特林发动机没有单一的“做功件”，而且来不及给零件加标记。
4. 主体占比偏小，ea001 / ea003 尤其明显：fit 时把 el 扫到了 70°。还没调到 spec 的 85–92%。
5. 删掉流向线和半透明工质色块后，进气/排气/扫气只能靠标签第三段和机构运动来表达。原图用颜色表达的工质状态不再可见。
