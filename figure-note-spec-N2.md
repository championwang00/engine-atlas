# figure-note-spec-N2 · 规范统一（ea019 ea020 ea028 ea031 ea036 ea037）

基准：`figure-style-spec.md` + `ea023.html`。备份：`assets/figures/<key>.pre-spec.html`（及 `.pre-spec.svg`）。

| key | 改动 | 标签 |
|---|---|---|
| ea019 | 已是 ea023 模板（双曲轴 + shift）；标签改为两段；删 `el:30`，用默认 -58/28 | `U8 · 2×I4 · 000°` |
| ea020 | 模板一致；删 `el:30` | `V16 · 45° · 000°` |
| ea028 | 原为旧版直列模型（自定义描边色 #626268 等、底部标签 y=426、`.model-base` 覆盖）；改为直接复用 ea023 全部源码，仅换 CFG：bore 78 / stroke 70 / rod 130，pins [0,240,120]（点火 1-3-2），bank 0 | `I3 · 240° · 000°` |
| ea031 | 同 ea028；bore 82 / stroke 76 / rod 140，pins [0,216,144,72,288]（点火 1-2-4-5-3） | `I5 · 144° · 000°` |
| ea036 | 模板一致，仅确认 CFG（默认相机） | `VR6 · 15° · 000°` |
| ea037 | 模板一致，仅确认 CFG（默认相机） | `V10 · 72° · 000°` |

全部：底座板 / camera()（全方位最小 scale，pad 14）/ 四档明暗 / 唯一高亮 `lit`（做功活塞冠）/ 55°/s / 拖动旋转 / `window.FIG` / `_embed-lite.js` 与 ea023 逐字一致。

## 验证（headless Chrome，?still，phi=90，az = -58 / 32 / 122 / 212，el 28）
- 控制台错误：6 张均 0。
- 运行时 `<text>` 节点：每个方位均恰好 1，位于 (16,24)。
- 包围盒：全部在 720×440 内（最紧 ea020 az32：x 64–656，y 56–390），无裁切。
- 遮挡：目测截图（ea019/028/031）排序正确，与 ea023 同一 painter key 逻辑。
- 海报：`node poster.mjs` 重新生成 6 张 svg，各含 1 个 `<text>`、无 gradient/filter。

结果：6 张全部通过，无恢复。
