import ast
import importlib
import inspect
import os
import subprocess
import sys

from reflex_ai import paths
from reflex_ai.scripts import get_module_script


def import_module_from_scratch(module_name: str, root_dir: str, scratch_dir: str):
    """Import the module from the scratchpad.

    Args:
        module_name: The name of the module to import.
        root_dir: The root directory of the module.
        scratch_dir: The scratch directory of the module.

    Returns:
        The imported module.
    """
    module_tmp_file = os.path.join(scratch_dir, *module_name.split('.')) + '.py'
    spec = importlib.util.spec_from_file_location(
        module_name,
        module_tmp_file,
    )
    new_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(new_module)
    return new_module


def get_module_source(module_name: str) -> str:
    """Get the file path of a module in a subprocess.

    Args:
        module_name: The name of the module.

    Returns:
        The source code of the module.
    
    Raises:
        Exception: If the subprocess fails.
    """
    path = inspect.getfile(get_module_script)
    try:
        result = subprocess.run(
            [
                sys.executable,
                path,
                module_name,
                str(paths.base_paths[0]),
                str(paths.tmp_root_path),
            ],
            capture_output=True,
            text=True,
            check=True,
        )
    except Exception as e:
        raise Exception(e.stderr)
    # Capture the output
    module_file = result.stdout.strip().split("\n")[-1]
    with open(module_file) as f:
        return f.read()


def get_module_ast(module_name: str) -> ast.Module:
    """Get the AST of a module.

    Args:
        module_name: The name of the module.

    Returns:
        The AST of the module.
    """
    # Import the module
    module_source = get_module_source(module_name)

    # Parse the module source code into an AST
    module_ast = ast.parse(module_source)
    return module_ast


def find_node(tree, element_type: str, element_name: str) -> ast.AST | None:
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.FunctionDef)
            and element_type == "function"
            and node.name == element_name
        ):
            return node
        elif (
            isinstance(node, ast.ClassDef)
            and element_type == "class"
            and node.name == element_name
        ):
            return node
        elif isinstance(node, ast.Assign) and element_type == "variable":
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == element_name:
                    return node
        elif isinstance(node, ast.Return) and element_type == "return":
            return node
    return None
