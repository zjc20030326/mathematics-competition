---
name: writing-math-competition-lectures
description: Use when creating, transcribing, editing, solving, proofreading, compiling, or validating mathematical lecture notes under the 数学竞赛 project, including 数学分析培优 and 高等代数培优, blank and answer editions, chapter structure, mathematical solutions, LaTeX, source-PDF collation, or lecture-note quality checks.
---

# 数学竞赛讲义编写

本 Skill 管理 `数学竞赛` 项目下讲义的工作流,质量门和各书专属规则. 它不取代数学排版,数学推理或 PDF 专项 Skill.

## 触发范围

以下任务必须使用本 Skill:

- 创建或调整讲义工程.
- 从原始资料录入或校勘讲义.
- 修改讲义正文,例题,证明或解答.
- 维护普通版和答案版.
- 调整章节目录,分页,水印或单章入口.
- 编译,检查日志或目视检查 PDF.
- 判断一章或一本讲义是否完成.

`CMC历年真题` 的纯资料归档不自动触发本 Skill. 若要基于其中资料编写新讲义,则触发.

## 必须先读取

1. 读取仓库根目录 `AGENTS.md`.
2. 读取目标子项目的 `README.md`,主文件,`preamble.tex`,章节入口和共享内容文件.
3. 读取 [通用规则](references/common-rules.md).
4. 若目标是 `数学分析培优`,读取 [数学分析培优专属规则](references/math-analysis-excellence.md).
5. 若目标是 `高等代数培优`,读取 [高等代数培优专属规则](references/advanced-algebra-excellence.md).
6. 若任务包含静态检查,编译,日志或 PDF 验证,读取 [验证规则](references/validation-rules.md).

先读取当前文件,再增量修改. 当前本地文件是代码层面的工作基线.

## 必须协作的专项 Skill

- 数学公式和 LaTeX 修改必须读取 `writing-mathematical-latex`.
- 数学证明和解答必须读取 `math-reasoning`.
- 读取原始 PDF 或检查渲染 PDF 时必须读取 `pdf`.
- 创建或维护本 Skill 时必须读取 `skill-creator`.

专项 Skill 负责各自领域的细节. 本 Skill 负责讲义工作流,书籍结构,教学方法优先级和完成标准.

## 核心工作流

1. 检查 Git 状态和目标文件的最新内容.
2. 判断任务是局部修改,整章检查,工程重构,资料录入,数学校勘还是成品输出.
3. 只读取任务所需的书籍专属规则和资料.
4. 若使用原始 PDF,记录 PDF 文件名和页码范围.
5. 在当前文件上做最小增量修改.
6. 检查数学正确性,本节方法,证明完整性,符号必要性和同书关联.
7. 对疑问题面保留当前表述,给出反例或条件分析,并更新对应问题记录.
8. 运行静态验证器.
9. 默认到此结束: 不编译, 也不做 PDF 目视检查.
10. 仅当用户明确要求编译验证时, 才按验证矩阵在纯英文临时目录编译, 扫描日志, 并在版式敏感时检查 PDF 页面.
11. 再次检查 Git 状态和目标文件,防止覆盖并发修改.
12. 按固定格式报告已验证和未验证范围.

发送任何新写的中文正文,测试回答或文件内容前,必须逐字符检查并清除中文逗号,句号,冒号,分号,问号,感叹号,顿号,引号,括号,省略号和破折号. 全部改用对应 ASCII 标点. 即使正文是中文,此规则仍然适用. 代码,路径,数学公式和必须逐字保留的原文除外.

## 验证器

默认检查 Git 新增和修改行:

```powershell
python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope changed
```

检查指定文件:

```powershell
python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope file --file PATH
```

检查一个讲义项目:

```powershell
python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope project --project PATH
```

`project` 和 `changed` 范围会按主文件名自动识别 `数学分析培优` 或 `高等代数培优`,并套用该书的章节档案. 两本书的 chapter profile 和 `section_break_required` 设置各自独立, 互不影响.

验证器只报告确定性的文本和结构问题,不会改写文件,也不能代替数学审查.

## 必须停下的情况

- 目标文件在读取后发生任何重叠修改. 不得根据旧内容推断合并,必须停止并请求用户确认.
- 用户选择会实质改变题面,答案,书籍结构或验证范围.
- 需要修改原始 PDF,全局 Skill,其他书籍或任务范围外文件.
- 疑问题面无法从当前源码和原始资料确认,且不同处理会改变数学结论.
- 需要执行发布,推送,合并或其他外部副作用.

局部任务暴露全章系统性问题时,先报告影响,未经用户授权不扩大修改范围.

## 完成声明

只有满足 [通用规则](references/common-rules.md) 的完成门和 [验证规则](references/validation-rules.md) 的证据要求后,才能称任务完成.

必须分别说明:

- 静态检查状态.
- 编译目标及结果.
- 日志中的错误和 warning.
- 目视检查的具体 PDF 和页码.
- 未验证范围.

默认不编译: 只报告静态检查状态,并明确说明没有进行编译和目视检查. 只有用户明确要求编译验证时,才执行编译矩阵并报告编译,日志和目视检查结果.
