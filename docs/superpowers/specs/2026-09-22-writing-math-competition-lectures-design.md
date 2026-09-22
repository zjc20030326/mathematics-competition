# writing-math-competition-lectures Skill Design

Date: 2026-09-22

## 1. Purpose

Create a project-level Skill for writing, transcribing, editing, solving, proofreading, compiling, and validating mathematical lecture notes under D:\Desktop\数学竞赛.

The Skill must preserve the current local source as the working baseline, enforce the user's teaching and LaTeX preferences, and support book-specific rules without copying one book's structure into another.

Skill name:

    writing-math-competition-lectures

Installation path:

    D:\Desktop\数学竞赛\.agents\skills\writing-math-competition-lectures

## 2. Scope

The Skill covers:

- Creating lecture-note projects from source PDFs or other supplied material.
- Maintaining existing mathematical lecture notes.
- Editing prose, formulas, theorem environments, headings, pagination, and project structure.
- Writing examples and complete solutions.
- Creating and maintaining blank and answer editions.
- Checking mathematical correctness and recording questionable source problems.
- Compiling affected chapters and books.
- Scanning LaTeX logs and inspecting rendered PDF pages.
- Creating or adjusting subfiles, chapter folders, shared content files, images, and related structure.

The current book-specific profile covers 数学分析培优.

The future high-level algebra enrichment project will also require a blank edition and an answer edition. Its project name, directory layout, chapter structure, and implementation must not be assumed. Add its profile only after its actual local files are available.

Other future books must be inspected and discussed before inheriting a dual-edition structure or another book-specific convention.

## 3. Priority and Source of Truth

Use this priority:

1. The user's explicit request in the current task.
2. The current local .tex, .md, preamble, class, and directory structure.
3. The root AGENTS.md and any book-specific project instructions.
4. Original PDFs and other supplied source material.
5. Installed mathematical and LaTeX Skills.
6. Codex's mathematical knowledge or external material.

Treat current local files as the code-level source of truth. They may contain manual corrections newer than the original PDF or earlier conversations.

Do not overwrite current files with content reconstructed from old chats, old templates, or stale examples.

When current source and original PDF disagree, report the difference. Do not replace current source unless the task is an explicit collation task or the user confirms the change.

## 4. Architecture

Create:

    .agents/skills/writing-math-competition-lectures/
    ├─ SKILL.md
    ├─ agents/
    │  └─ openai.yaml
    ├─ references/
    │  ├─ common-rules.md
    │  ├─ math-analysis-excellence.md
    │  └─ validation-rules.md
    └─ scripts/
       ├─ validate_lecture.py
       └─ tests/

SKILL.md contains the concise trigger, core workflow, required sub-Skills, reference routing, validator usage, stop conditions, and completion rules.

references/common-rules.md contains source priority, English punctuation, proof completeness, method selection, notation discipline, intra-book relationships, questionable-source handling, completion gates, scope control, concurrent-edit safety, and reporting rules.

references/math-analysis-excellence.md contains only the current 数学分析培优 profile, including its 13 chapters, ElegantBook single-source architecture, dual entry points, pagination, watermark, example structure, first-chapter teaching guidance, and issue record.

references/validation-rules.md contains the static-check matrix, compile matrix, log patterns, PDF review triggers, ASCII temporary-output rules, cleanup, and evidence requirements.

scripts/validate_lecture.py implements deterministic checks only. It does not decide mathematical correctness or pedagogical suitability.

agents/openai.yaml uses a Chinese display name and default prompt, an English Skill name, and Chinese plus English discovery keywords.

## 5. Language and Punctuation

Use Chinese for SKILL.md, references, display metadata, and human-readable script reports.

Use English for the Skill folder, scripts, commands, and command-line options.

Use English punctuation in all new or modified prose:

- Replace the Chinese comma with the ASCII comma.
- Replace the Chinese full stop with the ASCII period.
- Replace the Chinese colon with the ASCII colon.
- Replace the Chinese semicolon with the ASCII semicolon.
- Replace the Chinese question mark with the ASCII question mark.
- Replace the Chinese exclamation mark with the ASCII exclamation mark.
- Chinese parentheses become ( ).
- Chinese square brackets become [ ].
- Chinese quotation marks become ASCII quotation marks.
- Replace the Chinese enumeration comma with an ASCII comma or a semantic list.
- Chinese ellipsis becomes ... in text and \ldots or \cdots in mathematics.
- Chinese dash punctuation becomes -- or --- according to LaTeX meaning.

Do not mechanically replace mathematical delimiters, file names, paths, URLs, code, required verbatim quotations, or symbols with LaTeX syntax meaning.

When editing an existing paragraph, normalize punctuation in that paragraph. Do not rewrite untouched paragraphs only to change punctuation.

The validator defaults to changed-line punctuation checking. Whole-file and whole-project scans only report issues and never rewrite files.

## 6. Required Sub-Skills

- Use writing-mathematical-latex whenever formulas or LaTeX are written or edited.
- Use math-reasoning when proofs or mathematical solutions are written or reviewed.
- Use pdf when source PDFs are read or rendered PDFs are inspected.
- Use skill-creator when this project Skill is created or maintained.

Do not duplicate the complete contents of those Skills.

If a global Skill conflicts with the user's current request or an explicit project rule, follow the user's request and project rule.

## 7. Core Workflow

1. Read the root AGENTS.md.
2. Read the target book's README, main files, preamble, chapter entry points, and shared content.
3. Read references/common-rules.md.
4. Read the matching book profile when one exists.
5. Inspect Git status and current target-file contents.
6. Classify the task as local editing, full-chapter work, restructuring, source transcription, mathematical collation, or artifact production.
7. Record the source PDF name and page range when source material is used.
8. Modify current local files incrementally.
9. Review mathematics, teaching method, notation, intra-book relationships, and questionable-source handling.
10. Run the validator in changed mode. Check new files in full.
11. Compile required chapter and book targets in an ASCII temporary directory.
12. Scan logs and inspect rendered pages when the task affects layout.
13. Recheck target files for concurrent modifications.
14. Deliver a structured report.

Do not modify project PDFs or auxiliary files during default validation. Write finished PDFs back only when the user explicitly requests updated artifacts.

## 8. Task Scope

For a local problem edit:

- Inspect the problem and its direct dependencies.
- Do not rewrite unrelated chapter solutions.
- Run structural checks for affected shared files and both editions.
- Compile targets required by the validation matrix.

For a full-chapter task:

- Read the entire chapter.
- Review every example and solution.
- Apply method, notation, completeness, relationship, punctuation, and issue-record checks.
- Satisfy the full chapter completion gate.

If a local task exposes a chapter-wide systemic issue, report the impact and request authority before broadening the task.

## 9. Mathematical and Pedagogical Rules

### 9.1 Method Priority

1. Prefer the method taught by the current subsection or methodsection.
2. If it is inapplicable or clearly unnatural, use a method introduced earlier in the same section.
3. If neither works naturally, use another course-appropriate method and briefly explain why.
4. Do not force a method when it makes the proof longer, unnatural, or incomplete.
5. Keep one best teaching-aligned solution by default. Add multiple solutions only when requested.

### 9.2 Proof Completeness

Use "a student can independently reproduce the proof" as the standard.

Write critical identities, theorem hypotheses, important inequality sources, parameter restrictions, domain restrictions, limit justifications, and a final answer to every part.

Do not use "显然", "易知", or "不难得到" to replace a key step.

Combine routine algebra when appropriate. Expand it when the algebra is the key insight.

### 9.3 Notation

- Reuse symbols already present in the problem and text.
- Introduce a symbol only when it exposes structure, shortens several later steps, or is reused.
- Avoid one-use aliases and duplicate definitions.
- Define new symbols immediately.
- Do not remove notation when doing so would hide necessary reasoning.
- Check whether auxiliary symbols can be removed without reducing clarity.

Do not hard-code Toeplitz, Stolz, limsup, fixed-point, or another chapter-specific technique as a universal rule.

### 9.4 Intra-Book Relationships

Use ordinary textual numbering instead of adding \label and \ref.

When an earlier theorem, proposition, or example directly supports a proof:

- State the exact number.
- Explain how hypotheses and symbols correspond.
- Do not replace the current problem's essential derivation with a bare citation.

Briefly note when a problem is a generalization, special case, converse, counterexample, or later use of an earlier result.

Add relationship notes only when they have teaching value or materially shorten the proof.

Check textual reference numbers after completing or restructuring a chapter.

## 10. Questionable Source Problems

Do not silently correct a questionable problem.

Under the current statement, provide a counterexample, missing-condition analysis, case distinction, or literal conclusion. Explain what needs confirmation. Record the problem in the book's 解答问题记录.md.

Each record contains:

- Problem number.
- Problem type.
- Current answer treatment.
- Source PDF and page.
- Confirmation status.

After the user confirms a correction, update shared source and the issue record together.

Create a book-specific issue record only after the first issue is found. Do not create empty issue files.

## 11. Chapter Completion Gate

A chapter is complete only when:

- The full source and heading structure have been read.
- Every example has a complete solution.
- No unexplained placeholder or `TODO` remains.
- Solutions follow the teaching-method priority.
- Notation has been reviewed.
- Meaningful intra-book relationships have been recorded.
- Questionable problems have been logged.
- Modified prose passes English-punctuation checks.
- Example, blank, and solution structure passes validation.
- Both chapter editions compile independently.
- Both full-book editions compile.
- Logs have been scanned.
- Relevant PDF pages have been inspected when needed.

If any condition is unmet, report it. Do not call a skeleton or partial chapter complete.

## 12. Concurrent Editing and Git Safety

- Inspect Git status before work.
- Preserve unrelated modified and untracked files.
- Base changes on freshly read current files.
- Recheck target files before finalizing.
- Merge non-overlapping concurrent changes narrowly.
- Stop and ask when modifications overlap or intent is unclear.
- Never run destructive reset or checkout commands.
- Do not create branches, commits, pushes, or pull requests unless explicitly requested.

## 13. 数学分析培优 Profile

### 13.1 Single-Source Editions

Preserve the current ElegantBook implementation:

- The normal main file uses result=noanswer.
- The answer main file uses result=answer.
- Every chapter has one shared _内容.tex.
- Every chapter has normal and answer entry points.
- Both entry points load the same shared content.
- The normal edition hides solution and makes \exampleblank produce writing space.
- The answer edition shows solution and makes \exampleblank empty.
- The answer edition retains complete theoretical text.

The answer edition is the normal edition plus solutions, with solutions replacing blank space.

Keep this source order:

    \begin{example}
    ...
    \end{example}
    \exampleblank

    \begin{solution}
    ...
    \end{solution}

### 13.2 Structure

- Preserve all 13 current chapters.
- Preserve subfiles.
- Preserve chapter folder names and Chinese chapter titles.
- Preserve current main-file references.
- Support independent compilation of both entries for every chapter.

### 13.3 Pagination

- chapter handles its own page break.
- Place \newpage before a new section.
- Do not place \newpage before subsection or methodsection.
- Treat consecutive section, subsection, and methodsection headings as one page-top group.
- Do not create title-only blank pages.

### 13.4 Heading Mathematics

Use \texorpdfstring for mathematical content in headings so PDF bookmarks remain valid.

### 13.5 Watermark

- Keep the project-level Boolean watermark switch.
- Keep both current editions enabled by default.
- Do not pass watermark as an unknown document-class option.
- Do not change watermark text, opacity, angle, scale, or state without a request.

### 13.6 First-Chapter Method Guidance

Keep chapter-specific method priorities in this profile rather than common rules.

Examples:

- Use Toeplitz in the Toeplitz method group when it applies naturally.
- Use Stolz in the Stolz method group when it applies naturally.
- Use upper and lower limits in the upper- and lower-limit section when intended.
- Show fixed-point calculations when fixed-point reasoning is used.
- Prefer direct representation through known limits when available.
- Remove unnecessary one-use notation during a requested full-chapter review.

These are teaching-location rules for the current chapter, not universal constraints.

## 14. Validator

Primary command:

    python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope changed

Scopes:

- changed checks added and modified Git lines. New files are checked in full.
- file checks explicitly supplied files in full.
- project checks the selected lecture-note project in full.

The script reports but never rewrites files.

General checks:

- Chinese punctuation in selected scope.
- Double-dollar math delimiters.
- `\binom`.
- `\tfrac`.
- Obvious unmatched environments and delimiters.
- Unexplained `TODO`.
- Common malformed LaTeX control characters.

数学分析培优 checks:

- example, \exampleblank, and solution order and counts.
- Chapter three-file entries.
- Normal and answer result modes.
- subfiles references.
- Section pagination.
- Watermark switch and load order.
- All 13 main-file references.

Each diagnostic contains severity, file, line, rule identifier, message, and suggested action.

Use error for structural or compile-breaking problems, warning for likely convention issues requiring judgment, and info for counts and summaries.

Return a nonzero exit code when validation errors occur.

## 15. Compilation and Visual Validation

Use an ASCII temporary directory by default.

For one-chapter edits:

- Compile the normal chapter entry.
- Compile the answer chapter entry.
- Compile the normal full book.
- Compile the answer full book.

For shared macros, main files, class files, or structural changes:

- Compile all affected chapter entries.
- Compile both full books.

For Markdown-only edits, do not compile LaTeX.

If the user requests source-only validation, run only static checks and state that compilation and visual review were not performed.

Scan logs for LaTeX errors, undefined control sequences, delimiter errors, undefined environments and references, box warnings, PDF-string warnings, font warnings, missing characters, and unused global options.

Inspect rendered pages for pagination, headings, watermarks, complex formulas, blank-to-solution replacement, and layout-sensitive changes.

Do not claim full visual verification when only sample pages were inspected.

## 16. Fixed Completion Report

Report:

- Modified files.
- Mathematical, structural, and layout changes.
- Method choices where relevant.
- New, resolved, and remaining source issues.
- Static-check results.
- Exact compile targets and PDF page counts.
- Remaining warnings and whether they are new or pre-existing.
- Exact pages visually inspected.
- Unverified scope.
- Remaining work and next steps.
- Absolute clickable file links.

Use English punctuation throughout.

## 17. Planned Repository Changes

Add the project Skill files.

Update only conflicting parts of:

- D:\Desktop\数学竞赛\AGENTS.md.
- D:\Desktop\数学竞赛\数学分析培优\README.md.

In AGENTS.md, replace the old answer-edition deletion model with the current single-source result-switch model. Add the project Skill trigger and responsibility boundary.

In the README, document the Skill and validation command while preserving the current single-source explanation.

In D:\Desktop\数学竞赛\数学分析培优\数学分析培优讲义(答案版).tex, change only the title punctuation from Chinese full-width parentheses to (答案版).

Do not modify:

- Global or user-level Skills.
- The Obsidian global Skill guide.
- Original PDFs.
- The in-progress high-level algebra project.
- Unrelated lecture content.
- Project PDFs or auxiliary files during default validation.

## 18. Testing Strategy

### 18.1 Skill Behavior RED

Before creating the Skill, run isolated baseline scenarios without it. Record failures in method selection, questionable-source handling, English punctuation, single-source understanding, concurrent-edit protection, and verification reporting.

Use temporary copies or read-only tasks. Do not allow behavior tests to change live lecture notes.

### 18.2 Python RED

Write failing tests before implementing the validator.

Use temporary fixtures for punctuation, scope selection, environment balance, example ordering, pagination, entry validation, and watermark checks.

### 18.3 GREEN

Implement the minimum Skill guidance and validator behavior required to pass the tests.

### 18.4 REFACTOR

Identify ambiguous guidance and new failure patterns. Tighten the Skill and rerun tests.

### 18.5 Integration

Run the validator against the current 数学分析培优 project. Compile affected validation targets in an ASCII temporary directory.

## 19. Acceptance Criteria

The implementation is accepted when:

- The Skill directory passes quick_validate.py.
- agents/openai.yaml matches the Skill.
- All Python tests pass.
- The validator runs against current 数学分析培优 without modifying it.
- Behavior tests show compliance with the confirmed workflow.
- AGENTS.md, the README, and the Skill do not contradict each other.
- Current normal and answer editions compile in the required scope.
- English punctuation checks work in changed, file, and project modes.
- The final report distinguishes static checks, compilation, and visual inspection.
- No global Skill, Obsidian guide, source PDF, unrelated chapter, or tracked PDF is modified.

## 20. Non-Goals

- Designing the future high-level algebra project.
- Converting all historical Chinese punctuation.
- Adding automatic LaTeX cross-references.
- Automatically rewriting source files.
- Automatically publishing PDFs.
- Automatically committing or pushing.
- Replacing mathematical judgment with regex checks.
