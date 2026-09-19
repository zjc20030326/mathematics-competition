# 数学分析培优讲义 LaTeX 工程

建议使用 XeLaTeX / latexmk 编译：

```powershell
latexmk -xelatex -outdir=build main.tex
```

项目约定：

- `main.tex`：全书入口，只管理书名、前言、目录和章节载入。
- `preamble.tex`：所有宏包、定理环境、页眉页脚、自定义命令。
- `chapters/`：一章一个 `.tex` 文件。
- `figures/chXX/`：对应章节图片。
- `source/`：保存原始 PDF，不参与 LaTeX 编译。
- `ocr/`：保存 MinerU / Mathpix 等识别中间稿，不参与最终编译。
- `build/`：编译输出目录。

章节文件名建议使用 ASCII，正文标题仍使用中文，避免 Windows / LaTeX 工具链中的中文路径兼容问题。
