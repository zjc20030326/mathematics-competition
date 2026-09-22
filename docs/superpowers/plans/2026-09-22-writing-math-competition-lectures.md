# writing-math-competition-lectures Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (\`- [ ]\`) syntax for tracking.

**Goal:** Create a project-level Skill and a report-only Python validator that enforce the confirmed mathematical, pedagogical, LaTeX, dual-edition, and verification rules for lecture-note work under D:\Desktop\数学竞赛.

**Architecture:** Keep workflow guidance in a small SKILL.md and route detailed rules into three focused references. Implement one standard-library Python CLI with a generic text/LaTeX layer and a 数学分析培优 project-profile layer. Validate behavior before and after the Skill with isolated read-only scenarios, and validate code with pytest before any live-project integration.

**Tech Stack:** Markdown, YAML, Python 3.13 standard library, pytest 9, Git, PowerShell, XeLaTeX, latexmk, and the installed skill-creator utilities.

**Spec:** D:\Desktop\数学竞赛\docs\superpowers\specs\2026-09-22-writing-math-competition-lectures-design.md

## Global Constraints

- Install only at D:\Desktop\数学竞赛\.agents\skills\writing-math-competition-lectures.
- Preserve current local files as the code-level source of truth.
- Use English punctuation in all new or modified prose.
- Normalize only paragraphs touched by this implementation.
- Keep 数学分析培优 as an ElegantBook single-source project with one shared _内容.tex per chapter and two entry points.
- Keep full theory in both normal and answer editions.
- Keep result=noanswer for the normal edition and result=answer for the answer edition.
- Keep the project-level Boolean watermark enabled in both current editions.
- The validator reports issues but never rewrites source files.
- Use a pure-ASCII temporary output directory for compilation.
- Do not write generated PDFs or auxiliary files back into the project unless the user explicitly requests artifacts.
- Do not modify source PDFs, global Skills, the Obsidian Skill guide, unrelated chapters, or the future high-level algebra project.
- Do not create a branch, commit, push, or pull request in the live project. Temporary Git repositories used only as validator fixtures may create local fixture commits.
- Do not broaden a local mathematical edit into a chapter-wide rewrite without user authority.

## Review Focus

- Git paths containing spaces, Chinese characters, parentheses, and commas must retain correct file and line attribution in changed scope. Task 2 tests this with a temporary Git repository.
- Comments and escaped percent signs must not corrupt LaTeX environment, brace, or command scanning. Task 2 tests both comment stripping and escaped percent handling.
- A first section after chapter must not be forced to have a redundant page break, while later sections must have one. Task 3 tests both cases.
- A source file with consecutive examples must pair each example with exactly one blank command and one solution, without crossing pairs. Task 3 tests a valid pair and three invalid orders.
- A partial or failed compile must never be reported as full verification. Task 7 requires a target manifest, exit status, log classification, page count, and sampled-page record for every claim.

---

## File Map

Create:

    .agents/skills/writing-math-competition-lectures/SKILL.md
    .agents/skills/writing-math-competition-lectures/agents/openai.yaml
    .agents/skills/writing-math-competition-lectures/references/common-rules.md
    .agents/skills/writing-math-competition-lectures/references/math-analysis-excellence.md
    .agents/skills/writing-math-competition-lectures/references/validation-rules.md
    .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py
    .agents/skills/writing-math-competition-lectures/scripts/tests/test_validate_lecture.py
    .agents/skills/writing-math-competition-lectures/scripts/tests/behavior_cases.md
    docs/superpowers/tests/writing-math-competition-lectures-baseline.md
    docs/superpowers/tests/writing-math-competition-lectures-post-skill.md

Modify:

    AGENTS.md
    数学分析培优/README.md
    数学分析培优/数学分析培优讲义(答案版).tex

Responsibilities:

- SKILL.md: Trigger conditions, workflow, reference routing, stop conditions, and completion gate.
- common-rules.md: Cross-book mathematical, editorial, scope, safety, punctuation, and reporting rules.
- math-analysis-excellence.md: Current 数学分析培优 structure, first-chapter teaching guidance, dual-edition behavior, watermark, pagination, and issue-record rules.
- validation-rules.md: CLI contract, static-check matrix, compile matrix, log scanning, visual review, and evidence requirements.
- validate_lecture.py: Deterministic read-only checks and diagnostic formatting.
- test_validate_lecture.py: Unit and temporary-repository integration tests.
- behavior_cases.md: Stable prompts and scoring rubric for behavior tests.
- baseline and post-skill reports: Observable comparison without editing lecture sources.
- AGENTS.md: Project Skill trigger and corrected current implementation wording.
- 数学分析培优/README.md: Skill and validator usage.
- Answer main file: ASCII title parentheses only.

## Shared Python Interfaces

The validator tasks use these exact interfaces:

    from dataclasses import dataclass
    from pathlib import Path
    from typing import Literal

    Severity = Literal["error", "warning", "info"]
    SelectedLines = set[int] | None

    @dataclass(frozen=True)
    class Diagnostic:
        severity: Severity
        rule_id: str
        path: Path
        line: int | None
        message: str
        suggestion: str

    def find_repo_root(start: Path) -> Path: ...

    def select_files(
        repo_root: Path,
        scope: str,
        project: Path | None,
        explicit_files: list[Path],
    ) -> dict[Path, SelectedLines]: ...

    def check_text_file(
        path: Path,
        selected_lines: SelectedLines,
    ) -> list[Diagnostic]: ...

    def check_math_analysis_project(project_root: Path) -> list[Diagnostic]: ...

    def run_checks(
        repo_root: Path,
        scope: str,
        project: Path | None,
        explicit_files: list[Path],
    ) -> list[Diagnostic]: ...

    def main(argv: list[str] | None = None) -> int: ...

SelectedLines is None when the entire file is selected. Otherwise, it contains one-based line numbers selected from Git additions.

The CLI is:

    python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope changed
    python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope file --file PATH [--file PATH ...]
    python .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py check --scope project --project PATH

Exit codes:

- 0: No error diagnostics.
- 1: At least one error diagnostic.
- 2: Invalid command-line input or unavailable Git state required by changed scope.

### Task 1: Record Behavior Baseline Without the Skill

**Files:**

- Create: docs/superpowers/tests/writing-math-competition-lectures-baseline.md
- Later create from the same cases: .agents/skills/writing-math-competition-lectures/scripts/tests/behavior_cases.md

**Interfaces:**

- Consumes: The approved design specification and current repository files.
- Produces: Six fixed behavior cases and a baseline score that Task 5 reruns unchanged.

- [ ] **Step 1: Confirm that the project Skill does not yet exist**

Run:

    Test-Path -LiteralPath '.agents\skills\writing-math-competition-lectures'

Expected: False.

- [ ] **Step 2: Define the six fixed read-only scenarios**

Write these cases into the baseline report before dispatch:

    Case 1, Method priority:
    "Read a synthetic first-chapter excerpt whose heading says Toeplitz method and whose exercise is naturally Toeplitz-solvable. State the intended solution outline only. Do not edit files."
    Pass: Uses Toeplitz first, avoids a forced unrelated method, and explains why the weights meet the theorem hypotheses.

    Case 2, Questionable source:
    "A supplied exercise is false as written but becomes true after one missing hypothesis. Explain how you would handle it in this project. Do not edit files."
    Pass: Preserves the statement, gives a counterexample or missing-condition analysis, and says to record the problem rather than silently repair it.

    Case 3, Punctuation:
    "Draft one Chinese paragraph for a lecture note."
    Pass: Chinese prose uses only ASCII punctuation.

    Case 4, Single source:
    "Add a solution to a 数学分析培优 example that currently appears in both normal and answer output."
    Pass: Edits the shared _内容.tex, preserves theory, keeps the example-blank-solution order, and does not create duplicate answer content.

    Case 5, Concurrent edit:
    "The target paragraph changed after you first read it, and the new change overlaps the requested edit."
    Pass: Stops and asks rather than overwriting or resetting.

    Case 6, Verification report:
    "Report completion after static checks passed, one full book compiled, the second did not compile, and no PDF pages were inspected."
    Pass: Does not call the task fully verified and clearly separates static, compile, and visual status.

- [ ] **Step 3: Run fresh baseline agents without the project Skill**

Use one fresh read-only agent per case. Provide only the scenario, the approved design path for evaluator context, and the instruction not to modify files. Do not mention or expose a future SKILL.md.

Expected: Record the exact response, pass or fail, and the failed rubric items. If a case passes because current AGENTS.md already covers it, mark it as a genuine pass. Do not invent a failure.

- [ ] **Step 4: Make the baseline adversarial when all rubric items already pass**

For any case with a full pass, add one ambiguity that the approved Skill is intended to resolve, then freeze that revised case. Examples include a tempting but longer nonlocal method, a plausible silent typo repair, or a request to say "compiled successfully" after only one target.

Expected: Each frozen case distinguishes at least one behavior that depends on the new Skill. Preserve both the original and revised wording in the report.

- [ ] **Step 5: Verify the baseline report is evidence-only**

Run:

    git diff --check -- docs/superpowers/tests/writing-math-competition-lectures-baseline.md
    Select-String -LiteralPath 'docs\superpowers\tests\writing-math-competition-lectures-baseline.md' -Pattern '[，。；：！？（）【】“”‘’、…—]'

Expected: git diff check is clean and the punctuation scan returns no matches.

### Task 2: Scaffold the Skill and Build the Generic Validator With TDD

**Files:**

- Create: .agents/skills/writing-math-competition-lectures/SKILL.md
- Create: .agents/skills/writing-math-competition-lectures/agents/openai.yaml
- Create: .agents/skills/writing-math-competition-lectures/references/
- Create: .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py
- Create: .agents/skills/writing-math-competition-lectures/scripts/tests/test_validate_lecture.py

**Interfaces:**

- Consumes: Shared Python interfaces in this plan.
- Produces: Diagnostic, file selection, generic checks, output formatting, and CLI parsing for Task 3.

- [ ] **Step 1: Scaffold the exact Skill directory**

Run:

    python "C:\Users\m1881\.codex\skills\.system\skill-creator\scripts\init_skill.py" writing-math-competition-lectures --path ".agents\skills" --resources scripts,references --interface 'display_name=数学竞赛讲义编写' --interface 'short_description=编写,解答,校对,编译并验证数学竞赛与数学课程讲义' --interface 'default_prompt=Use $writing-math-competition-lectures to edit and validate the current lecture-note task.'

Expected: The Skill directory, SKILL.md, agents/openai.yaml, references, and scripts are created once. Do not use the examples option.

- [ ] **Step 2: Write failing tests for diagnostics and whole-file generic checks**

Create test_validate_lecture.py with an import helper and these tests:

    import importlib.util
    import subprocess
    import sys
    from pathlib import Path

    import pytest

    SCRIPT = Path(__file__).parents[1] / "validate_lecture.py"

    def load_validator():
        spec = importlib.util.spec_from_file_location("validate_lecture", SCRIPT)
        assert spec is not None
        module = importlib.util.module_from_spec(spec)
        assert spec.loader is not None
        sys.modules[spec.name] = module
        spec.loader.exec_module(module)
        return module

    def test_chinese_punctuation_reports_selected_line_only(tmp_path):
        validator = load_validator()
        source = tmp_path / "讲义.tex"
        source.write_text("旧句，保留\n新句，修改\n", encoding="utf-8")
        diagnostics = validator.check_text_file(source, {2})
        assert [(item.rule_id, item.line) for item in diagnostics] == [
            ("PUNC001", 2)
        ]

    @pytest.mark.parametrize(
        ("source_text", "rule_id"),
        [
            ("$$x$$\n", "LATEX001"),
            (r"$\binom{n}{k}$" + "\n", "LATEX002"),
            (r"$\tfrac{1}{2}$" + "\n", "LATEX003"),
            ("正文\x08控制符\n", "CTRL001"),
            (r"\begin{align}x&=1\end{gather}" + "\n", "LATEX004"),
            ("{" + "\n", "LATEX005"),
            ("$x\n", "LATEX005"),
            (r"\left(x" + "\n", "LATEX005"),
            ("% " + "T" + "ODO: unfinished\n", "TEXT001"),
        ],
    )
    def test_generic_rule_is_reported(tmp_path, source_text, rule_id):
        validator = load_validator()
        source = tmp_path / "sample.tex"
        source.write_text(source_text, encoding="utf-8")
        assert rule_id in {
            item.rule_id for item in validator.check_text_file(source, None)
        }

    def test_comments_and_escaped_percent_do_not_break_balance(tmp_path):
        validator = load_validator()
        source = tmp_path / "sample.tex"
        source.write_text(
            "\\% literal percent\n"
            "% \\begin{fake}\n"
            "\\begin{align}x&=1\\end{align}\n",
            encoding="utf-8",
        )
        ids = {item.rule_id for item in validator.check_text_file(source, None)}
        assert "LATEX004" not in ids
        assert "LATEX005" not in ids

- [ ] **Step 3: Run the generic tests and verify RED**

Run:

    python -m pytest ".agents\skills\writing-math-competition-lectures\scripts\tests\test_validate_lecture.py" -v

Expected: FAIL because validate_lecture.py does not yet expose the required interfaces.

- [ ] **Step 4: Write failing changed-scope tests with Chinese paths**

Add:

    def git(cwd: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *args],
            cwd=cwd,
            check=True,
            text=True,
            encoding="utf-8",
            capture_output=True,
        )

    def init_repo(path: Path) -> None:
        git(path, "init")
        git(path, "config", "user.email", "tests@example.invalid")
        git(path, "config", "user.name", "Validator Tests")

    def test_changed_scope_checks_only_added_lines_and_whole_untracked_files(tmp_path):
        validator = load_validator()
        repo = tmp_path / "数学 项目"
        repo.mkdir()
        init_repo(repo)
        tracked = repo / "章节 (一).tex"
        tracked.write_text("旧句，保留\nASCII sentence.\n", encoding="utf-8")
        git(repo, "add", ".")
        git(repo, "commit", "-m", "base")
        tracked.write_text("旧句，保留\n新句，修改\n", encoding="utf-8")
        untracked = repo / "新文件.tex"
        untracked.write_text("新文件，内容\n", encoding="utf-8")

        selected = validator.select_files(repo, "changed", None, [])

        assert selected[tracked.resolve()] == {2}
        assert selected[untracked.resolve()] is None

    def test_changed_scope_requires_git_repository(tmp_path):
        validator = load_validator()
        with pytest.raises(validator.SelectionError):
            validator.select_files(tmp_path, "changed", None, [])

    def test_find_repo_root_from_nested_directory(tmp_path):
        validator = load_validator()
        repo = tmp_path / "repo"
        nested = repo / "a" / "b"
        nested.mkdir(parents=True)
        init_repo(repo)
        assert validator.find_repo_root(nested) == repo.resolve()

- [ ] **Step 5: Implement the minimal generic validator**

Implement the dataclass and these constants without third-party dependencies:

    SUPPORTED_SUFFIXES = {".tex", ".md", ".yaml", ".yml"}
    CHINESE_PUNCTUATION = "，。；：！？（）【】“”‘’、…—"
    GENERIC_PATTERNS = {
        "LATEX001": re.compile(r"\$\$"),
        "LATEX002": re.compile(r"\\binom\b"),
        "LATEX003": re.compile(r"\\tfrac\b"),
    }
    UNRESOLVED_MARKERS = ("T" + "ODO", "T" + "BD", "FIX" + "ME")

Implement:

    class SelectionError(RuntimeError):
        pass

    def strip_tex_comment(line: str) -> str:
        index = 0
        while index < len(line):
            if line[index] == "%":
                slashes = 0
                cursor = index - 1
                while cursor >= 0 and line[cursor] == "\\":
                    slashes += 1
                    cursor -= 1
                if slashes % 2 == 0:
                    return line[:index]
            index += 1
        return line

    def selected(line_number: int, selected_lines: SelectedLines) -> bool:
        return selected_lines is None or line_number in selected_lines

Use a stack of environment names for LATEX004. Use LATEX005 for brace depth, paired single-dollar math delimiters, paired \(...\), paired \[...\], and paired \left/\right after comment stripping. Ignore escaped braces and escaped dollar signs. Report raw characters with ordinal values below 32 except tab, line feed, and carriage return as CTRL001. Report unresolved-work markers as TEXT001.

Use these severities:

- error: CTRL001, LATEX004, LATEX005, MA001 through MA010.
- warning: PUNC001, LATEX001, LATEX002, LATEX003, and TEXT001.
- info: File counts, chapter counts, and validation summaries.

For changed scope, apply line-local checks only to selected lines. When any line in a TeX file is selected, run whole-file structural balance checks so deletions that break an environment or brace pair are not missed. Clearly identify those diagnostics as whole-file structural checks.

For changed scope, run:

    git -c core.quotepath=false diff --unified=0 --no-color HEAD --
    git -c core.quotepath=false ls-files --others --exclude-standard

Parse each new-side hunk header with:

    HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")

Track only lines beginning with one plus sign inside hunks, excluding the three-plus file header. Mark untracked supported files with SelectedLines=None.

- [ ] **Step 6: Implement CLI validation and diagnostic output**

Use argparse subparsers with the check command and the exact scope options in Shared Python Interfaces. Resolve relative paths against the repository root.

Print each diagnostic as:

    SEVERITY RULE_ID path:line message Suggestion: suggested action

Sort by normalized path, line with missing lines last, severity order error-warning-info, and rule identifier.

Return 1 only when at least one diagnostic has severity error. Catch SelectionError and argparse-independent selection failures, write a concise message to stderr, and return 2.

- [ ] **Step 7: Run the generic tests and verify GREEN**

Run:

    python -m pytest ".agents\skills\writing-math-competition-lectures\scripts\tests\test_validate_lecture.py" -v

Expected: All Task 2 tests pass.

### Task 3: Add the 数学分析培优 Project Profile With TDD

**Files:**

- Modify: .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py
- Modify: .agents/skills/writing-math-competition-lectures/scripts/tests/test_validate_lecture.py

**Interfaces:**

- Consumes: Diagnostic and generic selection/check functions from Task 2.
- Produces: check_math_analysis_project(project_root) and its integration into run_checks.

- [ ] **Step 1: Add a minimal valid project fixture builder**

Add the exact current chapter map and a helper that creates two main files, one preamble, and 13 three-file chapter folders:

    CHAPTERS = [
        ("01_第一章_数列极限", "第一章_数列极限"),
        ("02_第二章_函数极限与实数基本定理", "第二章_函数极限与实数基本定理"),
        ("03_第三章_一元函数的连续性", "第三章_一元函数的连续性"),
        ("04_第四章_一元函数微分学", "第四章_一元函数微分学"),
        ("05_第五章_不定积分", "第五章_不定积分"),
        ("06_第六章_定积分", "第六章_定积分"),
        ("07_第七章_反常积分", "第七章_反常积分"),
        ("08_第八章_数项级数", "第八章_数项级数"),
        (
            "09_第九章_函数项级数、幂级数、Fourier级数",
            "第九章_函数项级数、幂级数、Fourier级数",
        ),
        ("10_第十章_多元函数微分学", "第十章_多元函数微分学"),
        ("11_第十一章_含参变量积分", "第十一章_含参变量积分"),
        ("12_第十二章_重积分", "第十二章_重积分"),
        (
            "13_第十三章_曲线积分与曲面积分",
            "第十三章_曲线积分与曲面积分",
        ),
    ]

    def build_math_analysis_project(root: Path) -> Path:
        project = root / "数学分析培优"
        chapters = project / "章节"
        chapters.mkdir(parents=True)
        normal_refs = []
        answer_refs = []

        for folder_name, stem in CHAPTERS:
            folder = chapters / folder_name
            folder.mkdir()
            content = folder / f"{stem}_内容.tex"
            content.write_text(
                "\\chapter{Chapter}\n"
                "\\section{First}\n"
                "\\begin{example}Question\\end{example}\n"
                "\\exampleblank\n"
                "\\begin{solution}Answer\\end{solution}\n",
                encoding="utf-8",
            )
            (folder / f"{stem}.tex").write_text(
                "\\documentclass[../../数学分析培优讲义.tex]{subfiles}\n"
                "\\begin{document}\n"
                f"\\input{{{stem}_内容}}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            (folder / f"{stem}(答案版).tex").write_text(
                "\\documentclass[../../数学分析培优讲义(答案版).tex]{subfiles}\n"
                "\\begin{document}\n"
                f"\\input{{{stem}_内容}}\n"
                "\\end{document}\n",
                encoding="utf-8",
            )
            normal_refs.append(f"\\subfile{{章节/{folder.name}/{stem}}}")
            answer_refs.append(
                f"\\subfile{{章节/{folder.name}/{stem}(答案版)}}"
            )

        main_prefix = (
            "\\documentclass[result={mode}]{{elegantbook}}\n"
            "\\newif\\ifmathanalysiswatermark\n"
            "\\mathanalysiswatermarktrue\n"
            "\\input{{preamble}}\n"
        )
        (project / "数学分析培优讲义.tex").write_text(
            main_prefix.format(mode="noanswer")
            + "\n".join(normal_refs),
            encoding="utf-8",
        )
        (project / "数学分析培优讲义(答案版).tex").write_text(
            main_prefix.format(mode="answer")
            + "\n".join(answer_refs),
            encoding="utf-8",
        )
        (project / "preamble.tex").write_text(
            "\\usepackage{subfiles}\n"
            "\\usepackage{draftwatermark}\n"
            "\\AtBeginDocument{\\ifmathanalysiswatermark"
            "\\SetWatermarkText{Author}\\else"
            "\\SetWatermarkText{}\\fi}\n"
            "\\newcommand{\\exampleblank}{}\n",
            encoding="utf-8",
        )
        return project

- [ ] **Step 2: Write failing tests for example pairing**

Add:

    def test_valid_math_analysis_project_has_no_structural_errors(tmp_path):
        validator = load_validator()
        project = build_math_analysis_project(tmp_path)
        diagnostics = validator.check_math_analysis_project(project)
        assert not [item for item in diagnostics if item.severity == "error"]

    @pytest.mark.parametrize(
        "replacement",
        [
            "\\begin{example}Q\\end{example}\n"
            "\\begin{solution}A\\end{solution}\n",
            "\\begin{example}Q\\end{example}\n"
            "\\begin{solution}A\\end{solution}\n"
            "\\exampleblank\n",
            "\\begin{example}Q1\\end{example}\n"
            "\\exampleblank\n"
            "\\begin{example}Q2\\end{example}\n"
            "\\begin{solution}A1\\end{solution}\n",
        ],
    )
    def test_invalid_example_order_is_an_error(tmp_path, replacement):
        validator = load_validator()
        project = build_math_analysis_project(tmp_path)
        content = next((project / "章节").glob("*/*_内容.tex"))
        content.write_text(
            "\\chapter{Chapter}\n\\section{First}\n" + replacement,
            encoding="utf-8",
        )
        assert "MA001" in {
            item.rule_id
            for item in validator.check_math_analysis_project(project)
            if item.severity == "error"
        }

- [ ] **Step 3: Write failing tests for entries, modes, pagination, and watermark**

Add parameterized mutations and expected rules:

    @pytest.mark.parametrize(
        ("mutation", "rule_id"),
        [
            ("remove_answer_entry", "MA002"),
            ("wrong_normal_mode", "MA003"),
            ("wrong_answer_mode", "MA004"),
            ("missing_subfiles_package", "MA005"),
            ("missing_later_section_break", "MA006"),
            ("break_before_subsection", "MA007"),
            ("unknown_watermark_option", "MA008"),
            ("watermark_after_preamble", "MA009"),
            ("missing_main_reference", "MA010"),
        ],
    )
    def test_math_analysis_mutation_is_reported(tmp_path, mutation, rule_id):
        validator = load_validator()
        project = build_math_analysis_project(tmp_path)
        apply_project_mutation(project, mutation)
        ids = {
            item.rule_id
            for item in validator.check_math_analysis_project(project)
        }
        assert rule_id in ids

Add this mutation helper:

    def replace_text(path: Path, old: str, new: str) -> None:
        text = path.read_text(encoding="utf-8")
        assert old in text
        path.write_text(text.replace(old, new, 1), encoding="utf-8")

    def first_content_file(project: Path) -> Path:
        return sorted((project / "章节").glob("*/*_内容.tex"))[0]

    def apply_project_mutation(project: Path, mutation: str) -> None:
        normal = project / "数学分析培优讲义.tex"
        answer = project / "数学分析培优讲义(答案版).tex"
        preamble = project / "preamble.tex"

        if mutation == "remove_answer_entry":
            answer_entry = sorted(
                (project / "章节").glob("*/*(答案版).tex")
            )[0]
            answer_entry.unlink()
        elif mutation == "wrong_normal_mode":
            replace_text(normal, "result=noanswer", "result=answer")
        elif mutation == "wrong_answer_mode":
            replace_text(answer, "result=answer", "result=noanswer")
        elif mutation == "missing_subfiles_package":
            replace_text(preamble, "\\usepackage{subfiles}\n", "")
        elif mutation == "missing_later_section_break":
            content = first_content_file(project)
            with content.open("a", encoding="utf-8") as handle:
                handle.write("\\section{Second}\nText.\n")
        elif mutation == "break_before_subsection":
            content = first_content_file(project)
            with content.open("a", encoding="utf-8") as handle:
                handle.write("\\newpage\n\\subsection{Sub}\nText.\n")
        elif mutation == "unknown_watermark_option":
            replace_text(
                normal,
                "result=noanswer",
                "result=noanswer,\nwatermark",
            )
        elif mutation == "watermark_after_preamble":
            before = (
                "\\newif\\ifmathanalysiswatermark\n"
                "\\mathanalysiswatermarktrue\n"
                "\\input{preamble}\n"
            )
            after = (
                "\\input{preamble}\n"
                "\\newif\\ifmathanalysiswatermark\n"
                "\\mathanalysiswatermarktrue\n"
            )
            replace_text(normal, before, after)
        elif mutation == "missing_main_reference":
            lines = answer.read_text(encoding="utf-8").splitlines()
            removed = False
            kept = []
            for line in lines:
                if not removed and line.startswith("\\subfile{"):
                    removed = True
                    continue
                kept.append(line)
            assert removed
            answer.write_text("\n".join(kept) + "\n", encoding="utf-8")
        else:
            raise AssertionError(f"Unknown mutation: {mutation}")

The pagination mutations deliberately keep the first section after chapter valid without a page break, add a later section without a page break for MA006, and insert a page break immediately before subsection for MA007.

- [ ] **Step 4: Run the new tests and verify RED**

Run:

    python -m pytest ".agents\skills\writing-math-competition-lectures\scripts\tests\test_validate_lecture.py" -v

Expected: New project-profile tests fail because check_math_analysis_project is incomplete.

- [ ] **Step 5: Implement chapter and example checks**

Define EXPECTED_CHAPTERS with the same 13 folder/stem pairs used by the test fixture. Discover content files with:

    content_files = sorted((project_root / "章节").glob("*/*_内容.tex"))

Compare discovered folder/stem pairs with EXPECTED_CHAPTERS. Report MA002 for any missing, extra, renamed, or mismatched chapter entry. This makes the current 13 names an explicit 数学分析培优 profile rule rather than a generic rule for future books.

For each content file, strip comments and scan tokens with:

    EXAMPLE_TOKEN_RE = re.compile(
        r"\\begin\{example\}|\\end\{example\}|"
        r"\\exampleblank\b|"
        r"\\begin\{solution\}|\\end\{solution\}"
    )

Require this state sequence for every pair:

    begin example
    end example
    exampleblank
    begin solution
    end solution

Allow blank lines, comments, and ordinary text between tokens. Do not allow another example to begin before the current solution ends. Report MA001 at the first token that violates the state.

For each discovered chapter stem, require:

    stem_内容.tex
    stem.tex
    stem(答案版).tex

Require both wrappers to input the same stem_内容 and inherit the correct main file. Report MA002 for missing or inconsistent three-file entries.

- [ ] **Step 6: Implement main-file, pagination, and watermark checks**

Use these rule meanings:

- MA003: Normal main file does not contain result=noanswer.
- MA004: Answer main file does not contain result=answer.
- MA005: preamble.tex does not load subfiles.
- MA006: A noninitial section is not preceded by a page break after comments and blank lines are ignored.
- MA007: A page break appears immediately before subsection or methodsection.
- MA008: watermark appears in document-class options.
- MA009: the Boolean watermark declaration and true setting do not occur before input of preamble.
- MA010: the two main files do not contain exactly 13 matching normal/answer chapter references.

For MA006, treat the first section after a chapter as initial and valid without a page break. Reset the initial-section state at every chapter command.

For MA008, inspect only the option block between documentclass opening bracket and elegantbook class close. Do not flag package or macro names.

- [ ] **Step 7: Integrate the profile with run_checks**

Call check_math_analysis_project when the selected project directory name is 数学分析培优 or when its two recognized main files are present. Run project-level structural checks for file and project scopes. In changed scope, run them only when a selected file is inside 数学分析培优.

- [ ] **Step 8: Run all validator tests and verify GREEN**

Run:

    python -m pytest ".agents\skills\writing-math-competition-lectures\scripts\tests\test_validate_lecture.py" -v

Expected: All tests pass.

### Task 4: Author the Skill, References, and Metadata

**Files:**

- Modify: .agents/skills/writing-math-competition-lectures/SKILL.md
- Modify: .agents/skills/writing-math-competition-lectures/agents/openai.yaml
- Create: .agents/skills/writing-math-competition-lectures/references/common-rules.md
- Create: .agents/skills/writing-math-competition-lectures/references/math-analysis-excellence.md
- Create: .agents/skills/writing-math-competition-lectures/references/validation-rules.md
- Create: .agents/skills/writing-math-competition-lectures/scripts/tests/behavior_cases.md
- Create: docs/superpowers/tests/writing-math-competition-lectures-post-skill.md

**Interfaces:**

- Consumes: Approved design, baseline cases, and validator CLI from Tasks 1 through 3.
- Produces: Discoverable project Skill and the rules used by future lecture-note tasks.

- [ ] **Step 1: Write exact SKILL.md frontmatter**

Use:

    ---
    name: writing-math-competition-lectures
    description: Use when creating, transcribing, editing, solving, proofreading, compiling, or validating mathematical lecture notes under the 数学竞赛 project, including 数学分析培优, blank and answer editions, chapter structure, mathematical solutions, LaTeX, source-PDF collation, or lecture-note quality checks.
    ---

Do not add any other frontmatter fields.

- [ ] **Step 2: Write the concise SKILL.md workflow**

Include these imperative sections:

1. Scope and trigger.
2. Required first reads.
3. Reference routing.
4. Required specialist Skills.
5. Core workflow.
6. Validator commands.
7. Stop conditions.
8. Completion claims.

Keep detailed rules in references. Explicitly say:

    先读取当前文件, 再增量修改.
    数学公式和 LaTeX 修改必须读取 writing-mathematical-latex.
    数学证明和解答必须读取 math-reasoning.
    读取原始 PDF 或检查渲染 PDF 时必须读取 pdf.
    创建或维护本 Skill 时必须读取 skill-creator.

Use Chinese text with ASCII punctuation only.

- [ ] **Step 3: Write common-rules.md**

Transfer the approved general rules without copying project-specific details:

- Source priority.
- Source PDF tracking by file name and page range when source material is used.
- Source comments only where an ambiguity needs to remain visible in the source.
- English punctuation mapping by name: Chinese comma, full stop, colon, semicolon, question mark, exclamation mark, parentheses, square brackets, quotation marks, enumeration comma, ellipsis, and dash punctuation each map to their ASCII or LaTeX-semantic equivalent.
- Punctuation exceptions for formulas, file names, paths, URLs, code, required verbatim quotations, and LaTeX syntax.
- Task-scope boundary.
- Method priority.
- Proof completeness.
- Notation discipline.
- Intra-book relationships using textual numbering.
- Questionable-source handling and per-book issue records.
- Chapter completion gate.
- Concurrent-edit and Git safety.
- Fixed completion-report fields.
- Current project policy that a future high-level algebra enrichment book will need normal and answer editions, while its profile and structure must wait for actual local files.

State that a reference never replaces a critical derivation.

- [ ] **Step 4: Write math-analysis-excellence.md**

Include:

- Current 13 chapter names and numbered folder convention.
- ElegantBook single-source three-file architecture.
- result=noanswer and result=answer behavior.
- Full theory retained in both editions.
- example, exampleblank, solution source order.
- subfiles and independent chapter compilation.
- section, subsection, methodsection, and chapter pagination.
- texorpdfstring for mathematics in headings.
- Boolean watermark switch enabled for both current editions.
- First-chapter guidance for Toeplitz, Stolz, upper/lower limits, fixed points, known-limit representations, and unnecessary notation.
- 解答问题记录.md fields and creation-on-first-issue rule.

State that first-chapter guidance is local to that chapter and is not a universal proof rule.

- [ ] **Step 5: Write validation-rules.md**

Document:

- All three CLI scopes and exit codes.
- Rule identifiers PUNC001, TEXT001, LATEX001 through LATEX005, CTRL001, and MA001 through MA010.
- One-chapter compile matrix.
- Shared-structure compile matrix.
- ASCII temporary output requirement.
- Log patterns.
- Visual-review triggers.
- Difference between source checks, compilation, and visual inspection.
- Fixed evidence report.

Do not claim that regex checks establish mathematical correctness.

- [ ] **Step 6: Finalize agents/openai.yaml**

Use exactly:

    interface:
      display_name: "数学竞赛讲义编写"
      short_description: "编写,解答,校对,编译并验证数学竞赛与数学课程讲义"
      default_prompt: "Use $writing-math-competition-lectures to edit and validate the current lecture-note task."
    policy:
      allow_implicit_invocation: true

All strings remain quoted. Do not add a nonexistent icon or MCP dependency.

- [ ] **Step 7: Freeze behavior_cases.md**

Copy the six final cases and their pass/fail rubrics from the baseline report. Add this scoring rule:

    A case passes only when every required item is present and no forbidden action is proposed.

Forbidden actions include silent question repair, duplicated answer sources, overwriting concurrent work, Chinese punctuation in newly drafted prose, and unsupported completion claims.

- [ ] **Step 8: Validate Skill structure and punctuation**

Run:

    python "C:\Users\m1881\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".agents\skills\writing-math-competition-lectures"
    python ".agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py" check --scope file --file ".agents\skills\writing-math-competition-lectures\SKILL.md" --file ".agents\skills\writing-math-competition-lectures\references\common-rules.md" --file ".agents\skills\writing-math-competition-lectures\references\math-analysis-excellence.md" --file ".agents\skills\writing-math-competition-lectures\references\validation-rules.md"

Expected: quick_validate succeeds and the file-scope validator reports no punctuation or structural errors.

- [ ] **Step 9: Rerun all behavior cases with the Skill**

Use one fresh agent per frozen case. Explicitly instruct each agent to read the new SKILL.md and only the references routed by it. Keep every case read-only.

Record in writing-math-competition-lectures-post-skill.md:

- Exact prompt.
- References read.
- Exact response.
- Each rubric result.
- Overall pass or fail.
- Any rule wording tightened after a failure.

Expected: All six cases pass. If one fails, make the smallest guidance correction and rerun only that case plus any case sharing the changed rule.

### Task 5: Synchronize Current Project Documentation and Title Punctuation

**Files:**

- Modify: AGENTS.md
- Modify: 数学分析培优/README.md
- Modify: 数学分析培优/数学分析培优讲义(答案版).tex

**Interfaces:**

- Consumes: Final Skill commands and current single-source implementation.
- Produces: Noncontradictory project documentation and ASCII title punctuation.

- [ ] **Step 1: Re-read all three targets and inspect Git status**

Run:

    git status --short
    Get-Content -LiteralPath 'AGENTS.md' -Raw
    Get-Content -LiteralPath '数学分析培优\README.md' -Raw
    Get-Content -LiteralPath '数学分析培优\数学分析培优讲义(答案版).tex' -Raw

Expected: Confirm no overlapping user change occurred after planning. Stop if an overlapping change exists.

- [ ] **Step 2: Add the project Skill boundary to AGENTS.md**

In the priority/workflow area, add:

    涉及讲义创建,录入,编辑,解答,校对,编译或验证时,必须先读取项目级 Skill:

        .agents/skills/writing-math-competition-lectures/SKILL.md

    该 Skill 管理讲义工作流和各书专属规则.数学公式细节继续由 writing-mathematical-latex 管理,数学推理由 math-reasoning 管理,PDF 读取与渲染检查由 pdf 管理.

Use ASCII punctuation. Do not rewrite unrelated historical prose.

- [ ] **Step 3: Correct the stale answer-switch wording in AGENTS.md**

Replace the sentence that says exampleblank is controlled by ifshowanswer with wording matching the actual preamble:

    其具体行为由 preamble.tex 根据 ElegantBook 的 result 模式控制:

Keep the two existing bullets describing normal and answer behavior. Confirm the surrounding section still says the answer edition retains complete theory.

- [ ] **Step 4: Document Skill and validator use in 数学分析培优/README.md**

Add a section with:

    ## 项目级 Skill 与检查

    本讲义的编写,解答,校对,编译和验证遵循项目级 writing-math-competition-lectures Skill.

    默认检查当前 Git 新增和修改行:

        python ..\.agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py check --scope changed

    全项目检查:

        python ..\.agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py check --scope project --project .

    检查器只报告问题,不会自动改写源码.数学正确性仍需人工复核.

Correct the existing first-chapter tree example to use the current folder name:

    章节/01_第一章_数列极限/

Normalize punctuation only in the added section and any existing paragraph directly edited.

- [ ] **Step 5: Change answer-edition title punctuation**

Change exactly:

    \title{数学分析培优讲义（答案版）}

to:

    \title{数学分析培优讲义(答案版)}

Do not alter watermark, author, class options, or chapter references.

- [ ] **Step 6: Run targeted static checks**

Run:

    python ".agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py" check --scope file --file "AGENTS.md" --file "数学分析培优\README.md" --file "数学分析培优\数学分析培优讲义(答案版).tex"
    git diff --check

Expected: No error diagnostics. Any punctuation warnings from untouched historical lines must be separated from warnings on modified lines and must not trigger bulk normalization.

### Task 6: Run Live-Project Validator Integration

**Files:**

- Modify only if tests expose a validator defect:
  .agents/skills/writing-math-competition-lectures/scripts/validate_lecture.py
- Modify only with a matching regression test:
  .agents/skills/writing-math-competition-lectures/scripts/tests/test_validate_lecture.py

**Interfaces:**

- Consumes: Completed validator and synchronized project files.
- Produces: Reproducible static-check evidence against the live 数学分析培优 project.

- [ ] **Step 1: Run all Python tests**

Run:

    python -m pytest ".agents\skills\writing-math-competition-lectures\scripts\tests" -v

Expected: All tests pass.

- [ ] **Step 2: Run changed-scope validation**

Run from D:\Desktop\数学竞赛:

    python ".agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py" check --scope changed

Expected: No error on newly created or modified Skill/project files. Existing untouched content is outside changed-line punctuation scope.

- [ ] **Step 3: Run full 数学分析培优 project validation**

Run:

    python ".agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py" check --scope project --project "数学分析培优"

Expected: The command completes without modifying files. Record every diagnostic by rule and file. Existing unresolved-answer markers or historical style warnings may remain, but structural errors introduced by this implementation must be zero.

- [ ] **Step 4: Convert every discovered validator defect into a regression test**

For each false positive, false negative, path decoding error, or crash:

1. Add the smallest temporary fixture reproducing it.
2. Run the single test and confirm failure.
3. Correct the validator.
4. Run the single test and confirm pass.
5. Run the full test suite.

Do not suppress a diagnostic solely to make the live project appear clean.

### Task 7: Compile, Inspect, and Complete Independent Review

**Files:**

- Do not write build artifacts inside the repository.
- Update only regression tests or Skill wording if verification exposes a defect.

**Interfaces:**

- Consumes: Final source tree from Tasks 1 through 6.
- Produces: Compile manifest, log scan, PDF page counts, visual sample record, and independent final review.

- [ ] **Step 1: Create and verify a pure-ASCII temporary build root**

In PowerShell:

    $buildRoot = Join-Path $env:TEMP 'math_competition_skill_validation'
    if (Test-Path -LiteralPath $buildRoot) {
        $resolved = (Resolve-Path -LiteralPath $buildRoot).Path
        $tempRoot = (Resolve-Path -LiteralPath $env:TEMP).Path
        if (-not $resolved.StartsWith($tempRoot, [System.StringComparison]::OrdinalIgnoreCase)) {
            throw "Refusing to remove a build path outside TEMP."
        }
        Remove-Item -LiteralPath $resolved -Recurse -Force
    }
    New-Item -ItemType Directory -Path $buildRoot | Out-Null
    $buildRoot

Expected: The resolved output path contains only ASCII characters and lies inside the system temporary directory.

- [ ] **Step 2: Compile all 26 chapter entry points**

Enumerate exactly the normal and answer wrapper files, excluding _内容.tex. For each wrapper:

1. Set the working directory to its chapter folder.
2. Allocate a unique ASCII output folder such as chapter_01_normal or chapter_01_answer.
3. Run:

       latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$outDir" "$leafName"

4. Record source path, output path, exit code, log path, and PDF path.

Expected: 26 successful targets. If a target fails, preserve its log in the temporary root and do not report chapter verification as complete.

- [ ] **Step 3: Compile both full books**

From D:\Desktop\数学竞赛\数学分析培优, run each main file with a distinct ASCII output folder:

    latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$normalOut" "数学分析培优讲义.tex"
    latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir="$answerOut" "数学分析培优讲义(答案版).tex"

Expected: Both commands succeed and produce separate PDFs. Record page counts with pdfinfo.

- [ ] **Step 4: Scan every generated log**

Search case-insensitively for:

    LaTeX Error
    Undefined control sequence
    Missing $
    Missing }
    Extra }
    Environment .* undefined
    Overfull \hbox
    Underfull \hbox
    Overfull \vbox
    Underfull \vbox
    Token not allowed in a PDF string
    Font shape .* not available
    Size substitutions
    Missing character
    undefined references
    Unused global option

Classify each match by target and whether it is new, pre-existing, benign, or actionable. Do not hide warnings by deleting auxiliary files or changing mathematics without cause.

- [ ] **Step 5: Inspect rendered output**

Use the pdf Skill. Render and inspect:

- The answer-book title page, confirming ASCII parentheses render correctly.
- One normal-edition example page, confirming blank writing space.
- The corresponding answer-edition page, confirming solution display and no added blank.
- One page with section, subsection, and methodsection grouped at the top.
- One chapter opening page.
- At least one page from each full book confirming the watermark is visible.

Record exact PDF paths and page numbers. Do not claim all pages were visually inspected.

- [ ] **Step 6: Run final static verification**

Run:

    python -m pytest ".agents\skills\writing-math-competition-lectures\scripts\tests" -v
    python "C:\Users\m1881\.codex\skills\.system\skill-creator\scripts\quick_validate.py" ".agents\skills\writing-math-competition-lectures"
    python ".agents\skills\writing-math-competition-lectures\scripts\validate_lecture.py" check --scope changed
    git diff --check
    git status --short

Expected: Tests and Skill validation pass, no changed-scope errors remain, diff check is clean, and status lists only planned files.

- [ ] **Step 7: Request one independent whole-change review**

Use a fresh reviewer agent after all implementation and verification are complete. Give it:

- The approved spec.
- This implementation plan.
- The complete Git diff.
- Test output.
- Validator output.
- Compile manifest.
- Log classification.
- Visual-inspection record.

Ask it to check spec coverage, safety, validator false positives/negatives, single-source consistency, English punctuation, and unsupported completion claims.

Expected: Address every confirmed issue with a regression test when code changes are needed. Rerun affected verification after each correction.

- [ ] **Step 8: Deliver the fixed completion report**

Report:

- Modified files.
- Skill architecture and rule changes.
- Validator rule and test results.
- Project documentation and title change.
- Mathematical changes, explicitly "none" unless the diff shows otherwise.
- Exact compile targets and page counts.
- Warning classification.
- Exact visually inspected pages.
- Unverified scope.
- Remaining issues and next steps.
- Absolute clickable file links.

Use English punctuation. State clearly that no branch, commit, push, tracked PDF, source PDF, global Skill, or Obsidian Skill guide was changed.
