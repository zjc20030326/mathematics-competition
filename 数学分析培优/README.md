# 数学分析培优讲义

本目录已经迁移为 ElegantBook 单源结构,当前包含 13 章数学分析培优内容.

## 当前结构

- `elegantbook.cls`:ElegantBook v4.7 中文注释定制版,负责通用排版、数学宏包、水印开关以及答案显示开关.
- `preamble.tex`:只保存本讲义的个性化设置,如页眉、水印文字、例题编号、方法标题、例题留白和自定义数学算子.
- `数学分析培优讲义.tex`:普通版,`result=noanswer`,完整理论正文 + 例题,隐藏题解并保留书写空白.
- `数学分析培优讲义(答案版).tex`:答案版,`result=answer`,完整理论正文 + 例题 + 解答.
- 每章采用“三文件结构”:一个真正的内容文件,以及普通版、答案版两个很小的独立编译入口.

## 单章结构

以第一章为例:

```text
章节/01_第一章_数列极限/
├─ 第一章_数列极限_内容.tex
├─ 第一章_数列极限.tex
└─ 第一章_数列极限(答案版).tex
```

真正的数学内容只维护在 `_内容.tex` 中;两个入口文件只负责选择普通版或答案版的主导言区.

## 编译

使用 XeLaTeX / latexmk:

```powershell
latexmk -xelatex "数学分析培优讲义.tex"
latexmk -xelatex "数学分析培优讲义(答案版).tex"
```

任一章的普通版、答案版入口也都可以直接单独编译.

## 字体、中文强调与标点

字体机制保持 ElegantBook 原样:定理类环境与 `solution`、`note` 等楷体正文环境用
`\citshape`(楷体),`proof` 用 `\cfs`(仿宋),`remark` 不切字体,`example` 等用宋体;
没有对 `zhkai` / `zhfs` 做任何 `BoldFont` 补丁.

楷体/仿宋正文里的中文强调统一用 `preamble.tex` 提供的 `\strongcn`:

```latex
\newcommand{\strongcn}[1]{{\cbfseries #1}}
```

`\cbfseries` 在中文环境下等于 `\heiti`,所以这类正文里写 `\strongcn{...}`,
不要写 `\textbf{...}`(楷体/仿宋没有声明粗体字重,`\textbf` 会退回伪粗体并报警).
宋体正文里 `\textbf{...}` 照常可用;ElegantBook 环境标题自身的 `\textbf` 不要改.

章节正文的自然语言使用 ASCII 标点(`,`、`.`、`;`、`:`、`()`、`` ``…'' ``、`--`),
不使用全角标点(如 `，`、`。`、`；`、`：`、`（）`、`“”`、`、`、`—`、`…`),
与 validator 的 `PUNC001` 一致;`$...$` 与数学环境内不受影响,省略号仍用
`\ldots` / `\cdots`.

## 项目级 Skill 与检查

本讲义的编写,解答,校对,编译和验证遵循项目级 `writing-math-competition-lectures` Skill.

默认检查当前 Git 新增和修改行:

```powershell
python ..\.agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py check --scope changed
```

全项目检查:

```powershell
python ..\.agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py check --scope project --project .
```

检查器只报告问题,不会自动改写源码. 数学正确性仍需人工复核.

本次迁移只调整工程结构与排版体系,不擅自修改既有题面、答案或疑问题面.后续工作是逐题数学二审与原始 PDF 校勘.
