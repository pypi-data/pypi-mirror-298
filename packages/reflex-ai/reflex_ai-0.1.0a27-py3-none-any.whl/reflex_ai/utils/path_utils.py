"""Utility functions for the reflex_ai package."""

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import black
import difflib
import filecmp
import inspect

import reflex as rx
from reflex.utils import console

from reflex_ai import paths
from reflex_ai.scripts import validate_source as validate_source_script

SCRATCH_DIR_NAME = "reflex_ai_tmp"


def get_scratch_dir(app_dir: Path) -> Path:
    """Get the location of the scratch directory where the agent makes changes.

    Args:
        app_dir: The directory of the app that was copied into the scratch directory.

    Returns:
        The path to the scratch directory.
    """
    return app_dir.parent / rx.constants.Dirs.WEB / SCRATCH_DIR_NAME


def create_scratch_dir(app_dir: Path, overwrite: bool = False) -> Path:
    """Create a scratch directory for the agent to make changes to.

    Args:
        app_dir: The directory of the app to copy into the scratch directory.
        overwrite: Whether to overwrite the scratch directory if it already exists.

    Returns:
        The path to the created directory.
    """
    scratch_dir = get_scratch_dir(app_dir)

    # If the scratch directory already exists, skip.
    if scratch_dir.exists() and not overwrite:
        console.debug(
            f"Scratch directory already exists at {scratch_dir}. Skipping creation."
        )
        return scratch_dir

    # Copy the app directory to a temporary path for modifications.
    shutil.copytree(
        app_dir,
        scratch_dir / app_dir.name,
        dirs_exist_ok=True,
    )

    # Rename the copied directory to the scratch directory name.
    modify_scratch_directory(scratch_dir)
    return scratch_dir


def modify_scratch_directory(directory: Path) -> None:
    """Modify Python files in the scratch directory to use the correct state class.

    Args:
        directory: The directory containing files to modify.
    """
    for root, _, files in os.walk(directory):
        for file in files:
            if not file.endswith(".py") or "rxconfig" in file:
                continue
            file_path = Path(root) / file
            modify_scratch_file(file_path)


def modify_scratch_file(file_path: Path):
    """Modify the content of a single file in the scratch directory.

    Args:
        file_path: The path to the file to modify.
    """
    with open(file_path, "r") as f:
        content = f.read()

    content = content.replace("(rx.State)", "(EditableState)")
    content = f"from reflex_ai import EditableState\n{content}"

    console.debug(f"Writing to {file_path}")
    with open(file_path, "w") as f:
        f.write(content)


def commit_scratch_dir(app_dir: Path, files: list[str]) -> None:
    """Copy all files from the scratch directory back to the corresponding app directory.

    Args:
        app_dir: The original app directory to copy files back to.
        files: The list of files to copy back.
    """
    scratch_dir = get_scratch_dir(app_dir)

    # Iterate over the files and copy them back to the app directory.
    for file in files:
        relative_path = Path(file).relative_to(app_dir.parent)
        source_file = scratch_dir / relative_path
        target_file = Path(file)

        with open(source_file, "r") as f:
            content = f.read()

        content = content.replace("(EditableState)", "(rx.State)")
        content = content.replace("from reflex_ai import EditableState\n", "")

        console.debug(f"Writing to {target_file}")
        with open(target_file, "w") as f:
            f.write(content)


def format_code(code: str) -> str:
    """Format the code using black.

    Args:
        code: The code to format.

    Returns:
        The formatted code.
    """
    return black.format_str(code, mode=black.FileMode())


def diff_directories(dir1: str, dir2: str) -> dict[str, list[str]]:
    """Diff two directories and return the diffs for all Python files.

    Args:
        dir1: The first directory.
        dir2: The second directory.

    Returns:
        A dictionary mapping file paths to their diffs.
    """
    diffs: dict[str, list[str]] = {}

    def compare_dirs(dcmp: filecmp.dircmp) -> None:
        for name in dcmp.diff_files:
            if not name.endswith(".py"):
                continue
            file1 = Path(dcmp.left) / name
            file2 = Path(dcmp.right) / name
            with file1.open() as f1, file2.open() as f2:
                f1_lines = format_code(f1.read()).splitlines()
                f2_lines = format_code(
                    f2.read()
                    .replace("(EditableState)", "(rx.State)")
                    .replace("from reflex_ai import EditableState\n", "")
                ).splitlines()
                diff = list(
                    difflib.unified_diff(
                        f1_lines, f2_lines, fromfile=str(file1), tofile=str(file2)
                    )
                )
                diffs[str(file1)] = diff
        for sub_dcmp in dcmp.subdirs.values():
            compare_dirs(sub_dcmp)

    dirs_cmp = filecmp.dircmp(dir1, dir2)
    compare_dirs(dirs_cmp)
    return diffs


def directory_diff() -> dict[str, list[str]]:
    """Diff the scratchpad and the base directories.

    Returns:
        A dictionary mapping file paths to their diffs.

    Raises:
        AssertionError: If the paths are not properly configured.
    """
    assert (
        isinstance(paths.base_paths, list)
        and len(paths.base_paths) > 0
        and isinstance(paths.base_paths[0], Path)
    )
    assert isinstance(paths.tmp_root_path, Path)
    return diff_directories(str(paths.base_paths[0].parent), str(paths.tmp_root_path))


def validate_source(source: str, validation_function: str):
    """Validate the diff and write the changes to the file.

    Args:
        source: The source code to validate.
        validation_function: The function to validate the source code.
    """
    # Write the source to a temporary file.
    with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
        tmp_file.write(source.encode())
        path = inspect.getfile(validate_source_script)

    # Run the validation script in a subprocess.
    try:
        subprocess.run(
            [sys.executable, path, tmp_file.name, validation_function],
            capture_output=True,
            text=True,
            check=True,
        )
    finally:
        os.unlink(tmp_file.name)
