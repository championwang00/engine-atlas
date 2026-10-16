> 历史基线记录。当前完成情况与仍有的缺口见 [work/coverage-final.md](work/coverage-final.md)；本文件中的旧条数和待核实清单不代表现状。

# content.json 空字段与 pending 清单

## 空字段（14 个）
- EA-005 tradeoffs：大纲 1.3 Brayton 未列优缺点。
- EA-006 tradeoffs：大纲 1.4 奥托四冲程未列优缺点。
- EA-011 principle：大纲 2.2 直列双缸只有年代、代表、优缺点，没有原理。
- EA-015 tradeoffs：大纲 2.8 V12 只有代表与现状，未列优缺点。
- EA-017 principle：大纲 2.7 直列八缸没有原理条目。
- EA-020 tradeoffs：大纲 2.8 V16 未列优缺点。
- EA-025 tradeoffs：大纲 2.8 V6 未列优缺点。
- EA-030 principle：大纲 5.1 化油器→电喷只有年代与现状，没有原理。
- EA-030 tradeoffs：同上，没有优缺点。
- EA-034 tradeoffs：F1 规格表只有排量、布局、功率，无优缺点。
- EA-037 tradeoffs：大纲 2.8 V10 未列优缺点。
- EA-043 tradeoffs：F1 规格表无优缺点。
- EA-045 tradeoffs：大纲 7.3 KERS 无优缺点。
- EA-052 tradeoffs：大纲 7.3 与 F1 规格表无 2026 规则优缺点。

## pending（30 条）
- EA-002：de Rivaz 年份 1806 vs 1807（待核实清单第 1 条）；大纲无该条专属来源，sources 为空。
- EA-005：Brayton 年份 1872 vs 1873 标为待核实；tradeoffs 为空。
- EA-006：Otto 年份多说法（待核实清单第 1 条）；tradeoffs 为空。
- EA-010：Mercedes 260 D 第一辆柴油轿车未核对（待核实清单第 2 条）。
- EA-011：principle 为空。
- EA-014：Cadillac 1914 第一台量产 V8 未核对（待核实清单第 2 条）。
- EA-015：条目卡片写的 Packard Twin Six、1915、60° 完全平衡在大纲中找不到依据；tradeoffs 为空。
- EA-017：principle 为空。
- EA-020：Marmon Sixteen 产量 390 vs 400（待核实清单第 3 条）；tradeoffs 为空。
- EA-022：Toyota FPEG 约 15 hp 数值归属不清（大纲标待核实，正文未采用该数值）。
- EA-023：Benz 水平对置双缸 1899 vs 1900（待核实清单第 3 条）。
- EA-024：LPG 历史无权威来源（大纲标待核实）。
- EA-025：Lancia Aurelia 第一台量产 V6 未核对（待核实清单第 2 条）；tradeoffs 为空。
- EA-026：Rover JET1 未核对、Chrysler Turbine Car 油耗与产量有冲突（待核实清单第 2、6 条）。
- EA-029：Jetfire 与 Corvair Spyder 先后顺序冲突（待核实清单第 4 条）。
- EA-030：Bendix/Bosch 电喷起点未核对（待核实清单第 2 条）；principle、tradeoffs 为空；大纲无该节专属来源。
- EA-031：Audi 直五首发 1976 vs 1977（待核实清单第 3 条）。
- EA-032：Alfa 1980 VVT 未核对（待核实清单第 2 条）；大纲无 VVT 专属来源。
- EA-034：tradeoffs 为空；F1 规格表注明边界年份以 FIA 原文为准。
- EA-037：tradeoffs 为空。
- EA-042：Bentley W12 2024 停产标为待核实。
- EA-043：tradeoffs 为空；条目卡片写的“统一缸径上限与转速限制”大纲无依据，正文未采用。
- EA-044：JCB 氢动力纪录待核实（待核实清单第 9 条，正文未采用）。
- EA-045：tradeoffs 为空。
- EA-046：BMW i3 REx 销售年份（待核实清单第 8 条）。
- EA-048：Audi SQ7 与 AMG e-turbo 未核对（待核实清单第 2 条）；大纲无该节来源。
- EA-049：VC-Turbo 停产口径（待核实清单第 8 条）。
- EA-050：Skyactiv-X 停产口径与 Skyactiv-Z 继任（待核实清单第 8 条）。
- EA-051：Haru Oni 扩产计划（待核实清单第 9 条）。
- EA-052：2026 F1 规则数值以 FIA 官方技术规则为准（待核实清单第 10 条）；tradeoffs 为空。

## 其他说明
- EA-035、EA-041 的 sources 为空：大纲 5.4 节的来源只覆盖 MultiAir 与 Freevalve，没有 VTEC 与 Valvetronic 的专属链接；内容本身无冲突，verify 为 ok。
- EA-028 条目卡片写“一阶不平衡”，大纲 2.3 写“一阶二阶往复力平衡，有端部摇摆力矩”，content.json 按大纲写。
- EA-047 条目卡片的“缸径 80 × 行程 53 mm”大纲无依据，正文未采用。
- EA-021、EA-022、EA-044、EA-051 的现状用了大纲中的“实验”标签，因为在用、淘汰、复兴都与大纲不符。
