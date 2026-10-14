# 本次扩展验证记录

日期：2026-10-13。

- 65 个唯一图型 ID：45 guided-svg + 20 python；所选规范与示例路径存在。
- paper-figure 通过 skill-creator/quick_validate.py 验证（Windows 使用 Python -X utf8）。
- 20 类科研示例实际生成 SVG / PDF / PNG / JSON / manifest；全部是有明确水印的合成演示数据。
- check.py 核对：同分阈值 ROC AUC、完美分类 AUC/AP、单类/非有限值/不匹配长度/非法区间拒绝，输入不被修改、真实数据来源记录。
- 核对 20 个 PNG 实际宽度、600 dpi 元数据与纯灰度通道；无检测到的画布外文本。
- 核对 20 个 PDF：单页、89 mm（单图）/180 mm（组合图）物理宽度、合成文字标记；逐张栅格化并查看 PDF 总览。
- 实际查看 PNG 与 PDF 总览，修复箱线图/小提琴默认彩色线，以及森林图/Bland–Altman 图例挤占数据的问题。此为总览读图记录，不替代用户真实数据图的逐项科学验收。
- 45 个上游标准示例通过 export_svg_document(..., system_fonts=True) 导出，均为合法 XML/SVG 且不含 Google Fonts 导入。未声称 45 类已为用户论文重新绘制或逐一视觉验收。
- 新增主入口与顶层 references 的 Markdown 本地链接核对通过。

manifest.visual_review 保持 pending，表示它是生成阶段的记录；本文件记录本次示例检查范围。用户真实图需另行核对事实、统计、标签、字体与布局。
