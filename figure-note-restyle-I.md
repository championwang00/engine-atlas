# restyle-I · 图注

范围：ea074 / ea075 / ea076 / ea077 / ea086 统一为 anatomy kit 画风，并按 `figure-style-spec.md`（以 ea023 为基准）执行。新文件 `<key>k.html` + `<key>k.svg`，原 ea*.html 没有改动。

## 已完成（已登记到 figures-map-restyle-I.json）

| id | key | 做法 | 高亮（lit） | 左上标签 |
|---|---|---|---|---|
| EA-074 | ea074k | 保留原 SCENES.ea074 的几何和动画（翅片缸、风扇、水泵、散热器、冷却液流动），重写 `render`：每个零件的可见面按法向分到 kit 的四档 `iso-shade`、`iso-top`，经 `solidSvg` 输出，外轮廓用 `hi`，折痕用 `faint`；底座板为 `mid` 薄板，加内描线 | 无 | `COOLING · AIR/WATER · 000°` |
| EA-075 | ea075k | 原 k-API 场景经适配层改用 kit `slabOf/cylinder/disc/solidOf/sphereOf`（g8 runtime，按深度排序）；去掉两处未核实的数字（IndyCar 1965–2006、约 2 倍体积） | 含氧比例柱（橙色段） | `METHANOL · CH3OH · 000°` |
| EA-076 | ea076k | 同上 | 无铅窄口油枪 | `UNLEADED · NO TEL · 000°` |
| EA-077 | ea077k | 同上 | HVO 储罐 | `BIODIESEL · FAME/HVO · 000°` |

共同处理：
- kit light 主题，不另设配色；原有彩色零件全部回到 kit 白色，流动点用 `--anatomy-mid`。
- 删掉所有中文标签、读数和标题，图内只有一个 `<text>`，第三段是相位，按 55°/s 计算。
- 相机为 az −58°、el 28°。缩放取全 360° 方位扫描的最小值，所以旋转时不会出框，也不会跳变。
- `FIG.play/reset/playing/view/setPhi` 都有。默认自动播放；`?still`、`?embed` 或减弱动态时不播放。
- 验证项：4 个方位角 × 3 个相位截图，控制台没有错误，运行时 `<text>` 为 1，减弱动态下 `playing=false`，海报 SVG 已生成，里面的 `<text>` 也是 1。

已知局限：
- 遮挡按零件中心深度排序，细长管路在个别角度可能和相邻零件有轻微的前后错位。
- ea075 和 ea076 里的分子模型仍然悬在空中，这是沿用原图的布局。
- 去掉颜色后，ea075 的含氧比例柱只靠 lit 区分，不如原图明显。
- ea076 的 lit 落在油枪的两个实体上（枪体和枪管），这算同一个零件组。

## 未完成

- **EA-086（ea086 Mazda 13B／RENESIS）**：没有做，也没有登记。原图用的是第三套自写引擎（带孔挤出、齿轮、按相位着色的燃烧室）。动画的意思靠给四个工作腔分别上色来表达，换成单色加单一 lit 需要重新设计做功腔的高亮。在 08:52 前做不完改造加 12 帧验证，所以留着。
