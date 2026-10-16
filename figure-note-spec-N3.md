# figure-note-spec-N3

依据 `figure-style-spec.md`，以 `ea023.html` 为基准，统一 6 张图。备份：`assets/figures/<key>.pre-spec.html`。

| key | 标签 | 改动 |
|---|---|---|
| ea042 | `W12 · 3 BANK · 000°` | 本来就是 ea023 模板，只把 tag 从四段（`W12 · 3×4 · 60°`，含 ×）改成两段 |
| ea078 | `FLATHEAD V8 · 90° BANK · 000°` | 见下面的通用改动；排气通道从 `hot`/`warm` 橙色改为 kit `lit`（排气门打开时） |
| ea079 | `SBC V8 · 90° BANK · 000°` | 通用改动 |
| ea080 | `OM617 · 5 CYL · 000°` | 通用改动 |
| ea081 | `OFFY · 4 CYL · 000°` | 通用改动 |
| ea082 | `EA888 · TURBO · 000°` | 通用改动；删掉 `FX.label()`（原来是中文 VTEC/直喷说明 + 点火顺序，位于 y=426）；默认 az 从 32 改为 -58 |

通用改动（ea078–082）：
- 删掉第二个 `<style>` 里的自定义覆盖样式（描边颜色/粗细、`.model-base` 填色、`.hot/.warm` 橙色、halo 不透明度），换成 ea023 的页面样式；给 svg 加上 `width=720 height=440`。
- 底座板：去掉板下支脚、螺丝、刻度条，只保留 ea023 的 `slabOf` 板 + `faint` 内描线（halo 与 ea023 一样保留）。
- 标签：原 `LABEL`（左下 y=426，内容为点火顺序，字距 .06em，颜色 #4a4a46）改为规范的 `label()`，位置 (16,24)，文字为 `TAG · 三位相位°`，每帧更新。
- 相机：el 默认值 30 → 28（包括 URL 默认值、双击复位、`FIG.reset`）。
- `window.FIG`：补上 `view(az,el)` 和 `setPhi(p)`；速度原本就是 55°/s；`_embed-lite.js` 保留。

检查（headless Chrome，`?still`，az = -58/32/122/212，phi=200）：6 张均无控制台错误；运行时 `<text>` 恰好 1 个；内容包围盒都在 720×440 以内，四边至少留出约 20px；遮挡目视正常。海报已用 `node poster.mjs` 重新生成，每个 svg 中 `<text>` 为 1。

遗留：ea078 的排气 `lit` 是逐缸判断，可能同一帧有多个排气通道同时高亮（规范要求 ≤1 组）；ea042 的做功活塞 lit 沿用 ea023 的逻辑（W12 有多缸同时满足条件）。
