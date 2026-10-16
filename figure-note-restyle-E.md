# Restyle E：EA-044 / 045 / 046 / 047 / 048

完成的有：ea044k、ea045k、ea046k、ea048k（html 和 svg 海报都已生成，并已登记到 `figures-map-restyle-E.json`）。
未完成的是 ea047k（F1 V6 混动），没有登记，也没有留下文件。

## 做法
- kit：从 v8.html 内联 anatomy kit（CSS 和 iso-kit / G 几何库，与 v6/v8 用的是同一份代码），只用 light 主题，页面底色为 #d9d9d6。
- ea044、ea046：原场景的 `build(t)` 原样保留，零件和动画都不变。box/cyl/ball/pipe 改用 kit 的 `prismOf` 和 `lathe` 渲染，加上 `solidSvg` 的四档明暗与细描边，绘制顺序按零件深度排列。
- ea045、ea048：原文件的场景代码原样保留（engineI4、齿轮、涡轮、皮带和 harvest/boost 状态机都没动），只把 `prism/annulus/render/mountFigure` 换成 kit 版本：圆截面用 `lathe` 画，其它截面（齿轮、叶轮）用 `prismOf` 画，绘制顺序沿用原图的零件深度。
- 按 figure-style-spec.md 处理：
  - 删掉所有中文标签、读数和图例，只在左上角留一行等宽标签：H2 ICE · 70 MPA / KERS · 60 KW / EREV · SERIES / E-BOOST · 48 V，后面跟 000°（55°/s）。
  - 底座用 kit 的 `slabOf` 圆角板，厚 11，向外扩 14；不画 halo，也不画投影。
  - 相机默认为 az -58、el 28，EA-045 例外，用 az 128，原因是 MGU 在 -58 时被缸体挡住。缩放取 360° 扫描的最小值。
  - 流向点改成 kit 的单色点（`iso-dots`），保留流动动画的含义。
  - lit 高亮：EA-044 是 H₂ 喷射轨，EA-046 是电池。
- FIG 接口：play/reset/playing/view/setPhi。传 ?still、?embed 或开启减弱动态时不自动播放，可以拖动旋转，并加载 `_embed-lite.js`。

## 验证
- 每张图都看了 4 个方位角（-58/32/122/212）× 3 个相位的截图，没有发现明显的遮挡错误，控制台也没有报错。
- 海报里的 `<text>` 节点只有 1 个。

## 未完成：ea047
- 原图是逐面排序的骨架 V6，缸体为半透明。改成按零件深度排序后，近侧缸排的活塞会盖到凸轮罩上，发动机也会悬在底座上方，没能在截止时间前修好。
- 建议直接拿 v6.html 的 kit 代码，套用它的 closedKey/endKey 排序，再加上涡轮、压气机和 MGU-H/K 实体。
- 当前用的仍是原 ea047.html。
