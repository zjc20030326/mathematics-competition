# 验证规则

## 1. 静态验证器

脚本:

```text
.agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py
```

脚本只读取和报告,不自动修改文件.

### changed scope

```powershell
python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope changed
```

- 已跟踪文件只检查 Git 新增和修改行的行级规则.
- 新文件检查全文.
- 被修改 TeX 文件的环境和定界符平衡检查全文,以识别删除造成的破坏.

### file scope

```powershell
python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope file --file PATH
```

可以重复 `--file`.

### project scope

```powershell
python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope project --project PATH
```

检查指定项目中的受支持文本文件,并在识别到 `数学分析培优` 或 `高等代数培优` 时运行该书专属的结构检查. 识别依据是主文件对, 见第 3 节.

### Exit code

- `0`: 没有 error 级诊断.
- `1`: 至少一个 error 级诊断.
- `2`: 命令参数,Git 状态或路径无法安全解析.

warning 不等于自动修复请求. 先判断是否为允许的代码,路径,公式或原文引用.

## 2. 通用规则编号

- `PUNC001`: 所选自然语言中出现中文标点. Markdown 代码围栏,行内代码和 URL 不检查.
- `TEXT001`: 存在未解决的待办标记.
- `LATEX001`: `.tex` 中使用 double-dollar 行间公式.
- `LATEX002`: 使用 `\binom`. 组合数改用 `C_k^n`; 上下堆叠的列向量改用 `\begin{pmatrix}` 环境 (`\pmatrix{...}` 是 amsmath 不接受的旧写法).
- `LATEX003`: 使用 `\tfrac`.
- `LATEX004`: `\begin` 和 `\end` 环境不匹配.
- `LATEX005`: 花括号,数学定界符或 `\left` 和 `\right` 不匹配.
- `CTRL001`: 出现异常控制字符.

Markdown 按项目规则允许 double-dollar 行间公式,因此 `LATEX001` 只检查 `.tex`.

## 3. 书籍结构规则编号

`MA` 规则按书籍档案 `BookProfile` 套用. 当前登记两本书:

```text
数学分析培优     13 章   section_break_required = True
高等代数培优     10 章   section_break_required = True
```

识别依据是同一目录下同时存在该书的普通版和答案版主文件.

- `MA001`: `example`,`exampleblank`,`solution` 顺序不完整或交叉.
- `MA002`: 章节目录,共享内容或双入口结构缺失或不一致.
- `MA003`: 普通版主文件不是 `result=noanswer`.
- `MA004`: 答案版主文件不是 `result=answer`.
- `MA005`: `preamble.tex` 未加载 `subfiles`.
- `MA006`: 章节后的首个 `section` 前出现多余 `\newpage`. 当该书 `section_break_required` 为真时,还检查后续 `section` 前是否缺少 `\newpage`.
- `MA007`: `subsection` 或 `methodsection` 前出现机械分页.
- `MA008`: 把 `watermark` 作为文档类选项传入.
- `MA009`: 水印 Boolean 声明或启用晚于 `preamble.tex`.
- `MA010`: 两个主文件没有按该书顺序引用全部章节.

两本书当前采用同一套分页约定: 每个非首个 `section` 前都紧跟 `\newpage`, 所以两本书的 `section_break_required` 都是 `True`.

该开关保留为按书配置: 某本书若改用不同的分页约定, 只需在该书档案里改成 `False`, 其余检查逻辑不变.

`MA` 规则只代表工程结构,不代表例题解答在数学上正确.

## 4. 编译矩阵

默认不编译. 修改完成后只运行静态验证器,并在报告里说明没有进行编译和目视检查.

只有用户明确要求编译验证时,才按下面的矩阵执行.

单章内容修改:

1. 该章普通版入口.
2. 该章答案版入口.
3. 整书普通版.
4. 整书答案版.

主文件,导言区,文档类,公共宏或工程结构修改:

1. 所有受影响的普通版章节入口.
2. 所有受影响的答案版章节入口.
3. 整书普通版.
4. 整书答案版.

## 5. 编译目录

用户要求编译验证时,默认使用系统临时目录中的纯英文路径作为 `latexmk -outdir`.

`-outdir` 的值必须是纯 ASCII. latexmk 4.87 (TeX Live 2026) 会把该目录同时作为环境变量 `TEXMF_OUTPUT_DIRECTORY` 传给 TeX, 值含非 ASCII 字符时 `xelatex.exe` 会在 `putenv` 阶段致命退出, 表现为退出码 12, 不生成 `.log`, 只留下一个 32 字节的占位 `.aux`. 源码路径和文件名含中文不受影响, 就地编译也正常.

要求:

- 不设置可能使 TeX 在启动前失败的中文输出环境变量.
- 每个编译目标使用独立输出目录.
- 不把 PDF 或辅助文件写回讲义目录.
- 只有用户明确要求更新成品 PDF 时才复制最终 PDF 回项目.

## 6. 日志扫描

用户要求编译验证时,逐个目标检查:

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
Unused global option
```

对每条 warning 说明:

- 所属目标.
- 是否由本次修改新增.
- 是否影响输出.
- 是否需要修复.

不得为了清零 warning 删除数学内容或全局屏蔽排版问题.

## 7. PDF 目视检查

用户要求编译验证时,以下改动必须目视检查:

- 分页和标题组.
- 章节开头.
- 水印.
- 标题页.
- 复杂公式或长公式.
- 普通版留白和答案版解答替换.
- 图片,表格和特殊环境.

记录实际查看的 PDF 路径和页码. 抽查部分页面时不得宣称检查了全部页面.

## 8. 证据报告

完成报告分别列出:

- 静态检查命令和诊断数量.
- 未执行或未覆盖的范围.

用户要求编译验证时,额外列出:

- 每个编译目标的源文件,exit code,日志和 PDF 页数.
- 日志错误和 warning 分类.
- 目视检查的 PDF 和具体页码.

未进行编译时,不得用静态检查结果暗示已经过编译或版面检查.
只有 PDF 生成不能证明编译质量. 只有源码扫描不能证明真实编译. 只有编译成功不能证明版面正确.
