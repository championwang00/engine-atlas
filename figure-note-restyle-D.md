# Restyle D：ea033 / ea034 / ea035 / ea040 / ea043 改用 anatomy kit 重画

新文件都是 `assets/figures/<key>k.html` 加 `.svg` 海报，原来的 ea*.html 没有动。
统一按 figure-style-spec.md 做：kit 浅色主题，ea013/ea023 的 kit 内联头，`#d9d9d6` 底，圆角 mid 底座板，相机 az -58 / el 28，pad 14，缩放取 360° 扫描中的最小值。
图内只留左上角一个 `<text>` 标签，其余中文标注、图例、表盘和读数全部删除。有 `window.FIG {play, reset, playing, view, setPhi}`，加载 `_embed-lite.js`，可拖动旋转。`?still`、`?embed` 和减弱动态都不自动播放。

| key | 做法 | 标签 | 高亮 |
|---|---|---|---|
| ea043k | v8.html 的 kit 代码参数化（V8 90°，98×39.75，连杆 104，曲拐 0/90/270/180） | `F1 V8 · 90° BANK · 000°` | 只亮最近点火的一缸活塞（ph < 720/n） |
| ea034k | 同上，V10 72°，93×51.5，连杆 110，曲拐 0/144/216/72/288 | `F1 V10 · 72° BANK · 000°` | 同上 |
| ea035k | 原机构代码（SCENE、凸轮/摇臂/锁销运动学、低速/高速交替）原样保留；box/cyl/prism/lobe 改由 `G.prismOf + solidSvg` 绘制，按零件深度排序；剖切只画两面远墙，实体不透明 | `VTEC · 3 LOBE · LO-CAM/HI-CAM 000°` | 高速时中间凸轮、摇臂和锁销 |
| ea033k | 原 build 函数原样保留；prism → `G.prismOf`，annulus → `G.ringBand`，flow 点 → `lineSvg flow` 点线（tone lo），去掉 label 和 legend | `TWIN · SC+TURBO · SC/TURBO 000°` | 旁通阀（acc） |
| ea040k | 同 ea033k 的适配方式；行星齿轮的 Willis 运动学不变 | `HYBRID · E-CVT · 000°` | 无 |

已知妥协：
- 齿轮、罗茨转子这类凹轮廓用凸包画实体，近端端面另加一条 lo 细线画出真实齿形或叶形。
- ea034 原图的进气喇叭没有画。
- ea033/ea040 的气流 flow 线在同一帧可能不止一条，规范只允许一条。
- ea035 速度按规范改为 55°/s，1440° 循环一次。
- 原图的转速、MG 转速数值读数和中文说明都删除了，按规范只留标签第三段的状态。

每张图都转了 4 个方位角（-58/32/122/212）× 3 个相位，控制台无报错，运行时 `<text>` 正好 1 个。
