import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest


SCRIPT = Path(__file__).parents[1] / "validate_lecture.py"

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

ADVANCED_ALGEBRA_CHAPTERS = [
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
]

MATH_ANALYSIS_MAINS = (
    "数学分析培优讲义.tex",
    "数学分析培优讲义(答案版).tex",
)
ADVANCED_ALGEBRA_MAINS = (
    "高等代数培优讲义.tex",
    "高等代数培优讲义(答案版).tex",
)


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_lecture", SCRIPT)
    assert spec is not None
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


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


def build_project(
    root: Path,
    directory: str,
    normal_main: str,
    answer_main: str,
    chapters: list[tuple[str, str]],
) -> Path:
    project = root / directory
    chapters_dir = project / "章节"
    chapters_dir.mkdir(parents=True)
    normal_refs = []
    answer_refs = []

    for folder_name, stem in chapters:
        folder = chapters_dir / folder_name
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
            f"\\documentclass[../../{normal_main}]{{subfiles}}\n"
            "\\begin{document}\n"
            f"\\input{{{stem}_内容}}\n"
            "\\end{document}\n",
            encoding="utf-8",
        )
        (folder / f"{stem}(答案版).tex").write_text(
            f"\\documentclass[../../{answer_main}]{{subfiles}}\n"
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
    (project / normal_main).write_text(
        main_prefix.format(mode="noanswer") + "\n".join(normal_refs),
        encoding="utf-8",
    )
    (project / answer_main).write_text(
        main_prefix.format(mode="answer") + "\n".join(answer_refs),
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


def build_math_analysis_project(root: Path) -> Path:
    return build_project(
        root,
        "数学分析培优",
        *MATH_ANALYSIS_MAINS,
        CHAPTERS,
    )


def build_advanced_algebra_project(root: Path) -> Path:
    return build_project(
        root,
        "高等代数培优",
        *ADVANCED_ALGEBRA_MAINS,
        ADVANCED_ALGEBRA_CHAPTERS,
    )


def replace_text(path: Path, old: str, new: str) -> None:
    text = path.read_text(encoding="utf-8")
    assert old in text
    path.write_text(text.replace(old, new, 1), encoding="utf-8")


def first_content_file(project: Path) -> Path:
    return sorted((project / "章节").glob("*/*_内容.tex"))[0]


def apply_project_mutation(
    project: Path,
    mutation: str,
    mains: tuple[str, str] = MATH_ANALYSIS_MAINS,
) -> None:
    normal = project / mains[0]
    answer = project / mains[1]
    preamble = project / "preamble.tex"

    if mutation == "remove_answer_entry":
        answer_entry = sorted((project / "章节").glob("*/*(答案版).tex"))[0]
        answer_entry.unlink()
    elif mutation == "wrong_normal_mode":
        replace_text(normal, "result=noanswer", "result=answer")
    elif mutation == "wrong_answer_mode":
        replace_text(answer, "result=answer", "result=noanswer")
    elif mutation == "missing_subfiles_package":
        replace_text(preamble, "\\usepackage{subfiles}\n", "")
    elif mutation == "missing_later_section_break":
        with first_content_file(project).open("a", encoding="utf-8") as handle:
            handle.write("\\section{Second}\nText.\n")
    elif mutation == "break_before_initial_section":
        replace_text(
            first_content_file(project),
            "\\chapter{Chapter}\n\\section{First}",
            "\\chapter{Chapter}\n\\newpage\n\\section{First}",
        )
    elif mutation == "break_before_subsection":
        with first_content_file(project).open("a", encoding="utf-8") as handle:
            handle.write("\\newpage\n\\subsection{Sub}\nText.\n")
    elif mutation == "unknown_watermark_option":
        replace_text(normal, "result=noanswer", "result=noanswer,\nwatermark")
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


def test_chinese_punctuation_reports_selected_line_only(tmp_path):
    validator = load_validator()
    source = tmp_path / "讲义.tex"
    source.write_text("旧句，保留\n新句，修改\n", encoding="utf-8")

    diagnostics = validator.check_text_file(source, {2})

    assert [(item.rule_id, item.line) for item in diagnostics] == [
        ("PUNC001", 2)
    ]


def test_markdown_punctuation_ignores_fenced_and_inline_code(tmp_path):
    validator = load_validator()
    source = tmp_path / "rules.md"
    source.write_text(
        "```text\n"
        "第九章_函数项级数、幂级数.tex\n"
        "```\n"
        "路径 `第九章_函数项级数、幂级数.tex` 保持原样.\n"
        "源码 `\\binom{n}{k}` 只用于说明禁用命令.\n"
        "    第九章_函数项级数、幂级数.tex\n"
        "    \\binom and TODO are literal examples.\n"
        "正文，必须报告.\n",
        encoding="utf-8",
    )

    diagnostics = validator.check_text_file(source, None)

    assert [(item.rule_id, item.line) for item in diagnostics] == [
        ("PUNC001", 8)
    ]


@pytest.mark.parametrize(
    ("source_text", "rule_id"),
    [
        ("$$x$$\n", "LATEX001"),
        (r"$\binom{n}{k}$" + "\n", "LATEX002"),
        (r"$\tfrac{1}{2}$" + "\n", "LATEX003"),
        (r"$\bigl(x\bigr)$" + "\n", "LATEX006"),
        (r"$\mathbb R$" + "\n", "LATEX007"),
        ("正文\x08控制符\n", "CTRL001"),
        (r"\begin{align}x&=1\end{gather}" + "\n", "LATEX004"),
        ("{\n", "LATEX005"),
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


def test_changed_scope_checks_only_added_lines_and_whole_untracked_files(
    tmp_path,
):
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
    content = first_content_file(project)
    content.write_text(
        "\\chapter{Chapter}\n\\section{First}\n" + replacement,
        encoding="utf-8",
    )

    assert "MA001" in {
        item.rule_id
        for item in validator.check_math_analysis_project(project)
        if item.severity == "error"
    }


@pytest.mark.parametrize(
    ("mutation", "rule_id"),
    [
        ("remove_answer_entry", "MA002"),
        ("wrong_normal_mode", "MA003"),
        ("wrong_answer_mode", "MA004"),
        ("missing_subfiles_package", "MA005"),
        ("missing_later_section_break", "MA006"),
        ("break_before_initial_section", "MA006"),
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
        item.rule_id for item in validator.check_math_analysis_project(project)
    }

    assert rule_id in ids


def check_algebra(validator, project):
    return validator.check_book_project(
        project,
        validator.ADVANCED_ALGEBRA_PROFILE,
    )


def test_find_book_root_detects_each_profile(tmp_path):
    validator = load_validator()
    math_project = build_math_analysis_project(tmp_path)
    algebra_project = build_advanced_algebra_project(tmp_path)

    assert validator._find_book_root(math_project, tmp_path) == (
        math_project.resolve(),
        validator.MATH_ANALYSIS_PROFILE,
    )
    assert validator._find_book_root(algebra_project, tmp_path) == (
        algebra_project.resolve(),
        validator.ADVANCED_ALGEBRA_PROFILE,
    )
    assert validator._find_book_root(tmp_path, tmp_path) is None


def test_valid_advanced_algebra_project_has_no_structural_errors(tmp_path):
    validator = load_validator()
    project = build_advanced_algebra_project(tmp_path)

    diagnostics = check_algebra(validator, project)

    assert not [item for item in diagnostics if item.severity == "error"]


def test_book_profiles_have_distinct_chapter_counts():
    validator = load_validator()

    assert len(validator.MATH_ANALYSIS_PROFILE.chapters) == 13
    assert len(validator.ADVANCED_ALGEBRA_PROFILE.chapters) == 10
    assert validator.MATH_ANALYSIS_PROFILE.section_break_required is True
    assert validator.ADVANCED_ALGEBRA_PROFILE.section_break_required is True


def test_repeated_section_break_is_required_for_math_analysis(tmp_path):
    validator = load_validator()
    project = build_math_analysis_project(tmp_path)
    with first_content_file(project).open("a", encoding="utf-8") as handle:
        handle.write("\\section{Second}\nText.\n")

    ids = {
        item.rule_id for item in validator.check_math_analysis_project(project)
    }

    assert "MA006" in ids


def test_repeated_section_break_is_required_for_advanced_algebra(tmp_path):
    validator = load_validator()
    project = build_advanced_algebra_project(tmp_path)
    with first_content_file(project).open("a", encoding="utf-8") as handle:
        handle.write("\\section{Second}\nText.\n")

    ids = {item.rule_id for item in check_algebra(validator, project)}

    assert "MA006" in ids


@pytest.mark.parametrize(
    ("mutation", "rule_id"),
    [
        ("remove_answer_entry", "MA002"),
        ("wrong_normal_mode", "MA003"),
        ("wrong_answer_mode", "MA004"),
        ("missing_subfiles_package", "MA005"),
        ("missing_later_section_break", "MA006"),
        ("break_before_initial_section", "MA006"),
        ("break_before_subsection", "MA007"),
        ("unknown_watermark_option", "MA008"),
        ("watermark_after_preamble", "MA009"),
        ("missing_main_reference", "MA010"),
    ],
)
def test_advanced_algebra_mutation_is_reported(tmp_path, mutation, rule_id):
    validator = load_validator()
    project = build_advanced_algebra_project(tmp_path)
    apply_project_mutation(project, mutation, ADVANCED_ALGEBRA_MAINS)

    ids = {item.rule_id for item in check_algebra(validator, project)}

    assert rule_id in ids
