# AGENTS.md — 数学竞赛 LaTeX 项目总规范

## 1. 项目定位

本仓库/目录的总项目是：

```text
数学竞赛
```

目标是把多套数学竞赛、数学分析、高等代数等讲义与资料整理为长期可维护的 LaTeX 工程。

当前已经正式开始整理的子项目是：

```text
数学分析培优讲义
```

后续还会继续整理：

```text
高等代数相关讲义
```

以及可能新增的其他数学竞赛资料。

因此：

> `数学分析培优讲义` 只是 `数学竞赛` 项目下的一个子项目，不是整个项目本身。

后续工作必须保留这种“总项目 + 多本书/多套讲义子项目”的结构，不要把所有规则都硬编码成只适用于数学分析。

---

# 2. 总目录结构

当前项目建议保持如下结构：

```text
数学竞赛/
│
├─ AGENTS.md
│
├─ source/
│  ├─ 高代基础打印版.pdf
│  ├─ 高代培优上打印版.pdf
│  ├─ 高代培优下打印版.pdf
│  ├─ 数分基础打印版.pdf
│  ├─ 数分培优上打印版.pdf
│  └─ 数分培优下打印版.pdf
│
├─ 数学分析培优/
│  ├─ 数学分析培优讲义.tex
│  ├─ preamble.tex
│  ├─ README.md
│  ├─ 章节/
│  │  ├─ 第一章_数列极限/
│  │  │  └─ 第一章_数列极限.tex
│  │  ├─ 第二章_函数极限与实数基本定理/
│  │  │  └─ 第二章_函数极限与实数基本定理.tex
│  │  ├─ ...
│  │  └─ 第十三章_曲线积分与曲面积分/
│  │     └─ 第十三章_曲线积分与曲面积分.tex
│  └─ 图片/
│
├─ 高等代数培优讲义/
│  └─ ...
│
└─ 其他后续子项目/
   └─ ...
```

其中：

1. `source/` 是整个“数学竞赛”项目共用的原始资料目录。
2. 每一本讲义/每一个独立项目使用自己的子文件夹。
3. 每个子项目可以拥有自己的：
   - 主 `.tex`
   - `preamble.tex`
   - `章节/`
   - `图片/`
   - `README.md`
4. 不要把不同书籍的章节文件混在同一个 `章节/` 中。
5. 不要把所有书籍共用同一个主 `.tex`。

---

# 3. source 目录

`source/` 位于“数学竞赛”根目录。

当前已有：

```text
高代基础打印版.pdf
高代培优上打印版.pdf
高代培优下打印版.pdf
数分基础打印版.pdf
数分培优上打印版.pdf
数分培优下打印版.pdf
```

规则：

1. `source/` 中的 PDF 是原始资料。
2. 不要擅自修改原始 PDF。
3. 不要擅自移动或重命名这些文件。
4. 某个子项目需要引用原始资料时，应从根目录 `source/` 读取。
5. 当前 `.tex` 源码是代码层面的工作基线；原始 PDF 是内容核对的重要依据。

---

# 4. 项目层级与规则继承

根目录：

```text
数学竞赛/AGENTS.md
```

负责整个项目的公共规则，包括：

- 数学 LaTeX 规范；
- 编译质量要求；
- 文件管理原则；
- Codex 工作方式；
- 通用命名规则；
- 不得覆盖用户人工修改等要求。

每一本书如果以后有大量专属规则，可以在对应子项目中增加自己的：

```text
数学分析培优讲义/AGENTS.md
高等代数培优讲义/AGENTS.md
```

子项目规则只负责该书特有内容，例如：

- 章名；
- 特殊环境；
- 特殊编号；
- 特殊分页；
- 特殊版式。

总原则：

```text
用户当前明确要求
>
子项目专属规则
>
根目录 AGENTS.md
>
全局 writing-mathematical-latex Skill
>
项目当前已有写法
>
模型默认习惯
```

但是数学公式本身的具体书写规范仍必须严格遵循用户本机的数学 LaTeX Skill。

---

# 5. 数学 LaTeX Skill

所有涉及数学公式、数学环境、符号、分式、极限、积分、矩阵、组合数、上下标、集合、区间等内容时，必须先读取：

```text
C:\Users\m1881\.codex\skills\writing-mathematical-latex
```

尤其是：

```text
SKILL.md
```

该 Skill 是整个“数学竞赛”项目的公共数学排版规范。

不要只凭已有文件或模型习惯写数学公式。

如果本 AGENTS.md 与该 Skill 在纯数学排版细节上有冲突：

> 以 `writing-mathematical-latex` Skill 为准。

---

# 6. 公共 LaTeX 数学规则

以下规则适用于整个“数学竞赛”项目。

## 6.1 行内公式

`.tex` 中使用：

```latex
$...$
```

例如：

```latex
设 $x>0$。
```

---

## 6.2 行间公式

使用：

```latex
\[
...
\]
```

或者根据需要使用：

```latex
equation
align
gather
cases
matrix
pmatrix
vmatrix
```

等环境。

禁止使用：

```latex
$$...$$
```

---

## 6.3 分式

普通位置优先使用：

```latex
\dfrac{a}{b}
```

上下标中的分式按照 `writing-mathematical-latex` Skill 使用：

```latex
\frac{...}{...}
```

不要机械使用：

```latex
\tfrac
```

---

## 6.4 大型运算符

极限、求和、乘积等必须严格按照 Skill。

典型形式：

```latex
\lim\limits_{n\to\infty}
```

```latex
\sum\limits_{k=1}^{n}
```

```latex
\prod\limits_{k=1}^{n}
```

行内出现大型运算符时，根据 Skill 判断是否需要：

```latex
\displaystyle
```

---

## 6.5 积分

普通一维定积分不要机械添加 `\limits`。

例如：

```latex
\int_{a}^{b} f(x)\,\mathrm{d}x
```

多重积分、曲线积分、曲面积分、区域积分等统一遵守 Skill。

---

# 7. 组合数 / 二项式系数

整个项目统一：

禁止：

```latex
\binom{n}{k}
```

使用：

```latex
C_{k}^{n}
```

例如：

```latex
C_{0}^{n},
\quad
C_{1}^{n},
\quad
C_{k}^{n},
\quad
C_{n}^{n}.
```

Leibniz 公式、Taylor 公式、高阶导数、组合恒等式等同样执行该规则。

---

# 8. 定理环境公共原则

数学讲义优先使用语义化环境。

常用：

```latex
definition
example
theorem
axiom
lemma
proposition
corollary
remark
```

例如：

```latex
\begin{theorem}
...
\end{theorem}
```

```latex
\begin{example}
...
\end{example}
```

不要把：

```text
定义
定理
命题
推论
例
注
```

全部退化成普通粗体文本。

不同书籍可以在各自的 `preamble.tex` 中定义自己的编号方式，但不要无理由破坏已有编号体系。

---

# 9. 说明、PS、注记

在已经采用 `remark` 环境的子项目中，说明性内容统一使用：

```latex
\begin{remark}
...
\end{remark}
```

不要无理由重新引入纯文本：

```text
PS:
```

如果未来其他书籍有自己的“注”“说明”“备注”格式，应优先保持该书当前已经确定的环境设计。

---

# 10. 当前子项目：数学分析培优讲义

## 10.1 基本信息

书名：

```latex
\title{数学分析培优讲义}
```

作者：

```latex
\author{欧拉的小迷弟}
```

作者名已经由用户手工修改并确认。

不要擅自改回其他作者名。

---

## 10.2 当前目录结构

```text
数学分析培优/
│
├─ 数学分析培优讲义.tex
├─ preamble.tex
├─ README.md
│
├─ 章节/
│  ├─ 第一章_数列极限/
│  │  └─ 第一章_数列极限.tex
│  ├─ 第二章_函数极限与实数基本定理/
│  │  └─ 第二章_函数极限与实数基本定理.tex
│  ├─ 第三章_一元函数的连续性/
│  │  └─ 第三章_一元函数的连续性.tex
│  ├─ 第四章_一元函数微分学/
│  │  └─ 第四章_一元函数微分学.tex
│  ├─ 第五章_不定积分/
│  │  └─ 第五章_不定积分.tex
│  ├─ 第六章_定积分/
│  │  └─ 第六章_定积分.tex
│  ├─ 第七章_反常积分/
│  │  └─ 第七章_反常积分.tex
│  ├─ 第八章_数项级数/
│  │  └─ 第八章_数项级数.tex
│  ├─ 第九章_函数项级数、幂级数、Fourier级数/
│  │  └─ 第九章_函数项级数、幂级数、Fourier级数.tex
│  ├─ 第十章_多元函数微分学/
│  │  └─ 第十章_多元函数微分学.tex
│  ├─ 第十一章_含参变量积分/
│  │  └─ 第十一章_含参变量积分.tex
│  ├─ 第十二章_重积分/
│  │  └─ 第十二章_重积分.tex
│  └─ 第十三章_曲线积分与曲面积分/
│     └─ 第十三章_曲线积分与曲面积分.tex
│
└─ 图片/
```

章节文件名固定采用：

```text
第X章_章名.tex
```

不要：

- 改成英文；
- 删除 `_`；
- 改变已经确定的章名。

---

# 11. 数学分析培优讲义十三章名称

固定为：

```text
第一章   数列极限
第二章   函数极限与实数基本定理
第三章   一元函数的连续性
第四章   一元函数微分学
第五章   不定积分
第六章   定积分
第七章   反常积分
第八章   数项级数
第九章   函数项级数、幂级数、Fourier级数
第十章   多元函数微分学
第十一章 含参变量积分
第十二章 重积分
第十三章 曲线积分与曲面积分
```

---

# 12. 数学分析培优讲义必须使用 subfiles

该子项目已经确定使用：

```latex
\usepackage{subfiles}
```

主文件使用：

```latex
\subfile{章节/第一章_数列极限/第一章_数列极限}
\subfile{章节/第二章_函数极限与实数基本定理/第二章_函数极限与实数基本定理}
\subfile{章节/第三章_一元函数的连续性/第三章_一元函数的连续性}
\subfile{章节/第四章_一元函数微分学/第四章_一元函数微分学}
\subfile{章节/第五章_不定积分/第五章_不定积分}
\subfile{章节/第六章_定积分/第六章_定积分}
\subfile{章节/第七章_反常积分/第七章_反常积分}
\subfile{章节/第八章_数项级数/第八章_数项级数}
\subfile{章节/第九章_函数项级数、幂级数、Fourier级数/第九章_函数项级数、幂级数、Fourier级数}
\subfile{章节/第十章_多元函数微分学/第十章_多元函数微分学}
\subfile{章节/第十一章_含参变量积分/第十一章_含参变量积分}
\subfile{章节/第十二章_重积分/第十二章_重积分}
\subfile{章节/第十三章_曲线积分与曲面积分/第十三章_曲线积分与曲面积分}
```

禁止擅自改回：

```latex
\include{...}
```

该规则目前只明确适用于“数学分析培优讲义”。

未来高等代数项目建立时，应根据实际需要决定是否沿用相同结构，不要未经确认直接假设。

---

# 13. 数学分析培优讲义必须支持单章编译

每个章节 `.tex` 都必须可以独立编译。

例如：

```latex
\documentclass[../../数学分析培优讲义.tex]{subfiles}

\begin{document}

...
\chapter{数列极限}

...

\end{document}
```

必须保证：

- 第一章单独编译仍显示第一章；
- 第二章单独编译仍显示第二章；
- ...
- 第十三章单独编译仍显示第十三章；
- 主文件完整编译时编号也正确。

如果当前章节文件中已经存在经过验证的：

```latex
\setcounter{chapter}{...}
```

逻辑，优先保留当前可工作的实现。

任何章节编号相关改动必须同时测试：

```text
单章编译
+
全书编译
```

---

# 14. 数学分析培优讲义的例题留白

该子项目明确要求：

每一个：

```latex
\begin{example}
...
\end{example}
```

后必须紧跟：

```latex
\exampleblank
```

例如：

```latex
\begin{example}
求下列极限……
\end{example}
\exampleblank
```

`\exampleblank` 在该书 `preamble.tex` 中统一定义。

不要逐题写死：

```latex
\vspace{...}
```

如果以后要改变例题后留白，只修改统一宏。

该规则目前是“数学分析培优讲义”的专属规则。

未来高等代数项目是否使用相同留白，由用户另行决定。

---

# 15. 数学分析培优讲义的重要性标记

当前该书正文中：

原来使用三角形标记的位置统一使用：

```latex
\markstar
```

正文不要调用：

```latex
\marktriangle
```

或：

```latex
\markstartriangle
```

但是 `preamble.tex` 中允许继续保留：

```latex
\newcommand{\marktriangle}{\ensuremath{\blacktriangle}}
```

即：

```text
宏定义可以保留
正文调用必须为 0
```

---

# 16. 数学分析培优讲义分页规则

这是该子项目非常重要的规则。

用户要求：

> 新的 `section` 内容从新的一页开始，`subsection` 和 `methodsection` 不分页。
>
> `\newpage` 应放在新标题之前。
>
> 不能在标题之后机械加 `\newpage`。
>
> 不能制造只有标题的大空白页。

错误：

```latex
\section{收敛数列}

\newpage

\subsection{证明极限存在}

\newpage

\methodsection{(A) 结合拟合法,由定义证明}
```

这会造成多个只有标题的页面。

正确思路：

```latex
上一部分正文……

\newpage

\section{收敛数列}

\subsection{证明极限存在}

\methodsection{(A) 结合拟合法,由定义证明}

正文……
```

也就是说：

如果：

```latex
\section
```

后立即跟：

```latex
\subsection
```

无论前面是否已有正文，均不要在 `\subsection` 前分页。

如果：

```latex
\subsection
```

后立即跟：

```latex
\methodsection
```

无论前面是否已有正文，均不要在 `\methodsection` 前分页。

连续层级标题属于同一个页首标题组。

目标效果：

```text
新的一页顶部：

1.2 收敛数列
1.2.1 证明极限存在
(A) 结合拟合法，由定义证明

正文……
```

而不是三个独立标题页。

---

# 17. chapter 分页

`\chapter` 本身会开启新页。

在“数学分析培优讲义”中：

不要在：

```latex
\chapter{...}
```

后机械添加：

```latex
\newpage
```

否则可能制造只有章标题的空白页。

---

# 18. methodsection

“数学分析培优讲义”使用：

```latex
\methodsection{(A) ...}
```

表示：

```text
(A)
(B)
(C)
...
```

等方法分类。

必须保留当前 `preamble.tex` 中已经工作的 `\methodsection` 定义。

不要擅自改成普通：

```latex
\section
```

或：

```latex
\subsection
```

也不要让其单独占一页。

---

# 19. 数学分析培优讲义标题中的数学公式

如果：

```latex
\section
\subsection
\methodsection
```

等标题里包含数学公式，需要兼容 `hyperref` 的 PDF bookmark。

例如不要直接写：

```latex
\subsection{$\mathbb{R}^n$ 中的点集}
```

应使用：

```latex
\subsection{
  \texorpdfstring{$\mathbb{R}^n$}{R^n} 中的点集
}
```

当前曾出现的标题数学内容包括：

```text
f(f(x))
f^{(n)}(0)
\mathbb{R}^n
\Gamma
n 重积分
```

必须避免重新出现：

```text
Package hyperref:
Token not allowed in a PDF string
```

不要通过删除数学标题内容解决问题。

---

# 20. 数学分析培优讲义字体设置

当前该书使用：

```latex
\usepackage{mathrsfs}
```

同时应保留：

```latex
\usepackage{anyfontsize}
```

用于避免非标准字号产生：

```text
Font shape `U/rsfs/m/n' ... not available
Size substitutions ...
```

不要无故删除：

```latex
\usepackage{anyfontsize}
```

当前项目使用 XeLaTeX。

---

# 21. 作者、页眉、水印

“数学分析培优讲义”的作者固定为：

```text
欧拉的小迷弟
```

但：

```text
页眉
水印
固定署名
```

以用户当前本地 `preamble.tex` 为准。

不要根据作者名自动推断并批量替换页眉或水印。

如果需要修改这些内容，应由用户明确指定。

---

# 22. 当前文件优先原则

整个“数学竞赛”项目都遵守：

> 当前本地文件是代码层面的 source of truth。

Codex 开始修改前必须：

1. 读取当前实际文件；
2. 理解用户已经手工做过的修改；
3. 在当前版本上增量修改；
4. 不要根据旧聊天、旧模板或旧输出覆盖用户现有内容。

尤其不要擅自覆盖：

```text
作者
书名
章节文件名
目录结构
preamble
分页逻辑
subfiles 结构
用户手工修正过的公式
```

---

# 23. 忠实整理原则

项目的首要目标是忠实整理原资料，而不是擅自“优化”内容。

如果发现原文疑似数学错误：

不要直接修改成模型认为正确的版本。

可以：

```latex
% TODO: CHECK SOURCE — 原文此处疑似有误
```

或者在最终报告中说明。

只有用户明确要求“检查并纠错”时，才修改原文数学内容。

---

# 24. 编译环境

主要环境：

```text
Windows
VS Code
LaTeX Workshop
XeLaTeX
latexmk
```

完整编译示例：

```powershell
latexmk -xelatex "数学分析培优讲义.tex"
```

清理辅助文件：

```powershell
latexmk -C
```

然后重新：

```powershell
latexmk -xelatex "数学分析培优讲义.tex"
```

其他未来子项目应使用各自主文件名。

---

# 25. 不要手工修改辅助文件

整个项目中以下文件均视为编译生成物：

```text
*.aux
*.toc
*.out
*.log
*.fls
*.fdb_latexmk
*.synctex.gz
```

遇到：

```text
目录
书签
编号
引用
```

问题时：

不要直接编辑这些辅助文件。

应修改 `.tex` 源码并重新编译。

---

# 26. 编译后质量检查

不能只检查：

```text
PDF 是否生成
```

每次较大修改后，应检查：

```text
LaTeX Error
Undefined control sequence
Missing $
Missing }
Extra }
Environment ... undefined
Overfull \hbox
Underfull \hbox
Overfull \vbox
Underfull \vbox
Token not allowed in a PDF string
Font shape ... not available
Size substitutions
Missing character
undefined references
```

如果出现 warning：

先理解原因，再修改源码。

不要为了“清零 warning”破坏数学内容或版面。

---

# 27. 公共机械检查

全项目涉及数学公式时，建议搜索：

```text
\binom
\tfrac
```

原则上正文应避免这两种写法。

对于“数学分析培优讲义”额外检查：

```text
\marktriangle
\markstartriangle
```

正文调用应为 0。

同时检查：

```text
所有 example 后是否有 \exampleblank
数学标题是否正确使用 \texorpdfstring
是否存在纯标题空白页
十三章是否均可独立编译
全书是否完整编译
```

---

# 28. Codex 工作方式

Codex 不应只负责“生成文本”。

标准工作流应为：

```text
读取根 AGENTS.md
↓
读取当前子项目文件
↓
读取 writing-mathematical-latex Skill
↓
理解当前任务
↓
增量修改源码
↓
编译
↓
读取编译日志
↓
修复错误与不合理 warning
↓
再次编译
↓
检查 PDF 版面
↓
报告修改内容
```

如果任务只涉及某一章：

先单独编译该章，再编译整书。

如果任务涉及工程结构：

必须验证所有相关子文件仍能工作。

---

# 29. 关于未来高等代数项目

后续会建立高等代数相关 LaTeX 子项目。

目前 `source/` 中已经有：

```text
高代基础打印版.pdf
高代培优上打印版.pdf
高代培优下打印版.pdf
```

未来可能建立：

```text
高等代数基础/
高等代数培优讲义/
```

或用户指定的其他中文名称。

在正式开始高等代数项目之前：

1. 不要自行假设最终书名；
2. 不要自行假设章节结构；
3. 不要自行复制数学分析的十三章结构；
4. 不要自行规定其例题留白方式；
5. 不要自行规定其分页规则；
6. 不要自行规定其特殊环境。

但以下全局规则仍然继承：

```text
writing-mathematical-latex Skill
组合数 C_k^n 规范
当前文件优先
忠实整理原则
编译与日志检查
不手改辅助文件
中文项目结构优先
```

正式开始高等代数时，应先读取该书当前资料与用户要求，再建立自己的子项目规则。

---

# 30. 禁止事项

除非用户明确要求，否则不要：

1. 把整个项目误认为只有“数学分析培优讲义”。
2. 把根目录 AGENTS.md 写成只适用于数学分析。
3. 把不同书籍的章节混到同一目录。
4. 擅自重命名 `source/` 中的原始资料。
5. 把中文项目名、章节名改成英文。
6. 未读取 `writing-mathematical-latex` 就大规模修改数学公式。
7. 使用 `\binom`。
8. 大量使用 `\tfrac`。
9. 用旧版本覆盖用户手工修改。
10. 擅自纠正原资料疑似错误。
11. 手工修改 `.toc`、`.aux` 等辅助文件。
12. 修改源码后不编译验证。
13. 只看“编译成功”而忽略明显 warning。
14. 为统一风格而破坏一个已经工作的子项目。
15. 把数学分析专属规则未经确认复制到未来高等代数项目。

---

# 31. 当前阶段重点

当前阶段主要工作对象是：

```text
数学分析培优讲义/
```

该子项目已经完成基本工程搭建，并已经有第 1—13 章源码。

后续重点应是：

```text
逐章检查
公式校对
版面修正
分页调整
warning 清理
单章编译稳定性
全书编译稳定性
```

在数学分析项目稳定后，再进入高等代数相关子项目。

---

# 32. 最终原则

整个“数学竞赛”项目的核心原则是：

```text
一个总项目
+
多本独立数学讲义子项目
+
统一数学 LaTeX Skill
+
各书保留自己的结构和版式
+
当前本地文件优先
+
修改后必须真实编译验证
```

如果本文件与用户后续的新要求冲突：

> 永远以用户最新明确要求为准。
