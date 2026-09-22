# AGENTS.md — mathematics-competition 项目总规范

## 1. 项目定位

本仓库是一个长期维护的数学竞赛与数学课程资料工程，目标是同时保存：

- 原始题目、真题、扫描资料与参考 PDF；
- 经过整理的 LaTeX 讲义；
- 普通版、答案版等不同输出；
- 后续可能新增的数学分析、高等代数、数学竞赛专题等独立子项目。

当前已经完成较完整工程化整理的正式子项目是：

```text
数学分析培优/
高等代数培优/
```

此外，仓库中还保存了：

```text
CMC历年真题/
source/
```

其中 `CMC历年真题/` 主要作为竞赛资料库使用，`source/` 保存后续整理讲义时需要对照的原始资料。

本文件是仓库根目录的总规则。后续如果某个子项目需要大量专属规则，可以在对应子目录中增加自己的 `AGENTS.md`；子项目规则只约束该子项目。

---

## 2. 规则优先级

工作时按以下优先级执行：

```text
用户当前明确要求
>
当前子项目中的 AGENTS.md（若存在）
>
根目录 AGENTS.md
>
writing-mathematical-latex Skill
>
当前源码已经形成的稳定写法
>
模型默认习惯
```

如果规则发生冲突，以更高优先级为准。

涉及讲义创建,录入,编辑,解答,校对,编译或验证时,必须先读取项目级 Skill:

```text
.agents/skills/writing-math-competition-lectures/SKILL.md
```

该 Skill 管理讲义工作流和各书专属规则. 数学公式细节继续由 `writing-mathematical-latex` 管理,数学推理由 `math-reasoning` 管理,PDF 读取与渲染检查由 `pdf` 管理.

涉及数学公式、数学环境、LaTeX 源码时，必须先读取：

```text
C:\Users\m1881\.codex\skills\writing-mathematical-latex\SKILL.md
```

不要仅凭模型习惯大规模改写数学 LaTeX。

---

## 3. 当前仓库结构

当前主要结构为：

```text
mathematics-competition/
│
├─ AGENTS.md
├─ README.md
├─ .gitignore
│
├─ CMC历年真题/
│  ├─ CMC 真题、汇编与解析资料
│  ├─ 历届 CMC 全部试题及解答
│  └─ 石油大学高数竞赛真题、备选题、模拟题等
│
├─ source/
│  ├─ 数分基础打印版.pdf
│  ├─ 数分培优上打印版.pdf
│  ├─ 数分培优下打印版.pdf
│  ├─ 高代基础打印版.pdf
│  ├─ 高代培优上打印版.pdf
│  └─ 高代培优下打印版.pdf
│
├─ 数学分析培优/
│  ├─ elegantbook.cls
│  ├─ preamble.tex
│  ├─ README.md
│  ├─ 数学分析培优讲义.tex
│  ├─ 数学分析培优讲义(答案版).tex
│  ├─ 数学分析培优讲义.pdf
│  ├─ 数学分析培优讲义(答案版).pdf
│  └─ 章节/
│     └─ 第X章_章名/
│        ├─ 第X章_章名_内容.tex
│        ├─ 第X章_章名.tex
│        └─ 第X章_章名(答案版).tex
│
└─ 高等代数培优/
   ├─ elegantbook.cls
   ├─ preamble.tex
   ├─ README.md
   ├─ 解答问题记录.md
   ├─ 高等代数培优讲义.tex
   ├─ 高等代数培优讲义(答案版).tex
   ├─ 高等代数培优讲义.pdf
   ├─ 高等代数培优讲义(答案版).pdf
   └─ 章节/
      └─ 第X章_章名/
         ├─ 第X章_章名_内容.tex
         ├─ 第X章_章名.tex
         └─ 第X章_章名(答案版).tex
```

不要擅自改变已经稳定使用的中文目录名、章节名和文件命名方式。

---

## 4. 不同目录的职责

### 4.1 `CMC历年真题/`

该目录是竞赛资料库。

除非用户明确要求整理、重命名、提取或重构，否则：

- 不批量移动文件；
- 不批量改名；
- 不修改原始 PDF、ZIP 或扫描资料；
- 不为了“统一项目结构”而把它改造成 LaTeX 工程。

如果需要基于其中资料生成新的专题讲义，应新建独立子项目，而不是破坏原资料目录。

### 4.2 `source/`

`source/` 是原始参考资料目录。

规则：

- 原始 PDF 只用于查阅、校对和溯源；
- 不擅自修改、压缩、覆盖、移动或重命名；
- 当前 `.tex` 源码是代码层面的工作基线，原始 PDF 是内容校勘依据；
- 若源码与原始资料疑似不一致，应先报告，不要直接把模型判断当作原文事实。

### 4.3 LaTeX 子项目

每一本正式整理的讲义使用独立目录，并拥有自己的：

```text
主 .tex
preamble.tex
elegantbook.cls
章节/
README.md
必要时的其他项目文件
```

规则：

- 两本讲义共用同一份 `elegantbook.cls` 与 `preamble.tex`，两份文件在各讲义目录下逐字节相同；
- 修改共享文件时必须同步到另一本，并且两本都要重新编译验证；
- 页眉、水印、标题页样式、例题编号、数学算子在两本之间保持一致；
- 需要新增自定义命令时，直接加进共享的 `preamble.tex`，不要只改其中一本。

各本之间仍然互相独立的只有：

- 书名与主文件名；
- 章节列表与章节目录名；
- 正文学术内容与例题；
- 各自的问题记录文件。

---

## 5. 当前文件优先原则

开始修改前必须读取当前最新文件。

始终遵守：

> 当前源码是代码层面的 source of truth。

不要根据旧聊天、旧分支、旧模板或以前生成过的文件覆盖用户之后已经手工修改的内容。

尤其不要擅自覆盖：

- 题面；
- 答案；
- 章节名；
- 作者名；
- 页眉、水印；
- 编号方式；
- 分页逻辑；
- 文件结构；
- 用户手工修正过的数学公式。

如果需要大规模重构，先理解当前结构，再增量修改。

---

## 6. 公共数学 LaTeX 规范

整个仓库中的正式 LaTeX 讲义遵守以下规则。

### 6.1 数学定界符

行内公式：

```latex
$...$
```

行间公式：

```latex
\[
...
\]
```

或者根据结构使用：

```latex
equation
align
aligned
gather
multline
cases
matrix
pmatrix
vmatrix
```

禁止使用：

```latex
$$...$$
```

### 6.2 分式与大型运算符

普通位置优先：

```latex
\dfrac{a}{b}
```

上下标中的分式根据 Skill 使用：

```latex
\frac{...}{...}
```

极限、求和、乘积等按照 Skill 使用显式上下标，例如：

```latex
\lim\limits_{n\to\infty}
\sum\limits_{k=1}^{n}
\prod\limits_{k=1}^{n}
```

普通一维定积分不要机械添加 `\limits`。

### 6.3 微分、组合数与列向量

微分符号使用直立体：

```latex
\mathrm{d}x
```

组合数统一使用：

```latex
C_{k}^{n}
```

一律不使用：

```latex
\binom{n}{k}
```

需要把两个分量上下堆成列向量时，同样不要用 `\binom{x}{y}`，
而使用矩阵环境：

```latex
\begin{pmatrix}
    x\\
    y
\end{pmatrix}
```

注意 `\pmatrix{x\\y}` 是 amsmath 不接受的旧写法，必须写完整的
`\begin{pmatrix}` 环境。

不要机械使用：

```latex
\tfrac
```

### 6.4 数学省略号

数学模式中不要直接输入 Unicode 省略号：

```text
…
```

根据语义使用：

```latex
\ldots
\cdots
```

例如：

```latex
$x_1,x_2,\ldots,x_n$
$a_1+a_2+\cdots+a_n$
```

---

## 7. 语义化环境

正式讲义优先使用语义化环境：

```latex
definition
example
theorem
axiom
lemma
proposition
corollary
remark
proof
solution
```

约定：

- `proof` 用于定理、命题等理论证明；
- `solution` 用于例题解答；
- 不再使用 `proof[解]` 充当例题答案。

说明性内容已经有明确环境时，不退化成普通粗体文本或随意的 `PS:`。

---

## 8. 数学分析培优

### 8.1 基本结构

`数学分析培优/` 已迁移为 ElegantBook 单源结构。

该项目包含 13 章：

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

不要擅自修改这些正式章名。

### 8.2 三文件单源结构

每章固定采用：

```text
第X章_章名_内容.tex
第X章_章名.tex
第X章_章名(答案版).tex
```

其中：

- `_内容.tex` 是唯一真正维护数学正文的文件；
- 普通版入口继承普通版主文件；
- 答案版入口继承答案版主文件；
- 两个入口只负责选择编译配置并载入同一内容文件；
- 禁止重新维护两套题目和两套正文。

两个入口通过 `subfiles` 的 `\documentclass[..........]{subfiles}` 继承主文件，
因此单章入口可以脱离整书独立编译。

### 8.3 普通版与答案版

普通版：

```latex
result=noanswer
```

输出：

```text
完整理论正文 + 例题 + 书写留白
```

`solution` 不显示。

答案版：

```latex
result=answer
```

输出：

```text
完整理论正文 + 例题 + 解答
```

正式 `proof` 在两个版本中都必须保留。

### 8.4 例题

例题保持 section 级编号，例如：

```text
例题 1.1.1
例题 1.1.2
例题 1.2.1
```

每个 `example` 后保留统一的：

```latex
\exampleblank
```

其具体行为由 `preamble.tex` 根据 ElegantBook 的 `result` 模式控制:

- 普通版留出书写空间；
- 答案版不额外留白。

标准结构：

```latex
\begin{example}
...
\end{example}
\exampleblank

\begin{solution}
...
\end{solution}
```

### 8.5 `methodsection`

本讲义使用：

```latex
\methodsection{(A) ...}
```

表示方法分类。

要求：

- 使用无编号 `subsubsection*`；
- 加入目录；
- 使用 `\phantomsection` 建立独立书签锚点；
- 不改成正式 section/subsection；
- 不机械分页。

### 8.6 ElegantBook 与 preamble 的职责

`elegantbook.cls` 负责较稳定、可复用的能力，例如：

- 页面布局；
- 标题系统；
- 数学宏包；
- 定理环境；
- `watermark/nowatermark`；
- `result=answer/noanswer`；
- `\ifshowanswer`；
- 目录与编号深度。

`preamble.tex` 负责数学分析讲义自己的可调设置，例如：

- 页眉页脚；
- 水印文字；
- 标题页；
- 例题编号；
- `\exampleblank`；
- `\methodsection`；
- 难度标记；
- 自定义数学算子；
- `enumerate` 间距；
- `\emergencystretch`。

不要把个人化配置重新写死到 class 中。

两本讲义都使用项目级开关控制水印，而不是文档类选项：

```latex
\newif\ifmathanalysiswatermark
\mathanalysiswatermarktrue
```

原因是单章入口通过 `subfiles` 继承主文件时，可能读到 TeX Live 自带的
`elegantbook.cls`，此时文档类选项不一定生效。修改水印行为时不要改成
`watermark` / `nowatermark` 文档类选项。

该开关由两本讲义共用的 `preamble.tex` 读取，因此这条规则对两本同时生效；
两本的主文件都必须定义同名开关。

### 8.7 中文字体与楷体粗体

`definition`、`theorem`、`remark` 等环境的正文用 `\cnormal`（即 `\kaishu`）
排成楷体。ctex 的 Windows 字体集没有给楷体声明 BoldFont，因此在楷体环境里
`\textbf` 会去要「粗体楷体」，触发：

```text
LaTeX Font Warning: Font shape `TU/KaiTi(0)/b/n' undefined
```

并退回常规字重，只能靠 AutoFakeBold 合成伪粗体。

共享 `elegantbook.cls` 的 `chinesefont=ctexfont` 分支（默认分支）中已补上真粗体：

```latex
\setCJKfamilyfont{zhkai}[BoldFont={SimHei}]{KaiTi}
```

- 方括号外的 `KaiTi` 是基础字体，楷体字形保持不变；
- 粗体用 `SimHei`，与本书 `\heiti` 已经在用的黑体是同一款，加粗与黑体风格一致；
- 这一行是有意重定义 ctex 已经定义过的字体族，所以只把这一次的 xeCJK 警告
  `CJKfamily-redef` 压掉，结束处立即恢复该消息的默认处理，以后真出现重复
  定义仍会报警。两个辅助宏 `\elegantkaiboldsilence`、`\elegantkaiboldrestore`
  必须定义在参数之外：把 `\ExplSyntaxOn` 写进 `\ifdefstring` 的分支参数里
  不生效，参数在被记成记号时 catcode 已经确定，直接写 `\msg_redirect_name:nnn`
  会被拆成 `\msg` 而报 `Undefined control sequence`；
- `preamble.tex` 中保留同一补丁的兜底分支：单章独立编译读到的是 TeX Live 自带的
  `elegantbook.cls`，class 中的补丁不会执行，此时按本地 class 是否定义了
  `\elegantkaiboldsilence` 判断并补做一次，使单章 PDF 与整书 PDF 的楷体粗体一致。

不要为了消除提示去删掉这一行或改成 `AutoFakeBold` 伪粗体；也不要把字体族的
定义重新挪回 `preamble.tex` 并与 class 各留一份。

不要改写成下面这种写法：

```latex
\setCJKfamilyfont{zhkai}[BoldFont={FZHei-B01}]{FZKai-Z03}
```

方括号外的 `FZKai-Z03` 是基础字体，那样写会连楷体字形一起换成方正楷体_GBK，
而宋体、黑体、仿宋仍是 Windows 字体，一本书里混两套厂商的字，风格不统一。

若要整套改用方正字族，正确做法是在主文件传 `chinesefont=founder`，
由 `elegantbook.cls` 的四族一起替换，而不是只改 `zhkai` 一行。

---

## 9. 高等代数培优

### 9.1 基本结构

`高等代数培优/` 同样采用 ElegantBook 单源结构，整理自原《高代培优上打印版》
《高代培优下打印版》。

该项目包含 10 章：

```text
第一章   多项式
第二章   行列式
第三章   矩阵
第四章   线性空间与线性方程组
第五章   线性变换
第六章   相似标准型
第七章   二次型
第八章   欧氏空间
第九章   矩阵综合
第十章   张量积与外积
```

不要擅自修改这些正式章名。

其中第十章《张量积与外积》是原讲义的选学章节。

### 9.2 章节目录命名

章节目录在书名之外额外使用两位数字前缀：

```text
章节/
├─ 01_第一章_多项式/
├─ 02_第二章_行列式/
├─ 03_第三章_矩阵/
├─ 04_第四章_线性空间与线性方程组/
├─ 05_第五章_线性变换/
├─ 06_第六章_相似标准型/
├─ 07_第七章_二次型/
├─ 08_第八章_欧氏空间/
├─ 09_第九章_矩阵综合/
└─ 10_第十章_张量积与外积/
```

这是为了在 Windows 资源管理器中按章节顺序排列，不要擅自删除前缀。
每章目录内部仍使用与 §8.2 相同的三文件结构：

```text
第X章_章名_内容.tex
第X章_章名.tex
第X章_章名(答案版).tex
```

`_内容.tex` 依旧是唯一维护理论正文、题目与解答的文件。

### 9.3 例题规模

本章讲义当前整理完成 511 道例题，每道例题对应一个 `solution`。

例题与解答的编号、留白和显示方式遵循 §8.3、§8.4 的同一套语义结构。

### 9.4 内容依据

高等代数培优的内容依据是：

```text
source/高代培优上打印版.pdf
source/高代培优下打印版.pdf
```

### 9.5 问题记录

整理过程中发现的原题问题统一记录到：

```text
高等代数培优/解答问题记录.md
```

该文件只保存真正需要后续核对的内容，不要把每一道正常例题都写进去。
登记范围包括：

- 原题题面错误或疑义；
- 条件不足；
- 符号、下标或印刷错误；
- 原讲义定理表述需要补充条件的地方；
- 仍值得第二轮数学复核的解答。

### 9.6 与数学分析培优共用同一套工程文件

高等代数培优与数学分析培优共用完全相同的工程文件，不维护两份：

- `elegantbook.cls` 与 `preamble.tex` 在两本讲义目录下逐字节相同；
- 主文件的文档类选项、项目级水印开关 `\ifmathanalysiswatermark`、
  `\input{preamble}` 的位置一致；
- 水印文字与页眉右侧文字统一为「欧拉的小迷弟」；
- 封面信息统一为 `\author{欧拉的小迷弟}`、`\date{\today}`；
- 数学算子（`\Tr`、`\tr`、`\rank`、`\diag`、`\Ree`、`\Imm`、`\Ker`、`\Span`）
  在共享 `preamble.tex` 中统一声明。

各本之间仍然互相独立的只有书名、章节列表、正文学术内容与问题记录。

改动共享文件后必须同步另一本并重新编译验证，不要只改其中一本。

### 9.7 标记与分类约定

难度标记只使用两档五角星：

```latex
\markstar         ★
\marktwostar      ★★
```

不使用 `\marktriangle`（▲）和 `\markstartriangle`（★▲）；需要时分别改用
`\markstar` 和 `\marktwostar`。标记写在定理、命题或例题的可选参数中，
未标记的条目视为基础难度。

选学章节在标题末尾加 ASCII 星号，例如：

```latex
\chapter{张量积与外积 *}
```

这与数学分析培优标记选学 `section` 的写法一致，除此之外不写额外说明。

高等代数培优不使用 `\methodsection`，方法分类用 `\subsection` 表达。

### 9.8 记号约定

- 矩阵和向量用 `\begin{pmatrix}`，行列式用 `\begin{vmatrix}`；
  不使用 `\pmatrix{...}`，该写法会被 amsmath 拒绝。
- 转置使用 `\mathsf T`，例如 `A^{\mathsf T}`。
- 组合数使用 `C_{k}^{n}`，不使用 `\binom`。
- 数学算子统一在共享 `preamble.tex` 中声明。

高等代数培优的完整专属规则见：

```text
.agents/skills/writing-math-competition-lectures/references/advanced-algebra-excellence.md
```

---

## 10. 分页与目录

两本讲义当前共同约定：

- `\chapter` 自己分页，不在其后机械添加 `\newpage`；
- 正式 `section` 按各自讲义既有规则处理分页；
- `subsection` 与 `methodsection` 不机械分页；
- 连续的多级标题应形成同一页首标题组；
- 不制造只有标题的大空白页。

无编号标题如果不需要进入目录，直接使用：

```latex
\section*{...}
```

不要机械追加 `\addcontentsline`。

如果确实需要无编号标题进入目录，则先建立独立锚点：

```latex
\phantomsection
\addcontentsline{toc}{...}{...}
```

---

## 11. hyperref 与数学标题

标题中含数学公式时，必须保证 PDF bookmark 可用。

例如：

```latex
\subsection{
    \texorpdfstring{$\mathbb{R}^n$}{R^n} 中的点集
}
```

不要通过删除标题中的数学内容来解决：

```text
Token not allowed in a PDF string
```

应正确使用 `\texorpdfstring`。

---

## 12. 行宽与排版 warning

不要通过以下方式全局掩盖问题：

```latex
\sloppy
\hfuzz=...
\hbadness=...
```

项目允许在各讲义自己的 `preamble.tex` 使用适度的：

```latex
\setlength{\emergencystretch}{2em}
```

处理轻微断行压力。

遇到明显 `Overfull \hbox` 时，应优先根据内容处理：

- 长行内公式改为行间公式；
- 多步等式使用 `aligned`；
- 单条超长行间公式使用 `multline`；
- 必须行内时可在自然位置使用 `\allowbreak`；
- 列表中注意正文可用宽度变窄。

不要仅为了 warning 数量为零而牺牲可读性。

---

## 13. 内容忠实原则

本项目以整理和校勘为主，不默认承担数学纠错。

如果发现题面、条件、符号或答案疑似有误：

- 不擅自改题；
- 不静默“修正”成模型认为正确的版本；
- 优先对照 `source/` 中原始资料；
- 不能确认时保留当前内容并明确标记待核对；
- 只有用户明确要求“校对并修正”时才修改数学内容。

整理中确实需要处理原题问题时的标准流程：

```text
对照 source/ 原始 PDF
↓
判断是题面问题、条件不足，还是答案问题
↓
在正文中明确说明原题问题
↓
给出能够可靠确定的标准结论，或按字面题意的结果
↓
同步登记到该讲义的解答问题记录
```

数学分析培优与高等代数培优各自维护自己的问题记录文件；
不要用模型推断静默替换原题内容。

---

## 14. 编译环境

主要环境：

```text
Windows
VS Code
LaTeX Workshop
XeLaTeX
latexmk
```

数学分析整书普通版：

```powershell
cd "数学分析培优"
latexmk -xelatex "数学分析培优讲义.tex"
```

数学分析整书答案版：

```powershell
cd "数学分析培优"
latexmk -xelatex "数学分析培优讲义(答案版).tex"
```

高等代数整书普通版：

```powershell
cd "高等代数培优"
latexmk -xelatex "高等代数培优讲义.tex"
```

高等代数整书答案版：

```powershell
cd "高等代数培优"
latexmk -xelatex "高等代数培优讲义(答案版).tex"
```

清理辅助文件：

```powershell
latexmk -C
```

两本讲义的章节入口文件也必须支持独立编译。

---

## 15. 修改后的验证要求

修改单章时，至少检查：

```text
该章普通版
该章答案版
```

涉及公共宏、`preamble.tex`、`elegantbook.cls`、主文件或工程结构时，还必须检查：

```text
整书普通版
整书答案版
```

只改某一本的章节正文时，不需要编译另一本；
但凡改动 `elegantbook.cls`、`preamble.tex` 或任一主文件，两本都必须重新编译验证。

编译后重点检查：

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
Missing character
Font shape ... not available
Size substitutions
undefined references
```

warning 要理解原因后再处理，不要机械屏蔽。

---

## 16. 编译生成物

以下均视为辅助文件，不手工编辑：

```text
*.aux
*.bbl
*.bcf
*.blg
*.fdb_latexmk
*.fls
*.log
*.out
*.run.xml
*.synctex.gz
*.toc
*.xdv
```

PDF 是否纳入 Git 由当前子项目既有习惯决定；不要在没有用户要求时批量删除已经提交的成品 PDF。

---

## 17. Codex / AI 标准工作流

处理仓库任务时，建议遵守：

```text
读取根 AGENTS.md
↓
读取目标子项目当前 README / preamble / 主文件
↓
读取 writing-mathematical-latex Skill
↓
读取需要修改的最新源码
↓
若涉及原题，读取对应 source PDF
↓
理解任务与现有结构
↓
增量修改
↓
编译相关单章
↓
编译相关整书
↓
读取日志
↓
修复真正的问题
↓
检查 PDF 版面
↓
必要时更新解答问题记录
↓
报告修改内容
```

如果任务只是整理资料，不要擅自扩展成全项目重构。

---

## 18. 未来子项目

后续可能建立：

```text
高等代数基础/
其他竞赛专题/
```

（`source/` 中已经备有高代基础打印版资料；数学分析培优、高等代数培优已完成第一轮整理。）

在正式建立之前，不自动复制现有讲义的：

- 章节结构；
- 例题编号；
- 10 行留白；
- `methodsection`；
- 两位数字目录前缀；
- 分页方式；
- 个人页眉、水印。

可以复用的是经过确认的通用 LaTeX 能力和数学排版规范。

---

## 19. 禁止事项

除非用户明确要求，否则禁止：

1. 把整个仓库误认为只有某一个讲义项目；
2. 批量改动 `CMC历年真题/` 或 `source/` 中的原始资料；
3. 把不同书籍的章节混在同一子项目；
4. 重新维护普通版、答案版两套数学正文；
5. 使用旧版本覆盖用户最新修改；
6. 擅自改题、改答案或“纠正”原始资料；
7. 用 `proof[解]` 表示例题答案；
8. 使用 `\binom`（包括用它把分量上下堆成列向量）或机械使用 `\tfrac`；
9. 在数学模式直接输入 Unicode 省略号 `…`；
10. 手工编辑 `.aux`、`.toc`、`.out` 等辅助文件；
11. 通过全局 `\sloppy`、大 `\hfuzz` 等方式掩盖明显排版问题；
12. 修改源码后不进行相应编译检查；
13. 只改一本讲义的 `elegantbook.cls` 或 `preamble.tex` 而不同步另一本（两份必须保持逐字节相同）；
14. 删除或静默改写 `解答问题记录.md` 中已经登记的原题疑义。

如果本文件与用户之后的新要求冲突，以用户最新明确要求为准。
