# MathGenius PRO - 小学生口算练习题生成器

MathGenius PRO 是一款专为小学生（1-6年级）设计的数学口算练习题生成工具。它拥有现代化的图形界面，能够快速生成各种类型的数学题目，并支持导出为高质量的 PDF 和 Word 文档，方便家长和老师打印使用。

## ✨ 主要功能

- **分年级预设**：针对 1-6 年级教学大纲，提供科学的题目难度预设。
- **多种题目类型**：
  - **基础加减法**：支持自定义范围（如 20以内、100以内）。
  - **连加连减**：多步运算练习。
  - **进位加法 & 退位减法**：针对性强化训练。
  - **乘除法运算**：表内乘除及大数运算。
  - **有余数除法**：专项练习。
  - **连乘连除**：多步乘除运算。
- **高度自定义**：
  - 自定义数值范围（最小值、最大值）。
  - 自定义每页题量（20/40/60/80/100 题）。
  - 自定义题目排版（列数、间距）。
  - 灵活的填空位置（结果填空或算式中间填空）。
- **专业导出**：
  - **PDF 导出**：支持生成带答案页的 PDF 文件，排版精美。
  - **Word 导出**：生成可编辑的 `.docx` 文件。
- **实时预览**：在软件界面中即可预览生成的题目样式。

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 依赖库：
  - `PyQt6` (界面框架)
  - `reportlab` (PDF 生成)
  - `python-docx` (Word 生成)

### 安装依赖

```bash
pip install PyQt6 reportlab python-docx
```

### 运行程序

```bash
python main.py
```

## 🛠️ 项目结构

```text
MathGenius/
├── core/               # 核心逻辑
│   ├── math_engine.py  # 题目生成引擎
│   └── presets.py      # 年级和题型预设
├── services/           # 导出服务
│   ├── pdf_exporter.py  # PDF 导出实现
│   └── word_exporter.py # Word 导出实现
├── ui/                 # 界面组件
│   ├── main_window.py   # 主窗口界面
│   └── preview_canvas.py# 预览画布
├── main.py             # 程序入口
└── MathGenius.spec     # PyInstaller 打包配置
```

## 📦 打包应用

项目已包含 `MathGenius.spec` 配置文件，可以使用 PyInstaller 进行打包：

```bash
pyinstaller MathGenius.spec
```

## 📜 开源协议

MIT License
