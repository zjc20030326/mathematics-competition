# AGENTS.md — 数学竞赛 LaTeX 项目总规范

## 1. 项目定位

本仓库是“数学竞赛”总项目,用于长期整理数学竞赛、数学分析、高等代数等讲义和资料.

当前已完成工程化整理的主要子项目是:

```text
数学分析培优/
```

后续可继续建立高等代数等独立子项目.不同书籍不得混用章节目录、主文件或专属排版规则.

---

## 2. 当前目录原则

```text
mathematics-competition/
├─ AGENTS.md
├─ source/
├─ 数学分析培优/
│  ├─ elegantbook.cls
│  ├─ preamble.tex
│  ├─ README.md
│  ├─ 数学分析培优讲义.tex
│  ├─ 数学分析培优讲义(答案版).tex
│  └─ 章节/
│     └─ 第X章_章名/
│        ├─ 第X章_章名_内容.tex
│        ├─ 第X章_章名.tex
│        └─ 第X章_章名(答案版).tex
└─ 其他后续子项目/
```

其中:

1. `source/` 保存原始 PDF,不擅自修改、移动或重命名.
2. 每本讲义使用自己的子目录、主文件和 `preamble.tex`.
3. “数学分析培优”当前把 `elegantbook.cls` 与 `preamble.tex` 放在同一子项目目录中.
4. 每章真正的数学内容只维护在一个 `_内容.tex` 文件中.

---

## 3. 规则优先级

```text
用户当前明确要求
>
本 AGENTS.md
>
全局 writing-mathematical-latex Skill
>
项目当前已有写法
>
模型默认习惯
```

数学公式、数学环境和 LaTeX 细节必须先读取:

```text
C:\Users\m1881\.codex\skills\writing-mathematical-latex\SKILL.md
```

---

## 4. 公共数学 LaTeX 规则

- 行内公式使用 `$...$`.
- 行间公式使用 `\[...\]`、`equation`、`align`、`gather` 等;禁止 `$$...$$`.
- 普通位置分式优先 `\dfrac`;上下标中的分式按 Skill 使用 `\frac`.
- 极限、求和、乘积按 Skill 使用 `\limits`.
- 普通一维定积分不要机械添加 `\limits`.
- 微分符号按 Skill 使用直立 `\mathrm{d}`.
- 组合数统一使用 `C_{k}^{n}`,禁止 `\binom{n}{k}`.
- 不机械使用 `\tfrac`.

---

## 5. 语义化环境

优先使用:

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

其中:

- `proof`:正式定理、命题等理论证明,普通版和答案版都保留;
- `solution`:例题解答,由 `result=answer/noanswer` 控制.

不要再用 `proof[解]` 表示例题答案.

---

## 6. 数学分析培优:两个输出版本

普通版主文件:

```text
数学分析培优讲义.tex
```

使用:

```latex
result=noanswer
```

输出“完整理论正文 + 例题 + 书写留白”,隐藏 `solution`.

答案版主文件:

```text
数学分析培优讲义(答案版).tex
```

使用:

```latex
result=answer
```

输出“完整理论正文 + 例题 + 解答”.

两个版本必须读取同一份章节内容,禁止再次维护两套数学正文.

---

## 7. 数学分析培优:三文件单源结构

每章固定为:

```text
第X章_章名_内容.tex
第X章_章名.tex
第X章_章名(答案版).tex
```

规则:

1. `_内容.tex` 是唯一内容源,包含 chapter、section、正文、例题、`solution`.
2. 普通入口通过 `subfiles` 继承普通版主文件,再 `\input` 同一个内容文件.
3. 答案入口通过 `subfiles` 继承答案版主文件,再 `\input` 同一个内容文件.
4. 两个入口文件禁止复制题目、理论正文或答案.
5. 普通版、答案版都必须支持单章独立编译.

---

## 8. 十三章名称

固定为:

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

不要擅自改章名、改英文或删除文件名中的下划线.

---

## 9. 例题规则

本讲义保留 section 级编号:

```text
例题 1.1.1
例题 1.1.2
例题 1.2.1
```

每个 `example` 后必须保留统一宏:

```latex
\exampleblank
```

其行为由 `preamble.tex` 根据 `\ifshowanswer` 自动控制:

- 普通版:留 `10\baselineskip`;
- 答案版:不留白.

答案统一紧跟在对应例题之后:

```latex
\begin{example}
...
\end{example}
\exampleblank

\begin{solution}
...
\end{solution}
```

---

## 10. methodsection

`\methodsection{(A) ...}` 表示讲义内部的方法分类.

- 使用无编号 `subsubsection*`;
- 进入目录;
- 必须使用 `\phantomsection` 建立独立书签锚点;
- 不得改成普通 section/subsection;
- 不得让其机械独占一页.

---

## 11. 分页规则

- `\chapter` 自己分页,不在其后机械加 `\newpage`.
- 新的正式 `section` 按当前讲义已有规则从新页开始.
- `subsection` 和 `methodsection` 不单独分页.
- 连续层级标题应作为同一页首标题组,不能制造只有标题的大空白页.

---

## 12. 标题中的数学公式

section/subsection/methodsection 标题中出现数学公式时,必须兼容 hyperref 书签,例如:

```latex
\subsection{\texorpdfstring{$\mathbb{R}^n$}{R^n} 中的点集}
```

不得通过删除数学内容来规避 PDF string warning.

---

## 13. ElegantBook 与 preamble 的职责

`elegantbook.cls` 放通用、稳定能力:

- ElegantBook 页面布局与标题系统;
- 数学宏包;
- 定理/例题/solution 环境;
- `watermark/nowatermark`;
- `result=answer/noanswer`;
- 公开的 `\ifshowanswer`;
- 目录与编号深度等通用设置.

`preamble.tex` 放本讲义的项目级设置:

- 页眉页脚;
- 水印文字;
- section 级例题编号;
- `\exampleblank`;
- `\methodsection`;
- 难度标记;
- 自定义数学算子;
- 本讲义标题页.

不要把个人昵称、具体页眉等写死进 class.

---

## 14. 当前答案状态

数学分析培优共 13 章,当前答案版已经覆盖全部例题.结构迁移时不得擅自补题、删题、改题或重写答案.

现阶段仍有一批题面需要对照原始 PDF 进一步校勘.若题面存在疑义,应保留当前已经给出的反例、按字面题意所得结果或分情况讨论,不擅自修改原题.

---

## 15. 当前文件优先与忠实整理

当前最新源码是代码层面的 source of truth.

修改前必须读取当前文件,在现有版本上增量修改.不要用旧聊天、旧模板、旧答案覆盖用户已完成的工作.

发现疑似数学错误时:

- 不擅自纠错;
- 可保留题解中的核对说明;
- 只有用户明确要求数学复核时才修改数学内容.

---

## 16. 编译环境

主要环境:

```text
Windows
VS Code
LaTeX Workshop
XeLaTeX
latexmk
```

整书:

```powershell
latexmk -xelatex "数学分析培优讲义.tex"
latexmk -xelatex "数学分析培优讲义(答案版).tex"
```

修改某一章时,应同时测试:

```text
该章普通版
该章答案版
整书普通版
整书答案版
```

---

## 17. 编译质量检查

较大修改后至少检查:

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

不要为了清零 warning 破坏数学内容.

---

## 18. 辅助文件

以下均为编译生成物,不手工编辑、不作为内容源:

```text
*.aux
*.toc
*.out
*.log
*.fls
*.fdb_latexmk
*.synctex.gz
```

生成 PDF 和 SyncTeX 不应与章节源码混为一体;清理后应能重新完整编译.

---

## 19. 公共机械检查

建议搜索:

```text
\binom
\tfrac
```

数学分析培优额外检查:

```text
正文中的 \marktriangle
正文中的 \markstartriangle
example 与 solution 数量
每个 example 后是否存在 \exampleblank
数学标题中的 \texorpdfstring
subfiles 单章编译
```

---

## 20. Codex 标准工作流

```text
读取 AGENTS.md
↓
读取当前子项目文件
↓
读取 writing-mathematical-latex Skill
↓
理解任务
↓
增量修改
↓
单章编译
↓
整书普通版与答案版编译
↓
读取日志并修复错误
↓
检查 PDF 版面
↓
报告修改
```

---

## 21. 未来高等代数项目

未来建立高等代数项目时,不自动复制数学分析的:

- 十三章结构;
- 例题 section 编号;
- 10 行留白;
- methodsection;
- 分页规则.

但可以复用经过确认的通用 ElegantBook 能力和全局数学 LaTeX 规范.

---

## 22. 禁止事项

除非用户明确要求,否则不要:

1. 把整个仓库误认为只有数学分析.
2. 把不同书籍章节混到同一目录.
3. 擅自修改 source 原始 PDF.
4. 用两套章节正文分别维护普通版和答案版.
5. 用 `proof[解]` 继续充当例题答案.
6. 使用 `\binom` 或机械使用 `\tfrac`.
7. 擅自修正疑问题面.
8. 用旧版本覆盖当前文件.
9. 手改 aux/toc/out 等辅助文件.
10. 修改后不做编译与日志检查.

---

## 23. 当前阶段重点

当前“数学分析培优”已完成 13 章和全部例题解答的第一版整理,并迁移为 ElegantBook 单源结构.

下一阶段重点:

```text
疑问题面对照原始 PDF 校勘
全部解答逐章数学二审
版面细节调整
warning 清理
单章与整书编译稳定性
```

如果本文件与用户后续的新明确要求冲突,以用户最新要求为准.
