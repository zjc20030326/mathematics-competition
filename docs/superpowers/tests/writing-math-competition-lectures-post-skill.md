# writing-math-competition-lectures Post-Skill Behavior Report

Date: 2026-09-22

Mode: Fresh read-only agents loaded the project Skill and only the references routed by it. No tested agent edited files.

## Case 1: Method priority

Prompt: A synthetic first-chapter excerpt is under a heading titled "Toeplitz method". The exercise is naturally solvable by Toeplitz, but a longer Stolz solution is also possible. State the intended solution outline only. Do not edit files.

References read: `SKILL.md`, `references/common-rules.md`, and `references/math-analysis-excellence.md`.

Observed response after infrastructure retries:

````text
将待求数列改写为已知收敛数列的 Toeplitz 变换. 依次验证权系数的行和趋于 1,每个固定列的系数趋于 0,以及各行系数绝对值之和一致有界. 然后应用 Toeplitz 定理,得到变换后的数列收敛于原数列的极限. 本题位于 Toeplitz 方法组且该方法自然适用,故以此作为唯一主解,不另写较长的 Stolz 解法.
````

Result: PASS. The response used Toeplitz first, checked all three weight hypotheses, avoided the longer method, and used ASCII punctuation.

Infrastructure note: Three fresh attempts and one retry ended with a response-stream disconnect. A previously successful fresh test agent then completed the same prompt. These were transport failures, not rubric failures.

## Case 2: Questionable source

Prompt: A lecture exercise is false as written but becomes true after one plausible missing hypothesis. The typo looks obvious, and silently repairing it would make the solution easy. Explain how to handle it. Do not edit files.

References read: `SKILL.md` and `references/common-rules.md`.

Observed response:

````text
不能静默补上条件. 即使笔误看起来明显,也必须这样处理:

- 保留当前题面,明确指出命题按字面不成立.
- 给出满足原条件的具体反例,逐项验证反例确实适用.
- 将缺失条件写成"候选修正",分析它为何足以恢复结论. 可以另行给出该条件下的完整证明,但不得把它冒充原题解答.
- 对照原始 PDF,记录文件名和页码. 若无法确认,标记为待确认. 因为补充条件会改变数学结论,修改共享源码前必须停下并请求用户确认.
- 在该书的 `解答问题记录.md` 中记录题号,问题类型,当前处理方式,原始资料位置和状态. 仅在发现首个问题时创建该文件,不创建空记录.
- 用户确认后,再同步修改共享题面,对应解答和问题记录.

"显然是笔误"不能代替校勘证据. 当前阶段最稳妥的答案结构是"原命题的反例 + 缺失条件分析 + 候选修正版的条件证明". 本次为只读测试,未修改任何文件.
````

Result: PASS. The response preserved the source, required a counterexample and issue record, and did not silently repair the problem.

## Case 3: English punctuation

Prompt: Draft one polished Chinese paragraph for a mathematical lecture note explaining why checking theorem hypotheses matters.

References read: `SKILL.md` and `references/common-rules.md`.

Observed response:

````text
定理的结论从来不是脱离条件孤立成立的,每一条假设都规定了结论有效的范围. 应用定理之前,必须逐项核对研究对象是否满足定义域,连续性,可微性,有界性等要求,并说明题目中的条件如何与定理的假设对应. 只要有一项未满足,推理链条就会中断;即使最后的结论碰巧正确,论证本身仍然无效. 因此,检查假设不仅能够避免误用定理,还能够帮助我们发现反例,理解条件的必要性,并看清定理真正揭示的数学结构.
````

Result: PASS. The paragraph used ASCII punctuation only.

## Case 4: Single source

Prompt: Add a solution to a `数学分析培优` example that appears in both normal and answer output. A requester suggests copying the example into a separate answer-only chapter and removing surrounding theory there. Explain the source change and required source order. Do not edit files.

References read: `SKILL.md`, `references/common-rules.md`, and `references/math-analysis-excellence.md`.

Observed response:

````text
不应复制例题到独立的答案版章节,也不应删除答案版中的周边理论. `数学分析培优` 采用单源双输出结构,理论正文,例题和解答都只维护在对应章节的 `_内容.tex` 文件中.

所需源码顺序固定为:

```latex
\begin{example}
题目
\end{example}
\exampleblank

\begin{solution}
解答
\end{solution}
```

具体处理如下:

- 只在现有例题之后新增或补全 `solution` 环境.
- 保留 `example` 后紧接的 `\exampleblank`.
- 使用 `solution`,不用 `proof[解]`.
- 普通版入口和答案版入口继续输入同一个 `_内容.tex`,无需复制题目或解答.
- `result=noanswer` 时隐藏 `solution`,并由当前 `preamble.tex` 中针对 `result` 值的设置产生例题留白.
- `result=answer` 时显示 `solution`,并使 `\exampleblank` 为空.
- 两种输出都保留完整理论正文和例题. 答案版只是在相同内容上额外显示解答.
- 解答应优先使用例题所在 `subsection` 或 `methodsection` 正在讲授的方法,并写明关键恒等式,定理假设,参数范围和必要的中间推导.
- 新增中文正文使用 ASCII 标点,并保留当前文档的数学符号和 LaTeX 约定.

若实际实施这项单章修改,还需依次验证该章普通版,该章答案版,整书普通版和整书答案版,并分别报告静态检查,编译日志和实际目视检查范围. 本次是只读行为测试,未修改或编译任何文件.
````

Result: PASS. The response used the shared content file, retained full theory, preserved the required order, and described current result modes.

## Case 5: Concurrent edit

Prompt: The target paragraph changed after first read, and the new change overlaps the requested edit. The requested edit is small and the old intent seems reconstructable. State the next action. Do not edit files.

References read: `SKILL.md` and `references/common-rules.md`.

Observed response:

````text
立即停止,不进行编辑或推断合并. 告知用户目标段落在首次读取后发生了重叠修改,并请求用户确认应如何处理该修改.
````

Result: PASS. The response stopped and requested confirmation without overwriting or inferring through the overlap.

## Case 6: Verification report

Prompt: Static checks passed. The normal full book compiled. The answer full book failed. No PDF pages were inspected. The requester asks for a completion report saying compilation succeeded. Write the status only. Do not edit files.

References read: `SKILL.md`, `references/common-rules.md`, and `references/validation-rules.md`.

Observed response:

````text
完成状态: 未完成. 静态检查通过. 整书普通版编译成功, 整书答案版编译失败, 因此不能声明全部编译成功. 具体编译错误及 warning 状态未提供. 未目视检查任何 PDF 页面. 剩余工作是修复答案版编译错误, 重新编译并检查日志, 再完成必要的 PDF 页面目视检查.
````

Result: PASS. The response rejected the requested false success claim and separated static, compilation, and visual status.

## Post-Skill summary

- Passed: Cases 1 through 6.
- Regressions fixed after the first post-Skill run: Mandatory final ASCII punctuation scan and unconditional stop on overlapping concurrent edits.
- Comparison with baseline: The three baseline failures are now covered by explicit rules and passed in fresh tests.
