# restyle-H：ea065 / ea066 / ea067 / ea072 / ea073 → kit 画风

产出：`assets/figures/ea065k.html … ea073k.html` 及同名 `.svg` 海报；原 `ea0xx.html` 未改。

做法：
- 页面头、CSS 与 anatomy kit（iso-kit + G/lathe）整段取自 `ea023.html`（第 1–1976 行），按 `figure-style-spec.md` 执行：只用 light 主题，`#d9d9d6` 底，圆角底座板（slabOf，tone mid，厚 11，平面为机构包围盒每边外扩 14），相机 az -58 / el 28、pad 14、取 360° 扫描中的最小 scale，图内只有左上角一行 mono 标签，速度 55°/s，提供 `window.FIG {play, reset, playing, view, setPhi}`，`?still` / `?embed` / 减弱动态时不自动播放，可拖动旋转。
- 机构与运动学原样保留：把原图的场景函数（零件尺寸、相位、升程曲线、曲拐角、平衡轴 2× 反转）直接复用，只把底层的 box/cyl/rod/sph/lobe/spring 换成 kit 的 `prismOf / disc / solidOf / sphereOf` + `solidSvg`（四档明暗、细描边），每个零件按视线深度做画家排序。
- 依规范删掉了：中文引线标签、读数、升程小图、相位环与力箭头、彩色材质、半透明缸体与盖。
- 唯一高亮（kit 的 `lit`）：ea065 灼热管点火闪光；ea066 停缸的解耦挺柱；ea067 电液执行器；ea072 做功冲程活塞；ea073 平衡轴配重。
- 标签：`DAIMLER · 1 CYL`、`CYL DEACT · 2 CYL`、`CAMLESS · EHVA`、`V8 · FLAT/CROSS`、`I4 · 2 BAL SHAFT`，后接 `000°` 相位。
- ea066/067 的剖面墙改为随视角挑远侧（用 kit 视线向量），保证墙永远在机构后方。

验证：每张都检查了 4 个方位角（-140 / -58 / 30 / 120）× 3 个相位，控制台 0 错误，运行时 `<text>` = 1，720×440 内不裁切。

已知局限（沿用原图的几何）：
- ea066/067 只有活塞盘，没有缸套和连杆；
- ea072/073 的曲轴悬空，没有轴承座；
- 删掉箭头后，ea073 不再直接画出力的方向，只靠平衡轴的 2× 反向旋转来体现。
