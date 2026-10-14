# 来源与维护

本次扩展以用户指定的本地「AI Agent 绘图 Skill-45 类图表-灰色」项目为参考。

上游：diagram-design，SKILL.md metadata.version=2.6。完整许可保存在 [diagram-design/LICENSE](diagram-design/LICENSE)，Copyright (c) 2025 Cathryn Lavery。`diagram-design/` 中资料、HTML 示例、技能内脚本及相关校验器按原路径结构保留；主入口以本库论文规范覆盖品牌/字体/商业数据图建议。

本库新增：65 类检索目录、20 类科研 JSON 渲染、科学方法声明、灰度样式、可编辑 SVG/PDF/600dpi PNG、输入哈希与环境记录、离线检索画廊和行为检查。未把上游示例或本库合成数据当成实验结果。

更新上游时重新核对图型 ID、类型规范与示例路径；更新科研模板时同步 catalog.json 与 scientific-recipes.md 并运行 check.py。所有依赖本地安装；脚本不会联网下载字体、包或上传数据。
