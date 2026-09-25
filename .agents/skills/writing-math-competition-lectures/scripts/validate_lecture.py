"""Read-only validator for mathematical lecture-note projects."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal


Severity = Literal["error", "warning", "info"]
SelectedLines = set[int] | None

SUPPORTED_SUFFIXES = {".tex", ".md", ".yaml", ".yml"}
CHINESE_PUNCTUATION = "，。；：！？（）【】“”‘’、…—"
PUNC_EXEMPT_NAMES = {"AGENTS.md", "README.md"}
GENERIC_PATTERNS = {
    "LATEX002": re.compile(r"\\binom\b"),
    "LATEX003": re.compile(r"\\tfrac\b"),
    "LATEX006": re.compile(
        r"\\bigl\b|\\bigr\b|\\Bigl\b|\\Bigr\b|"
        r"\\biggl\b|\\biggr\b|\\Biggl\b|\\Biggr\b"
    ),
    "LATEX007": re.compile(r"\\mathbb\s+[A-Za-z]"),
}
GENERIC_REPLACEMENTS = {
    "LATEX002": (
        "C_n^k for a binomial coefficient, or a pmatrix "
        "environment for a stacked column vector"
    ),
    "LATEX003": "dfrac or frac",
    "LATEX006": "left and right for auto-sized delimiters",
    "LATEX007": "mathbb{R} with braces",
}
DOUBLE_DOLLAR_RE = re.compile(r"\$\$")
UNRESOLVED_MARKERS = ("T" + "ODO", "T" + "BD", "FIX" + "ME")
HUNK_RE = re.compile(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@")
ENV_RE = re.compile(r"\\(begin|end)\{([^{}]+)\}")
MATH_DELIMITER_RE = re.compile(r"(?<!\\)(\\\(|\\\)|\\\[|\\\])")
LEFT_RIGHT_RE = re.compile(r"\\(left|right)\b")
EXAMPLE_TOKEN_RE = re.compile(
    r"\\begin\{example\}|\\end\{example\}|"
    r"\\exampleblank\b|"
    r"\\begin\{solution\}|\\end\{solution\}"
)

@dataclass(frozen=True)
class BookProfile:
    """Structural contract for one lecture-note book."""

    display_name: str
    normal_main: str
    answer_main: str
    chapters: tuple[tuple[str, str], ...]
    # 非首个 section 前必须紧跟 \newpage. 数学分析培优和高等代数培优
    # 都采用这条约定, 因此当前两本书都是 True. 保留该开关是为了让
    # 未来可能采用不同分页约定的书不必修改检查逻辑.
    section_break_required: bool


MATH_ANALYSIS_PROFILE = BookProfile(
    display_name="数学分析培优",
    normal_main="数学分析培优讲义.tex",
    answer_main="数学分析培优讲义(答案版).tex",
    chapters=(
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
    ),
    section_break_required=True,
)

ADVANCED_ALGEBRA_PROFILE = BookProfile(
    display_name="高等代数培优",
    normal_main="高等代数培优讲义.tex",
    answer_main="高等代数培优讲义(答案版).tex",
    chapters=(
        ("01_第一章_多项式", "第一章_多项式"),
        ("02_第二章_行列式", "第二章_行列式"),
        ("03_第三章_矩阵", "第三章_矩阵"),
        ("04_第四章_线性空间与线性方程组", "第四章_线性空间与线性方程组"),
        ("05_第五章_线性变换", "第五章_线性变换"),
        ("06_第六章_相似标准型", "第六章_相似标准型"),
        ("07_第七章_二次型", "第七章_二次型"),
        ("08_第八章_欧氏空间", "第八章_欧氏空间"),
        ("09_第九章_矩阵综合", "第九章_矩阵综合"),
        ("10_第十章_张量积与外积", "第十章_张量积与外积"),
    ),
    section_break_required=True,
)

BOOK_PROFILES = (MATH_ANALYSIS_PROFILE, ADVANCED_ALGEBRA_PROFILE)

SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}


@dataclass(frozen=True)
class Diagnostic:
    severity: Severity
    rule_id: str
    path: Path
    line: int | None
    message: str
    suggestion: str


class SelectionError(RuntimeError):
    """Raised when a validation scope cannot be resolved safely."""


def strip_tex_comment(line: str) -> str:
    """Remove an unescaped TeX comment while preserving escaped percent signs."""
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


def find_repo_root(start: Path) -> Path:
    """Find the nearest Git worktree root at or above start."""
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise SelectionError(f"No Git repository found above {start}")


def _run_git(repo_root: Path, args: list[str]) -> str:
    result = subprocess.run(
        ["git", "-c", "core.quotepath=false", *args],
        cwd=repo_root,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
    )
    if result.returncode != 0:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise SelectionError(f"Git command failed: {detail}")
    return result.stdout


def _within(path: Path, parent: Path) -> bool:
    try:
        path.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def _resolve_input(repo_root: Path, value: Path) -> Path:
    return (value if value.is_absolute() else repo_root / value).resolve()


def _select_changed_files(
    repo_root: Path,
    project: Path | None,
) -> dict[Path, SelectedLines]:
    _run_git(repo_root, ["rev-parse", "--verify", "HEAD"])
    diff = _run_git(
        repo_root,
        ["diff", "--unified=0", "--no-color", "--no-renames", "HEAD", "--"],
    )
    chosen: dict[Path, SelectedLines] = {}
    current_path: Path | None = None
    new_line: int | None = None

    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            relative_path = line[6:].split("\t", 1)[0]
            current_path = (repo_root / relative_path).resolve()
            new_line = None
            continue
        hunk = HUNK_RE.match(line)
        if hunk:
            new_line = int(hunk.group(1))
            continue
        if current_path is None or new_line is None:
            continue
        if line.startswith("+") and not line.startswith("+++"):
            if current_path.suffix.lower() in SUPPORTED_SUFFIXES:
                current = chosen.setdefault(current_path, set())
                if current is not None:
                    current.add(new_line)
            new_line += 1
        elif line.startswith("-") and not line.startswith("---"):
            continue
        elif line.startswith(" "):
            new_line += 1

    untracked = _run_git(
        repo_root,
        ["ls-files", "--others", "--exclude-standard"],
    )
    for relative in untracked.splitlines():
        path = (repo_root / relative).resolve()
        if path.suffix.lower() in SUPPORTED_SUFFIXES and path.is_file():
            chosen[path] = None

    if project is not None:
        chosen = {
            path: lines
            for path, lines in chosen.items()
            if _within(path, project)
        }
    return chosen


def select_files(
    repo_root: Path,
    scope: str,
    project: Path | None,
    explicit_files: list[Path],
) -> dict[Path, SelectedLines]:
    """Resolve files and selected lines for changed, file, or project scope."""
    repo_root = find_repo_root(repo_root)
    resolved_project = (
        _resolve_input(repo_root, project) if project is not None else None
    )

    if scope == "changed":
        return _select_changed_files(repo_root, resolved_project)
    if scope == "file":
        if not explicit_files:
            raise SelectionError("File scope requires at least one --file path")
        result: dict[Path, SelectedLines] = {}
        for value in explicit_files:
            path = _resolve_input(repo_root, value)
            if not path.is_file():
                raise SelectionError(f"Selected file does not exist: {value}")
            if path.suffix.lower() in SUPPORTED_SUFFIXES:
                result[path] = None
        return result
    if scope == "project":
        if resolved_project is None or not resolved_project.is_dir():
            raise SelectionError("Project scope requires an existing --project path")
        return {
            path.resolve(): None
            for path in resolved_project.rglob("*")
            if path.is_file()
            and path.suffix.lower() in SUPPORTED_SUFFIXES
            and ".git" not in path.parts
            and ".superpowers" not in path.parts
        }
    raise SelectionError(f"Unsupported scope: {scope}")


def _diagnostic(
    path: Path,
    line: int | None,
    rule_id: str,
    message: str,
    suggestion: str,
    severity: Severity = "warning",
) -> Diagnostic:
    return Diagnostic(severity, rule_id, path, line, message, suggestion)


def _is_escaped(text: str, index: int) -> bool:
    slashes = 0
    cursor = index - 1
    while cursor >= 0 and text[cursor] == "\\":
        slashes += 1
        cursor -= 1
    return slashes % 2 == 1


def _check_environment_balance(path: Path, lines: list[str]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    stack: list[tuple[str, int]] = []
    for line_number, raw in enumerate(lines, 1):
        line = strip_tex_comment(raw)
        for match in ENV_RE.finditer(line):
            action, name = match.groups()
            if action == "begin":
                stack.append((name, line_number))
            elif not stack or stack[-1][0] != name:
                expected = stack[-1][0] if stack else "no open environment"
                diagnostics.append(
                    _diagnostic(
                        path,
                        line_number,
                        "LATEX004",
                        f"Environment end {name} does not match {expected}.",
                        "Match every begin environment with the correct end.",
                        "error",
                    )
                )
            else:
                stack.pop()
    for name, line_number in stack:
        diagnostics.append(
            _diagnostic(
                path,
                line_number,
                "LATEX004",
                f"Environment {name} is not closed.",
                f"Add the matching end for {name}.",
                "error",
            )
        )
    return diagnostics


def _check_delimiter_balance(path: Path, lines: list[str]) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    brace_stack: list[int] = []
    dollar_stack: list[int] = []
    paired_stack: list[tuple[str, int]] = []
    left_stack: list[int] = []

    for line_number, raw in enumerate(lines, 1):
        line = strip_tex_comment(raw)
        index = 0
        while index < len(line):
            char = line[index]
            if char in "{}" and not _is_escaped(line, index):
                if char == "{":
                    brace_stack.append(line_number)
                elif brace_stack:
                    brace_stack.pop()
                else:
                    diagnostics.append(
                        _diagnostic(
                            path,
                            line_number,
                            "LATEX005",
                            "Closing brace has no matching opening brace.",
                            "Balance the braces in this TeX file.",
                            "error",
                        )
                    )
            if char == "$" and not _is_escaped(line, index):
                if index + 1 < len(line) and line[index + 1] == "$":
                    index += 2
                    continue
                if dollar_stack:
                    dollar_stack.pop()
                else:
                    dollar_stack.append(line_number)
            index += 1

        for match in MATH_DELIMITER_RE.finditer(line):
            token = match.group(1)
            if token in (r"\(", r"\["):
                paired_stack.append((token, line_number))
            else:
                expected = r"\(" if token == r"\)" else r"\["
                if paired_stack and paired_stack[-1][0] == expected:
                    paired_stack.pop()
                else:
                    diagnostics.append(
                        _diagnostic(
                            path,
                            line_number,
                            "LATEX005",
                            f"Math delimiter {token} has no matching opener.",
                            "Pair all TeX math delimiters.",
                            "error",
                        )
                    )
        for match in LEFT_RIGHT_RE.finditer(line):
            if match.group(1) == "left":
                left_stack.append(line_number)
            elif left_stack:
                left_stack.pop()
            else:
                diagnostics.append(
                    _diagnostic(
                        path,
                        line_number,
                        "LATEX005",
                        "A right delimiter has no matching left delimiter.",
                        "Pair every left delimiter with a right delimiter.",
                        "error",
                    )
                )

    for line_number in brace_stack:
        diagnostics.append(
            _diagnostic(
                path,
                line_number,
                "LATEX005",
                "Opening brace is not closed.",
                "Balance the braces in this TeX file.",
                "error",
            )
        )
    for line_number in dollar_stack:
        diagnostics.append(
            _diagnostic(
                path,
                line_number,
                "LATEX005",
                "Inline dollar math delimiter is not closed.",
                "Add the matching dollar delimiter.",
                "error",
            )
        )
    for token, line_number in paired_stack:
        diagnostics.append(
            _diagnostic(
                path,
                line_number,
                "LATEX005",
                f"Math delimiter {token} is not closed.",
                "Add the matching TeX math delimiter.",
                "error",
            )
        )
    for line_number in left_stack:
        diagnostics.append(
            _diagnostic(
                path,
                line_number,
                "LATEX005",
                "A left delimiter has no matching right delimiter.",
                "Pair every left delimiter with a right delimiter.",
                "error",
            )
        )
    return diagnostics


def _markdown_prose_lines(lines: list[str]) -> list[str]:
    visible: list[str] = []
    fence: str | None = None
    for line in lines:
        marker = re.match(r"^\s*(`{3,}|~{3,})", line)
        if marker:
            token = marker.group(1)
            if fence is None:
                fence = token[0]
            elif token[0] == fence:
                fence = None
            visible.append("")
            continue
        if fence is not None:
            visible.append("")
            continue
        if re.match(r"^(?: {4}|\t)", line):
            visible.append("")
            continue
        prose = re.sub(r"`[^`]*`", "", line)
        prose = re.sub(r"https?://\S+", "", prose)
        visible.append(prose)
    return visible


def punctuation_exempt(path: Path) -> bool:
    """Return True for documents exempt from the ASCII punctuation rule.

    AGENTS.md section 6.5 keeps AGENTS.md, README.md and the skill documents
    outside the ASCII punctuation convention. Chapter sources and every other
    Markdown file, including the per-book problem log, stay subject to PUNC001.
    """
    if path.name in PUNC_EXEMPT_NAMES:
        return True
    parts = path.parts
    return any(
        parts[index] == ".agents" and parts[index + 1] == "skills"
        for index in range(len(parts) - 1)
    )


def check_text_file(
    path: Path,
    selected_lines: SelectedLines,
) -> list[Diagnostic]:
    """Run deterministic generic checks without modifying path."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    prose_lines = (
        _markdown_prose_lines(lines)
        if path.suffix.lower() == ".md"
        else lines
    )
    diagnostics: list[Diagnostic] = []
    exempt_from_punctuation = punctuation_exempt(path)

    for line_number, line in enumerate(lines, 1):
        if not selected(line_number, selected_lines):
            continue
        prose_line = prose_lines[line_number - 1]
        check_line = prose_line if path.suffix.lower() == ".md" else line
        if (
            not exempt_from_punctuation
            and any(character in CHINESE_PUNCTUATION for character in prose_line)
        ):
            diagnostics.append(
                _diagnostic(
                    path,
                    line_number,
                    "PUNC001",
                    "Chinese punctuation appears in selected prose.",
                    "Use ASCII punctuation unless this is an allowed literal.",
                )
            )
        if path.suffix.lower() == ".tex" and DOUBLE_DOLLAR_RE.search(line):
            diagnostics.append(
                _diagnostic(
                    path,
                    line_number,
                    "LATEX001",
                    "Double-dollar display math appears in a TeX file.",
                    "Use a LaTeX display environment such as bracket display math.",
                )
            )
        for rule_id, pattern in GENERIC_PATTERNS.items():
            if pattern.search(check_line):
                replacement = GENERIC_REPLACEMENTS[rule_id]
                diagnostics.append(
                    _diagnostic(
                        path,
                        line_number,
                        rule_id,
                        f"Disallowed LaTeX command matched {pattern.pattern}.",
                        f"Use the project convention, such as {replacement}.",
                    )
                )
        if any(marker in check_line for marker in UNRESOLVED_MARKERS):
            diagnostics.append(
                _diagnostic(
                    path,
                    line_number,
                    "TEXT001",
                    "An unresolved-work marker remains.",
                    "Resolve it or explain it in the completion report.",
                )
            )
        for character in line:
            if ord(character) < 32 and character not in "\t\r\n":
                diagnostics.append(
                    _diagnostic(
                        path,
                        line_number,
                        "CTRL001",
                        f"Raw control character U+{ord(character):04X} appears.",
                        "Remove the malformed control character.",
                        "error",
                    )
                )
                break

    if path.suffix.lower() == ".tex":
        diagnostics.extend(_check_environment_balance(path, lines))
        diagnostics.extend(_check_delimiter_balance(path, lines))
    return diagnostics


def _read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8-sig")


def _project_error(
    path: Path,
    rule_id: str,
    message: str,
    suggestion: str,
    line: int | None = None,
) -> Diagnostic:
    return _diagnostic(path, line, rule_id, message, suggestion, "error")


def _check_example_sequence(path: Path) -> list[Diagnostic]:
    states = [
        r"\begin{example}",
        r"\end{example}",
        r"\exampleblank",
        r"\begin{solution}",
        r"\end{solution}",
    ]
    state = 0
    diagnostics: list[Diagnostic] = []
    lines = _read_utf8(path).splitlines()
    for line_number, raw in enumerate(lines, 1):
        line = strip_tex_comment(raw)
        for match in EXAMPLE_TOKEN_RE.finditer(line):
            token = match.group(0)
            expected = states[state]
            if token != expected:
                diagnostics.append(
                    _project_error(
                        path,
                        "MA001",
                        f"Expected {expected} but found {token}.",
                        "Keep each example, blank command, and solution in order.",
                        line_number,
                    )
                )
                return diagnostics
            state = (state + 1) % len(states)
    if state:
        diagnostics.append(
            _project_error(
                path,
                "MA001",
                f"Example sequence ends before {states[state]}.",
                "Complete the example, blank command, and solution sequence.",
                len(lines) if lines else 1,
            )
        )
    return diagnostics


def _check_chapter_entries(
    project_root: Path,
    profile: BookProfile,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    chapters_root = project_root / "章节"
    discovered = {
        (path.parent.name, path.name.removesuffix("_内容.tex"))
        for path in chapters_root.glob("*/*_内容.tex")
    }
    expected = set(profile.chapters)
    if discovered != expected:
        diagnostics.append(
            _project_error(
                chapters_root,
                "MA002",
                "Chapter folder and content-file map does not match the "
                f"{profile.display_name} chapter profile.",
                "Restore the expected numbered folder and chapter stem names.",
            )
        )

    for folder_name, stem in profile.chapters:
        folder = chapters_root / folder_name
        content = folder / f"{stem}_内容.tex"
        normal = folder / f"{stem}.tex"
        answer = folder / f"{stem}(答案版).tex"
        required = (content, normal, answer)
        missing = [path.name for path in required if not path.is_file()]
        if missing:
            diagnostics.append(
                _project_error(
                    folder,
                    "MA002",
                    f"Chapter entry files are missing: {', '.join(missing)}.",
                    "Restore the shared content and both entry files.",
                )
            )
            continue

        normal_text = _read_utf8(normal)
        answer_text = _read_utf8(answer)
        expected_input = rf"\input{{{stem}_内容}}"
        normal_class = (
            rf"\documentclass[../../{profile.normal_main}]{{subfiles}}"
        )
        answer_class = (
            rf"\documentclass[../../{profile.answer_main}]{{subfiles}}"
        )
        if expected_input not in normal_text or normal_class not in normal_text:
            diagnostics.append(
                _project_error(
                    normal,
                    "MA002",
                    "Normal chapter entry does not load the expected main and content files.",
                    "Use the normal main file and the shared chapter content file.",
                )
            )
        if expected_input not in answer_text or answer_class not in answer_text:
            diagnostics.append(
                _project_error(
                    answer,
                    "MA002",
                    "Answer chapter entry does not load the expected main and content files.",
                    "Use the answer main file and the shared chapter content file.",
                )
            )
        diagnostics.extend(_check_example_sequence(content))
    return diagnostics


def _check_pagination(content: Path, profile: BookProfile) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    previous = ""
    first_section_after_chapter = False
    for line_number, raw in enumerate(_read_utf8(content).splitlines(), 1):
        line = strip_tex_comment(raw).strip()
        if not line:
            continue
        if re.match(r"^\\chapter(?:\[[^]]*\])?\s*\{", line):
            first_section_after_chapter = True
            previous = line
            continue
        if re.match(r"^\\section(?:\[[^]]*\])?\s*\{", line):
            if first_section_after_chapter:
                first_section_after_chapter = False
                if previous == r"\newpage":
                    diagnostics.append(
                        _project_error(
                            content,
                            "MA006",
                            "The initial section after a chapter is preceded by newpage.",
                            "Let the chapter command supply the page break.",
                            line_number,
                        )
                    )
            elif profile.section_break_required and previous != r"\newpage":
                diagnostics.append(
                    _project_error(
                        content,
                        "MA006",
                        "A noninitial section is not preceded by newpage.",
                        "Place newpage immediately before the section title.",
                        line_number,
                    )
                )
        if (
            re.match(r"^\\(?:subsection|methodsection)", line)
            and previous == r"\newpage"
        ):
            diagnostics.append(
                _project_error(
                    content,
                    "MA007",
                    "A page break appears immediately before a lower-level heading.",
                    "Remove the page break before subsection or methodsection.",
                    line_number,
                )
            )
        previous = line
    return diagnostics


def _documentclass_options(text: str) -> str:
    match = re.search(
        r"\\documentclass\s*\[(.*?)\]\s*\{elegantbook\}",
        text,
        re.DOTALL,
    )
    return match.group(1) if match else ""


def _check_main_files(
    project_root: Path,
    profile: BookProfile,
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    normal = project_root / profile.normal_main
    answer = project_root / profile.answer_main
    preamble = project_root / "preamble.tex"
    if not normal.is_file() or not answer.is_file() or not preamble.is_file():
        missing = [
            path.name for path in (normal, answer, preamble) if not path.is_file()
        ]
        return [
            _project_error(
                project_root,
                "MA002",
                f"Project entry files are missing: {', '.join(missing)}.",
                "Restore both main files and preamble.tex.",
            )
        ]

    normal_text = _read_utf8(normal)
    answer_text = _read_utf8(answer)
    preamble_text = _read_utf8(preamble)

    if not re.search(r"\bresult\s*=\s*noanswer\b", normal_text):
        diagnostics.append(
            _project_error(
                normal,
                "MA003",
                "Normal main file does not use result=noanswer.",
                "Restore the normal result mode.",
            )
        )
    if not re.search(r"\bresult\s*=\s*answer\b", answer_text):
        diagnostics.append(
            _project_error(
                answer,
                "MA004",
                "Answer main file does not use result=answer.",
                "Restore the answer result mode.",
            )
        )
    if not re.search(r"\\usepackage(?:\[[^]]*\])?\{subfiles\}", preamble_text):
        diagnostics.append(
            _project_error(
                preamble,
                "MA005",
                "preamble.tex does not load subfiles.",
                "Load the subfiles package in the project preamble.",
            )
        )

    for path, text in ((normal, normal_text), (answer, answer_text)):
        options = _documentclass_options(text)
        if re.search(r"(?:^|,)\s*watermark\s*(?:,|$)", options):
            diagnostics.append(
                _project_error(
                    path,
                    "MA008",
                    "watermark is passed as a document-class option.",
                    "Use the project Boolean watermark switch instead.",
                )
            )
        preamble_index = text.find(r"\input{preamble}")
        declaration_index = text.find(r"\newif\ifmathanalysiswatermark")
        enabled_index = text.find(r"\mathanalysiswatermarktrue")
        if (
            preamble_index < 0
            or declaration_index < 0
            or enabled_index < 0
            or declaration_index > preamble_index
            or enabled_index > preamble_index
        ):
            diagnostics.append(
                _project_error(
                    path,
                    "MA009",
                    "Watermark Boolean declaration and enabled state must precede preamble input.",
                    "Declare and enable the project watermark before loading preamble.tex.",
                )
            )

    normal_refs = re.findall(r"\\subfile\{([^}]+)\}", normal_text)
    answer_refs = re.findall(r"\\subfile\{([^}]+)\}", answer_text)
    expected_normal = [
        f"章节/{folder}/{stem}" for folder, stem in profile.chapters
    ]
    expected_answer = [
        f"章节/{folder}/{stem}(答案版)" for folder, stem in profile.chapters
    ]
    if normal_refs != expected_normal or answer_refs != expected_answer:
        diagnostics.append(
            _project_error(
                project_root,
                "MA010",
                "Main files do not contain the expected "
                f"{len(profile.chapters)} ordered chapter references for "
                f"{profile.display_name}.",
                "Restore matching normal and answer subfile references.",
            )
        )
    return diagnostics


def check_book_project(
    project_root: Path,
    profile: BookProfile,
) -> list[Diagnostic]:
    """Check one book's single-source project contract."""
    project_root = project_root.resolve()
    diagnostics = _check_main_files(project_root, profile)
    diagnostics.extend(_check_chapter_entries(project_root, profile))
    for content in sorted((project_root / "章节").glob("*/*_内容.tex")):
        diagnostics.extend(_check_pagination(content, profile))
    return diagnostics


def check_math_analysis_project(project_root: Path) -> list[Diagnostic]:
    """Check the 数学分析培优 contract; kept for existing callers."""
    return check_book_project(project_root, MATH_ANALYSIS_PROFILE)


def _find_book_root(
    path: Path,
    repo_root: Path,
) -> tuple[Path, BookProfile] | None:
    start = path if path.is_dir() else path.parent
    for candidate in (start, *start.parents):
        if not _within(candidate, repo_root):
            break
        for profile in BOOK_PROFILES:
            if (
                (candidate / profile.normal_main).is_file()
                and (candidate / profile.answer_main).is_file()
            ):
                return candidate, profile
    return None


def run_checks(
    repo_root: Path,
    scope: str,
    project: Path | None,
    explicit_files: list[Path],
) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    selected_files = select_files(
        repo_root,
        scope,
        project,
        explicit_files,
    )
    for path, selected_lines in selected_files.items():
        diagnostics.extend(check_text_file(path, selected_lines))

    project_roots: set[tuple[Path, BookProfile]] = set()
    if project is not None:
        project_path = _resolve_input(repo_root, project)
        found = _find_book_root(project_path, repo_root)
        if found is not None:
            project_roots.add(found)
    for path in selected_files:
        found = _find_book_root(path, repo_root)
        if found is not None:
            project_roots.add(found)
    for project_root, profile in sorted(
        project_roots,
        key=lambda item: item[0].as_posix(),
    ):
        diagnostics.extend(check_book_project(project_root, profile))
    return diagnostics


def _sort_key(item: Diagnostic) -> tuple[str, int, int, str]:
    return (
        item.path.as_posix().casefold(),
        item.line if item.line is not None else 2**31,
        SEVERITY_ORDER[item.severity],
        item.rule_id,
    )


def _display_path(path: Path, repo_root: Path) -> str:
    try:
        return path.resolve().relative_to(repo_root.resolve()).as_posix()
    except ValueError:
        return path.resolve().as_posix()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    check = subparsers.add_parser("check", help="Run read-only lecture checks")
    check.add_argument(
        "--scope",
        choices=("changed", "file", "project"),
        required=True,
    )
    check.add_argument("--project", type=Path)
    check.add_argument("--file", type=Path, action="append", default=[])
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        repo_root = find_repo_root(Path.cwd())
        diagnostics = run_checks(
            repo_root,
            args.scope,
            args.project,
            args.file,
        )
    except SelectionError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    for item in sorted(diagnostics, key=_sort_key):
        location = _display_path(item.path, repo_root)
        if item.line is not None:
            location = f"{location}:{item.line}"
        print(
            f"{item.severity.upper()} {item.rule_id} {location} "
            f"{item.message} Suggestion: {item.suggestion}"
        )
    return 1 if any(item.severity == "error" for item in diagnostics) else 0


if __name__ == "__main__":
    raise SystemExit(main())
