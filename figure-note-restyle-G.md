# restyle-G 记录（2026-10-16 08:29–08:35）

完成：ea056k / ea061k / ea062k / ea063k（html 加 svg 海报），已登记在 figures-map-restyle-G.json。
未完成：ea064（Cosworth DFV），没有生成文件。

## 做法（如实说明）
时间只有约 20 分钟，所以**没有用 kit 的 solidSvg/lathe/prismOf 重建几何**。几何、运动学、相位、标签、readout 和 `window.FIG` 接口都沿用原图代码，只把输出层改成 kit 的视觉体系：
- 整段内联 v8.html 的 kit CSS（`.iso` light 主题变量，以及 iso-fill / iso-shade[data-shade] / iso-top / iso-edge / iso-line），`body.iso[data-theme=light]`，底色用 `--anatomy-page`。
- 面按光照量化成四档：top 加 shade-3…0，面与面之间不描边；实体外轮廓用 `iso-edge` 细线（tone hi，0.6px，non-scaling）。深色件用单独一组四档深灰。
- 原来的彩色基色（催化载体米黄、hot/cool/acc 色等）统一改成 kit 单色；只有气流点、导线、图例保留语义色。
- 标签、标题、readout 改成 kit 等宽字体样式；标签去掉白框。
- ea056/062/063 共用一个多场景绘制器，替换的是 `render()`；ea061 换了调色板和描边。

## 验证
每张图都在 4 个方位角 × 3 个相位下截图（共 12 帧）：无控制台错误、720×440 内不裁切、遮挡顺序与原图一致。ea061 只能按播放时长取相位，因为它的 FIG 没有 setT。

## ea064 为什么没做
原绘制器逐面排序，缸体原本是 0.9 半透明。改成不透明后，点火活塞从缸体中穿出来，单体壳也成了大块深色。要修好得按实体重排顺序，再给缸体做封口剖切（或者基于 v8.html 的 kit 代码重建），时间不够，所以留空，没有硬凑。

## 08:34 按 figure-style-spec.md 追加修改（部分合规）
已改：
- 图内只剩 1 个 `<text>`，位于 (16,24)，样式按规范；4 个标签分别是：
  - `CAT · 3-WAY · 000°`
  - `TDI · VGT+EGR · 000°`
  - `DIESEL AT · DPF+SCR · 000°`
  - `FLEX FUEL · E10-E85 · 000°`
  相位按 t×55°/s 计算。
- 删掉了中文引线标签、readout、图例和标题。
- 背景改为 #d9d9d6，默认相机 az -58 / el 28。
- 流动点和导线改成 kit 单色。
- 补上 `FIG.view/setPhi`。
- 运行时检查：4 方位 × 3 相位下 `<text>` 都恰好 1 个，无控制台错误；海报已重新生成。

仍不合规，所以 **figures-map-restyle-G.json 清空为 {}**：
- 规范第 2 节禁止自写渲染器，这 4 张仍用原图的绘制器，不是 kit 原语。
- 没有 kit `lit` 唯一高亮。
- 底座板不是 kit `slabOf`；ea061 完全没有底座板。
- 默认不自动播放，速度/周期也没有按 55°/s 和 720° 循环核对。

要真正合规，需要用 kit 原语按 ea023 重建，08:52 前做不完。
