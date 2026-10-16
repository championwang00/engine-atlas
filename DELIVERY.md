# Engine Atlas 交付说明

中文预览：http://127.0.0.1:8766/zh/index.html  
英文预览：http://127.0.0.1:8766/en/index.html

静态成品位于dist/，可将其中内容交给静态托管服务。当前未部署。网络字体与Commons图片需要网络访问，各图保留作者、许可和来源。

数据研究/覆盖矩阵：work/coverage-final.md  
实体/术语缺图：work/preview-missing-images.md  
数据完整性：work/data-validation.json  
最终评审：outputs/design-reviews/20261015-132628-06fd7acb/report.json

核验通过：348个中英详情手机/桌面组合，40个主要页面尺寸组合，16个标题对齐组合，168张不同预览图加载，搜索/筛选/缩放/返回状态/跨文档转场/预览键盘与触屏，3图中英及减弱动态的12组控制检查、288渲染状态，dist本地链接和私有文件排除。

保留事项：EA-060 Croma年份争议；59个实体和51个术语仍为文字预览；未绘主图按既定要求留空；人工编辑审阅未做；模型不是特定实机复原，没有全kit碰撞证明。第三轮视觉8.3/10，三轮预算已用完，未达9分目标，不能宣称视觉完全验收。没有commit/push/deploy。

重新生成：python3 merge_research.py → python3 build_previews.py → python3 make.py。打包：python3 package_site.py。以公共HTTP服务预览，不用file协议验证转场。

2026-10-15 局部交互更新：V6/V8/V12 详情默认以骨架视图自动播放；系统减弱动态设置下保持暂停，可手动播放。骨架视图采用44px高、灰黑轨道与圆形滑块的开关，点击、空格、X及程序调用状态同步；旋转视角保留播放/暂停状态，Shift手动转曲轴与重置暂停，重新显现时只恢复既有播放状态。索引仍为静态骨架海报。验证见outputs/verification/figure-controls.json；截图见outputs/design-reviews/20261015-153228-670fb3de/motion-switch-v2/。

2026-10-15 第二轮转场修复：上一轮仍有正文双曝和整页亮灭，已撤下整页淡化、附近卡片分层与顶栏独立换层。页面同步切换，只保留400ms图位展开和回程；图像使用单一快照，54px控件不参与飞行。海报与交互内容共用真实图像视口。资源版本transition-fix-2；1939px真实Codex浏览器复查、连续帧、7项回归及包校验见work/flash-round2/delivery.md。移动目标页字体尚在loading时，正文可能在首帧后约40–50ms补绘，记录为单独边界。dist与zip已同步。
