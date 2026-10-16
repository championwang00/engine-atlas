# 静态发布准备

此项目保持独立，无 Next.js 依赖。本轮没有登录 Vercel、创建项目、上传、推送或部署。

本地预览：

```sh
python3 atlas.py
python3 -m http.server 8766
```

发布包（本地操作）：

```sh
python3 package_site.py
```

`dist/` 只收录 `build-manifest.json` 中的公开 HTML、`atlas.css`、`atlas.js` 和已生成的三图资产。研究全文、来源日志、HANDOFF、work、评审记录与生成脚本均不进入发布包。不要直接把工程根目录作为静态发布目录。

若未来明确授权部署，在 Vercel 选本目录 `outputs/engine-atlas` 为项目根，Framework 设 Other。`vercel.json` 已指定 build 和 `dist` 输出。确定实际域名后设置 `ATLAS_SITE_URL=https://实际域名` 再构建：canonical/hreflang 会转为绝对 URL，生成 `sitemap.xml` 与对应 robots 声明。未定域名时使用合法的相对 alternate 链接，不伪造生产 URL。

插图只有在源码变化时需要重建，要求已有经过审阅的 Anatomy 安装：

```sh
ANATOMY_SKILL_DIR=/实际/anatomy路径 node ../engines/build.mjs
node prepare_figures.mjs
```

日常站点构建不依赖 Anatomy 或浏览器；三张自包含 HTML 和静态 SVG 已留在 `assets/figures/`。`--audit` 会明确拒绝，因为旧图尚未接入 kit 几何 recorder；当前具备的是另行记录的运动学、线端点及浏览器验证，不能代替完整几何碰撞证明。

Google Fonts 与 Wikimedia 图片继续按原站点外链策略加载。Commons 图片在预览中展示作者、许可与原始文件页；加载失败时退回文字预览。未购买或使用 Big Bird。
